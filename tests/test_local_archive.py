"""Experimental local SQLite archive (eptr2.archive, eptr2.mapping.settle)."""

import json
import sqlite3
import threading
from datetime import date, timedelta
from types import SimpleNamespace

import pytest

import eptr2.archive as archive
import eptr2.main as main
from eptr2 import EPTR2, set_archive
from eptr2.mapping import get_path_map
from eptr2.mapping import settle

OLD = "2026-01-05"  ## settled for every rule


@pytest.fixture(autouse=True)
def _isolate(monkeypatch, tmp_path):
    monkeypatch.setattr(archive, "_process", {n: None for n in archive.OPTION_NAMES})
    monkeypatch.setattr(archive, "_initialized", set())
    ## setenv first so monkeypatch restores the original state even when a test
    ## (the .env loader) sets a variable that was unset
    for name in archive.ENV_VARS + ("EPTR_USERNAME", "EPTR_PASSWORD"):
        monkeypatch.setenv(name, "")
        monkeypatch.delenv(name)
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "xdg"))


class Transport:
    def __init__(self, items=None, body=None, status=200, exc=None):
        self.n = 0
        self.items = [{"date": "2026-01-05T00:00:00+03:00", "price": 1.0}] if items is None else items
        self.body = body
        self.status = status
        self.exc = exc
        self.bodies = []

    def __call__(self, *a, **kw):
        self.n += 1
        self.bodies.append(kw.get("call_body"))
        if self.exc is not None:
            raise self.exc
        data = self.body if self.body is not None else json.dumps({"items": self.items}).encode()
        return SimpleNamespace(data=data, status=self.status)


def _client(monkeypatch, transport, **attrs):
    eptr = EPTR2.__new__(EPTR2)
    eptr.renewals = 0

    def renew(**kw):
        eptr.renewals += 1

    eptr.check_renew_tgt = renew
    eptr.custom_aliases = {}
    eptr.path_map_keys = get_path_map(just_call_keys=True)
    eptr.root_phrase = "https://seffaflik.epias.com.tr"
    eptr.ssl_verify = True
    eptr.is_test = False
    eptr.tgt = "TGT-SECRET"
    eptr.tgt_exp = 9999999999
    eptr.recycle_tgt = False
    eptr.postprocess = False
    eptr.get_raw_response = False
    eptr.strict_params = True
    eptr.username = "someone@example.com"
    for k, v in attrs.items():
        eptr.__dict__[k] = v
    monkeypatch.setattr(main, "transparency_call", transport)
    return eptr


def _mcp(eptr, day=OLD, **kw):
    return eptr.call("mcp", start_date=day, end_date=day, **kw)


def _rows(path):
    con = sqlite3.connect(path)
    try:
        return con.execute("SELECT * FROM responses").fetchall()
    finally:
        con.close()


def test_off_by_default(monkeypatch, tmp_path):
    t = Transport()
    eptr = _client(monkeypatch, t)
    _mcp(eptr)
    _mcp(eptr)
    assert t.n == 2
    assert not (tmp_path / "xdg").exists()


def test_miss_then_hit_without_network_or_login(monkeypatch, tmp_path):
    t = Transport()
    path = tmp_path / "c.sqlite"
    eptr = _client(monkeypatch, t, archive=True, archive_path=str(path))
    first = _mcp(eptr)
    assert (t.n, eptr.renewals) == (1, 1)
    second = _mcp(eptr)
    assert (t.n, eptr.renewals) == (1, 1)
    assert first == second
    ## The same row serves the postprocessed frame.
    df = _mcp(eptr, postprocess=True)
    assert t.n == 1 and len(df) == 1


def test_default_path_and_env_switches(monkeypatch, tmp_path):
    t = Transport()
    eptr = _client(monkeypatch, t)
    monkeypatch.setenv("EPTR2_ARCHIVE", "yes")
    _mcp(eptr)
    _mcp(eptr)
    assert t.n == 1
    assert (tmp_path / "xdg" / "eptr2" / "archive.sqlite").exists()
    monkeypatch.setenv("EPTR2_ARCHIVE", "0")
    _mcp(eptr)
    assert t.n == 2


def test_resolution_order(monkeypatch, tmp_path):
    t = Transport()
    eptr = _client(monkeypatch, t, archive=False)
    set_archive(True, path=str(tmp_path / "p.sqlite"))
    _mcp(eptr)
    _mcp(eptr)
    assert t.n == 2  ## client off beats process on
    _mcp(eptr, archive=True)
    _mcp(eptr, archive=True)
    assert t.n == 3  ## call on beats client off
    ## set_archive changes only the arguments given
    set_archive(overwrite=True)
    assert archive._process["archive"] is True
    set_archive(enabled=None)
    assert archive.resolve_archive_settings() is None


