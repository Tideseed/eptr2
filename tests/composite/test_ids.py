"""
Unit tests for eptr2.composite.ids module.

Tests cover the get_all_important_ids function which retrieves
various ID lists from the EPIAS API.
"""

import pytest
from dotenv import load_dotenv
import pandas as pd

from eptr2 import EPTR2
from eptr2.composite.ids import get_all_important_ids
from tests import common_params


@pytest.fixture
def ids_params():
    """Get common parameters for ID tests."""
    d = common_params()
    return {"the_date": d["start_date"]}


class TestGetAllImportantIds:
    """Tests for the get_all_important_ids function."""

    @pytest.mark.api_call
    def test_get_all_important_ids_returns_dict(self, ids_params):
        """Test that function returns a dictionary."""
        is_env_ok = load_dotenv(".env")
        assert is_env_ok

        eptr = EPTR2()
        result = get_all_important_ids(
            the_date=ids_params["the_date"],
            eptr=eptr,
            export_to_excel=False,
            verbose=False,
        )

        assert result is not None
        assert isinstance(result, dict)

    @pytest.mark.api_call
    def test_get_all_important_ids_contains_expected_keys(self, ids_params):
        """Test that result contains all expected keys."""
        is_env_ok = load_dotenv(".env")
        assert is_env_ok

        eptr = EPTR2()
        result = get_all_important_ids(
            the_date=ids_params["the_date"],
            eptr=eptr,
            export_to_excel=False,
            verbose=False,
        )

        expected_keys = [
            "dam_clearing_org_list",
            "imb_org_list",
            "gen_org_uevcb",
            "pp_list",
            "uevm_pp_list",
        ]

        for key in expected_keys:
            assert key in result, f"Expected key '{key}' not found in result"

    @pytest.mark.api_call
    def test_get_all_important_ids_returns_dataframes(self, ids_params):
        """Test that all values in result are DataFrames."""
        is_env_ok = load_dotenv(".env")
        assert is_env_ok

        eptr = EPTR2()
        result = get_all_important_ids(
            the_date=ids_params["the_date"],
            eptr=eptr,
            export_to_excel=False,
            verbose=False,
        )

        for key, value in result.items():
            assert isinstance(value, pd.DataFrame), (
                f"Value for '{key}' is not a DataFrame"
            )

    @pytest.mark.api_call
    def test_get_all_important_ids_dataframes_not_empty(self, ids_params):
        """Test that returned DataFrames are not empty."""
        is_env_ok = load_dotenv(".env")
        assert is_env_ok

        eptr = EPTR2()
        result = get_all_important_ids(
            the_date=ids_params["the_date"],
            eptr=eptr,
            export_to_excel=False,
            verbose=False,
        )

        for key, df in result.items():
            assert len(df) > 0, f"DataFrame for '{key}' is empty"

    @pytest.mark.api_call
    def test_get_all_important_ids_auto_creates_eptr(self, ids_params):
        """Test that function auto-creates EPTR2 instance if not provided."""
        is_env_ok = load_dotenv(".env")
        assert is_env_ok

        # Don't pass eptr - should create automatically
        result = get_all_important_ids(
            the_date=ids_params["the_date"],
            export_to_excel=False,
            verbose=False,
        )

        assert result is not None
        assert isinstance(result, dict)

    @pytest.mark.api_call
    def test_get_all_important_ids_verbose_mode(self, ids_params, capsys):
        """Test that verbose mode produces output."""
        is_env_ok = load_dotenv(".env")
        assert is_env_ok

        eptr = EPTR2()
        get_all_important_ids(
            the_date=ids_params["the_date"],
            eptr=eptr,
            export_to_excel=False,
            verbose=True,
        )

        captured = capsys.readouterr()
        assert "Fetching" in captured.out

    @pytest.mark.api_call
    def test_get_all_important_ids_dam_clearing_org_list_structure(self, ids_params):
        """Test DAM clearing org list has expected structure."""
        is_env_ok = load_dotenv(".env")
        assert is_env_ok

        eptr = EPTR2()
        result = get_all_important_ids(
            the_date=ids_params["the_date"],
            eptr=eptr,
            export_to_excel=False,
            verbose=False,
        )

        df = result["dam_clearing_org_list"]
        assert len(df) > 0
        # Check some expected columns exist (may vary by API version)
        assert df.columns.size > 0

    @pytest.mark.api_call
    def test_get_all_important_ids_pp_list_structure(self, ids_params):
        """Test power plant list has expected structure."""
        is_env_ok = load_dotenv(".env")
        assert is_env_ok

        eptr = EPTR2()
        result = get_all_important_ids(
            the_date=ids_params["the_date"],
            eptr=eptr,
            export_to_excel=False,
            verbose=False,
        )

        df = result["pp_list"]
        assert len(df) > 0
        assert df.columns.size > 0

    @pytest.mark.api_call
    def test_get_all_important_ids_with_timeout(self, ids_params):
        """Test that custom timeout is accepted."""
        is_env_ok = load_dotenv(".env")
        assert is_env_ok

        eptr = EPTR2()
        result = get_all_important_ids(
            the_date=ids_params["the_date"],
            eptr=eptr,
            export_to_excel=False,
            verbose=False,
            timeout=30,
        )

        assert result is not None
        assert isinstance(result, dict)

    @pytest.mark.api_call
    def test_get_all_important_ids_with_max_lives(self, ids_params):
        """Test that max_lives parameter is accepted."""
        is_env_ok = load_dotenv(".env")
        assert is_env_ok

        eptr = EPTR2()
        result = get_all_important_ids(
            the_date=ids_params["the_date"],
            eptr=eptr,
            export_to_excel=False,
            verbose=False,
            max_lives=5,
        )

        assert result is not None
        assert isinstance(result, dict)


class TestGetAllImportantIdsExport:
    """Tests for export functionality of get_all_important_ids."""

    @pytest.mark.api_call
    def test_get_all_important_ids_export_creates_file(self, ids_params, tmp_path):
        """Test that export_to_excel creates an Excel file."""
        is_env_ok = load_dotenv(".env")
        assert is_env_ok

        eptr = EPTR2()
        get_all_important_ids(
            the_date=ids_params["the_date"],
            eptr=eptr,
            export_to_excel=True,
            main_dir=str(tmp_path),
            verbose=False,
        )

        # Check that the file was created
        expected_file = tmp_path / f"all_important_ids_{ids_params['the_date']}.xlsx"
        assert expected_file.exists(), f"Expected file {expected_file} was not created"

    @pytest.mark.api_call
    def test_get_all_important_ids_export_contains_sheets(self, ids_params, tmp_path):
        """Test that exported Excel file contains all expected sheets."""
        is_env_ok = load_dotenv(".env")
        assert is_env_ok

        eptr = EPTR2()
        get_all_important_ids(
            the_date=ids_params["the_date"],
            eptr=eptr,
            export_to_excel=True,
            main_dir=str(tmp_path),
            verbose=False,
        )

        expected_file = tmp_path / f"all_important_ids_{ids_params['the_date']}.xlsx"

        # Read the Excel file and check sheets
        with pd.ExcelFile(expected_file) as xls:
            sheet_names = xls.sheet_names
            expected_sheets = [
                "dam_clearing_org_list",
                "imb_org_list",
                "gen_org_uevcb",
                "pp_list",
                "uevm_pp_list",
            ]
            for sheet in expected_sheets:
                assert sheet in sheet_names, f"Expected sheet '{sheet}' not found"
