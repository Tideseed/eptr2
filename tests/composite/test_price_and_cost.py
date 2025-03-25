## Add test for eptr2/composite/mms.py
from eptr2.composite.price_and_cost import (
    get_hourly_price_and_cost_data,
    get_hourly_imbalance_data,
)
from dotenv import load_dotenv, find_dotenv
from eptr2 import EPTR2
import pytest
from tests import common_params
import pandas as pd


@pytest.fixture
def pc_params():
    d = common_params()
    d = {k: v for k, v in d.items() if k in ["start_date", "end_date"]}
    return d


def test_eptr2_price_and_cost(pc_params):
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()
    df = get_hourly_price_and_cost_data(
        eptr=eptr,
        start_date=pc_params["start_date"],
        end_date=pc_params["end_date"],
        verbose=True,
        include_contract_symbol=True,
        include_wap=True,
        add_kupst_cost=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)
    assert "contract" in df


def test_eptr2_imbalance(pc_params):
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()
    df = get_hourly_imbalance_data(
        eptr=eptr,
        start_date=pc_params["start_date"],
        end_date=pc_params["end_date"],
        verbose=True,
        include_contract_symbol=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)
    assert "contract" in df
