# EPTR2 for AI Agents

This document provides a quick reference guide for AI agents working with the eptr2 library.

## Quick Start for AI Agents

eptr2 is a Python client for accessing Turkish electricity market data from EPIAS Transparency Platform v2.0.

### Authentication

Two methods available:
1. **Environment variables** (recommended):
   - Set `EPTR_USERNAME` and `EPTR_PASSWORD` in `.env` file
   - Use `EPTR2(use_dotenv=True, recycle_tgt=True)`

2. **Direct credentials**:
   - Use `EPTR2(username="email@example.com", password="password")`

### Basic Usage Pattern

```python
from eptr2 import EPTR2

# Initialize with auto-auth
eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

# Call any endpoint
result = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
```

## Most Common API Calls

### Prices
- `mcp` or `ptf`: Market Clearing Price (day-ahead market price)
- `smp` or `smf`: System Marginal Price
- `imbalance-price`: Imbalance prices (positive and negative)

### Consumption & Generation
- `rt-consumption`: Real-time electricity consumption
- `rt-generation`: Real-time generation by resource type
- `load-plan`: Demand forecast (UECM)

### Market Data
- `dpp` or `kgup`: Daily production plan
- `uevm`: Generation forecast by plant
- `rt-gen`: Real-time generation by plant

## Composite Functions

These combine multiple API calls for convenience:

### From eptr2.composite:

```python
from eptr2.composite import (
    get_hourly_consumption_and_forecast_data,
    get_hourly_price_and_cost_data,
    get_imbalance_data,
    get_hourly_production_data,
    get_hourly_production_plan_data
)

# Example
df = get_hourly_consumption_and_forecast_data(
    eptr, 
    start_date="2024-07-29", 
    end_date="2024-07-29"
)
```

## Date Format

Always use ISO format: `YYYY-MM-DD` (e.g., "2024-07-29")

## Return Format

- By default returns pandas DataFrame (if pandas installed)
- Can return raw JSON with `postprocess=False`

## Discovery

```python
# List all available calls (213+ endpoints)
eptr.get_available_calls()

# Get call count and categories
eptr.get_number_of_calls()

# View aliases
eptr.get_aliases()
```

## Common Parameters

Most calls accept:
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)
- Some require specific IDs:
  - `org_id`: Organization ID
  - `pp_id`: Power plant ID
  - `uevcb_id`: Production unit ID

## MCP Server

For AI agents using Model Context Protocol:

```python
from eptr2.mcp import run_mcp_server
import asyncio

# Run MCP server
asyncio.run(run_mcp_server(use_dotenv=True))
```

Or from command line:
```bash
python -m eptr2.mcp.server
```

### Available MCP Tools

1. `get_market_clearing_price` - Day-ahead market prices
2. `get_system_marginal_price` - System marginal prices  
3. `get_real_time_consumption` - Real-time consumption
4. `get_real_time_generation` - Generation by type
5. `get_demand_forecast` - Demand forecasts
6. `get_imbalance_price` - Imbalance pricing
7. `get_available_eptr2_calls` - List all endpoints
8. `call_eptr2_api` - Generic call to any endpoint
9. `get_hourly_consumption_and_forecast` - Composite consumption data
10. `get_price_and_cost_data` - Composite pricing data

## Error Handling

```python
try:
    result = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
except Exception as e:
    print(f"Error: {e}")
```

## Key Features

- 213+ API endpoints for Turkish electricity market
- Automatic TGT (Ticket Granting Ticket) management
- Credential management via .env files
- Composite functions for common data analysis
- Pandas DataFrame integration
- MCP server for AI agent integration

## Example: Complete Analysis

```python
from eptr2 import EPTR2
from eptr2.composite import (
    get_hourly_consumption_and_forecast_data,
    get_hourly_price_and_cost_data
)

# Initialize
eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

# Get consumption and forecast
consumption_df = get_hourly_consumption_and_forecast_data(
    eptr, 
    start_date="2024-07-01", 
    end_date="2024-07-31"
)

# Get pricing data
price_df = get_hourly_price_and_cost_data(
    eptr, 
    start_date="2024-07-01", 
    end_date="2024-07-31"
)

# Merge for analysis
import pandas as pd
analysis = pd.merge(
    consumption_df, 
    price_df, 
    on=['date', 'hour'], 
    how='inner'
)
```

## Resources

- Main README: `/README.md`
- Package: https://pypi.org/project/eptr2/
- Demo: https://eptr2demo.streamlit.app/
- EPIAS Platform: https://seffaflik.epias.com.tr/

## Installation

```bash
# With all extras (recommended for agents)
pip install "eptr2[allextras]"

# With MCP support
pip install "eptr2[allextras]" mcp

# Basic installation
pip install eptr2
```
