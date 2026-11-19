"""Experimental local SQLite cache of EPİAŞ responses.

Off by default. When on, :meth:`eptr2.EPTR2.call` looks the request up in a SQLite
file before going to the network, and stores settled responses after fetching them.
A hit needs no network and no login, and goes through the normal postprocessing, so
``postprocess=True`` and ``False`` share one row and later fixes in eptr2's
processing apply to stored data.

Settings (the narrowest one given wins):

- per call: ``eptr.call(..., cache=True, cache_path=..., cache_overwrite=True,
  cache_settle_days=..., cache_max_age=...)``
- per client: ``EPTR2(..., cache=True, cache_path=..., ...)`` (same names)
- per process: :func:`set_cache`
- by environment: ``EPTR2_CACHE``, ``EPTR2_CACHE_PATH``, ``EPTR2_CACHE_OVERWRITE``,
  ``EPTR2_CACHE_SETTLE_DAYS``, ``EPTR2_CACHE_MAX_AGE`` (also read from the ``.env``
  file of ``EPTR2(use_dotenv=True)``; a variable already set in the environment wins)

What is stored (see :mod:`eptr2.mapping.settle`):

- only responses whose last date is outside the call's settle window; a request
  reaching into the window is not stored at all
- only JSON bodies with a non-empty ``items`` list (or ``installedCapacities``):
  empty, error and non-JSON (e.g. a firewall page) responses are not stored
- never requests without a date parameter, nor :data:`~eptr2.mapping.settle.NEVER_CACHE` calls

``cache_overwrite=True`` skips the lookup, fetches and replaces the stored row; a
failed, empty or unsettled refetch keeps the existing row. ``cache_max_age`` (days)
refetches rows older than that.
"""

from __future__ import annotations

import json
import logging
import os
import sqlite3
import threading
import zlib
from dataclasses import dataclass
from datetime import date, datetime, timezone
from hashlib import sha256

from eptr2.mapping.settle import _ISTANBUL

logger = logging.getLogger(__name__)

ENV_ENABLED = "EPTR2_CACHE"
ENV_PATH = "EPTR2_CACHE_PATH"
ENV_OVERWRITE = "EPTR2_CACHE_OVERWRITE"
ENV_SETTLE_DAYS = "EPTR2_CACHE_SETTLE_DAYS"
ENV_MAX_AGE = "EPTR2_CACHE_MAX_AGE"
ENV_VARS = (ENV_ENABLED, ENV_PATH, ENV_OVERWRITE, ENV_SETTLE_DAYS, ENV_MAX_AGE)

## Names of the options on EPTR2(...) and eptr.call(...)
OPTION_NAMES = ("cache", "cache_path", "cache_overwrite", "cache_settle_days", "cache_max_age")

SCHEMA_VERSION = 1
_TRUE_VALUES = {"1", "true", "yes", "on"}

_UNSET = object()
_process: dict = {name: None for name in OPTION_NAMES}
_init_lock = threading.Lock()
_initialized: set[str] = set()
_announced = False


@dataclass(frozen=True)
class CacheSettings:
    path: str
    overwrite: bool
    settle_days: int | None  ## replaces DEFAULT_SETTLE_DAYS only (client/process/env)
    call_settle_days: int | None  ## replaces the key's rule (per call)
    max_age: float | None  ## days


def set_cache(
    enabled=_UNSET, path=_UNSET, overwrite=_UNSET, settle_days=_UNSET, max_age=_UNSET
) -> None:
    """Set the process-wide cache settings (experimental).

    Only the arguments given change; ``None`` clears one, so it follows the
    environment variable again. ``settle_days`` replaces only the general default
    window (2 days); calls with their own rule keep it.

    >>> import eptr2
    >>> eptr2.set_cache(True, path="/tmp/eptr2.sqlite")  # doctest: +SKIP
    """
    global _process
    new = dict(_process)
    for name, value in zip(OPTION_NAMES, (enabled, path, overwrite, settle_days, max_age)):
        if value is not _UNSET:
            new[name] = value
    _process = new


def _env_bool(name: str) -> bool | None:
    value = os.environ.get(name)
    if value is None or value.strip() == "":
        return None
    return value.strip().lower() in _TRUE_VALUES


