## Add test for eptr2/composite/price_and_cost.py
from eptr2.composite.price_and_cost import (
    get_hourly_price_and_cost_data,
    get_hourly_imbalance_data,
)
from dotenv import load_dotenv
from eptr2 import EPTR2
import pytest
from tests import common_params
import pandas as pd


@pytest.fixture
def pc_params():
    d = common_params()
    d = {k: v for k, v in d.items() if k in ["start_date", "end_date"]}
    return d


@pytest.mark.timeout(30)
def test_eptr2_price_and_cost(pc_params):
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()
    df = get_hourly_price_and_cost_data(
        pc_params["start_date"],
        pc_params["end_date"],
        eptr=eptr,
        verbose=True,
        include_contract_symbol=True,
        include_wap=True,
        add_kupst_cost=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)
    assert "contract" in df
    assert "mcp" in df
    assert "smp" in df


@pytest.mark.timeout(30)
def test_eptr2_imbalance(pc_params):
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()
    df = get_hourly_imbalance_data(
        pc_params["start_date"],
        pc_params["end_date"],
        eptr=eptr,
        verbose=True,
        include_contract_symbol=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)
    assert "contract" in df
    assert "pos_imb_vol" in df
    assert "neg_imb_vol" in df


@pytest.mark.timeout(30)
def test_eptr2_price_and_cost_without_eptr(pc_params):
    """Test that functions work without passing eptr (auto-initialization)"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    df = get_hourly_price_and_cost_data(
        pc_params["start_date"],
        pc_params["end_date"],
        verbose=True,
        include_contract_symbol=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)


@pytest.mark.timeout(30)
def test_eptr2_imbalance_without_eptr(pc_params):
    """Test that imbalance function works without passing eptr (auto-initialization)"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    df = get_hourly_imbalance_data(
        pc_params["start_date"],
        pc_params["end_date"],
        verbose=True,
        include_contract_symbol=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)

    assert "contract" in df
