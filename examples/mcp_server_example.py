"""
Example: Using the EPTR2 MCP Server

This example demonstrates how to set up and use the MCP server
for AI agent integration with the eptr2 library.
"""

import asyncio
import json
from eptr2.mcp import run_mcp_server


async def example_run_mcp_server():
    """
    Run the MCP server for AI agent integration.

    This server exposes eptr2 functionality via the Model Context Protocol,
    allowing AI assistants to query Turkish electricity market data.
    """
    print("=" * 60)
    print("Starting EPTR2 MCP Server")
    print("=" * 60)
    print()
    print("The server will expose the following tools:")
    print()
    print("1. get_market_clearing_price - Day-ahead market prices")
    print("2. get_system_marginal_price - System marginal prices")
    print("3. get_real_time_consumption - Real-time consumption data")
    print("4. get_real_time_generation - Generation by resource type")
    print("5. get_demand_forecast - Demand forecasts")
    print("6. get_imbalance_price - Imbalance pricing")
    print("7. get_available_eptr2_calls - List all API endpoints")
    print("8. call_eptr2_api - Generic API call")
    print("9. get_hourly_consumption_and_forecast - Composite data")
    print("10. get_price_and_cost_data - Comprehensive pricing")
    print()
    print("=" * 60)
    print()
    print("Server is running and waiting for connections...")
    print("Press Ctrl+C to stop the server.")
    print()

    # Run the server
    # This will use credentials from .env file (EPTR_USERNAME, EPTR_PASSWORD)
    await run_mcp_server(use_dotenv=True, recycle_tgt=True)


def print_configuration_guide():
    """Print configuration guide for various MCP clients."""
    print("=" * 60)
    print("MCP Server Configuration Guide")
    print("=" * 60)
    print()

    print("1. Prerequisites:")
    print("   - Install eptr2 with MCP support:")
    print("     pip install 'eptr2[mcp]'")
    print()
    print("   - Create .env file with credentials:")
    print("     EPTR_USERNAME=your.email@example.com")
    print("     EPTR_PASSWORD=yourpassword")
    print()

    print("2. Running the server:")
    print()
    print("   Option A - Command line:")
    print("     eptr2-mcp-server")
    print()
    print("   Option B - Python module:")
    print("     python -m eptr2.mcp.server")
    print()
    print("   Option C - Programmatically:")
    print("     from eptr2.mcp import run_mcp_server")
    print("     import asyncio")
    print("     asyncio.run(run_mcp_server())")
    print()

    print("3. Claude Desktop Configuration:")
    print()
    claude_config = {
        "mcpServers": {
            "eptr2": {
                "command": "eptr2-mcp-server",
                "env": {
                    "EPTR_USERNAME": "your.email@example.com",
                    "EPTR_PASSWORD": "yourpassword",
                },
            }
        }
    }
    print("   Add this to your Claude Desktop config file:")
    print("   Location: YOUR_CLAUDE_PATH/claude_desktop_config.json")
    print()
    print(json.dumps(claude_config, indent=2))
    print()

    print("4. Alternative Configuration (with environment variables):")
    print()
    alt_config = {
        "mcpServers": {
            "eptr2": {
                "command": "python",
                "args": ["-m", "eptr2.mcp.server"],
                "env": {
                    "EPTR_USERNAME": "${EPTR_USERNAME}",
                    "EPTR_PASSWORD": "${EPTR_PASSWORD}",
                },
            }
        }
    }
    print(json.dumps(alt_config, indent=2))
    print()

    print("=" * 60)
    print()


