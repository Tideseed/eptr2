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
    assert df["da_id_close"].tolist() == [40.0, 0.0, 30.0, 0.0]
    ## free = da_net + bi_net + idm_net (positive consume, negative generate)
    assert df["dabi_idm_net"].tolist() == [50.0, 80.0, 15.0, 0.0]
    ## dabi_net: day ahead (GÖP + İA) net position
    assert df["dabi_net"].tolist() == [90.0, 50.0, -30.0, 0.0]
    assert df["bi_net"].tolist() == [-10.0, 0.0, 0.0, 0.0]


def test_org_activity_pnl(pos_df):
    df = calculate_org_activity(pos_df).set_index("contract")

    ## DA long 40 sold in IDM 100 above MCP
    assert df.loc["A", "da_id_pnl"] == pytest.approx(4000.0)
    ## DA short 30 bought back in IDM 100 below MCP
    assert df.loc["C", "da_id_pnl"] == pytest.approx(3000.0)
    assert df.loc["B", "da_id_pnl"] == 0.0

    assert df["day_trade_pnl"].tolist() == pytest.approx([1000.0, 500.0, 200.0, 450.0])
    assert df.loc["A", "total_pnl"] == pytest.approx(5000.0)


def test_org_activity_missing_price_is_nan_not_zero(pos_df):
    pos_df.loc[0, "idm_wap"] = np.nan
    df = calculate_org_activity(pos_df).set_index("contract")
    assert np.isnan(df.loc["A", "da_id_pnl"])
    assert np.isnan(df.loc["A", "total_pnl"])
    ## Missing WAP without a closed quantity has no effect
    assert df.loc["D", "da_id_pnl"] == 0.0


def test_org_activity_invariants(pos_df):
    df = calculate_org_activity(pos_df)
    assert np.allclose(df["idm_long"] + df["idm_short"], 2 * df["day_trade"] + df["idm_net"].abs())
    assert np.allclose(df["dabi_net"], df["da_net"] + df["bi_net"])
    assert np.allclose(df["dabi_idm_net"], df["dabi_net"] + df["idm_net"])
    assert (df["da_id_close"] <= df["da_net"].abs()).all()
    assert (df["da_id_close"] <= df["idm_net"].abs()).all()


def test_org_activity_without_bilateral(pos_df):
    df = calculate_org_activity(pos_df.drop(columns=["bi_long", "bi_short"]))
    assert (df["bi_net"] == 0).all()


def test_org_activity_without_prices_has_no_pnl(pos_df):
    df = calculate_org_activity(pos_df.drop(columns=["mcp", "idm_wap", "idm_tad"]))
    assert df["day_trade"].tolist() == [20.0, 10.0, 5.0, 15.0]
    assert df["dabi_idm_net"].tolist() == [50.0, 80.0, 15.0, 0.0]
    assert "total_pnl" not in df


def test_org_activity_wap_only_pnl(pos_df):
    df = calculate_org_activity(pos_df.drop(columns=["idm_tad"]))
    assert "day_trade_pnl" not in df
    assert df["total_pnl"].tolist() == df["da_id_pnl"].tolist()
    assert df.set_index("contract").loc["A", "da_id_pnl"] == pytest.approx(4000.0)
