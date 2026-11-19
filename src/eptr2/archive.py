"""Experimental local SQLite archive of EPİAŞ responses.

Off by default. When on, :meth:`eptr2.EPTR2.call` answers a request from a local
SQLite file if it has it, and keeps settled responses after fetching them, so an
archive builds up as a side effect of ordinary use. A hit needs no network and no
login, and goes through the normal postprocessing, so ``postprocess=True`` and
``False`` share one row and later fixes in eptr2's processing apply to archived data.
Archived rows do not expire.

Settings (the narrowest one given wins):

- per call: ``eptr.call(..., archive=True, archive_path=..., archive_overwrite=True,
  archive_settle_days=...)``
- per client: ``EPTR2(..., archive=True, archive_path=..., ...)`` (same names)
- per process: :func:`set_archive`
- by environment: ``EPTR2_ARCHIVE``, ``EPTR2_ARCHIVE_PATH``, ``EPTR2_ARCHIVE_OVERWRITE``,
  ``EPTR2_ARCHIVE_SETTLE_DAYS`` (also read from the ``.env`` file of
  ``EPTR2(use_dotenv=True)``; a variable already set in the environment wins)

What is kept (see :mod:`eptr2.mapping.settle`):

- only responses whose last date is outside the call's settle window; a request
  reaching into the window is not kept at all
- only JSON bodies with a non-empty ``items`` list (or ``installedCapacities``):
  empty, error and non-JSON (e.g. a firewall page) responses are not kept
- never requests without a date parameter, nor :data:`~eptr2.mapping.settle.NEVER_ARCHIVE` calls

Rows are keyed by the exact request, so the same period asked as one range and as
single days is kept twice, and a different range is fetched. ``archive_overwrite=True``
skips the lookup, fetches and replaces the row; a failed, empty or unsettled refetch
keeps the existing row.
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

ENV_ENABLED = "EPTR2_ARCHIVE"
ENV_PATH = "EPTR2_ARCHIVE_PATH"
ENV_OVERWRITE = "EPTR2_ARCHIVE_OVERWRITE"
ENV_SETTLE_DAYS = "EPTR2_ARCHIVE_SETTLE_DAYS"
ENV_VARS = (ENV_ENABLED, ENV_PATH, ENV_OVERWRITE, ENV_SETTLE_DAYS)

## Names of the options on EPTR2(...) and eptr.call(...)
OPTION_NAMES = ("archive", "archive_path", "archive_overwrite", "archive_settle_days")

SCHEMA_VERSION = 1
_TRUE_VALUES = {"1", "true", "yes", "on"}

_UNSET = object()
_process: dict = {name: None for name in OPTION_NAMES}
_init_lock = threading.Lock()
_initialized: set[str] = set()
_announced = False


@dataclass(frozen=True)
class ArchiveSettings:
    path: str
    overwrite: bool
    settle_days: int | None  ## replaces DEFAULT_SETTLE_DAYS only (client/process/env)
    call_settle_days: int | None  ## replaces the key's rule (per call)


def set_archive(enabled=_UNSET, path=_UNSET, overwrite=_UNSET, settle_days=_UNSET) -> None:
    """Set the process-wide archive settings (experimental).

    Only the arguments given change; ``None`` clears one, so it follows the
    environment variable again. ``settle_days`` replaces only the general default
    window (2 days); calls with their own rule keep it.

    >>> import eptr2
    >>> eptr2.set_archive(True, path="/data/eptr2_archive.sqlite")  # doctest: +SKIP
    """
    global _process
    new = dict(_process)
    for name, value in zip(OPTION_NAMES, (enabled, path, overwrite, settle_days)):
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


def default_archive_path() -> str:
    """``$XDG_DATA_HOME/eptr2/archive.sqlite``, else ``~/.local/share/eptr2/archive.sqlite``.

    A data directory, not a cache directory: cleanup tools may empty cache directories.
    """
    root = os.environ.get("XDG_DATA_HOME") or os.path.join("~", ".local", "share")
    return os.path.abspath(os.path.expanduser(os.path.join(root, "eptr2", "archive.sqlite")))


def _first(*values):
    for v in values:
        if v is not None:
            return v
    return None


def resolve_archive_settings(call: dict | None = None, client: dict | None = None) -> ArchiveSettings | None:
    """Resolve the archive settings of one call, or None if the archive is off.

    ``call`` and ``client`` map the option names (:data:`OPTION_NAMES`) to values;
    None or a missing name defers to the next level (process, then environment).
    """
    call = call or {}
    client = client or {}
    p = _process

    def pick(name, env_value):
        return _first(call.get(name), client.get(name), p.get(name), env_value)

    enabled = pick("archive", _env_bool(ENV_ENABLED))
    if not enabled:
        return None
    path = pick("archive_path", os.environ.get(ENV_PATH) or None) or default_archive_path()
    overwrite = bool(pick("archive_overwrite", _env_bool(ENV_OVERWRITE)))
    settle_days = _first(
        client.get("archive_settle_days"), p.get("archive_settle_days"), _env_number(ENV_SETTLE_DAYS, int)
    )
    call_days = call.get("archive_settle_days")
    return ArchiveSettings(
        path=os.path.abspath(os.path.expanduser(str(path))),
        overwrite=overwrite,
        settle_days=None if settle_days is None else int(settle_days),
        call_settle_days=None if call_days is None else int(call_days),
    )


def request_key(call_key: str, method: str, url: str, body_json: str) -> str:
    """Archive key of a request: a hash of the call key, method, URL and canonical body."""
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
    request_key TEXT PRIMARY KEY,
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
    """Open the archive file, creating the schema once per path; None if unusable."""
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
                        "eptr2 archive %s has schema version %s (this eptr2 knows %s); not using it.",
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
                    logger.info("eptr2 local archive (experimental) in use: %s", path)
        con.execute("PRAGMA synchronous=NORMAL")
        return con
    except Exception:
        con.close()
        raise


def lookup(settings: ArchiveSettings, archive_key: str) -> dict | None:
    """Archived row for ``archive_key`` (with the decompressed ``response`` bytes), or None.

    Errors (unreadable file, corrupt row) are logged and count as a miss.
    """
    try:
        con = _connect(settings.path, create=False)
        if con is None:
            return None
        try:
            row = con.execute(
                "SELECT response, fetched_at, end_date, n_items, eptr2_version FROM responses WHERE request_key = ?",
                (archive_key,),
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
        logger.warning("eptr2 archive lookup failed (%s); fetching instead.", e)
        return None


def store(
    settings: ArchiveSettings,
    archive_key: str,
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
    """Insert or replace a row; False (logged) if the archive cannot be written."""
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
                        archive_key,
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
        logger.warning("eptr2 archive store failed (%s); the result is returned without archiving.", e)
        return False


def fetched_day_istanbul(fetched_at: datetime) -> date:
    return fetched_at.astimezone(_ISTANBUL).date()


def archive_info(path: str | None = None) -> dict:
    """Path, size, row count and, per call key, rows and the range of archived end dates."""
    path = os.path.abspath(os.path.expanduser(path)) if path else resolve_path()
    out = {"path": path, "exists": os.path.exists(path), "rows": 0, "bytes": 0, "calls": {}}
    if not out["exists"]:
        return out
    out["bytes"] = os.path.getsize(path)
    con = sqlite3.connect(path, timeout=30)
    try:
        rows = con.execute(
            "SELECT call_key, COUNT(*), MIN(end_date), MAX(end_date) FROM responses GROUP BY call_key"
        ).fetchall()
    except sqlite3.Error:
        rows = []
    finally:
        con.close()
    out["calls"] = {k: {"rows": n, "first_end_date": lo, "last_end_date": hi} for k, n, lo, hi in rows}
    out["rows"] = sum(v["rows"] for v in out["calls"].values())
    return out


def clear_archive(path: str | None = None, call_key: str | None = None) -> int:
    """Delete all rows (or one call key's rows) from an archive file; returns the count."""
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
    """The archive path from the process setting, the environment or the default."""
    path = _process.get("archive_path") or os.environ.get(ENV_PATH) or default_archive_path()
    return os.path.abspath(os.path.expanduser(str(path)))
