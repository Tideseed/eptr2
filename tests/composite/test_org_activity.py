## Add test for eptr2/composite/org_activity.py
from eptr2.composite.org_activity import get_org_estimated_activity
from dotenv import load_dotenv
from eptr2 import EPTR2
import numpy as np


def test_get_org_estimated_activity():
    """Positions only: GÖP, İA and GİP matchings by organization id, no trade log"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()
    df = get_org_estimated_activity(
        start_date="2026-10-20",
        end_date="2026-10-20",
        org_id=104000,
        eptr=eptr,
    )

    assert len(df) == 24
    for col in ["day_trade", "da_id_close", "free_qty"]:
        assert col in df
    assert "total_pnl" not in df and "idm_wap" not in df
    assert np.allclose(df["free_qty"], df["da_net"] + df["bi_net"] + df["idm_net"])


def test_get_org_estimated_activity_with_pnl():
    """include_pnl adds MCP, published WAP and the DA open / IDM close PnL, without the trade log"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()
    df = get_org_estimated_activity(
        start_date="2026-10-20",
        end_date="2026-10-20",
        org_id=104000,
        eptr=eptr,
        include_pnl=True,
    )

    assert len(df) == 24
    for col in ["mcp", "idm_wap", "da_id_pnl", "total_pnl"]:
        assert col in df
    assert "idm_tad" not in df and "day_trade_pnl" not in df
    assert df["idm_wap"].notna().all()
    assert np.allclose(df["total_pnl"], df["da_id_pnl"])


def test_get_org_estimated_activity_with_day_trade_pnl():
    """include_day_trade_pnl adds TAD from the trade log and the day trade PnL"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()
    df = get_org_estimated_activity(
        start_date="2026-10-20",
        end_date="2026-10-20",
        org_id=104000,
        eptr=eptr,
        include_day_trade_pnl=True,
    )

    for col in ["mcp", "idm_wap", "idm_tad", "da_id_pnl", "day_trade_pnl", "total_pnl"]:
        assert col in df
    assert df["idm_tad"].notna().all()
    assert np.allclose(df["total_pnl"], df["da_id_pnl"] + df["day_trade_pnl"])