def _env_number(name: str, cast):
    value = os.environ.get(name)
    if value is None or value.strip() == "":
        return None
    try:
        return cast(value.strip())
    except ValueError:
        logger.warning("Ignoring %s=%r: not a number.", name, value)
        return None


def default_cache_path() -> str:
    """``$XDG_CACHE_HOME/eptr2/responses.sqlite``, else ``~/.cache/eptr2/responses.sqlite``."""
    root = os.environ.get("XDG_CACHE_HOME") or os.path.join("~", ".cache")
    return os.path.abspath(os.path.expanduser(os.path.join(root, "eptr2", "responses.sqlite")))


def _first(*values):
    for v in values:
        if v is not None:
            return v
    return None


def resolve_cache_settings(call: dict | None = None, client: dict | None = None) -> CacheSettings | None:
    """Resolve the cache settings of one call, or None if the cache is off.

    ``call`` and ``client`` map the option names (:data:`OPTION_NAMES`) to values;
    None or a missing name defers to the next level (process, then environment).
    """
    call = call or {}
    client = client or {}
    p = _process

    def pick(name, env_value):
        return _first(call.get(name), client.get(name), p.get(name), env_value)

    enabled = pick("cache", _env_bool(ENV_ENABLED))
    if not enabled:
        return None
    path = pick("cache_path", os.environ.get(ENV_PATH) or None) or default_cache_path()
    overwrite = bool(pick("cache_overwrite", _env_bool(ENV_OVERWRITE)))
    settle_days = _first(client.get("cache_settle_days"), p.get("cache_settle_days"), _env_number(ENV_SETTLE_DAYS, int))
    max_age = pick("cache_max_age", _env_number(ENV_MAX_AGE, float))
    return CacheSettings(
        path=os.path.abspath(os.path.expanduser(str(path))),
        overwrite=overwrite,
        settle_days=None if settle_days is None else int(settle_days),
        call_settle_days=None if call.get("cache_settle_days") is None else int(call["cache_settle_days"]),
        max_age=None if max_age is None else float(max_age),
    )


def request_key(call_key: str, method: str, url: str, body_json: str) -> str:
    """Cache key of a request: a hash of the call key, method, URL and canonical body."""
    raw = json.dumps([call_key, method, url, body_json], separators=(",", ":"), ensure_ascii=False)
    return sha256(raw.encode("utf-8")).hexdigest()


def storable_items(data: bytes) -> int:
    """Number of records in a response body, 0 if it must not be stored.

    Only UTF-8 JSON objects with a non-empty ``items`` (or ``installedCapacities``)
    list count; empty, error-shaped and non-JSON bodies (a firewall page served with
    HTTP 200) give 0.
    """
    try:
        payload = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, ValueError, AttributeError):
        return 0
    if not isinstance(payload, dict):
        return 0
    for name in ("items", "installedCapacities"):
        value = payload.get(name)
        if isinstance(value, list) and value:
            return len(value)
    return 0


_SCHEMA = """
CREATE TABLE IF NOT EXISTS responses (
    cache_key TEXT PRIMARY KEY,
    call_key TEXT NOT NULL,
    method TEXT NOT NULL,
    url TEXT NOT NULL,
    request_body TEXT NOT NULL,
    end_date TEXT NOT NULL,
    response BLOB NOT NULL,
    n_items INTEGER NOT NULL,
    http_status INTEGER NOT NULL,
    fetched_at TEXT NOT NULL,
    eptr2_version TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS responses_call ON responses(call_key, end_date);
"""


def _connect(path: str, create: bool) -> sqlite3.Connection | None:
    """Open the cache file, creating the schema once per path; None if unusable."""
    global _announced
    if not create and not os.path.exists(path):
        return None
    if create:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    con = sqlite3.connect(path, timeout=30)
    try:
        with _init_lock:
            if path not in _initialized:
                con.execute("PRAGMA journal_mode=WAL")
                version = con.execute("PRAGMA user_version").fetchone()[0]
                if version > SCHEMA_VERSION:
                    con.close()
                    logger.warning(
                        "eptr2 cache %s has schema version %s (this eptr2 knows %s); not using it.",
                        path,
                        version,
                        SCHEMA_VERSION,
                    )
                    return None
                con.executescript(_SCHEMA)
                con.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
                _initialized.add(path)
                if not _announced:
                    _announced = True
                    logger.info("eptr2 response cache (experimental) in use: %s", path)
        con.execute("PRAGMA synchronous=NORMAL")
        return con
    except Exception:
        con.close()
        raise


