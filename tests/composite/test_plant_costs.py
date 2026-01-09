## Add test for eptr2/composite/plant_costs.py
from eptr2.composite.plant_costs import gather_and_calculate_plant_costs
from dotenv import load_dotenv
from eptr2 import EPTR2
import pytest
from tests import common_params
import pandas as pd


@pytest.fixture
def plant_costs_params():
    d = common_params()
    d = {k: v for k, v in d.items() if k in ["start_date", "end_date"]}
    return d


def test_gather_and_calculate_plant_costs_wind(plant_costs_params):
    """Test gather_and_calculate_plant_costs for wind plant"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()

    # Using example wind plant parameters
    df = gather_and_calculate_plant_costs(
        plant_costs_params["start_date"],
        plant_costs_params["end_date"],
        pp_id=120,  # Example wind plant
        org_id=195,  # Example organization
        uevcb_id=3204384,  # Example UEVCB
        plant_type="wind",
        eptr=eptr,
        forecast_source="kudup",
        actual_source="uevm",
        verbose=True,
        postprocess=False,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)
    assert "contract" in df
    assert "forecast" in df
    assert "actual" in df
    assert "total_kupst_cost" in df
    assert "total_imb_cost" in df


def test_gather_and_calculate_plant_costs_without_eptr(plant_costs_params):
    """Test function works without passing eptr (auto-initialization)"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    df = gather_and_calculate_plant_costs(
        plant_costs_params["start_date"],
        plant_costs_params["end_date"],
        pp_id=120,
        org_id=195,
        uevcb_id=3204384,
        plant_type="wind",
        forecast_source="kudup",
        actual_source="uevm",
        verbose=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)


def test_gather_and_calculate_plant_costs_with_postprocess(plant_costs_params):
    """Test function with postprocessing enabled"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()

    result = gather_and_calculate_plant_costs(
        plant_costs_params["start_date"],
        plant_costs_params["end_date"],
        pp_id=120,
        org_id=195,
        uevcb_id=3204384,
        plant_type="wind",
        eptr=eptr,
        postprocess=True,
        verbose=True,
    )

    assert result is not None
    assert isinstance(result, dict)
    assert "summary" in result
    assert "data" in result
    assert isinstance(result["data"], pd.DataFrame)
    assert isinstance(result["summary"], dict)
    assert "total_cost" in result["summary"]
    assert "total_kupst_cost" in result["summary"]
    assert "total_imb_cost" in result["summary"]


def test_gather_and_calculate_plant_costs_solar(plant_costs_params):
    """Test function for solar plant"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()

    df = gather_and_calculate_plant_costs(
        plant_costs_params["start_date"],
        plant_costs_params["end_date"],
        pp_id=641,  # Example solar plant
        org_id=195,
        uevcb_id=3204384,
        plant_type="solar",
        eptr=eptr,
        verbose=True,
    )

    assert df is not None
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)


def test_gather_and_calculate_plant_costs_different_sources(plant_costs_params):
    """Test function with different forecast and actual sources"""
    is_env_ok = load_dotenv(".env")
    assert is_env_ok

    eptr = EPTR2()

    df = gather_and_calculate_plant_costs(
        plant_costs_params["start_date"],
        plant_costs_params["end_date"],
        pp_id=672,
        org_id=20680,
        uevcb_id=4521,
        plant_type="wind",
        eptr=eptr,
        forecast_source="kgup",
        actual_source="rt",
        verbose=True,
    )

    assert df is not None
    assert isinstance(df, pd.DataFrame)
