# EPTR2 for AI Agents

This document provides a quick reference guide for AI agents working with the eptr2 library.

## Claude Agent Skills

eptr2 includes Claude Agent Skills for enhanced AI assistance. Skills are automatically loaded based on your request and provide specialized guidance for:

| Skill | Triggers On | Location |
|-------|------------|----------|
| **eptr2-price-analysis** | Electricity prices, MCP, PTF, SMP, WAP | `.claude/skills/eptr2-price-analysis/` |
| **eptr2-consumption-data** | Consumption, demand forecast, UECM, load plan | `.claude/skills/eptr2-consumption-data/` |
| **eptr2-generation-tracking** | Generation, UEVM, power plants, renewables | `.claude/skills/eptr2-generation-tracking/` |
| **eptr2-imbalance-costs** | Imbalance, KUPST, deviation costs, penalties | `.claude/skills/eptr2-imbalance-costs/` |
| **eptr2-market-operations** | DAM, IDM, GÖP, GİP, bilateral contracts | `.claude/skills/eptr2-market-operations/` |
| **eptr2-api-discovery** | Available endpoints, API search, discovery | `.claude/skills/eptr2-api-discovery/` |

### Using Skills

Skills are model-invoked - Claude automatically selects the relevant skill based on your request. For example:
- "What are today's electricity prices?" → triggers `eptr2-price-analysis`
- "Show me wind generation data" → triggers `eptr2-generation-tracking`
- "Calculate imbalance costs" → triggers `eptr2-imbalance-costs`
- "What APIs are available?" → triggers `eptr2-api-discovery`

### Installing Skills Personally

To use skills across all your projects, copy to your personal skills directory:

```bash
# macOS/Linux
cp -r .claude/skills/* ~/.claude/skills/

# Windows
xcopy /E /I .claude\skills %USERPROFILE%\.claude\skills
```

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
- `mcp-smp-imb`: Imbalance prices (positive and negative)

### Consumption & Generation
- `rt-cons`: Real-time electricity consumption
- `rt-gen`: Real-time generation by resource type
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

## API Call Help and Documentation

The `get_help_d` function provides detailed metadata for each API endpoint:

```python
from eptr2.mapping.help import get_help_d

# Get help for a specific call
help_info = get_help_d("mcp")

# Returns a dictionary with:
# - "category": Market category (e.g., "GÖP" for Day-Ahead Market)
# - "title": {"tr": "Turkish title", "en": "English title"}
# - "desc": {"tr": "Turkish description", "en": "English description"}
# - "url": Link to official documentation

# Get all available help entries
all_help = get_help_d()
```

**Important**: Descriptions are bilingual:
- Turkish text is under `"tr"` keys
- English text is under `"en"` keys

This function is useful for:
- Understanding what each API call returns
- Getting official Turkish terminology
- Finding links to official EPIAS documentation
- Discovering the category/market type for each endpoint

## Common Parameters

Most calls accept:
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)
- Some require specific IDs:
  - `org_id`: Organization ID
  - `pp_id`: Power plant ID
  - `uevcb_id`: Production unit ID

## MCP Server (Claude Desktop Integration)

For AI agents using Model Context Protocol (e.g., Claude Desktop):

**For detailed setup instructions, see `CLAUDE_SETUP.md`**

Quick command-line usage:

```python
from eptr2.mcp import run_mcp_server
import asyncio

# Run MCP server
asyncio.run(run_mcp_server(use_dotenv=True))
```

Or from command line:
```bash
# Using uv (recommended)
uv run --extra mcp eptr2-mcp-server

# Using standard Python
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
# Recommended: Install with all extras (includes MCP support)
pip install "eptr2[allextras]"

# Basic installation (minimal dependencies)
pip install eptr2
```

**Note:** The `[allextras]` variant includes everything needed for Claude Desktop integration, data analysis (pandas), and the demo app (streamlit).

**For Claude Desktop setup:** See `CLAUDE_SETUP.md` for step-by-step instructions.

## Common Abbreviations

Since eptr is about the Turkish electricity market, many terms are abbreviated in Turkish:

- MCP: Market Clearing Price (Piyasa Takas Fiyatı)
- SMP: System Marginal Price (Sistem Marjinal Fiyatı)
- KGÜP: Daily Production Plan (Kesinleşmiş Günlük Üretim Planı)
- UEÇM: Settlement Actual Demand (Uzlaştırmaya Esas Çekiş Miktarı)
- UEVM: Settlement Actual Generation (Uzlaştırmaya Esas Veriş Miktarı)
- KÜPST: Deviation Cost from Production Plan (Kesinleşmiş Üretim Planından Sapma Tutarı)
- KUDÜP: Settlement Production Plan (Kesinleşmiş Uzlaştırma Dönemi Üretim Planı)
- AOF: Weighted Average Price (Ağırlıklı Ortalama Fiyat)
- GİP: Intraday Market (Gün İçi Piyasası)
- GÖP: Day-Ahead Market (Gün Öncesi Piyasası)
- DGP: Balancing Power Market (Dengeleme Güç Piyasası)
- YAL: Up regulation (Yük Alma)
- YAT: Down regulation (Yük Atma)