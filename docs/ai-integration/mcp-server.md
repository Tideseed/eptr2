# MCP Server

eptr2 includes a Model Context Protocol (MCP) server that enables AI assistants like Claude to directly query Turkish electricity market data.

## What is MCP?

The Model Context Protocol (MCP) is a standard for connecting AI assistants to external data sources and tools. With eptr2's MCP server, AI assistants can:

- Query real-time electricity prices
- Fetch consumption and generation data
- Access all 213+ API endpoints
- Perform complex market analysis

## Quick Start

### Installation

Install eptr2 with MCP support:

```bash
pip install "eptr2[allextras]"
```

### Running the Server

From command line:

```bash
eptr2-mcp-server
```

Or programmatically:

```python
from eptr2.mcp import create_mcp_server, run_mcp_server
import asyncio

# Option A: async helper
asyncio.run(run_mcp_server(use_dotenv=True, recycle_tgt=True))

# Option B: explicit server creation
server = create_mcp_server(use_dotenv=True, recycle_tgt=True)
# server.run()
```

## Configuration

### Environment Variables

Create a `.env` file with your credentials:

```env
EPTR_USERNAME=your.email@example.com
EPTR_PASSWORD=yourpassword
```

### Server Options

```python
from eptr2.mcp import run_mcp_server
import asyncio

asyncio.run(run_mcp_server(
    use_dotenv=True,       # Load credentials from .env
    recycle_tgt=True,      # Reuse authentication tickets
    dotenv_path=".env",    # Path to .env file
))
```

## Available MCP Tools

The MCP server exposes 17 tools:

### Price Tools

| Tool | Description |
|------|-------------|
| `get_market_clearing_price` | Day-ahead market prices (MCP/PTF) |
| `get_system_marginal_price` | System marginal prices (SMP/SMF) |
| `get_imbalance_price` | Positive and negative imbalance prices |

### Consumption Tools

| Tool | Description |
|------|-------------|
| `get_real_time_consumption` | Real-time consumption data |
| `get_demand_forecast` | Load plan forecasts |

### Generation Tools

| Tool | Description |
|------|-------------|
| `get_real_time_generation` | Generation by resource type |
| `get_bulk_production_plans` | Bulk per-plant production plans (dpp/kgup) |

### Market Operations Tools

| Tool | Description |
|------|-------------|
| `get_market_operations_summary` | DAM matched + bilateral + intraday volumes |
| `get_balancing_market_data` | Balancing market (YAL/YAT + SMP) |

### Composite Tools

| Tool | Description |
|------|-------------|
| `get_hourly_consumption_and_forecast` | Combined consumption and forecast data |
| `get_price_and_cost_data` | Comprehensive price and cost data |

### Discovery Tools (no credentials needed)

| Tool | Description |
|------|-------------|
| `get_available_eptr2_calls` | List all 231 API endpoints |
| `describe_eptr2_call` | Parameters and metadata for one call key |
| `search_eptr2_calls` | Keyword search over endpoints (EN/TR) |
| `call_eptr2_api` | Call any API endpoint by key (`additional_params` supported) |

### Calculation Tools (pure, no credentials needed)

| Tool | Description |
|------|-------------|
| `calculate_imbalance_prices_and_costs` | Unit imbalance prices/costs for one hour |
| `calculate_kupst_deviation_cost` | Production plan deviation (KUPST) cost |

### Resources and Prompts

| Resource | Description |
|----------|-------------|
| `eptr2://schema` | Machine-readable schema of all endpoints (generated live) |
| `eptr2://help/{call_key}` | Details for one call key |

The `analyze_market_prices` prompt guides a price analysis over a date range.

## Example Queries

Once connected to Claude or another MCP-compatible assistant, you can ask:

- "What are today's electricity prices in Turkey?"
- "Show me the real-time generation by fuel type"
- "Compare MCP and SMP for the last week"
- "What was the peak consumption yesterday?"

## Integration Methods

### 1. MCP Clients (VS Code, Claude Desktop/Code, Cursor, ...)

See [MCP Client Setup](mcp-clients.md) for per-client instructions, or print a ready-to-paste config:

```bash
eptr2 mcp-config --client vscode
```

### 2. Custom Integration

Use the MCP client library:

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="eptr2-mcp-server"
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print(tools)
            
            # Call a tool
            result = await session.call_tool(
                "get_market_clearing_price",
                {"start_date": "2024-07-29", "end_date": "2024-07-29"}
            )
            print(result)

asyncio.run(main())
```

## Debugging

### Check Server Status

```bash
# Run with verbose output
EPTR_USERNAME=... EPTR_PASSWORD=... eptr2-mcp-server --verbose
```

### Test Connection

```python
from eptr2.mcp.server import create_mcp_server

server = create_mcp_server(use_dotenv=True)
print(f"Server created: {server}")
```

## Best Practices

1. **Use environment variables** - Don't hardcode credentials
2. **Enable TGT recycling** - Reduces authentication overhead
3. **Set appropriate timeouts** - For slow network connections
4. **Monitor usage** - Be aware of API rate limits

## Security Considerations

- Never commit `.env` files to version control
- Use secure credential management in production
- Consider network isolation for sensitive deployments

## Next Steps

- [MCP Client Setup](mcp-clients.md)
- [Agent Skills](agent-skills.md)
- [CLI for Agents](cli.md)
- [API Reference - MCP](../api/mcp.md)