def print_example_queries():
    """Print example queries AI agents can make."""
    print("=" * 60)
    print("Example AI Agent Queries")
    print("=" * 60)
    print()
    print("Once the MCP server is connected to an AI assistant,")
    print("you can make natural language queries like:")
    print()

    examples = [
        "What was the market clearing price in Turkey on July 29, 2024?",
        "Show me the real-time electricity consumption for the last week",
        "Get the system marginal price for August 2024",
        "What are the imbalance prices for today?",
        "Show me electricity generation by type for yesterday",
        "Get demand forecasts for the next 7 days",
        "What API endpoints are available for querying?",
        "Get comprehensive pricing data for July 2024",
        "Show me consumption and forecast data for last month",
        "What was the average MCP price in September 2024?",
    ]

    for i, query in enumerate(examples, 1):
        print(f"{i:2d}. {query}")

    print()
    print("=" * 60)
    print()


def print_tool_details():
    """Print detailed information about available MCP tools."""
    print("=" * 60)
    print("MCP Tools - Detailed Reference")
    print("=" * 60)
    print()

    tools = [
        {
            "name": "get_market_clearing_price",
            "params": "start_date, end_date",
            "returns": "Hourly market clearing prices (TL/MWh)",
            "example": "start_date='2024-07-29', end_date='2024-07-29'",
        },
        {
            "name": "get_system_marginal_price",
            "params": "start_date, end_date",
            "returns": "Hourly system marginal prices (TL/MWh)",
            "example": "start_date='2024-07-01', end_date='2024-07-31'",
        },
        {
            "name": "get_real_time_consumption",
            "params": "start_date, end_date",
            "returns": "Hourly electricity consumption (MWh)",
            "example": "start_date='2024-08-01', end_date='2024-08-31'",
        },
        {
            "name": "get_real_time_generation",
            "params": "start_date, end_date",
            "returns": "Hourly generation by type (wind, solar, etc.)",
            "example": "start_date='2024-07-29', end_date='2024-07-29'",
        },
        {
            "name": "get_demand_forecast",
            "params": "start_date, end_date",
            "returns": "Forecasted electricity demand (MWh)",
            "example": "start_date='2024-09-01', end_date='2024-09-30'",
        },
        {
            "name": "get_imbalance_price",
            "params": "start_date, end_date",
            "returns": "Positive and negative imbalance prices",
            "example": "start_date='2024-07-29', end_date='2024-07-29'",
        },
        {
            "name": "get_available_eptr2_calls",
            "params": "None",
            "returns": "List of all 213+ available API endpoints",
            "example": "No parameters required",
        },
        {
            "name": "call_eptr2_api",
            "params": "call_key, start_date, end_date, additional_params",
            "returns": "Data from specified API endpoint",
            "example": "call_key='mcp', start_date='2024-07-29', end_date='2024-07-29'",
        },
        {
            "name": "get_hourly_consumption_and_forecast",
            "params": "start_date, end_date",
            "returns": "Combined consumption and forecast data",
            "example": "start_date='2024-07-01', end_date='2024-07-31'",
        },
        {
            "name": "get_price_and_cost_data",
            "params": "start_date, end_date",
            "returns": "Comprehensive pricing with costs",
            "example": "start_date='2024-07-01', end_date='2024-07-31'",
        },
    ]

    for i, tool in enumerate(tools, 1):
        print(f"{i}. {tool['name']}")
        print(f"   Parameters: {tool['params']}")
        print(f"   Returns: {tool['returns']}")
        print(f"   Example: {tool['example']}")
        print()

    print("=" * 60)
    print()


def main():
    """Main function to display information and optionally run server."""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--run":
        # Run the server
        try:
            asyncio.run(example_run_mcp_server())
        except KeyboardInterrupt:
            print("\n\nServer stopped by user.")
            print("=" * 60)
    else:
        # Display configuration and usage information
        print()
        print_configuration_guide()
        print_tool_details()
        print_example_queries()

        print("=" * 60)
        print("To run the MCP server now, execute:")
        print("  python examples/mcp_server_example.py --run")
        print()
        print("Or use the command:")
        print("  eptr2-mcp-server")
        print("=" * 60)
        print()


if __name__ == "__main__":
    main()
