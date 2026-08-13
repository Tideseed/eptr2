"""Offline tests for eptr2.agentic.schema, including freshness of the
committed schema copies (no credentials needed)."""

import json
from pathlib import Path

import eptr2
from eptr2.agentic import schema
from eptr2.mapping.path import get_path_map

REPO_ROOT = Path(__file__).resolve().parents[1]
ROOT_SCHEMA = REPO_ROOT / "eptr2_api_schema.json"
ASSETS_SCHEMA = REPO_ROOT / "src" / "eptr2" / "assets" / "eptr2_api_schema.json"


def test_build_schema_covers_all_endpoints():
    s = schema.build_schema()
    assert set(s["endpoints"]) == set(get_path_map(just_call_keys=True))
    assert s["endpoint_count"] == len(s["endpoints"])


def test_schema_endpoint_entries_complete():
    s = schema.build_schema()
    for key, entry in s["endpoints"].items():
        assert entry["call_path"], key
        assert entry["call_method"] in ("GET", "POST"), key
        assert isinstance(entry["required_params"], list), key
        assert isinstance(entry["optional_params"], list), key


def test_schema_version_matches_package():
    assert schema.build_schema()["eptr2_version"] == eptr2.__version__


def test_schema_has_composites_and_cost_utilities():
    s = schema.build_schema()
    assert "get_hourly_price_and_cost_data" in s["composite_functions"]
    assert "calculate_kupst_cost_by_contract" in s["cost_utilities"]
    for entry in s["cost_utilities"].values():
        assert entry["module"] == "eptr2.util.costs"


def test_schema_json_deterministic():
    assert schema.schema_json() == schema.schema_json()


def test_schema_json_is_valid_json():
    parsed = json.loads(schema.schema_json())
    assert parsed["schema_format_version"] == schema.SCHEMA_FORMAT_VERSION


def test_committed_schemas_are_fresh():
    """Both committed schema copies must match a fresh build.

    If this fails, run: eptr2 schema
    """
    assert schema.check_schema(ROOT_SCHEMA), (
        f"{ROOT_SCHEMA} is stale — regenerate with `eptr2 schema`"
    )
    assert schema.check_schema(ASSETS_SCHEMA), (
        f"{ASSETS_SCHEMA} is stale — regenerate with `eptr2 schema`"
    )
