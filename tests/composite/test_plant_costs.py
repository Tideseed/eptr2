"""
Unit tests for eptr2.composite.plant_costs module.

Tests cover:
- gather_and_calculate_plant_costs function
- calculate_portfolio_costs function
- postprocess_plant_cost_df function
- create_template_id_df function
"""

import pytest
import pandas as pd
from dotenv import load_dotenv

from eptr2 import EPTR2
from eptr2.composite.plant_costs import (
    gather_and_calculate_plant_costs,
    postprocess_plant_cost_df,
    create_template_id_df,
)
from tests import common_params


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


# ============================================================================
# Tests for postprocess_plant_cost_df function
# ============================================================================


class TestPostprocessPlantCostDf:
    """Tests for the postprocess_plant_cost_df function."""

    def test_postprocess_returns_dict(self):
        """Test that postprocess returns a dictionary with expected keys."""
        # Create sample DataFrame
        df = pd.DataFrame(
            {
                "forecast": [100, 110, 90],
                "actual": [95, 105, 85],
                "diff": [5, 5, 5],
                "kupsm": [2, 2, 2],
                "total_kupst_cost": [100, 100, 100],
                "total_imb_cost": [50, 50, 50],
                "total_cost": [150, 150, 150],
            }
        )

        result = postprocess_plant_cost_df(df)

        assert isinstance(result, dict)
        assert "summary" in result
        assert "data" in result

    def test_postprocess_summary_keys(self):
        """Test that summary contains expected keys."""
        df = pd.DataFrame(
            {
                "forecast": [100, 110, 90],
                "actual": [95, 105, 85],
                "diff": [5, 5, 5],
                "kupsm": [2, 2, 2],
                "total_kupst_cost": [100, 100, 100],
                "total_imb_cost": [50, 50, 50],
                "total_cost": [150, 150, 150],
            }
        )

        result = postprocess_plant_cost_df(df)

        expected_keys = [
            "total_forecast",
            "total_actual",
            "total_kupsm",
            "total_bias",
            "total_mae",
            "total_kupst_cost",
            "total_imb_cost",
            "total_cost",
        ]

        for key in expected_keys:
            assert key in result["summary"], f"Expected key '{key}' not in summary"

    def test_postprocess_cumulative_columns(self):
        """Test that cumulative columns are added."""
        df = pd.DataFrame(
            {
                "forecast": [100, 110, 90],
                "actual": [95, 105, 85],
                "diff": [5, 5, 5],
                "kupsm": [2, 2, 2],
                "total_kupst_cost": [100, 100, 100],
                "total_imb_cost": [50, 50, 50],
                "total_cost": [150, 150, 150],
            }
        )

        result = postprocess_plant_cost_df(df)

        assert "cumulative_kupst_cost" in result["data"].columns
        assert "cumulative_imb_cost" in result["data"].columns
        assert "cumulative_total_cost" in result["data"].columns

    def test_postprocess_summary_calculations(self):
        """Test that summary calculations are correct."""
        df = pd.DataFrame(
            {
                "forecast": [100, 100],
                "actual": [90, 110],
                "diff": [10, -10],  # forecast - actual
                "kupsm": [5, 5],
                "total_kupst_cost": [100, 100],
                "total_imb_cost": [50, 50],
                "total_cost": [150, 150],
            }
        )

        result = postprocess_plant_cost_df(df)

        assert result["summary"]["total_forecast"] == 200
        assert result["summary"]["total_actual"] == 200
        assert result["summary"]["total_kupsm"] == 10
        assert result["summary"]["total_bias"] == 0  # 10 + (-10)
        assert result["summary"]["total_mae"] == 20  # |10| + |-10|
        assert result["summary"]["total_kupst_cost"] == 200
        assert result["summary"]["total_imb_cost"] == 100
        assert result["summary"]["total_cost"] == 300


# ============================================================================
# Tests for create_template_id_df function
# ============================================================================


class TestCreateTemplateIdDf:
    """Tests for the create_template_id_df function."""

    def test_create_template_returns_dataframe(self):
        """Test that function returns a DataFrame."""
        df = create_template_id_df()
        assert isinstance(df, pd.DataFrame)

    def test_create_template_has_expected_columns(self):
        """Test that template has expected columns."""
        df = create_template_id_df()

        expected_columns = [
            "org_id",
            "uevcb_id",
            "rt_id",
            "uevm_id",
            "uevcb_name",
            "rt_shortname",
            "source",
        ]

        for col in expected_columns:
            assert col in df.columns, f"Expected column '{col}' not found"

    def test_create_template_is_empty(self):
        """Test that template DataFrame is empty (no rows)."""
        df = create_template_id_df()
        assert len(df) == 0

    def test_create_template_export_to_excel(self, tmp_path):
        """Test that template can be exported to Excel."""
        export_path = tmp_path / "template.xlsx"
        df = create_template_id_df(export_to_excel=True, export_path=str(export_path))

        assert export_path.exists()
        # Read back and verify
        df_read = pd.read_excel(export_path)
        assert list(df_read.columns) == list(df.columns)
