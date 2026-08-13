"""Regression tests for eptr2 MCP server surface and call-key wiring."""

import pytest

from eptr2 import mcp as mcp_module
from eptr2.mcp import server as mcp_server


class _FakeClient:
    def __init__(self):
        self.calls = []

    def call(self, call_key, **params):
        self.calls.append((call_key, params))
        return {"ok": True, "call_key": call_key, "params": params}

    def get_available_calls(self, include_aliases=False):
        return {
            "include_aliases": include_aliases,
            "keys": ["mcp", "rt-cons", "rt-gen"],
        }


@pytest.mark.skipif(not mcp_server.MCP_AVAILABLE, reason="fastmcp is not installed")
def test_public_exports_are_available():
    assert hasattr(mcp_module, "run_mcp_server")
    assert hasattr(mcp_module, "create_mcp_server")


@pytest.mark.skipif(not mcp_server.MCP_AVAILABLE, reason="fastmcp is not installed")
def test_mcp_tool_aliases(monkeypatch):
    fake = _FakeClient()
    monkeypatch.setattr(mcp_server, "_get_eptr_client", lambda: fake)

    mcp_server.get_real_time_consumption("2024-01-01", "2024-01-01")
    mcp_server.get_real_time_generation("2024-01-01", "2024-01-01")
    mcp_server.get_imbalance_price("2024-01-01", "2024-01-01")

    assert fake.calls[0][0] == "rt-cons"
    assert fake.calls[1][0] == "rt-gen"
    assert fake.calls[2][0] == "mcp-smp-imb"


@pytest.mark.skipif(not mcp_server.MCP_AVAILABLE, reason="fastmcp is not installed")
def test_call_eptr2_api_merges_additional_params(monkeypatch):
    fake = _FakeClient()
    monkeypatch.setattr(mcp_server, "_get_eptr_client", lambda: fake)

    mcp_server.call_eptr2_api(
        "mcp",
        start_date="2024-01-01",
        end_date="2024-01-02",
        additional_params={"org_id": 195},
    )

    call_key, params = fake.calls[-1]
    assert call_key == "mcp"
    assert params["start_date"] == "2024-01-01"
    assert params["end_date"] == "2024-01-02"
    assert params["org_id"] == 195


@pytest.mark.skipif(not mcp_server.MCP_AVAILABLE, reason="fastmcp is not installed")
def test_call_eptr2_api_accepts_json_additional_params(monkeypatch):
    fake = _FakeClient()
    monkeypatch.setattr(mcp_server, "_get_eptr_client", lambda: fake)

    mcp_server.call_eptr2_api(
        "load-plan",
        additional_params='{"region_id": 34}',
    )

    call_key, params = fake.calls[-1]
    assert call_key == "load-plan"
    assert params["region_id"] == 34


@pytest.mark.skipif(not mcp_server.MCP_AVAILABLE, reason="fastmcp is not installed")
def test_describe_eptr2_call_no_client_needed():
    import json

    out = json.loads(mcp_server.describe_eptr2_call("ptf"))
    assert out["key"] == "mcp"
    assert out["required_body_params"] == ["start_date", "end_date"]

    err = json.loads(mcp_server.describe_eptr2_call("nope-nope"))
    assert "error" in err


@pytest.mark.skipif(not mcp_server.MCP_AVAILABLE, reason="fastmcp is not installed")
def test_search_eptr2_calls_no_client_needed():
    import json

    out = json.loads(mcp_server.search_eptr2_calls("market clearing"))
    assert "mcp" in out
    assert out["mcp"]["category"] == "GÖP"

    filtered = json.loads(mcp_server.search_eptr2_calls("price", category="DGP"))
    assert all(v["category"] == "DGP" for v in filtered.values())


