"""
MCP Server implementation for eptr2 library.

This server exposes eptr2's API functionality through the Model Context Protocol,
allowing AI agents to query Turkish electricity market data from EPIAS Transparency Platform.
"""

import json
import sys
from typing import Any, Optional
import asyncio
from datetime import datetime

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("Warning: MCP SDK not installed. Install with: pip install mcp", file=sys.stderr)

from eptr2 import EPTR2


# Tool definitions for the most commonly used eptr2 functions
EPTR2_TOOLS = [
    Tool(
        name="get_market_clearing_price",
        description="Get Market Clearing Price (MCP/PTF) data from Turkish electricity market. "
                   "Returns hourly electricity prices for the day-ahead market.",
        inputSchema={
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "Start date in YYYY-MM-DD format (e.g., '2024-07-29')"
                },
                "end_date": {
                    "type": "string",
                    "description": "End date in YYYY-MM-DD format (e.g., '2024-07-29')"
                }
            },
            "required": ["start_date", "end_date"]
        }
    ),
    Tool(
        name="get_system_marginal_price",
        description="Get System Marginal Price (SMP/SMF) data from Turkish electricity market. "
                   "Returns hourly system marginal prices.",
        inputSchema={
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "Start date in YYYY-MM-DD format"
                },
                "end_date": {
                    "type": "string",
                    "description": "End date in YYYY-MM-DD format"
                }
            },
            "required": ["start_date", "end_date"]
        }
    ),
    Tool(
        name="get_real_time_consumption",
        description="Get real-time electricity consumption data from Turkish electricity market. "
                   "Returns hourly consumption values in MWh.",
        inputSchema={
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "Start date in YYYY-MM-DD format"
                },
                "end_date": {
                    "type": "string",
                    "description": "End date in YYYY-MM-DD format"
                }
            },
            "required": ["start_date", "end_date"]
        }
    ),
    Tool(
        name="get_real_time_generation",
        description="Get real-time electricity generation data by resource type. "
                   "Returns hourly generation breakdown by source (wind, solar, hydro, etc.).",
        inputSchema={
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "Start date in YYYY-MM-DD format"
                },
                "end_date": {
                    "type": "string",
                    "description": "End date in YYYY-MM-DD format"
                }
            },
            "required": ["start_date", "end_date"]
        }
    ),
    Tool(
        name="get_demand_forecast",
        description="Get demand forecast data (Load Plan/UECM). "
                   "Returns forecasted electricity demand.",
        inputSchema={
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "Start date in YYYY-MM-DD format"
                },
                "end_date": {
                    "type": "string",
                    "description": "End date in YYYY-MM-DD format"
                }
            },
            "required": ["start_date", "end_date"]
        }
    ),
    Tool(
        name="get_imbalance_price",
        description="Get electricity imbalance prices (positive and negative). "
                   "Returns hourly imbalance pricing data.",
        inputSchema={
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "Start date in YYYY-MM-DD format"
                },
                "end_date": {
                    "type": "string",
                    "description": "End date in YYYY-MM-DD format"
                }
            },
            "required": ["start_date", "end_date"]
        }
    ),
    Tool(
        name="get_available_eptr2_calls",
        description="List all available API calls in the eptr2 library. "
                   "Use this to discover what data you can query from EPIAS Transparency Platform.",
        inputSchema={
            "type": "object",
            "properties": {}
        }
    ),
    Tool(
        name="call_eptr2_api",
        description="Generic function to call any eptr2 API endpoint. "
                   "Use get_available_eptr2_calls first to see available endpoints. "
                   "Supports 213+ different API calls for Turkish electricity market data.",
        inputSchema={
            "type": "object",
            "properties": {
                "call_key": {
                    "type": "string",
                    "description": "The API call key (e.g., 'mcp', 'smp', 'rt-consumption'). "
                                 "Use get_available_eptr2_calls to see all options."
                },
                "start_date": {
                    "type": "string",
                    "description": "Start date in YYYY-MM-DD format (if applicable)"
                },
                "end_date": {
                    "type": "string",
                    "description": "End date in YYYY-MM-DD format (if applicable)"
                },
                "additional_params": {
                    "type": "object",
                    "description": "Additional parameters as key-value pairs (optional)"
                }
            },
            "required": ["call_key"]
        }
    ),
    Tool(
        name="get_hourly_consumption_and_forecast",
        description="Get composite data combining load plan, UECM, and real-time consumption. "
                   "This is a convenience function that merges multiple data sources.",
        inputSchema={
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "Start date in YYYY-MM-DD format"
                },
                "end_date": {
                    "type": "string",
                    "description": "End date in YYYY-MM-DD format"
                }
            },
            "required": ["start_date", "end_date"]
        }
    ),
    Tool(
        name="get_price_and_cost_data",
        description="Get composite data for prices and costs including MCP, SMP, and imbalance costs. "
                   "Comprehensive pricing analysis for the electricity market.",
        inputSchema={
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "Start date in YYYY-MM-DD format"
                },
                "end_date": {
                    "type": "string",
                    "description": "End date in YYYY-MM-DD format"
                }
            },
            "required": ["start_date", "end_date"]
        }
    )
]