def test_dotenv_reads_archive_variables(monkeypatch, tmp_path):
    from eptr2.main import load_eptr_credentials_from_dotenv

    env = tmp_path / ".env"
    env.write_text(f"EPTR_USERNAME=a\nEPTR_PASSWORD=b\nEPTR2_ARCHIVE=1\nEPTR2_ARCHIVE_PATH={tmp_path / 'd.sqlite'}\n")
    monkeypatch.setenv("EPTR2_ARCHIVE_SETTLE_DAYS", "5")
    load_eptr_credentials_from_dotenv(str(env))
    s = archive.resolve_archive_settings()
    assert s.path == str(tmp_path / "d.sqlite")
    assert s.settle_days == 5


def test_key_identity(monkeypatch, tmp_path):
    t = Transport()
    eptr = _client(monkeypatch, t, archive=True, archive_path=str(tmp_path / "c.sqlite"))
    eptr.call("mcp", start_date=OLD, end_date=OLD)
    eptr.call("ptf", end_date=OLD, start_date=OLD)  ## alias, other kwarg order
    eptr.call("mcp", start_date=date(2026, 1, 5), end_date=date(2026, 1, 5))
    assert t.n == 1
    eptr.call("dam-clearing", start_date=OLD, end_date=OLD, transparency_warnings=False)
    eptr.call("dam-clearing", start_date=OLD, end_date=OLD, org_id=1, transparency_warnings=False)
    assert t.n == 3
    eptr.root_phrase = "https://seffaflik-prp.epias.com.tr"
    _mcp(eptr)
    assert t.n == 4
    for row in _rows(tmp_path / "c.sqlite"):
        text = repr(row)
        assert "TGT-SECRET" not in text and "someone@example.com" not in text


def test_settle_windows():
    d = date(2026, 3, 10)
    assert settle.settled_from("mcp", d) == d + timedelta(days=2)
    assert settle.settled_from("kgup", d) == d + timedelta(days=9)
    assert settle.settled_from("dam-clearing", d) == d + timedelta(days=6)
    assert settle.settled_from("bi-euas", d) == d + timedelta(days=120)
    assert settle.settled_from("uevm", d) == date(2026, 3, 31) + timedelta(days=45)
    assert settle.settled_from("mcp", d, default_days=0) == d
    assert settle.settled_from("uevm", d, default_days=0) == date(2026, 3, 31) + timedelta(days=45)
    assert settle.settled_from("uevm", d, call_days=0) == d
    assert settle.request_end_date({"period": "2026-02-01T00:00:00+03:00"}) == date(2026, 2, 28)
    assert settle.request_end_date({"start_date": "2026-02-01", "end_date": "2026-02-03"}) == date(2026, 2, 3)
    assert settle.request_end_date({"org_id": 1}) is None
    assert settle.request_end_date({"date_time": "garbage!!!"}) is None


def test_unsettled_and_spanning_requests_are_not_stored(monkeypatch, tmp_path):
    t = Transport()
    path = tmp_path / "c.sqlite"
    eptr = _client(monkeypatch, t, archive=True, archive_path=str(path))
    today = settle.today_istanbul()
    yesterday = (today - timedelta(days=1)).isoformat()
    eptr.call("mcp", start_date=OLD, end_date=yesterday)
    eptr.call("mcp", start_date=OLD, end_date=yesterday)
    assert t.n == 2
    assert not path.exists() or _rows(path) == []


def test_short_window_row_not_served_to_default_reader(monkeypatch, tmp_path):
    t = Transport()
    eptr = _client(monkeypatch, t, archive=True, archive_path=str(tmp_path / "c.sqlite"))
    yesterday = (settle.today_istanbul() - timedelta(days=1)).isoformat()
    _mcp(eptr, day=yesterday, archive_settle_days=0)
    _mcp(eptr, day=yesterday, archive_settle_days=0)
    assert t.n == 1
    _mcp(eptr, day=yesterday)
    assert t.n == 2


def test_undated_and_never_archive_calls(monkeypatch, tmp_path):
    t = Transport()
    eptr = _client(monkeypatch, t, archive=True, archive_path=str(tmp_path / "c.sqlite"))
    eptr.call("pp-list")
    eptr.call("pp-list")
    eptr.call("page-update-date")
    eptr.call("page-update-date")
    assert t.n == 4


@pytest.mark.parametrize(
    "body",
    [
        json.dumps({"items": []}).encode(),
        b"<html>Request blocked</html>",
        json.dumps([1, 2]).encode(),
    ],
)
def test_invalid_bodies_are_not_stored(monkeypatch, tmp_path, body):
    path = tmp_path / "c.sqlite"
    t = Transport(body=body)
    eptr = _client(monkeypatch, t, archive=True, archive_path=str(path))
    for _ in range(2):
        try:
            _mcp(eptr)
        except ValueError:
            pass  ## the HTML page does not decode as JSON
    assert t.n == 2
    assert not path.exists() or _rows(path) == []
    assert archive.storable_items(body) == 0