@pytest.mark.skipif(not mcp_server.MCP_AVAILABLE, reason="fastmcp is not installed")
def test_composite_tools_pass_client_as_keyword(monkeypatch):
    import eptr2.composite as composite

    fake = _FakeClient()
    monkeypatch.setattr(mcp_server, "_get_eptr_client", lambda: fake)

    received = {}

    def fake_composite(start_date, end_date, eptr=None, **kwargs):
        received["args"] = (start_date, end_date, eptr)
        return {"ok": True}

    monkeypatch.setattr(composite, "get_dabi_idm_data", fake_composite)
    mcp_server.get_market_operations_summary("2024-01-01", "2024-01-02")
    assert received["args"] == ("2024-01-01", "2024-01-02", fake)

    monkeypatch.setattr(composite, "get_bpm_range", fake_composite)
    mcp_server.get_balancing_market_data("2024-01-01", "2024-01-02")
    assert received["args"] == ("2024-01-01", "2024-01-02", fake)

    monkeypatch.setattr(composite, "get_hourly_consumption_and_forecast_data", fake_composite)
    mcp_server.get_hourly_consumption_and_forecast("2024-01-01", "2024-01-02")
    assert received["args"] == ("2024-01-01", "2024-01-02", fake)

    monkeypatch.setattr(composite, "get_hourly_price_and_cost_data", fake_composite)
    mcp_server.get_price_and_cost_data("2024-01-01", "2024-01-02")
    assert received["args"] == ("2024-01-01", "2024-01-02", fake)


@pytest.mark.skipif(not mcp_server.MCP_AVAILABLE, reason="fastmcp is not installed")
def test_bulk_production_plans_dispatch(monkeypatch):
    import eptr2.composite as composite

    fake = _FakeClient()
    monkeypatch.setattr(mcp_server, "_get_eptr_client", lambda: fake)

    received = {}

    def fake_dpp(start_date, end_date, pp_ids, eptr=None, **kwargs):
        received["dpp"] = (start_date, end_date, pp_ids, eptr)
        return {"ok": True}

    def fake_kgup(start_date, end_date, uevcb_ids, eptr=None, **kwargs):
        received["kgup"] = (start_date, end_date, uevcb_ids, eptr)
        return {"ok": True}

    monkeypatch.setattr(composite, "get_dpp_bulk_range", fake_dpp)
    monkeypatch.setattr(composite, "get_kgup_bulk_range", fake_kgup)

    mcp_server.get_bulk_production_plans("2024-01-01", "2024-01-02", [1, 2])
    assert received["dpp"] == ("2024-01-01", "2024-01-02", [1, 2], fake)

    mcp_server.get_bulk_production_plans(
        "2024-01-01", "2024-01-02", [3], plan_type="kgup"
    )
    assert received["kgup"] == ("2024-01-01", "2024-01-02", [3], fake)

    with pytest.raises(ValueError, match="plan_type"):
        mcp_server.get_bulk_production_plans("2024-01-01", "2024-01-02", [1], plan_type="x")


@pytest.mark.skipif(not mcp_server.MCP_AVAILABLE, reason="fastmcp is not installed")
def test_calculate_imbalance_prices_and_costs_pure():
    import json

    out = json.loads(
        mcp_server.calculate_imbalance_prices_and_costs(
            "PH26010100", mcp_price=100, smp_price=110
        )
    )
    assert out == {
        "pos_imb_price": -103.0,
        "neg_imb_price": 159.0,
        "unit_pos_imb_cost": 203.0,
        "unit_neg_imb_cost": 59.0,
        "unit_kupst": 37.5,
    }


@pytest.mark.skipif(not mcp_server.MCP_AVAILABLE, reason="fastmcp is not installed")
def test_calculate_kupst_deviation_cost_pure():
    import json

    out = json.loads(
        mcp_server.calculate_kupst_deviation_cost(
            "PH26010100",
            actual=90.0,
            forecast=100.0,
            mcp_price=100,
            smp_price=110,
            source="wind",
        )
    )
    assert isinstance(out, dict)
    assert out  # detailed breakdown returned


@pytest.mark.skipif(not mcp_server.MCP_AVAILABLE, reason="fastmcp is not installed")
def test_server_surface_counts():
    import asyncio

    tools = asyncio.run(mcp_server.mcp.list_tools())
    assert len(tools) == 17

    resources = asyncio.run(mcp_server.mcp.list_resources())
    templates = asyncio.run(mcp_server.mcp.list_resource_templates())
    assert len(resources) + len(templates) == 2

    prompts = asyncio.run(mcp_server.mcp.list_prompts())
    assert len(prompts) == 1