class EPTR2MCPServer:
    """MCP Server wrapper for eptr2 library."""
    
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None,
                 use_dotenv: bool = True, recycle_tgt: bool = True):
        """
        Initialize the EPTR2 MCP Server.
        
        Args:
            username: EPIAS Transparency Platform username (optional if using .env)
            password: EPIAS Transparency Platform password (optional if using .env)
            use_dotenv: Whether to load credentials from .env file
            recycle_tgt: Whether to recycle TGT (Ticket Granting Ticket)
        """
        self.eptr = None
        self.username = username
        self.password = password
        self.use_dotenv = use_dotenv
        self.recycle_tgt = recycle_tgt
        
    def _ensure_eptr_client(self):
        """Ensure EPTR2 client is initialized."""
        if self.eptr is None:
            self.eptr = EPTR2(
                username=self.username,
                password=self.password,
                use_dotenv=self.use_dotenv,
                recycle_tgt=self.recycle_tgt
            )
    
    async def handle_get_market_clearing_price(self, arguments: dict) -> str:
        """Handle get_market_clearing_price tool call."""
        self._ensure_eptr_client()
        result = self.eptr.call("mcp", **arguments)
        return self._format_result(result)
    
    async def handle_get_system_marginal_price(self, arguments: dict) -> str:
        """Handle get_system_marginal_price tool call."""
        self._ensure_eptr_client()
        result = self.eptr.call("smp", **arguments)
        return self._format_result(result)
    
    async def handle_get_real_time_consumption(self, arguments: dict) -> str:
        """Handle get_real_time_consumption tool call."""
        self._ensure_eptr_client()
        result = self.eptr.call("rt-consumption", **arguments)
        return self._format_result(result)
    
    async def handle_get_real_time_generation(self, arguments: dict) -> str:
        """Handle get_real_time_generation tool call."""
        self._ensure_eptr_client()
        result = self.eptr.call("rt-generation", **arguments)
        return self._format_result(result)
    
    async def handle_get_demand_forecast(self, arguments: dict) -> str:
        """Handle get_demand_forecast tool call."""
        self._ensure_eptr_client()
        result = self.eptr.call("load-plan", **arguments)
        return self._format_result(result)
    
    async def handle_get_imbalance_price(self, arguments: dict) -> str:
        """Handle get_imbalance_price tool call."""
        self._ensure_eptr_client()
        result = self.eptr.call("imbalance-price", **arguments)
        return self._format_result(result)
    
    async def handle_get_available_eptr2_calls(self, arguments: dict) -> str:
        """Handle get_available_eptr2_calls tool call."""
        self._ensure_eptr_client()
        calls = self.eptr.get_available_calls(include_aliases=True)
        return json.dumps(calls, indent=2)
    
    async def handle_call_eptr2_api(self, arguments: dict) -> str:
        """Handle generic call_eptr2_api tool call."""
        self._ensure_eptr_client()
        call_key = arguments.pop("call_key")
        additional_params = arguments.pop("additional_params", {})
        
        # Merge arguments
        params = {**arguments, **additional_params}
        
        result = self.eptr.call(call_key, **params)
        return self._format_result(result)
    
    async def handle_get_hourly_consumption_and_forecast(self, arguments: dict) -> str:
        """Handle get_hourly_consumption_and_forecast composite function."""
        self._ensure_eptr_client()
        from eptr2.composite import get_hourly_consumption_and_forecast_data
        
        result = get_hourly_consumption_and_forecast_data(self.eptr, **arguments)
        return self._format_result(result)
    
    async def handle_get_price_and_cost_data(self, arguments: dict) -> str:
        """Handle get_price_and_cost_data composite function."""
        self._ensure_eptr_client()
        from eptr2.composite import get_hourly_price_and_cost_data
        
        result = get_hourly_price_and_cost_data(self.eptr, **arguments)
        return self._format_result(result)
    
    def _format_result(self, result: Any) -> str:
        """Format result for MCP response."""
        # Check if result is a pandas DataFrame
        if hasattr(result, 'to_json'):
            # It's a DataFrame
            return result.to_json(orient='records', date_format='iso', indent=2)
        elif isinstance(result, (dict, list)):
            return json.dumps(result, indent=2, default=str)
        else:
            return str(result)


