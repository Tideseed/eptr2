"""
MCP Server implementation for eptr2 library using FastMCP.

This server exposes eptr2 API functionality through the Model Context Protocol,
allowing AI agents to query Turkish electricity market data from EPIAS Transparency Platform.
"""

import json
import sys
import logging
import asyncio
import functools
from typing import Any, Optional

from eptr2 import EPTR2
from eptr2.agentic.validation import (
    DATE_PARAMS,
    EptrValidationError,
    validate_call,
    validate_date_value,
)


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


# Global EPTR2 client instance (lazy-loaded) and its configuration.
# The client is created on first authenticated use, never at import or server
# startup, so discovery/search/describe/calculation tools remain usable without
# credentials.
_eptr_client: Optional[EPTR2] = None
_client_config: dict[str, Any] = {
    "use_dotenv": True,
    "recycle_tgt": True,
    "dotenv_path": ".env",
    "tgt_path": ".",
    ## Agents cannot see a UserWarning on stderr. Without this, a misspelled
    ## filter is dropped and the call still returns a plausible-looking but
    ## unfiltered result -- a wrong answer rather than an error.
    "strict_params": True,
}


def _get_eptr_client() -> EPTR2:
    """Get or create the EPTR2 client instance (credentials required)."""
    global _eptr_client
    if _eptr_client is None:
        _eptr_client = EPTR2(**_client_config)
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

    ## Store configuration only. Creating the client here would make the whole
    ## server (including credential-free discovery tools) fail to start without
    ## credentials.
    global _eptr_client, _client_config
    _client_config = {
        "use_dotenv": use_dotenv,
        "recycle_tgt": recycle_tgt,
        "dotenv_path": dotenv_path,
        "tgt_path": tgt_path,
        "strict_params": True,
    }
    _eptr_client = None
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


def _input_error(message: str) -> str:
    """Render an input error as data the calling agent can act on.

    An exception raised out of a tool reaches the agent as an opaque protocol
    error with a traceback. A structured payload naming the problem lets it
    correct the call instead of guessing or retrying unchanged.
    """
    return json.dumps(
        {"error": "invalid_input", "message": message},
        indent=2,
        ensure_ascii=False,
    )


