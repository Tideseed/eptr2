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
pip install eptr2 mcp
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

### For Claude Desktop

**For complete setup instructions, see `CLAUDE_SETUP.md` in the repository root.**

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

Or reference the provided `mcp-config.json`:

```json
{
  "mcpServers": {
    "eptr2": {
      "command": "python",
      "args": ["-m", "eptr2.mcp.server"],
      "env": {
        "EPTR_USERNAME": "${EPTR_USERNAME}",
        "EPTR_PASSWORD": "${EPTR_PASSWORD}"
      }
    }
  }
}
```

## Available Tools

The MCP server exposes 10 tools:

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
List all available API calls in the eptr2 library (213+ endpoints).

**Parameters:** None

### 8. call_eptr2_api
Generic function to call any eptr2 API endpoint.

**Parameters:**
- `call_key` (required): The API call key (e.g., 'mcp', 'smp', 'rt-consumption')
- `start_date` (optional): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format
- `additional_params` (optional): Additional parameters as key-value pairs

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

1. Add tool definition to `EPTR2_TOOLS` in `server.py`
2. Implement handler method in `EPTR2MCPServer` class
3. Add case to `call_tool` handler
4. Update documentation

## Resources

- **MCP Documentation**: https://modelcontextprotocol.io/
- **EPTR2 Documentation**: See main README.md
- **EPTR2 PyPI**: https://pypi.org/project/eptr2/
- **EPIAS Platform**: https://seffaflik.epias.com.tr/

## Troubleshooting

### Server won't start
- Check that `mcp` package is installed: `pip install mcp`
- Verify credentials in `.env` file
- Check Python version (>=3.9.6 required)

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
