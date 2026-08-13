# EPTR2 for AI Agents

This document is the canonical quick reference for AI agents and assistants working with the eptr2 library. It is provider-agnostic: everything here works with any agent runtime (MCP clients, shell-driven agents, SKILL.md-compatible assistants).

eptr2 is a Python client for Turkish electricity and natural gas market data from the EPIAS Transparency Platform v2.0, with 231 API endpoints.

## Installation

```bash
# Recommended: all extras (pandas, MCP server support)
pip install "eptr2[allextras]"

# Basic installation (minimal dependencies)
pip install eptr2
```

## Authentication

Register at https://kayit.epias.com.tr/epias-transparency-platform-registration-form to get credentials.

1. **Environment variables** (recommended): set `EPTR_USERNAME` and `EPTR_PASSWORD` in a `.env` file, then `EPTR2(use_dotenv=True, recycle_tgt=True)`
2. **Direct credentials**: `EPTR2(username="email@example.com", password="password")`

## Basic Usage Pattern

```python
from eptr2 import EPTR2

eptr = EPTR2(use_dotenv=True, recycle_tgt=True)
result = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
```

## Command-Line Interface

The `eptr2` CLI is designed for shell-driven agents: data goes to stdout, diagnostics to stderr, nonzero exit codes on error.

```bash
eptr2 list                          # All 231 call keys, grouped by category
eptr2 list --category GÖP           # One category
eptr2 categories                    # Categories with endpoint counts
eptr2 search imbalance              # Keyword search (English and Turkish)
eptr2 describe mcp                  # Parameters, method, path for one call
eptr2 call mcp --start-date 2024-07-29 --end-date 2024-07-29
eptr2 call mcp ... --format csv --output prices.csv
eptr2 call some-key -p org_id=123   # Extra parameters
eptr2 schema                        # (Re)generate the machine-readable API schema
eptr2 install-skills                # Install bundled agent skills
eptr2 mcp-config --client vscode    # Print MCP client config snippet
eptr2 mcp-server                    # Run the MCP server (stdio)
```

Discovery commands need no credentials; only `call` and `mcp-server` do.

## Agent Skills

eptr2 bundles 7 agent skills in the open Agent Skills format (a directory with a `SKILL.md` file). Any SKILL.md-compatible runtime can consume them. They ship inside the pip package and install with:

```bash
eptr2 install-skills                 # into ./.claude/skills (project)
eptr2 install-skills --dest user     # into ~/.claude/skills
eptr2 install-skills --dest PATH     # anywhere your runtime looks for skills
```

| Skill | Triggers On |
|-------|------------|
| **eptr2-price-analysis** | Electricity prices, MCP, PTF, SMP, WAP |
| **eptr2-consumption-data** | Consumption, demand forecast, UECM, load plan |
| **eptr2-generation-tracking** | Generation, UEVM, power plants, renewables |
| **eptr2-imbalance-costs** | Imbalance, KUPST, deviation costs, penalties |
| **eptr2-market-operations** | DAM, IDM, GÖP, GİP, bilateral contracts |
| **eptr2-api-discovery** | Available endpoints, API search, discovery |
| **eptr2-convenience-wrappers** | get_* functions, typed wrappers, eptr2.calls |

## Machine-Readable API Schema

`eptr2_api_schema.json` (repo root; also shipped in the package under `eptr2/assets/`) describes all 231 endpoints — categories, bilingual titles/descriptions, HTTP method, path, required and optional parameters — plus composite functions and cost utilities. It is generated from the library's own metadata with `eptr2 schema`, so it never drifts from the code.

```python
from eptr2.agentic import build_schema, list_calls, search_calls, describe_call
```

## Most Common API Calls

### Prices
- `mcp` or `ptf`: Market Clearing Price (day-ahead market price)
- `smp` or `smf`: System Marginal Price
- `mcp-smp-imb`: Imbalance prices (positive and negative)

### Consumption & Generation
- `rt-cons`: Real-time electricity consumption
- `rt-gen`: Real-time generation by resource type
- `load-plan`: Demand forecast (load plan)

### Market Data
- `dpp` or `kgup`: Daily production plan
- `uevm`: Settlement-based actual generation (Uzlaştırmaya Esas Veriş Miktarı)
- `pp-list`: Power plant list (for plant-level calls)

## Composite Functions

These combine multiple API calls for convenience:

```python
from eptr2.composite import (
    get_hourly_consumption_and_forecast_data,
    get_hourly_price_and_cost_data,
    get_dabi_idm_data,     # DAM + bilateral + intraday volumes
    get_bpm_range,         # Balancing market (YAL/YAT + SMP)
    get_dpp_bulk_range,    # Bulk per-plant production plans
)

df = get_hourly_consumption_and_forecast_data(
    start_date="2024-07-29",
    end_date="2024-07-29",
    eptr=eptr,
)
```

Note: composite functions take `start_date`/`end_date` first and the client as the `eptr` keyword argument.

## Date Format

