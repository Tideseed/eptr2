## Add test for eptr2/composite/dabi_idm.py
from eptr2.composite.dabi_idm import (
    get_day_ahead_and_bilateral_matches,
    get_dabi_idm_data,
    get_day_ahead_detail_info,
)
from dotenv import load_dotenv
from eptr2 import EPTR2
import pytest
from tests import common_params
import pandas as pd


@pytest.fixture
def dabi_params():
    d = common_params()
    d = {k: v for k, v in d.items() if k in ["start_date", "end_date"]}
    return d


def test_get_day_ahead_and_bilateral_matches(dabi_params):
    """Test get_day_ahead_and_bilateral_matches function"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()
    df = get_day_ahead_and_bilateral_matches(
        dabi_params["start_date"],
        dabi_params["end_date"],
        eptr=eptr,
        verbose=True,
        include_contract_symbol=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)
    assert "dabi_net" in df
    assert "contract" in df


def test_get_day_ahead_and_bilateral_matches_without_eptr(dabi_params):
    """Test function works without passing eptr (auto-initialization)"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    df = get_day_ahead_and_bilateral_matches(
        dabi_params["start_date"],
        dabi_params["end_date"],
        verbose=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)


def test_get_dabi_idm_data(dabi_params):
    """Test get_dabi_idm_data function"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()
    df = get_dabi_idm_data(
        dabi_params["start_date"],
        dabi_params["end_date"],
        eptr=eptr,
        verbose=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)
    assert "dabi_idm_net" in df


def test_get_dabi_idm_data_without_eptr(dabi_params):
    """Test get_dabi_idm_data works without passing eptr"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    df = get_dabi_idm_data(
        dabi_params["start_date"],
        dabi_params["end_date"],
        verbose=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)


def test_get_day_ahead_detail_info(dabi_params):
    """Test get_day_ahead_detail_info function"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()
    df = get_day_ahead_detail_info(
        dabi_params["start_date"],
        dabi_params["end_date"],
        eptr=eptr,
        verbose=True,
        include_contract_symbol=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)
    assert "contract" in df


def test_get_day_ahead_detail_info_without_eptr(dabi_params):
    """Test get_day_ahead_detail_info works without passing eptr"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    df = get_day_ahead_detail_info(
        dabi_params["start_date"],
        dabi_params["end_date"],
        verbose=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)
