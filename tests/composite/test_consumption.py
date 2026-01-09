## Add test for eptr2/composite/consumption.py
from eptr2.composite.consumption import get_hourly_consumption_and_forecast_data
from dotenv import load_dotenv
from eptr2 import EPTR2
import pytest
from tests import common_params
import pandas as pd


@pytest.fixture
def cons_params():
    d = common_params()
    d = {k: v for k, v in d.items() if k in ["start_date", "end_date"]}
    return d


def test_eptr2_consumption(cons_params):
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()
    df = get_hourly_consumption_and_forecast_data(
        cons_params["start_date"],
        cons_params["end_date"],
        eptr=eptr,
        include_contract_symbol=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)
    assert "contract" in df
    assert "load_plan" in df
    assert "consumption" in df


def test_eptr2_consumption_without_eptr(cons_params):
    """Test consumption function works without passing eptr (auto-initialization)"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    df = get_hourly_consumption_and_forecast_data(
        cons_params["start_date"],
        cons_params["end_date"],
        include_contract_symbol=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)
    assert "contract" in df


def test_eptr2_consumption_without_contract(cons_params):
    """Test consumption function without contract symbol"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()
    df = get_hourly_consumption_and_forecast_data(
        cons_params["start_date"],
        cons_params["end_date"],
        eptr=eptr,
        include_contract_symbol=False,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)
    assert "contract" not in df
    assert "consumption" in df