def _validated(func):
    """Validate date-like arguments and report input errors as data.

    Applies to every tool, including those that go through composite helpers
    rather than ``EPTR2.call``, so a malformed date is named at the surface
    instead of surfacing as ``Invalid isoformat string`` from deep in the
    request layer -- or, worse, as an authentication error because the client
    was constructed first.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            for name, value in kwargs.items():
                if name in DATE_PARAMS:
                    validate_date_value(name, value)
            return func(*args, **kwargs)
        except EptrValidationError as exc:
            return _input_error(str(exc))

    return wrapper


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
    @_validated
    def get_market_clearing_price(start_date: str, end_date: str) -> str:
        """Get Market Clearing Price (MCP/PTF) data from Turkish electricity market."""
        client = _get_eptr_client()
        result = client.call("mcp", start_date=start_date, end_date=end_date)
        return _format_result(result)

    @mcp.tool()
    @_validated
    def get_system_marginal_price(start_date: str, end_date: str) -> str:
        """Get System Marginal Price (SMP/SMF) data from Turkish electricity market."""
        client = _get_eptr_client()
        result = client.call("smp", start_date=start_date, end_date=end_date)
        return _format_result(result)

    @mcp.tool()
    @_validated
    def get_real_time_consumption(start_date: str, end_date: str) -> str:
        """Get real-time electricity consumption data in MWh."""
        client = _get_eptr_client()
        result = client.call("rt-cons", start_date=start_date, end_date=end_date)
        return _format_result(result)

    @mcp.tool()
    @_validated
    def get_real_time_generation(start_date: str, end_date: str) -> str:
        """Get real-time generation data by resource type (wind, solar, hydro, etc.)."""
        client = _get_eptr_client()
        result = client.call("rt-gen", start_date=start_date, end_date=end_date)
        return _format_result(result)

    @mcp.tool()
    @_validated
    def get_demand_forecast(start_date: str, end_date: str) -> str:
        """Get demand forecast data (Load Plan/UECM)."""
        client = _get_eptr_client()
        result = client.call("load-plan", start_date=start_date, end_date=end_date)
        return _format_result(result)

    @mcp.tool()
    @_validated
    def get_imbalance_price(start_date: str, end_date: str) -> str:
        """Get electricity imbalance prices (positive and negative)."""
        client = _get_eptr_client()
        result = client.call("mcp-smp-imb", start_date=start_date, end_date=end_date)
        return _format_result(result)

    @mcp.tool()
    @_validated
    def get_available_eptr2_calls() -> str:
        """List all 231 available API calls in the eptr2 library.
        Requires no credentials."""
        from eptr2.agentic.discovery import list_calls
        from eptr2.mapping.path import get_alias_map

        return json.dumps(
            {
                "keys": sorted(list_calls()),
                "default_aliases": dict(sorted(get_alias_map().items())),
            },
            indent=2,
            ensure_ascii=False,
        )

    @mcp.tool()
    @_validated
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
    @_validated
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
    @_validated
    def call_eptr2_api(
        call_key: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        additional_params: Optional[dict[str, Any] | str] = None,
    ) -> str:
        """Generic function to call any eptr2 API endpoint. Use get_available_eptr2_calls first."""
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if additional_params:
            if isinstance(additional_params, str):
                try:
                    additional_params = json.loads(additional_params)
                except json.JSONDecodeError as exc:
                    return _input_error(
                        "additional_params is not valid JSON "
                        f"({exc.msg} at position {exc.pos}). Pass an object such as "
                        '{"pp_id": 123}, or omit it.'
                    )
            if not isinstance(additional_params, dict):
                return _input_error(
                    "additional_params must be a JSON object (or a JSON string "
                    f"encoding one), got {type(additional_params).__name__}."
                )
            params.update(additional_params)

        ## Validate the key and its parameters before touching the client: a
        ## typo would otherwise surface as an authentication failure, or -- for
        ## an unrecognised parameter -- as a successful but silently unfiltered
        ## result, which is the harder mistake for an agent to notice.
        key = validate_call(call_key, params)

        client = _get_eptr_client()
        result = client.call(key, **params)
        return _format_result(result)

    @mcp.tool()
    @_validated
    def get_hourly_consumption_and_forecast(start_date: str, end_date: str) -> str:
        """Get composite data combining load plan, UECM, and real-time consumption."""
        client = _get_eptr_client()
        from eptr2.composite import get_hourly_consumption_and_forecast_data

        result = get_hourly_consumption_and_forecast_data(
            start_date=start_date, end_date=end_date, eptr=client
        )
        return _format_result(result)

    @mcp.tool()
    @_validated
    def get_price_and_cost_data(start_date: str, end_date: str) -> str:
        """Get comprehensive price and cost data including MCP, SMP, and imbalance costs."""
        client = _get_eptr_client()
        from eptr2.composite import get_hourly_price_and_cost_data

        result = get_hourly_price_and_cost_data(
            start_date=start_date, end_date=end_date, eptr=client
        )
        return _format_result(result)

    @mcp.tool()
    @_validated
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
    @_validated
    def get_balancing_market_data(start_date: str, end_date: str) -> str:
        """Get Balancing Power Market (DGP) data: up/down regulation
        instructions (YAL/YAT) together with the System Marginal Price."""
        client = _get_eptr_client()
        from eptr2.composite import get_bpm_range

        result = get_bpm_range(start_date=start_date, end_date=end_date, eptr=client)
        return _format_result(result)

    @mcp.tool()
    @_validated
    def get_bulk_production_plans(
        start_date: str,
        end_date: str,
        uevcb_ids: list[int],
    ) -> str:
        """Get bulk per-plant PRODUCTION PLANS (KGÜP/DPP - forecast) for a date
        range. This is planned generation, NOT realized generation; use
        get_bulk_actual_generation for realizations.

        uevcb_ids are UEVCB (production unit) ids, NOT powerplant ids - the two
        are different namespaces and are not interchangeable. Find them with the
        'uevcb-list-bulk' call via call_eptr2_api."""
        client = _get_eptr_client()
        from eptr2.composite import get_kgup_bulk_range

        result = get_kgup_bulk_range(
            start_date=start_date,
            end_date=end_date,
            uevcb_ids=uevcb_ids,
            eptr=client,
        )
        return _format_result(result)

    @mcp.tool()
    @_validated
    def get_bulk_actual_generation(
        start_date: str,
        end_date: str,
        pp_ids: list[int],
    ) -> str:
        """Get bulk per-plant REALIZED (actual, real-time) generation for a date
        range. This is metered generation, NOT a plan or forecast; use
        get_bulk_production_plans for planned generation.

        pp_ids are powerplant ids, NOT UEVCB ids - the two are different
        namespaces and are not interchangeable. Find them with the 'pp-list'
        call via call_eptr2_api."""
        client = _get_eptr_client()
        from eptr2.composite import get_rt_gen_bulk_range

        result = get_rt_gen_bulk_range(
            start_date=start_date,
            end_date=end_date,
            pp_ids=pp_ids,
            eptr=client,
        )
        return _format_result(result)

    @mcp.tool()
    @_validated
    def calculate_imbalance_prices_and_costs(
        contract: str,
        mcp_price: float,
        smp_price: float,
        include_kupst: bool = True,
        system_direction: Optional[str] = None,
    ) -> str:
        """Calculate unit imbalance prices and costs (and optionally unit KUPST
        cost) for one hour. Pure calculation, no API call. contract is the
        hourly contract code 'PHYYMMDDhh' (e.g. 'PH26010100' = 2026-01-01
        hour 00); the applicable regulation period is derived from it.
        mcp_price/smp_price are MCP (PTF) and SMP (SMF) in TL/MWh.

        system_direction is the system imbalance direction for the hour: -1
        (deficit / 'Enerji Açığı'), 1 (surplus / 'Enerji Fazlası') or 0
        (balanced). The EPIAS 'systemStatus' label from the 'mcp-smp-imb'
        endpoint is accepted directly. It is REQUIRED when mcp_price equals
        smp_price, because the direction cannot be inferred from equal prices
        and assuming a balanced system understates the negative imbalance
        price. Otherwise it is optional and inferred from MCP vs SMP.

        Returns pos/neg imbalance prices and costs per MWh."""
        from eptr2.util.costs import calculate_unit_price_and_costs_by_contract

        if system_direction is None and float(mcp_price) == float(smp_price):
            return json.dumps(
                {
                    "error": (
                        "system_direction is required when mcp_price equals "
                        "smp_price: the system imbalance direction cannot be "
                        "inferred from equal prices, and assuming a balanced "
                        "system understates the negative imbalance price. "
                        "Pass -1 (deficit / 'Enerji Açığı'), 1 (surplus / "
                        "'Enerji Fazlası') or 0 (balanced). The 'systemStatus' "
                        "field of the 'mcp-smp-imb' endpoint provides it."
                    ),
                    "contract": contract,
                    "mcp_price": mcp_price,
                    "smp_price": smp_price,
                },
                indent=2,
                ensure_ascii=False,
            )

        result = calculate_unit_price_and_costs_by_contract(
            contract=contract,
            mcp=mcp_price,
            smp=smp_price,
            include_kupst=include_kupst,
            system_direction=system_direction,
        )
        return _format_result(result)

    @mcp.tool()
    @_validated
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
        from eptr2.agentic import schema as schema_mod

        try:
            return schema_mod.schema_json()
        except schema_mod.SchemaGenerationUnavailable:
            ## Minimal install without pandas: serve the bundled schema.
            return schema_mod.load_bundled_schema()

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
