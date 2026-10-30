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
    for col in ["day_trade", "dabi_idm_close", "dabi_net", "dabi_idm_net"]:
        assert col in df
    assert "dabi_idm_pnl" not in df and "idm_wap" not in df
    assert np.allclose(df["dabi_net"], df["da_net"] + df["bi_net"])
    assert np.allclose(df["dabi_idm_net"], df["dabi_net"] + df["idm_net"])


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
    for col in ["mcp", "idm_wap", "dabi_idm_pnl"]:
        assert col in df
    assert "idm_tad" not in df and "day_trade_tad" not in df
    assert df["idm_wap"].notna().all()


def test_get_org_estimated_activity_with_tad():
    """include_tad adds TAD from the trade log and day_trade_tad, without MCP and WAP"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()
    df = get_org_estimated_activity(
        start_date="2026-10-20",
        end_date="2026-10-20",
        org_id=104000,
        eptr=eptr,
        include_tad=True,
    )

    for col in ["idm_tad", "day_trade_tad"]:
        assert col in df
    assert "mcp" not in df and "dabi_idm_pnl" not in df
    assert df["idm_tad"].notna().all()
    assert np.allclose(df["day_trade_tad"], df["day_trade"] * df["idm_tad"])
