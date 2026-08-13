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
        """List all 231 available API calls in the eptr2 library."""
        client = _get_eptr_client()
        calls = client.get_available_calls(include_aliases=True)
        return json.dumps(calls, indent=2)

    @mcp.tool()
    def describe_eptr2_call(call_key: str) -> str:
        """Get full details for one API call key: description (EN/TR), category,
        HTTP method, endpoint path, and required/optional parameters.
        Use before call_eptr2_api to learn which parameters an endpoint needs.
        Resolves aliases (e.g. 'ptf' -> 'mcp'). Requires no credentials."""
        from eptr2.agentic.discovery import describe_call

        d = describe_call(call_key)
        if d is None:
            return json.dumps(
                {"error": f"Unknown call key '{call_key}'. Use search_eptr2_calls to find keys."}
            )
        return json.dumps(d, indent=2, ensure_ascii=False, default=str)

    @mcp.tool()
    def search_eptr2_calls(query: str, category: Optional[str] = None) -> str:
        """Search API call keys by keyword (matches key, title and description in
        English and Turkish). Optionally filter by category (e.g. GÖP, GİP, DGP).
        Returns a compact key -> summary mapping. Requires no credentials."""
        from eptr2.agentic.discovery import search_calls

        matches = search_calls(query, category=category)
        compact = {
            key: {
                "category": info.get("category"),
                "title_en": info.get("title", {}).get("en"),
                "desc_en": (info.get("desc", {}).get("en") or "")[:150],
            }
            for key, info in matches.items()
        }
        return json.dumps(compact, indent=2, ensure_ascii=False)

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
            start_date=start_date, end_date=end_date, eptr=client
        )
        return _format_result(result)

    @mcp.tool()
    def get_price_and_cost_data(start_date: str, end_date: str) -> str:
        """Get comprehensive price and cost data including MCP, SMP, and imbalance costs."""
        client = _get_eptr_client()
        from eptr2.composite import get_hourly_price_and_cost_data

        result = get_hourly_price_and_cost_data(
            start_date=start_date, end_date=end_date, eptr=client
        )
        return _format_result(result)

    @mcp.tool()
    def get_market_operations_summary(start_date: str, end_date: str) -> str:
        """Get combined market operations data: Day-Ahead Market (GÖP) matched
        quantities, bilateral contracts (İA) and Intraday Market (GİP) volumes,
        merged into one hourly table."""
        client = _get_eptr_client()
        from eptr2.composite import get_dabi_idm_data

        result = get_dabi_idm_data(
            start_date=start_date, end_date=end_date, eptr=client
        )
        return _format_result(result)

    @mcp.tool()
    def get_balancing_market_data(start_date: str, end_date: str) -> str:
        """Get Balancing Power Market (DGP) data: up/down regulation
        instructions (YAL/YAT) together with the System Marginal Price."""
        client = _get_eptr_client()
        from eptr2.composite import get_bpm_range

        result = get_bpm_range(start_date=start_date, end_date=end_date, eptr=client)
        return _format_result(result)

    @mcp.tool()
    def get_bulk_production_plans(
        start_date: str,
        end_date: str,
        plant_ids: list[int],
        plan_type: str = "dpp",
    ) -> str:
        """Get bulk per-plant production plans for a date range. plan_type is
        'dpp' (Final Daily Production Plan) with plant_ids as powerplant ids
        (see the 'pp-list' call), or 'kgup' (Daily Production Plan / KGÜP)
        with plant_ids as UEVCB ids (see the 'uevcb-list-bulk' call). Use
        call_eptr2_api with those list endpoints to find the ids first."""
        client = _get_eptr_client()
        from eptr2.composite import get_dpp_bulk_range, get_kgup_bulk_range

        if plan_type == "dpp":
            result = get_dpp_bulk_range(
                start_date=start_date,
                end_date=end_date,
                pp_ids=plant_ids,
                eptr=client,
            )
        elif plan_type == "kgup":
            result = get_kgup_bulk_range(
                start_date=start_date,
                end_date=end_date,
                uevcb_ids=plant_ids,
                eptr=client,
            )
        else:
            raise ValueError("plan_type must be 'dpp' or 'kgup'")
        return _format_result(result)

    @mcp.tool()
    def calculate_imbalance_prices_and_costs(
        contract: str,
        mcp_price: float,
        smp_price: float,
        include_kupst: bool = True,
    ) -> str:
        """Calculate unit imbalance prices and costs (and optionally unit KUPST
        cost) for one hour. Pure calculation, no API call. contract is the
        hourly contract code 'PHYYMMDDhh' (e.g. 'PH26010100' = 2026-01-01
        hour 00); the applicable regulation period is derived from it.
        mcp_price/smp_price are MCP (PTF) and SMP (SMF) in TL/MWh. Returns
        pos/neg imbalance prices and costs per MWh."""
        from eptr2.util.costs import calculate_unit_price_and_costs_by_contract

        result = calculate_unit_price_and_costs_by_contract(
            contract=contract,
            mcp=mcp_price,
            smp=smp_price,
            include_kupst=include_kupst,
        )
        return _format_result(result)

    @mcp.tool()
    def calculate_kupst_deviation_cost(
        contract: str,
        actual: float,
        forecast: float,
        mcp_price: float,
        smp_price: float,
        source: str = "other",
        tolerance: Optional[float] = None,
    ) -> str:
        """Calculate the KUPST production-plan deviation cost for one hour.
        Pure calculation, no API call. contract is 'PHYYMMDDhh'; actual and
        forecast are production in MWh; mcp_price/smp_price in TL/MWh.
        source sets the tolerance band (e.g. 'wind', 'solar', 'other') unless
        an explicit tolerance (decimal, e.g. 0.15) is given. Returns the cost
        breakdown including deviation amount and unit KUPST price."""
        from eptr2.util.costs import calculate_kupst_cost_by_contract

        result = calculate_kupst_cost_by_contract(
            contract=contract,
            actual=actual,
            forecast=forecast,
            mcp=mcp_price,
            smp=smp_price,
            tol=tolerance,
            source=source,
            return_detail=True,
        )
        return _format_result(result)

    @mcp.resource(
        "eptr2://schema",
        description="Machine-readable schema of all eptr2 API endpoints, "
        "composite functions and cost utilities (generated live).",
        mime_type="application/json",
    )
    def schema_resource() -> str:
        from eptr2.agentic.schema import schema_json

        return schema_json()

    @mcp.resource(
        "eptr2://help/{call_key}",
        description="Details for one eptr2 API call key: parameters, method, "
        "path and bilingual descriptions.",
        mime_type="application/json",
    )
    def call_help_resource(call_key: str) -> str:
        from eptr2.agentic.discovery import describe_call

        d = describe_call(call_key)
        if d is None:
            return json.dumps({"error": f"Unknown call key '{call_key}'"})
        return json.dumps(d, indent=2, ensure_ascii=False, default=str)

    @mcp.prompt()
    def analyze_market_prices(start_date: str, end_date: str) -> str:
        """Guided analysis of Turkish electricity market prices for a date range."""
        return (
            f"Analyze Turkish electricity market prices between {start_date} and "
            f"{end_date}. Use get_market_clearing_price for day-ahead prices (MCP/PTF), "
            "get_system_marginal_price for balancing prices (SMP/SMF), and "
            "get_imbalance_price for imbalance prices. Summarize the price levels, "
            "daily patterns (peak vs off-peak hours), and any notable spreads between "
            "MCP and SMP (a positive SMP-MCP spread signals an energy-deficit system, "
            "negative signals surplus). Prices are in TL/MWh and hours are in "
            "Europe/Istanbul time."
        )


def main():
    """Entry point for the eptr2-mcp-server command."""
    if not MCP_AVAILABLE:
        logger.error("FastMCP is not installed. Install it with: pip install fastmcp")
        sys.exit(1)
    asyncio.run(run_mcp_server())


if __name__ == "__main__":
    main()
