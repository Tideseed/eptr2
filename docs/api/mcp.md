# MCP Server

The `eptr2.mcp` module provides a Model Context Protocol (MCP) server for AI agent integration.

## Overview

The MCP server enables AI assistants like Claude to directly query Turkish electricity market data through a standardized protocol.

## Quick Start

```bash
# Run the server
eptr2-mcp-server
```

Or programmatically:

```python
from eptr2.mcp import run_mcp_server
import asyncio

asyncio.run(run_mcp_server(use_dotenv=True, recycle_tgt=True))
```

## Module Reference

### run_mcp_server

Main entry point for the MCP server.

```python
from eptr2.mcp import run_mcp_server
import asyncio

asyncio.run(run_mcp_server(
    use_dotenv=True,       # Load credentials from .env
    recycle_tgt=True,      # Reuse TGT tickets
    dotenv_path=".env",    # Path to .env file
))
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `use_dotenv` | `bool` | `True` | Load credentials from `.env` file |
| `recycle_tgt` | `bool` | `True` | Reuse authentication tickets |
| `dotenv_path` | `str` | `".env"` | Path to `.env` file |

## Available Tools

The MCP server exposes these tools:

### Price Tools

#### get_market_clearing_price

Fetches Day-Ahead Market prices (MCP/PTF).

```json
{
  "name": "get_market_clearing_price",
  "arguments": {
    "start_date": "2024-07-29",
    "end_date": "2024-07-29"
  }
}
```

#### get_system_marginal_price

Fetches System Marginal Prices (SMP/SMF).

```json
{
  "name": "get_system_marginal_price",
  "arguments": {
    "start_date": "2024-07-29",
    "end_date": "2024-07-29"
  }
}
```

#### get_imbalance_price

Fetches positive and negative imbalance prices.

```json
{
  "name": "get_imbalance_price",
  "arguments": {
    "start_date": "2024-07-29",
    "end_date": "2024-07-29"
  }
}
```

### Consumption Tools

#### get_real_time_consumption

Fetches real-time electricity consumption data.

```json
{
  "name": "get_real_time_consumption",
  "arguments": {
    "start_date": "2024-07-29",
    "end_date": "2024-07-29"
  }
}
```

#### get_demand_forecast

Fetches demand forecast (load plan) data.

```json
{
  "name": "get_demand_forecast",
  "arguments": {
    "start_date": "2024-07-29",
    "end_date": "2024-07-29"
  }
}
```

### Generation Tools

#### get_real_time_generation

Fetches real-time generation data by resource type.

```json
{
  "name": "get_real_time_generation",
  "arguments": {
    "start_date": "2024-07-29",
    "end_date": "2024-07-29"
  }
}
```

### Composite Tools

#### get_hourly_consumption_and_forecast

Fetches combined consumption and forecast data.

```json
{
  "name": "get_hourly_consumption_and_forecast",
  "arguments": {
    "start_date": "2024-07-29",
    "end_date": "2024-07-29"
  }
}
```

#### get_price_and_cost_data

Fetches comprehensive price and cost data.

```json
{
  "name": "get_price_and_cost_data",
  "arguments": {
    "start_date": "2024-07-29",
    "end_date": "2024-07-29"
  }
}
```

### Discovery Tools

#### get_available_eptr2_calls

Lists all 213+ available API endpoints.

```json
{
  "name": "get_available_eptr2_calls",
  "arguments": {}
}
```

#### call_eptr2_api

Calls any API endpoint by key.

```json
{
  "name": "call_eptr2_api",
  "arguments": {
    "call_key": "mcp",
    "start_date": "2024-07-29",
    "end_date": "2024-07-29"
  }
}
```

## Claude Desktop Configuration

Add to `claude_desktop_config.json`:

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

## VS Code Configuration

Enable MCP in VS Code settings:

```json
{
  "chat.mcp.discovery.enabled": true
}
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `EPTR_USERNAME` | EPIAS platform username (email) |
| `EPTR_PASSWORD` | EPIAS platform password |
| `EPTR_TGT_PATH` | Custom path for TGT storage |

## Error Handling

The MCP server returns errors in a standardized format:

```json
{
  "error": {
    "code": "authentication_error",
    "message": "Invalid credentials"
  }
}
```

## See Also

- [MCP Server Guide](../ai-integration/mcp-server.md)
- [Claude Desktop Setup](../ai-integration/claude-desktop.md)
- [Agent Skills](../ai-integration/agent-skills.md)
