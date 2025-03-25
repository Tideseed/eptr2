## Add test for eptr2/composite/mms.py
from eptr2.composite.consumption import get_hourly_consumption_and_forecast_data
from dotenv import load_dotenv, find_dotenv
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
        eptr=eptr,
        start_date=cons_params["start_date"],
        end_date=cons_params["end_date"],
        include_contract_symbol=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)
    assert "contract" in df
