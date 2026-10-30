"""Offline tests for the organization activity decomposition and IDM log statistics."""

import numpy as np
import pandas as pd
import pytest

from eptr2.composite.org_activity import (
    calculate_idm_contract_stats,
    calculate_org_activity,
)


@pytest.fixture
def log_df():
    return pd.DataFrame(
        {
            "contractName": ["PH26102000", "PH26102000", "PH26102001", "PB26102000"],
            "price": [100.0, 130.0, 200.0, 9999.0],
            "quantity": [20, 10, 5, 50],
        }
    )


def test_idm_contract_stats(log_df):
    stats = calculate_idm_contract_stats(log_df).set_index("contract")

    ## Non hourly (PB) contracts are left out
    assert list(stats.index) == ["PH26102000", "PH26102001"]

    ## wap = (100*20 + 130*10) / 30 = 110, tad = (20*10 + 10*20) / 30
    assert stats.loc["PH26102000", "idm_wap"] == pytest.approx(110.0)
    assert stats.loc["PH26102000", "idm_tad"] == pytest.approx(400 / 30)
    assert stats.loc["PH26102000", "idm_trade_count"] == 2
    ## Log quantities are lots of 0.1 MWh
    assert stats.loc["PH26102000", "idm_volume_mwh"] == pytest.approx(3.0)

    ## A single price has no deviation
    assert stats.loc["PH26102001", "idm_tad"] == pytest.approx(0.0)


def test_idm_contract_stats_empty():
    stats = calculate_idm_contract_stats(pd.DataFrame())
    assert stats.empty
    assert "idm_tad" in stats.columns


@pytest.fixture
def pos_df():
    return pd.DataFrame(
        {
            "contract": ["A", "B", "C", "D"],
            ## A: DA long, IDM net sell -> partly closed
            ## B: DA long, IDM net buy -> nothing closed
            ## C: DA short, IDM net buy more than DA -> fully closed, IDM residual is free
            ## D: no DA, only day trades
            "da_long": [100.0, 50.0, 0.0, 0.0],
            "da_short": [0.0, 0.0, 30.0, 0.0],
            "bi_long": [0.0, 0.0, 0.0, 0.0],
            "bi_short": [10.0, 0.0, 0.0, 0.0],
            "idm_long": [20.0, 40.0, 50.0, 15.0],
            "idm_short": [60.0, 10.0, 5.0, 15.0],
            "mcp": [1000.0, 1000.0, 1000.0, 1000.0],
            "idm_wap": [1100.0, 1100.0, 900.0, np.nan],
            "idm_tad": [50.0, 50.0, 40.0, 30.0],
        }
    )


def test_org_activity_decomposition(pos_df):
    df = calculate_org_activity(pos_df).set_index("contract")

    assert df["day_trade"].tolist() == [20.0, 10.0, 5.0, 15.0]
    assert df["dabi_idm_close"].tolist() == [40.0, 0.0, 30.0, 0.0]
    ## free = da_net + bi_net + idm_net (positive consume, negative generate)
    assert df["dabi_idm_net"].tolist() == [50.0, 80.0, 15.0, 0.0]
    ## dabi_net: day ahead (GÖP + İA) net position
    assert df["dabi_net"].tolist() == [90.0, 50.0, -30.0, 0.0]
    assert df["bi_net"].tolist() == [-10.0, 0.0, 0.0, 0.0]


def test_org_activity_pnl(pos_df):
    df = calculate_org_activity(pos_df).set_index("contract")

    ## DA long 40 sold in IDM 100 above MCP
    assert df.loc["A", "dabi_idm_pnl"] == pytest.approx(4000.0)
    ## DA short 30 bought back in IDM 100 below MCP
    assert df.loc["C", "dabi_idm_pnl"] == pytest.approx(3000.0)
    assert df.loc["B", "dabi_idm_pnl"] == 0.0

    assert df["day_trade_tad"].tolist() == pytest.approx([1000.0, 500.0, 200.0, 450.0])
    assert "total_pnl" not in df


def test_org_activity_missing_price_is_nan_not_zero(pos_df):
    pos_df.loc[0, "idm_wap"] = np.nan
    df = calculate_org_activity(pos_df).set_index("contract")
    assert np.isnan(df.loc["A", "dabi_idm_pnl"])
    ## Missing WAP without a closed quantity has no effect
    assert df.loc["D", "dabi_idm_pnl"] == 0.0


def test_org_activity_invariants(pos_df):
    df = calculate_org_activity(pos_df)
    assert np.allclose(df["idm_long"] + df["idm_short"], 2 * df["day_trade"] + df["idm_net"].abs())
    assert np.allclose(df["dabi_net"], df["da_net"] + df["bi_net"])
    assert np.allclose(df["dabi_idm_net"], df["dabi_net"] + df["idm_net"])
    assert (df["dabi_idm_close"] <= df["dabi_net"].abs()).all()
    assert (df["dabi_idm_close"] <= df["idm_net"].abs()).all()


def test_org_activity_without_bilateral(pos_df):
    df = calculate_org_activity(pos_df.drop(columns=["bi_long", "bi_short"]))
    assert (df["bi_net"] == 0).all()


