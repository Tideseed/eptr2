## Add test for eptr2/composite/mms.py
from eptr2.composite.production import wrapper_hourly_production_plan_and_realized
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
        eptr=eptr,
        start_date=prod_params["start_date"],
        end_date=prod_params["end_date"],
        verbose=True,
        include_contract_symbol=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)
    assert "contract" in df
