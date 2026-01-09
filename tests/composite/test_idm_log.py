## Add test for eptr2/composite/idm_log.py
from eptr2.composite.idm_log import idm_log_longer, idm_log_period
from dotenv import load_dotenv
from eptr2 import EPTR2
import pytest
from tests import common_params
import pandas as pd


@pytest.fixture
def idm_log_params():
    d = common_params()
    d = {k: v for k, v in d.items() if k in ["start_date", "end_date"]}
    return d


def test_idm_log_longer(idm_log_params):
    """Test idm_log_longer function"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()
    df = idm_log_longer(
        idm_log_params["start_date"],
        idm_log_params["end_date"],
        eptr=eptr,
        verbose=True,
        contract_wise=False,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)


def test_idm_log_longer_without_eptr(idm_log_params):
    """Test idm_log_longer works without passing eptr (auto-initialization)"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    df = idm_log_longer(
        idm_log_params["start_date"],
        idm_log_params["end_date"],
        verbose=True,
        contract_wise=False,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)


def test_idm_log_longer_contract_wise(idm_log_params):
    """Test idm_log_longer with contract_wise parameter"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()
    df = idm_log_longer(
        idm_log_params["start_date"],
        idm_log_params["end_date"],
        eptr=eptr,
        verbose=True,
        contract_wise=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)
    assert "contractName" in df


def test_idm_log_period(idm_log_params):
    """Test idm_log_period function"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()
    # Use start_date as period (YYYY-MM-DD format)
    period = idm_log_params["start_date"]

    df = idm_log_period(
        period,
        eptr=eptr,
        verbose=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)


def test_idm_log_period_without_eptr(idm_log_params):
    """Test idm_log_period works without passing eptr"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    period = idm_log_params["start_date"]

    df = idm_log_period(
        period,
        verbose=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)
