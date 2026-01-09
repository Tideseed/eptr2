## Add test for eptr2/composite/production.py
from eptr2.composite.production import (
    get_hourly_production_data,
    get_hourly_production_plan_data,
    wrapper_hourly_production_plan_and_realized,
)
from dotenv import load_dotenv, find_dotenv
from eptr2 import EPTR2
import pytest
from tests import common_params
import pandas as pd


@pytest.fixture
def prod_params():
    d = common_params()
    d = {k: v for k, v in d.items() if k in ["start_date", "end_date"]}
    return d


def test_eptr2_production(prod_params):
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()

    df = wrapper_hourly_production_plan_and_realized(
        prod_params["start_date"],
        prod_params["end_date"],
        eptr=eptr,
        verbose=True,
        include_contract_symbol=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)
    assert "contract" in df


def test_eptr2_production_without_eptr(prod_params):
    """Test production function works without passing eptr (auto-initialization)"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    df = wrapper_hourly_production_plan_and_realized(
        prod_params["start_date"],
        prod_params["end_date"],
        verbose=True,
        include_contract_symbol=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)
    assert "contract" in df


def test_eptr2_hourly_production_data(prod_params):
    """Test get_hourly_production_data function"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()

    df = get_hourly_production_data(
        prod_params["start_date"],
        prod_params["end_date"],
        eptr=eptr,
        verbose=True,
        include_contract_symbol=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)
    assert "contract" in df


def test_eptr2_hourly_production_plan_data(prod_params):
    """Test get_hourly_production_plan_data function"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()

    df = get_hourly_production_plan_data(
        prod_params["start_date"],
        prod_params["end_date"],
        eptr=eptr,
        verbose=True,
        include_contract_symbol=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)
    assert "contract" in df
