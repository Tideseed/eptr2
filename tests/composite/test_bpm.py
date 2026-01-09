## Add test for eptr2/composite/bpm.py
from eptr2.composite.bpm import get_bpm_range, get_bpm_period
from dotenv import load_dotenv
from eptr2 import EPTR2
import pytest
from tests import common_params
import pandas as pd


@pytest.fixture
def bpm_params():
    d = common_params()
    d = {k: v for k, v in d.items() if k in ["start_date", "end_date"]}
    return d


def test_get_bpm_range(bpm_params):
    """Test get_bpm_range function"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()
    df = get_bpm_range(
        bpm_params["start_date"],
        bpm_params["end_date"],
        eptr=eptr,
        verbose=True,
        include_contract_symbol=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)
    assert "contract" in df


def test_get_bpm_range_without_eptr(bpm_params):
    """Test get_bpm_range works without passing eptr (auto-initialization)"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    df = get_bpm_range(
        bpm_params["start_date"],
        bpm_params["end_date"],
        verbose=True,
        include_contract_symbol=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)


def test_get_bpm_range_strict_mode(bpm_params):
    """Test get_bpm_range with strict mode"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()
    df = get_bpm_range(
        bpm_params["start_date"],
        bpm_params["end_date"],
        eptr=eptr,
        verbose=True,
        strict=False,
    )

    assert df is not None
    assert isinstance(df, pd.DataFrame)


def test_get_bpm_period(bpm_params):
    """Test get_bpm_period function"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()
    # Use start_date to get the period (YYYY-MM-DD format)
    period = bpm_params["start_date"]

    df = get_bpm_period(
        period,
        eptr=eptr,
        verbose=True,
        include_contract_symbol=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)
    assert "contract" in df
