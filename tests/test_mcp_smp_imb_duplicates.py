"""EPİAŞ's mcp-smp-imb returned every hour of 2026-11-01 twice; eptr2 keeps one row per hour (no credentials needed)."""
import logging

import pytest

from eptr2.mapping.processing import get_postprocess_function
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


def test_postprocess_drops_identical_duplicates(eptr2_caplog):
    res = {"items": [ROW, ROW, NEXT, NEXT]}
    with eptr2_caplog.at_level(logging.WARNING):
        df = get_postprocess_function("mcp-smp-imb")(res, key="mcp-smp-imb")
    assert len(df) == 2 and df["date"].is_unique
    assert "dropped 2 duplicate" in eptr2_caplog.text


def test_postprocess_keeps_conflicting_rows_with_warning(eptr2_caplog):
    res = {"items": [ROW, {**ROW, "smf": 2700.0}]}
    with eptr2_caplog.at_level(logging.WARNING):
        df = get_postprocess_function("mcp-smp-imb")(res, key="mcp-smp-imb")
    assert len(df) == 2
    assert "conflicting rows" in eptr2_caplog.text


def test_calculate_imbalance_prices_one_row_per_hour():
    rows = calculate_imbalance_prices(prices=[ROW, ROW, NEXT, NEXT], return_df=False)
    assert [r["contract"] for r in rows] == ["PH26110100", "PH26110101"]


def test_calculate_imbalance_prices_conflicting_rows_raise():
    with pytest.raises(ValueError, match="Conflicting price rows for PH26110100"):
        calculate_imbalance_prices(prices=[ROW, {**ROW, "smf": 2700.0}], return_df=False)
