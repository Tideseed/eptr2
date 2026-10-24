## Add test for eptr2/composite/org_activity.py
from eptr2.composite.org_activity import get_org_estimated_activity
from dotenv import load_dotenv
from eptr2 import EPTR2
import numpy as np


def test_get_org_estimated_activity():
    """Test get_org_estimated_activity function"""
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
    for col in ["day_trade", "da_id_close", "free_qty", "idm_wap", "idm_tad", "total_pnl"]:
        assert col in df
    assert np.allclose(df["free_qty"], df["da_net"] + df["bi_net"] + df["idm_net"])
    assert df["idm_wap"].notna().all()
