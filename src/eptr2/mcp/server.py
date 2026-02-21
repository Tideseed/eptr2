"""
MCP Server implementation for eptr2 library using FastMCP.

This server exposes eptr2 API functionality through the Model Context Protocol,
allowing AI agents to query Turkish electricity market data from EPIAS Transparency Platform.
"""

import json
import sys
import logging
import asyncio
from typing import Any, Optional

from eptr2 import EPTR2


logger = logging.getLogger(__name__)

# Try to import FastMCP
try:
    from fastmcp import FastMCP

    MCP_AVAILABLE = True
    # Initialize FastMCP server
    mcp = FastMCP("eptr2")
except ImportError:
    MCP_AVAILABLE = False
    mcp = None


# Global EPTR2 client instance (lazy-loaded)
_eptr_client: Optional[EPTR2] = None


def _get_eptr_client() -> EPTR2:
    """Get or create the EPTR2 client instance."""
    global _eptr_client
    if _eptr_client is None:
        _eptr_client = EPTR2(use_dotenv=True, recycle_tgt=True)
    return _eptr_client


def create_mcp_server(
    use_dotenv: bool = True,
    recycle_tgt: bool = True,
    dotenv_path: str = ".env",
    tgt_path: str = ".",
):
    """
    Create and configure the FastMCP server instance for eptr2.

    Parameters mirror EPTR2 initialization so users can configure credential loading
    and TGT recycling behavior programmatically.
    """
    if not MCP_AVAILABLE:
        raise ImportError(
            "FastMCP is not installed. Install it with: pip install fastmcp"
        )

    global _eptr_client
    _eptr_client = EPTR2(
        use_dotenv=use_dotenv,
        recycle_tgt=recycle_tgt,
        dotenv_path=dotenv_path,
        tgt_path=tgt_path,
    )
    return mcp


async def run_mcp_server(
    use_dotenv: bool = True,
    recycle_tgt: bool = True,
    dotenv_path: str = ".env",
    tgt_path: str = ".",
) -> None:
    """Run the eptr2 MCP server with configurable EPTR2 initialization."""
    server = create_mcp_server(
        use_dotenv=use_dotenv,
        recycle_tgt=recycle_tgt,
        dotenv_path=dotenv_path,
        tgt_path=tgt_path,
    )
    await asyncio.to_thread(server.run)


def _format_result(result: Any) -> str:
    """Format result for MCP response."""
    if hasattr(result, "to_json"):
        return result.to_json(orient="records", date_format="iso", indent=2)
    elif isinstance(result, (dict, list)):
        return json.dumps(result, indent=2, default=str)
    else:
        return str(result)


# Only define tools if FastMCP is available
if MCP_AVAILABLE:

    @mcp.tool()
    def get_market_clearing_price(start_date: str, end_date: str) -> str:
        """Get Market Clearing Price (MCP/PTF) data from Turkish electricity market."""
        client = _get_eptr_client()
        result = client.call("mcp", start_date=start_date, end_date=end_date)
        return _format_result(result)

    @mcp.tool()
    def get_system_marginal_price(start_date: str, end_date: str) -> str:
        """Get System Marginal Price (SMP/SMF) data from Turkish electricity market."""
        client = _get_eptr_client()
        result = client.call("smp", start_date=start_date, end_date=end_date)
        return _format_result(result)

    @mcp.tool()
    def get_real_time_consumption(start_date: str, end_date: str) -> str:
        """Get real-time electricity consumption data in MWh."""
        client = _get_eptr_client()
        result = client.call("rt-cons", start_date=start_date, end_date=end_date)
        return _format_result(result)

    @mcp.tool()
    def get_real_time_generation(start_date: str, end_date: str) -> str:
        """Get real-time generation data by resource type (wind, solar, hydro, etc.)."""
        client = _get_eptr_client()
        result = client.call("rt-gen", start_date=start_date, end_date=end_date)
        return _format_result(result)

    @mcp.tool()
    def get_demand_forecast(start_date: str, end_date: str) -> str:
        """Get demand forecast data (Load Plan/UECM)."""
        client = _get_eptr_client()
        result = client.call("load-plan", start_date=start_date, end_date=end_date)
        return _format_result(result)

    @mcp.tool()
    def get_imbalance_price(start_date: str, end_date: str) -> str:
        """Get electricity imbalance prices (positive and negative)."""
        client = _get_eptr_client()
        result = client.call("mcp-smp-imb", start_date=start_date, end_date=end_date)
        return _format_result(result)

    @mcp.tool()
    def get_available_eptr2_calls() -> str:
        """List all 213+ available API calls in the eptr2 library."""
        client = _get_eptr_client()
        calls = client.get_available_calls(include_aliases=True)
        return json.dumps(calls, indent=2)

    @mcp.tool()
    def call_eptr2_api(
        call_key: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        additional_params: Optional[dict[str, Any] | str] = None,
    ) -> str:
        """Generic function to call any eptr2 API endpoint. Use get_available_eptr2_calls first."""
        client = _get_eptr_client()
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if additional_params:
            if isinstance(additional_params, str):
                additional_params = json.loads(additional_params)
            if not isinstance(additional_params, dict):
                raise TypeError("additional_params must be a dictionary or JSON string")
            params.update(additional_params)
        result = client.call(call_key, **params)
        return _format_result(result)

    @mcp.tool()
    def get_hourly_consumption_and_forecast(start_date: str, end_date: str) -> str:
        """Get composite data combining load plan, UECM, and real-time consumption."""
        client = _get_eptr_client()
        from eptr2.composite import get_hourly_consumption_and_forecast_data

        result = get_hourly_consumption_and_forecast_data(
            client, start_date=start_date, end_date=end_date
        )
        return _format_result(result)

    @mcp.tool()
    def get_price_and_cost_data(start_date: str, end_date: str) -> str:
        """Get comprehensive price and cost data including MCP, SMP, and imbalance costs."""
        client = _get_eptr_client()
        from eptr2.composite import get_hourly_price_and_cost_data

        result = get_hourly_price_and_cost_data(
            client, start_date=start_date, end_date=end_date
        )
        return _format_result(result)


def main():
    """Entry point for the eptr2-mcp-server command."""
    if not MCP_AVAILABLE:
        logger.error("FastMCP is not installed. Install it with: pip install fastmcp")
        sys.exit(1)
    asyncio.run(run_mcp_server())


if __name__ == "__main__":
    main()
