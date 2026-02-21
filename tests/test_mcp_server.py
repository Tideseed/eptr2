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

    mcp_server.get_real_time_consumption.fn("2024-01-01", "2024-01-01")
    mcp_server.get_real_time_generation.fn("2024-01-01", "2024-01-01")
    mcp_server.get_imbalance_price.fn("2024-01-01", "2024-01-01")

    assert fake.calls[0][0] == "rt-cons"
    assert fake.calls[1][0] == "rt-gen"
    assert fake.calls[2][0] == "mcp-smp-imb"


@pytest.mark.skipif(not mcp_server.MCP_AVAILABLE, reason="fastmcp is not installed")
def test_call_eptr2_api_merges_additional_params(monkeypatch):
    fake = _FakeClient()
    monkeypatch.setattr(mcp_server, "_get_eptr_client", lambda: fake)

    mcp_server.call_eptr2_api.fn(
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

    mcp_server.call_eptr2_api.fn(
        "load-plan",
        additional_params='{"region_id": 34}',
    )

    call_key, params = fake.calls[-1]
    assert call_key == "load-plan"
    assert params["region_id"] == 34