Always use ISO format: `YYYY-MM-DD` (e.g., "2024-07-29"). The market timezone is Europe/Istanbul.

## Return Format

- By default returns pandas DataFrame (if pandas installed)
- Can return raw JSON with `postprocess=False`

## Discovery

```python
# In Python
from eptr2.agentic import list_calls, search_calls, describe_call
describe_call("mcp")          # parameters, method, path, descriptions
search_calls("imbalance")     # keyword search in EN/TR

# Or via the client
eptr.get_available_calls()    # list all callable keys
eptr.get_aliases()            # e.g. ptf -> mcp
```

The `get_help_d` function provides raw bilingual metadata for each endpoint (`"tr"` and `"en"` keys):

```python
from eptr2.mapping.help import get_help_d
help_info = get_help_d("mcp")   # category, title, desc, url
```

## Common Parameters

Most calls accept:
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)
- Some require specific IDs:
  - `org_id`: Organization ID
  - `pp_id`: Power plant ID
  - `uevcb_id`: Production unit ID

Use `eptr2 describe <key>` (or `describe_call`) to see exactly which parameters a call needs.

## MCP Server

For agents using the Model Context Protocol:

```bash
eptr2-mcp-server        # or: eptr2 mcp-server, or: python -m eptr2.mcp.server
```

Print a ready-to-paste client configuration:

```bash
eptr2 mcp-config --client vscode         # .vscode/mcp.json shape
eptr2 mcp-config --client claude-desktop
eptr2 mcp-config --client cursor
eptr2 mcp-config                          # generic mcpServers shape
```

### Available MCP Tools (17)

Discovery (no credentials needed):
1. `get_available_eptr2_calls` - List all endpoints
2. `describe_eptr2_call` - Parameters and metadata for one call key
3. `search_eptr2_calls` - Keyword search over endpoints

Data (credentials required):
4. `get_market_clearing_price` - Day-ahead market prices (MCP/PTF)
5. `get_system_marginal_price` - System marginal prices (SMP/SMF)
6. `get_real_time_consumption` - Real-time consumption
7. `get_real_time_generation` - Generation by resource type
8. `get_demand_forecast` - Demand forecasts (load plan)
9. `get_imbalance_price` - Imbalance pricing
10. `call_eptr2_api` - Generic call to any endpoint
11. `get_hourly_consumption_and_forecast` - Composite consumption data
12. `get_price_and_cost_data` - Composite pricing data
13. `get_market_operations_summary` - DAM + bilateral + intraday volumes
14. `get_balancing_market_data` - Balancing market (YAL/YAT + SMP)
15. `get_bulk_production_plans` - Bulk per-plant production plans (dpp/kgup)

Calculations (pure, no credentials needed):
16. `calculate_imbalance_prices_and_costs` - Unit imbalance prices/costs per hour
17. `calculate_kupst_deviation_cost` - Production plan deviation (KUPST) cost

Plus resources `eptr2://schema` and `eptr2://help/{call_key}`.

## Error Handling

```python
try:
    result = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
except Exception as e:
    print(f"Error: {e}")
```

## Key Features

- 231 API endpoints for Turkish electricity and natural gas markets
- Automatic TGT (Ticket Granting Ticket) management
- Credential management via .env files
- Composite functions for common data analysis
- Imbalance/KUPST cost utilities (`eptr2.util.costs`)
- Pandas DataFrame integration
- CLI, MCP server, agent skills and machine-readable schema for AI agents

## Resources

- Main README: `/README.md`
- Documentation: https://tideseed.github.io/eptr2/
- Package: https://pypi.org/project/eptr2/
- Demo: https://eptr2demo.streamlit.app/
- EPIAS Platform: https://seffaflik.epias.com.tr/

## Common Abbreviations

Since eptr2 is about the Turkish electricity market, many terms are abbreviated in Turkish:

- MCP: Market Clearing Price (Piyasa Takas Fiyatı, PTF)
- SMP: System Marginal Price (Sistem Marjinal Fiyatı, SMF)
- KGÜP: Daily Production Plan (Kesinleşmiş Günlük Üretim Planı)
- UEÇM: Settlement Actual Demand (Uzlaştırmaya Esas Çekiş Miktarı)
- UEVM: Settlement Actual Generation (Uzlaştırmaya Esas Veriş Miktarı)
- KÜPST: Deviation Cost from Production Plan (Kesinleşmiş Üretim Planından Sapma Tutarı)
- KUDÜP: Settlement Production Plan (Kesinleşmiş Uzlaştırma Dönemi Üretim Planı)
- AOF: Weighted Average Price (Ağırlıklı Ortalama Fiyat)
- GİP: Intraday Market (Gün İçi Piyasası)
- GÖP: Day-Ahead Market (Gün Öncesi Piyasası)
- DGP: Balancing Power Market (Dengeleme Güç Piyasası)
- İA: Bilateral Agreements (İkili Anlaşmalar)
- YAL: Up regulation (Yük Alma)
- YAT: Down regulation (Yük Atma)
