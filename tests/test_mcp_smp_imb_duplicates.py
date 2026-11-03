"""EPİAŞ's mcp-smp-imb returned every hour of 2026-11-01 twice; eptr2 keeps one row per hour (no credentials needed)."""
import logging

import pytest

from eptr2.util.costs import calculate_imbalance_prices

ROW = {
    "date": "2026-11-01T00:00:00+03:00",
    "time": "2026-11-01T00:00:00+03:00",
    "ptf": 3633.99,
    "smf": 2600.0,
    "positiveImbalance": 2444.0,
    "negativeImbalance": 3743.0097,
    "systemStatus": "Enerji Fazlası",
}
NEXT = {**ROW, "date": "2026-11-01T01:00:00+03:00", "time": "2026-11-01T01:00:00+03:00"}


@pytest.fixture
def eptr2_caplog(caplog, monkeypatch):
    ## the eptr2 logger writes to its own stderr handler and does not propagate
    monkeypatch.setattr(logging.getLogger("eptr2"), "propagate", True)
    return caplog


def _client(monkeypatch, items):
    """Offline client (as in test_agent_contract_regressions) returning ``items``, with postprocessing on."""
    import json
    from types import SimpleNamespace

    import eptr2.main as main
    from eptr2 import EPTR2
    from eptr2.mapping import get_path_map

    eptr = EPTR2.__new__(EPTR2)
    eptr.check_renew_tgt = lambda **kw: None
    eptr.custom_aliases = {}
    eptr.path_map_keys = get_path_map(just_call_keys=True)
    eptr.root_phrase = "https://example.invalid"
    eptr.ssl_verify = True
    eptr.is_test = False
    eptr.tgt = "TGT-FAKE"
    eptr.tgt_exp = 9999999999
    eptr.recycle_tgt = False
    eptr.postprocess = True
    eptr.get_raw_response = False
    eptr.strict_params = True  # drop_duplicates must be a reserved option, not an unknown parameter
    response = SimpleNamespace(data=json.dumps({"items": items}).encode(), status=200)
    monkeypatch.setattr(main, "transparency_call", lambda *a, **kw: response)
    return eptr


def test_call_keeps_duplicates_by_default(monkeypatch):
    eptr = _client(monkeypatch, [ROW, ROW, NEXT])
    assert len(eptr.call("mcp-smp-imb", start_date="2026-11-01", end_date="2026-11-01")) == 3


def test_call_drop_duplicates(monkeypatch, eptr2_caplog):
    eptr = _client(monkeypatch, [ROW, ROW, NEXT, {**NEXT, "smf": 2700.0}])
    with eptr2_caplog.at_level(logging.WARNING):
        df = eptr.call(
            "mcp-smp-imb", start_date="2026-11-01", end_date="2026-11-01", drop_duplicates=True
        )
    assert len(df) == 3  # identical rows dropped, differing rows of the same hour kept
    assert "dropped 1 duplicate" in eptr2_caplog.text


def test_calculate_imbalance_prices_one_row_per_hour():
    rows = calculate_imbalance_prices(prices=[ROW, ROW, NEXT, NEXT], return_df=False)
    assert [r["contract"] for r in rows] == ["PH26110100", "PH26110101"]


def test_calculate_imbalance_prices_conflicting_rows_raise():
    with pytest.raises(ValueError, match="Conflicting price rows for PH26110100"):
        calculate_imbalance_prices(prices=[ROW, {**ROW, "smf": 2700.0}], return_df=False)
