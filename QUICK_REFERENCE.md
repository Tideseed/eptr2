# EPTR2 Quick Reference for AI Agents

## TL;DR
```python
from eptr2 import EPTR2
eptr = EPTR2(use_dotenv=True, recycle_tgt=True)
df = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
```

Or from the shell:
```bash
eptr2 call mcp --start-date 2024-07-29 --end-date 2024-07-29
```

## CLI One-Liners

```bash
eptr2 list                    # All call keys by category
eptr2 search imbalance        # Keyword search (EN/TR)
eptr2 describe mcp            # Parameters for one call
eptr2 call mcp --start-date 2024-07-29 --end-date 2024-07-29 --format csv
eptr2 install-skills          # Install bundled agent skills
eptr2 mcp-config --client vscode
```

## Top Most Used API Calls

| Call Key | Alias | Description | Returns |
|----------|-------|-------------|---------|
| `mcp` | `ptf` | Market Clearing Price | Day-ahead prices (TL/MWh) |
| `smp` | `smf` | System Marginal Price | System prices (TL/MWh) |
| `rt-cons` | - | Real-time Consumption | Hourly consumption (MWh) |
| `rt-gen` | - | Real-time Generation | Generation by type (MWh) |
| `mcp-smp-imb` | - | Imbalance Prices | Pos/neg imbalance prices |
| `load-plan` | - | Load Plan (UECM) | Demand forecast (MWh) |
| `dpp` | `kgup` | Daily Production Plan | Production plans by unit |
| `uevm` | - | Settlement Actual Generation | Plant-level settlement generation |
| `wap` | - | Weighted Average Price | Volume-weighted price |

## Common Patterns

### Get Price Data
```python
# Market clearing price
mcp = eptr.call("mcp", start_date="2024-07-01", end_date="2024-07-31")

# System marginal price
smp = eptr.call("smp", start_date="2024-07-01", end_date="2024-07-31")

# Imbalance prices
imb = eptr.call("mcp-smp-imb", start_date="2024-07-01", end_date="2024-07-31")
```

### Get Consumption/Generation
```python
# Real-time consumption
cons = eptr.call("rt-cons", start_date="2024-07-01", end_date="2024-07-31")

# Real-time generation by type
gen = eptr.call("rt-gen", start_date="2024-07-01", end_date="2024-07-31")

# Demand forecast
forecast = eptr.call("load-plan", start_date="2024-07-01", end_date="2024-07-31")
```

### Use Composite Functions
```python
from eptr2.composite import (
    get_hourly_consumption_and_forecast_data,
    get_hourly_price_and_cost_data
)

# Comprehensive consumption data
cons_df = get_hourly_consumption_and_forecast_data(
    start_date="2024-07-01", end_date="2024-07-31", eptr=eptr
)

# Comprehensive pricing data
price_df = get_hourly_price_and_cost_data(
    start_date="2024-07-01", end_date="2024-07-31", eptr=eptr
)
```

## Date Handling
- **Format**: Always use `YYYY-MM-DD` (ISO 8601)
- **Examples**: `"2024-07-29"`, `"2024-01-01"`, `"2023-12-31"`
- **Range**: Both `start_date` and `end_date` are inclusive

## Response Format
- Default: pandas DataFrame with columns for date, hour, values
- Alternative: Set `postprocess=False` for raw JSON/dict
- Data is hourly (24 hours per day, hours 0-23)

## Authentication
```python
# Method 1: .env file (recommended)
eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

# Method 2: Direct credentials
eptr = EPTR2(username="email@example.com", password="password", recycle_tgt=True)
```

`.env` file format:
```
EPTR_USERNAME=your.email@example.com
EPTR_PASSWORD=yourpassword
```

## Discovery
```python
# List all 231 available calls
calls = eptr.get_available_calls()

# Include aliases
calls_with_aliases = eptr.get_available_calls(include_aliases=True)

# Rich discovery without a client (no credentials needed)
from eptr2.agentic import list_calls, search_calls, describe_call
describe_call("mcp")        # parameters, method, path, descriptions
search_calls("imbalance")   # keyword search in EN/TR

# View aliases
aliases = eptr.get_aliases()
```

## Common Parameters

### Required (most calls)
- `start_date`: YYYY-MM-DD
- `end_date`: YYYY-MM-DD

### Optional (specific calls)
- `org_id`: Organization ID (integer)
- `pp_id`: Power plant ID (integer)
- `uevcb_id`: Production unit ID (integer)
- `date`: Single date for bulk calls

## Bulk Calls
```python
# Daily production plan for multiple units
dpp = eptr.call("dpp-bulk", date="2024-08-31", uevcb_ids=[123, 456, 789])

# Real-time generation for multiple plants
rtg = eptr.call("rt-gen-bulk", date="2024-08-31", pp_ids=[100, 200, 300])

# UEVCB list for multiple orgs
uevcb = eptr.call("uevcb-list-bulk", date="2024-08-31", org_ids=[10, 20, 30])
```

## Error Handling
```python
try:
    df = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
except Exception as e:
    print(f"API call failed: {e}")
    # Common issues:
    # - Invalid date format
    # - Authentication failure
    # - Invalid call key
    # - Missing required parameters
```

## Data Categories

### Pricing
- MCP/PTF, SMP/SMF, WAP, Imbalance Prices

### Consumption
- Real-time, Forecasts (UECM/Load Plan)

### Generation
- Real-time (by type/plant), Forecasts (UEVM), Plans (DPP/KGUP)

### Market
- Day-ahead trades, Intraday (IDM), Balancing (BPM)

### System
- Ancillary services, Reserves, Frequency

## MCP Server (AI Agents)

### Run Server
```bash
eptr2-mcp-server
```

### Available Tools (via MCP)

17 tools: 6 price/consumption/generation calls, 3 discovery tools
(`get_available_eptr2_calls`, `describe_eptr2_call`, `search_eptr2_calls`),
the generic `call_eptr2_api`, 5 composite/market tools, and 2 pure cost
calculators (`calculate_imbalance_prices_and_costs`,
`calculate_kupst_deviation_cost`). See [AGENTS.md](AGENTS.md) for the full
list, plus the `eptr2://schema` and `eptr2://help/{call_key}` resources.

Print a client config with:
```bash
eptr2 mcp-config --client vscode   # or claude-desktop, claude-code, cursor, generic
```

## Tips for AI Agents

1. **Always use TGT recycling**: `recycle_tgt=True` prevents repeated authentication
2. **Use composite functions** when you need multiple related datasets
3. **Check available calls** first if unsure about endpoint names
4. **Date ranges are inclusive** - both start and end dates are included
5. **Hourly data** - most data is hourly (0-23 hours per day)
6. **Use aliases** - shorter names like `ptf` instead of `mcp` work fine
7. **Bulk calls** - use when querying multiple IDs for same date
8. **Error messages are descriptive** - read them for troubleshooting

## Resources
- Full docs: [README.md](README.md)
- Agent guide: [AGENT_GUIDE.md](AGENT_GUIDE.md)
- MCP docs: [src/eptr2/mcp/README.md](src/eptr2/mcp/README.md)
- API schema: [eptr2_api_schema.json](eptr2_api_schema.json)
