# EPTR2 MCP Server

This directory contains the Model Context Protocol (MCP) server implementation for eptr2.

## What is MCP?

Model Context Protocol (MCP) is a standardized protocol developed by Anthropic for connecting AI assistants to external data sources and tools. It enables AI agents to:

- Access real-time data
- Execute functions safely
- Integrate with existing systems
- Work with structured APIs

## EPTR2 MCP Server

The EPTR2 MCP server exposes the Turkish electricity market data API to AI agents, allowing them to:

- Query market prices (MCP, SMP)
- Get consumption and generation data
- Access forecasts and plans
- Retrieve imbalance prices
- Use composite data functions
- Discover available API endpoints

## Installation

### Basic Installation

```bash
pip install "eptr2[mcp]"
```

### With All Features

```bash
pip install "eptr2[allextras,mcp]"
```

### Manual Installation

```bash
pip install eptr2 fastmcp
```

## Setup

### 1. Configure Credentials

Create a `.env` file in your working directory:

```env
EPTR_USERNAME=your.email@example.com
EPTR_PASSWORD=yourpassword
```

### 2. Run the Server

#### Option A: Using the command-line script

```bash
eptr2-mcp-server
```

#### Option B: Using Python module

```bash
python -m eptr2.mcp.server
```

#### Option C: Programmatically

```python
from eptr2.mcp import run_mcp_server
import asyncio

asyncio.run(run_mcp_server(use_dotenv=True, recycle_tgt=True))
```

## Configuration

### For MCP Clients