def lookup(settings: CacheSettings, cache_key: str) -> dict | None:
    """Stored row for ``cache_key`` (with the decompressed ``response`` bytes), or None.

    Errors (unreadable file, corrupt row) are logged and count as a miss.
    """
    try:
        con = _connect(settings.path, create=False)
        if con is None:
            return None
        try:
            row = con.execute(
                "SELECT response, fetched_at, end_date, n_items, eptr2_version FROM responses WHERE cache_key = ?",
                (cache_key,),
            ).fetchone()
        finally:
            con.close()
        if row is None:
            return None
        return {
            "response": zlib.decompress(row[0]),
            "fetched_at": datetime.fromisoformat(row[1]),
            "end_date": date.fromisoformat(row[2]),
            "n_items": row[3],
            "eptr2_version": row[4],
        }
    except (sqlite3.Error, OSError, zlib.error, ValueError) as e:
        logger.warning("eptr2 cache lookup failed (%s); fetching instead.", e)
        return None


def store(
    settings: CacheSettings,
    cache_key: str,
    *,
    call_key: str,
    method: str,
    url: str,
    body_json: str,
    end_date: date,
    data: bytes,
    n_items: int,
    http_status: int,
) -> bool:
    """Insert or replace a row; False (logged) if the cache cannot be written."""
    from eptr2 import __version__

    try:
        con = _connect(settings.path, create=True)
        if con is None:
            return False
        try:
            with con:
                con.execute(
                    "INSERT OR REPLACE INTO responses VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        cache_key,
                        call_key,
                        method,
                        url,
                        body_json,
                        end_date.isoformat(),
                        zlib.compress(data),
                        int(n_items),
                        int(http_status),
                        datetime.now(timezone.utc).isoformat(),
                        str(__version__),
                    ),
                )
        finally:
            con.close()
        return True
    except (sqlite3.Error, OSError) as e:
        logger.warning("eptr2 cache store failed (%s); the result is returned uncached.", e)
        return False


def fetched_day_istanbul(fetched_at: datetime) -> date:
    return fetched_at.astimezone(_ISTANBUL).date()


def cache_info(path: str | None = None) -> dict:
    """Path, row count, size and rows per call key of a cache file."""
    path = os.path.abspath(os.path.expanduser(path)) if path else resolve_path()
    out = {"path": path, "exists": os.path.exists(path), "rows": 0, "bytes": 0, "calls": {}}
    if not out["exists"]:
        return out
    out["bytes"] = os.path.getsize(path)
    con = sqlite3.connect(path, timeout=30)
    try:
        rows = con.execute("SELECT call_key, COUNT(*) FROM responses GROUP BY call_key").fetchall()
    except sqlite3.Error:
        rows = []
    finally:
        con.close()
    out["calls"] = {k: n for k, n in rows}
    out["rows"] = sum(out["calls"].values())
    return out


def clear_cache(path: str | None = None, call_key: str | None = None) -> int:
    """Delete all rows (or one call key's rows) from a cache file; returns the count."""
    path = os.path.abspath(os.path.expanduser(path)) if path else resolve_path()
    if not os.path.exists(path):
        return 0
    con = sqlite3.connect(path, timeout=30)
    try:
        with con:
            if call_key is None:
                cur = con.execute("DELETE FROM responses")
            else:
                cur = con.execute("DELETE FROM responses WHERE call_key = ?", (call_key,))
        return cur.rowcount
    finally:
        con.close()


def resolve_path() -> str:
    """The cache path from the process setting, the environment or the default."""
    path = _process.get("cache_path") or os.environ.get(ENV_PATH) or default_cache_path()
    return os.path.abspath(os.path.expanduser(str(path)))