def test_org_activity_without_prices_has_no_pnl(pos_df):
    df = calculate_org_activity(pos_df.drop(columns=["mcp", "idm_wap", "idm_tad"]))
    assert df["day_trade"].tolist() == [20.0, 10.0, 5.0, 15.0]
    assert df["dabi_idm_net"].tolist() == [50.0, 80.0, 15.0, 0.0]
    assert "dabi_idm_pnl" not in df


def test_org_activity_tad_without_prices(pos_df):
    """TAD is a volatility metric: day_trade_tad needs no MCP or WAP"""
    df = calculate_org_activity(pos_df.drop(columns=["mcp", "idm_wap"]))
    assert df["day_trade_tad"].tolist() == pytest.approx([1000.0, 500.0, 200.0, 450.0])
    assert "dabi_idm_pnl" not in df


def test_org_activity_wap_only_pnl(pos_df):
    df = calculate_org_activity(pos_df.drop(columns=["idm_tad"]))
    assert "day_trade_tad" not in df
    assert df.set_index("contract").loc["A", "dabi_idm_pnl"] == pytest.approx(4000.0)


def test_org_activity_bilateral_position_closed_in_idm():
    """A bilateral (İA) long sold in the intraday market is a day ahead open / intraday close"""
    df = calculate_org_activity(
        pd.DataFrame(
            {
                "da_long": [0.0],
                "da_short": [0.0],
                "bi_long": [50.0],
                "bi_short": [0.0],
                "idm_long": [0.0],
                "idm_short": [30.0],
                "mcp": [1000.0],
                "idm_wap": [1100.0],
            }
        )
    )
    assert df.loc[0, "dabi_idm_close"] == 30.0
    assert df.loc[0, "dabi_idm_pnl"] == pytest.approx(3000.0)
    assert df.loc[0, "dabi_idm_net"] == 20.0


class _FakeEPTR:
    def __init__(self, fail=False):
        self.fail = fail

    def call(self, key, **kwargs):
        if self.fail:
            raise AssertionError(f"{key} should have been read from file")
        dates = ["2026-10-20T00:00:00+03:00", "2026-10-20T01:00:00+03:00"]
        if key == "mcp":
            return pd.DataFrame({"date": dates, "price": [1000.0, 1200.0]})
        return pd.DataFrame({"date": dates, "wap": [1100.0, 1150.0]})


def test_get_org_estimated_activity_export_and_reuse(tmp_path, monkeypatch):
    """export_to_csv writes the raw data, check_existing reads it back without fetching"""
    import eptr2.composite.org_activity as oa

    contracts = [f"PH261020{h:02d}" for h in range(24)]
    pos_df = pd.DataFrame(
        {
            "contract": contracts,
            "date": [f"2026-10-20T{h:02d}:00:00+03:00" for h in range(24)],
            "da_long": [100.0] * 24,
            "da_short": [0.0] * 24,
            "bi_long": [0.0] * 24,
            "bi_short": [0.0] * 24,
            "idm_long": [10.0] * 24,
            "idm_short": [40.0] * 24,
        }
    )
    log_df = pd.DataFrame(
        {
            "contractName": ["PH26102000", "PH26102000", "PH26102001"],
            "price": [1050.0, 1150.0, 1150.0],
            "quantity": [10, 10, 5],
        }
    )
    calls = []
    monkeypatch.setattr(
        oa, "get_dabi_idm_data", lambda **kw: calls.append("pos") or pos_df.copy()
    )
    monkeypatch.setattr(
        oa, "idm_log_longer", lambda **kw: calls.append("log") or log_df.copy()
    )
    kw = dict(
        start_date="2026-10-20",
        end_date="2026-10-20",
        org_id=1,
        include_pnl=True,
        include_tad=True,
        export_dir=str(tmp_path),
        verbose=False,
    )

    first = oa.get_org_estimated_activity(eptr=_FakeEPTR(), export_to_csv=True, **kw)
    names = sorted(f.name for f in tmp_path.iterdir())
    assert names == [
        f"{n}_2026-10-20_2026-10-20.csv"
        for n in sorted(
            [
                "idm_contract_stats",
                "idm_log",
                "mcp",
                "org_1_activity",
                "org_1_positions",
                "wap",
            ]
        )
    ]
    assert calls == ["pos", "log"]

    second = oa.get_org_estimated_activity(
        eptr=_FakeEPTR(fail=True), check_existing=True, **kw
    )
    assert calls == ["pos", "log"]
    pd.testing.assert_frame_equal(first, second, check_dtype=False)
    assert first.loc[0, "idm_tad"] == pytest.approx(50.0)


@pytest.mark.parametrize("end_date", ["2026-10-30", "2026-10-31"])
def test_get_org_estimated_activity_rejects_today_or_later(end_date, monkeypatch):
    """Data of the current day is not final, so end_date must be before today"""
    import eptr2.composite.org_activity as oa

    monkeypatch.setattr(oa, "get_today_utc3", lambda: "2026-10-30")
    with pytest.raises(ValueError, match="before today"):
        oa.get_org_estimated_activity(
            start_date="2026-10-29", end_date=end_date, org_id=1, eptr=_FakeEPTR(fail=True)
        )