def test_installed_capacities_body_is_storable():
    assert archive.storable_items(json.dumps({"installedCapacities": [{"a": 1}]}).encode()) == 1


def test_overwrite_replaces_and_failures_keep_the_row(monkeypatch, tmp_path):
    path = tmp_path / "c.sqlite"
    t = Transport(items=[{"v": 1}])
    eptr = _client(monkeypatch, t, archive=True, archive_path=str(path))
    _mcp(eptr)
    t.items = [{"v": 2}]
    assert _mcp(eptr, archive_overwrite=True)["items"] == [{"v": 2}]
    assert _mcp(eptr)["items"] == [{"v": 2}] and t.n == 2
    t.items = []
    assert _mcp(eptr, archive_overwrite=True)["items"] == []
    t.exc = RuntimeError("boom")
    with pytest.raises(RuntimeError):
        _mcp(eptr, archive_overwrite=True)
    t.exc = None
    assert _mcp(eptr)["items"] == [{"v": 2}]
    assert len(_rows(path)) == 1


def test_bypass_raw_response(monkeypatch, tmp_path):
    t = Transport()
    eptr = _client(monkeypatch, t, archive=True, archive_path=str(tmp_path / "c.sqlite"))
    _mcp(eptr, get_raw_response=True)
    _mcp(eptr, get_raw_response=True)
    assert t.n == 2


def test_broken_archive_files_fall_back_to_network(monkeypatch, tmp_path):
    t = Transport()
    bad = tmp_path / "bad.sqlite"
    bad.write_bytes(b"not a database at all" * 100)
    eptr = _client(monkeypatch, t, archive=True, archive_path=str(bad))
    assert _mcp(eptr)["items"]
    newer = tmp_path / "newer.sqlite"
    con = sqlite3.connect(newer)
    con.execute("PRAGMA user_version = 99")
    con.close()
    _mcp(eptr, archive_path=str(newer))
    _mcp(eptr, archive_path=str(newer))
    assert t.n == 3
    blocked = tmp_path / "file"
    blocked.write_text("x")
    _mcp(eptr, archive_path=str(blocked / "sub" / "c.sqlite"))
    assert t.n == 4


def test_row_metadata_wal_and_threads(monkeypatch, tmp_path):
    from eptr2 import __version__

    path = tmp_path / "c.sqlite"
    t = Transport()
    eptr = _client(monkeypatch, t, archive=True, archive_path=str(path))
    days = [f"2026-01-{d:02d}" for d in range(1, 13)]
    threads = [threading.Thread(target=_mcp, args=(eptr, d)) for d in days]
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    rows = _rows(path)
    assert len(rows) == 12
    assert {r[1] for r in rows} == {"mcp"} and {r[8] for r in rows} == {200}
    assert {r[10] for r in rows} == {str(__version__)}
    con = sqlite3.connect(path)
    assert con.execute("PRAGMA journal_mode").fetchone()[0] == "wal"
    con.close()


def test_archive_info_and_clear(monkeypatch, tmp_path):
    path = str(tmp_path / "c.sqlite")
    t = Transport()
    eptr = _client(monkeypatch, t, archive=True, archive_path=path)
    _mcp(eptr)
    _mcp(eptr, day="2026-01-06")
    eptr.call("smp", start_date=OLD, end_date=OLD)
    info = archive.archive_info(path)
    assert info["rows"] == 3
    assert info["calls"]["mcp"] == {"rows": 2, "first_end_date": "2026-01-05", "last_end_date": "2026-01-06"}
    assert info["calls"]["smp"]["rows"] == 1
    assert archive.clear_archive(path, call_key="smp") == 1
    assert archive.clear_archive(path) == 2


def test_registry_keys_exist():
    keys = set(get_path_map(just_call_keys=True))
    assert set(settle.SETTLE_RULES) <= keys
    assert settle.NEVER_ARCHIVE <= keys


def test_every_monthly_call_has_a_month_rule():
    from eptr2.mapping.parameters import get_optional_parameters, get_required_parameters

    missing = []
    for key in get_path_map(just_call_keys=True):
        params = get_required_parameters(key) + get_optional_parameters(key)
        if key in settle.NEVER_ARCHIVE or not any(p in settle._MONTH_PARAMS for p in params):
            continue
        if settle.SETTLE_RULES.get(key, ("days", 0))[0] != "month":
            missing.append(key)
    assert missing == []


def test_invalid_key_raises_before_login(monkeypatch):
    t = Transport()
    eptr = _client(monkeypatch, t)
    with pytest.raises(Exception, match="not yet defined"):
        eptr.call("no-such-call")
    assert eptr.renewals == 0
