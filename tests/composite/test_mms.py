## Add test for eptr2/composite/mms.py
from eptr2.composite.mms import get_mms_detail, get_mms_loss_summary_by_contract
from dotenv import load_dotenv, find_dotenv
from eptr2 import EPTR2
import pytest
from tests import common_params
import pandas as pd


@pytest.fixture
def mms_params():
    d = common_params()
    d = {k: v for k, v in d.items() if k in ["start_date", "end_date"]}
    return d


def test_eptr2_composite_mms(mms_params):
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()
    d = get_mms_detail(
        mms_params["start_date"],
        mms_params["end_date"],
        eptr=eptr,
        verbose=True,
        include_contract_symbol=True,
        include_summary=True,
    )
    assert d is not None
    assert isinstance(d, dict)
    assert "detail" in d
    assert "summary" in d
    assert d["detail"] is not None
    assert d["summary"] is not None
    assert len(d["detail"]) > 0
    assert len(d["summary"]) > 0
    assert "contract" in d["detail"]
    assert "contract" in d["summary"]


def test_eptr2_composite_mms_without_eptr(mms_params):
    """Test MMS function works without passing eptr (auto-initialization)"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    d = get_mms_detail(
        mms_params["start_date"],
        mms_params["end_date"],
        verbose=True,
        include_contract_symbol=True,
    )

    assert d is not None
    assert isinstance(d, pd.DataFrame)
    assert len(d) > 0
    assert "contract" in d


def test_eptr2_composite_mms_detail_only(mms_params):
    """Test MMS function without summary"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()
    df = get_mms_detail(
        mms_params["start_date"],
        mms_params["end_date"],
        eptr=eptr,
        verbose=True,
        include_contract_symbol=True,
        include_summary=False,
    )

    assert df is not None
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "contract" in df


def test_eptr2_composite_mms_with_org_id(mms_params):
    """Test MMS function with org_id filter"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()
    df = get_mms_detail(
        mms_params["start_date"],
        mms_params["end_date"],
        eptr=eptr,
        org_id="195",  # Example org_id
        include_contract_symbol=True,
    )

    assert df is not None
    assert isinstance(df, pd.DataFrame)