**For per-client setup instructions (VS Code, Claude Desktop/Code, Cursor), see the [MCP Client Setup guide](https://tideseed.github.io/eptr2/ai-integration/mcp-clients/), or print a ready-to-paste config with `eptr2 mcp-config --client <name>`.**

Quick reference - Add to your Claude Desktop configuration:

| OS | Config File Location |
|----|---------------------|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| Linux | `~/.config/Claude/claude_desktop_config.json` |

**Recommended configuration using uv:**

```json
{
  "mcpServers": {
    "eptr2": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/FULL/PATH/TO/YOUR/eptr2",
        "--extra",
        "mcp",
        "eptr2-mcp-server"
      ]
    }
  }
}
```

**Alternative using environment variables:**

```json
{
  "mcpServers": {
    "eptr2": {
      "command": "eptr2-mcp-server",
      "env": {
        "EPTR_USERNAME": "your.email@example.com",
        "EPTR_PASSWORD": "yourpassword"
      }
    }
  }
}
```

Or generate the config for your client (most clients do not expand `${VAR}` placeholders, so use literal values):

```bash
eptr2 mcp-config --client claude-desktop   # or: vscode, claude-code, cursor, generic
```

## Available Tools

The MCP server exposes 17 tools:

### 1. get_market_clearing_price
Get day-ahead market clearing prices (MCP/PTF).

**Parameters:**
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format

### 2. get_system_marginal_price
Get system marginal prices (SMP/SMF).

**Parameters:**
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format

### 3. get_real_time_consumption
Get real-time electricity consumption data.

**Parameters:**
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format

### 4. get_real_time_generation
Get real-time generation data by resource type (wind, solar, hydro, etc.).

**Parameters:**
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format

### 5. get_demand_forecast
Get demand forecast data (Load Plan/UECM).

**Parameters:**
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format

### 6. get_imbalance_price
Get imbalance prices (positive and negative).

**Parameters:**
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format

### 7. get_available_eptr2_calls
List all available API calls in the eptr2 library (231 endpoints).

**Parameters:** None

### 8. call_eptr2_api
Generic function to call any eptr2 API endpoint.

**Parameters:**
- `call_key` (required): The API call key (e.g., 'mcp', 'smp', 'rt-cons')
- `start_date` (optional): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format
- `additional_params` (optional): Additional parameters as key-value pairs (dict or JSON string)

### 9. get_hourly_consumption_and_forecast
Get composite data combining load plan, UECM, and real-time consumption.

**Parameters:**
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format

### 10. get_price_and_cost_data
Get composite pricing data (MCP, SMP, imbalance costs).

**Parameters:**
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format

### 11. describe_eptr2_call
Get parameters, HTTP method, path and bilingual descriptions for one call key. Resolves aliases. No credentials needed.

**Parameters:**
- `call_key` (required): The API call key (e.g., 'mcp', 'ptf')

### 12. search_eptr2_calls
Keyword search over all call keys, titles and descriptions (English and Turkish). No credentials needed.

**Parameters:**
- `query` (required): Search keyword
- `category` (optional): Restrict to a category (e.g., 'GÖP', 'DGP')

### 13. get_market_operations_summary
Combined DAM matched quantities, bilateral contracts and intraday volumes.

**Parameters:**
- `start_date`, `end_date` (required): YYYY-MM-DD

### 14. get_balancing_market_data
Balancing Power Market data: YAL/YAT instructions with SMP.

**Parameters:**
- `start_date`, `end_date` (required): YYYY-MM-DD

### 15. get_bulk_production_plans
Bulk per-plant production plans ('dpp' or 'kgup').

**Parameters:**
- `start_date`, `end_date` (required): YYYY-MM-DD
- `plant_ids` (required): Powerplant ids for 'dpp' (see 'pp-list'), UEVCB ids for 'kgup' (see 'uevcb-list-bulk')
- `plan_type` (optional): 'dpp' (default) or 'kgup'

### 16. calculate_imbalance_prices_and_costs
Pure calculation of unit imbalance prices/costs for one hour. No credentials needed.

**Parameters:**
- `contract` (required): Hourly contract code 'PHYYMMDDhh'
- `mcp_price`, `smp_price` (required): Prices in TL/MWh
- `include_kupst` (optional): Include unit KUPST cost (default true)

### 17. calculate_kupst_deviation_cost
Pure calculation of the KUPST production-plan deviation cost for one hour. No credentials needed.

**Parameters:**
- `contract` (required): Hourly contract code 'PHYYMMDDhh'
- `actual`, `forecast` (required): Production in MWh
- `mcp_price`, `smp_price` (required): Prices in TL/MWh
- `source` (optional): Energy source for tolerance (default 'other')
- `tolerance` (optional): Explicit tolerance as decimal (e.g. 0.15)

### Resources

- `eptr2://schema` — machine-readable schema of all endpoints (generated live)
- `eptr2://help/{call_key}` — details for one call key

### Prompts

- `analyze_market_prices(start_date, end_date)` — guided market price analysis

## Example AI Agent Queries

Once configured, AI agents can make queries like:

- "What was the market clearing price in Turkey on July 29, 2024?"
- "Show me the real-time electricity consumption for the last week"
- "Get the system marginal price and imbalance prices for August 2024"
- "What are all the available API endpoints I can query?"
- "Get comprehensive pricing data including costs for July 2024"

## Return Format

All tools return data in JSON format:
- Most tools return arrays of records (compatible with pandas DataFrame)
- Timestamps are in ISO format
- Numeric values preserve decimal precision

## Error Handling

The server handles errors gracefully and returns descriptive error messages:
- Authentication failures
- Invalid date formats
- Missing required parameters
- API errors

## Development

### Testing the Server

```python
# test_mcp_server.py
from eptr2.mcp import run_mcp_server
import asyncio

async def test():
    # This will start the server
    await run_mcp_server(use_dotenv=True, recycle_tgt=True)

if __name__ == "__main__":
    asyncio.run(test())
```

### Extending the Server

To add new tools:

1. Add a new function in `server.py`
2. Decorate it with `@mcp.tool()`
3. Use `_get_eptr_client()` and `client.call(...)` for endpoint execution
4. Update documentation

## Resources

- **MCP Documentation**: https://modelcontextprotocol.io/
- **EPTR2 Documentation**: See main README.md
- **EPTR2 PyPI**: https://pypi.org/project/eptr2/
- **EPIAS Platform**: https://seffaflik.epias.com.tr/

## Troubleshooting

### Server won't start
- Check that `fastmcp` package is installed: `pip install fastmcp`
- Verify credentials in `.env` file
- Check Python version (>=3.10 required)

### Authentication errors
- Verify your EPIAS Transparency Platform credentials
- Ensure `.env` file is in the correct directory
- Check that `use_dotenv=True` is set

### Tool call failures
- Verify date format (must be YYYY-MM-DD)
- Check that required parameters are provided
- Review error messages for specific issues

## License

Apache License 2.0 - Same as the eptr2 library

## Support

For issues and questions:
- GitHub: https://github.com/Tideseed/eptr2
- Email: info@tideseed.com