async def run_mcp_server(username: Optional[str] = None, password: Optional[str] = None,
                        use_dotenv: bool = True, recycle_tgt: bool = True):
    """
    Run the EPTR2 MCP server.
    
    This server exposes eptr2 functionality through the Model Context Protocol,
    allowing AI agents to query Turkish electricity market data.
    
    Args:
        username: EPIAS Transparency Platform username (optional if using .env)
        password: EPIAS Transparency Platform password (optional if using .env)
        use_dotenv: Whether to load credentials from .env file
        recycle_tgt: Whether to recycle TGT tokens
        
    Example:
        To run the server:
        ```python
        from eptr2.mcp import run_mcp_server
        import asyncio
        
        asyncio.run(run_mcp_server(use_dotenv=True))
        ```
        
        Or from command line:
        ```bash
        python -m eptr2.mcp.server
        ```
    """
    if not MCP_AVAILABLE:
        raise ImportError(
            "MCP SDK is not installed. Install it with: pip install mcp\n"
            "For more information, visit: https://modelcontextprotocol.io/"
        )
    
    server = Server("eptr2")
    eptr_server = EPTR2MCPServer(username, password, use_dotenv, recycle_tgt)
    
    # Register tools
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return EPTR2_TOOLS
    
    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        """Handle tool calls."""
        try:
            if name == "get_market_clearing_price":
                result = await eptr_server.handle_get_market_clearing_price(arguments)
            elif name == "get_system_marginal_price":
                result = await eptr_server.handle_get_system_marginal_price(arguments)
            elif name == "get_real_time_consumption":
                result = await eptr_server.handle_get_real_time_consumption(arguments)
            elif name == "get_real_time_generation":
                result = await eptr_server.handle_get_real_time_generation(arguments)
            elif name == "get_demand_forecast":
                result = await eptr_server.handle_get_demand_forecast(arguments)
            elif name == "get_imbalance_price":
                result = await eptr_server.handle_get_imbalance_price(arguments)
            elif name == "get_available_eptr2_calls":
                result = await eptr_server.handle_get_available_eptr2_calls(arguments)
            elif name == "call_eptr2_api":
                result = await eptr_server.handle_call_eptr2_api(arguments)
            elif name == "get_hourly_consumption_and_forecast":
                result = await eptr_server.handle_get_hourly_consumption_and_forecast(arguments)
            elif name == "get_price_and_cost_data":
                result = await eptr_server.handle_get_price_and_cost_data(arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")
            
            return [TextContent(type="text", text=result)]
        except Exception as e:
            error_msg = f"Error executing {name}: {str(e)}"
            return [TextContent(type="text", text=error_msg)]
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    """Entry point for the eptr2-mcp-server command."""
    asyncio.run(run_mcp_server(use_dotenv=True, recycle_tgt=True))


if __name__ == "__main__":
    """Run the MCP server from command line."""
    main()
