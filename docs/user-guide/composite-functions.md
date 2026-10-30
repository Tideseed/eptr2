# Composite Functions

Composite functions combine multiple API calls to provide ready-to-use data for common analysis tasks. They save time by handling data fetching, merging, and transformation automatically.

## Available Composite Functions

### Consumption and Forecast

```python
from eptr2.composite import get_hourly_consumption_and_forecast_data

df = get_hourly_consumption_and_forecast_data(
    start_date="2024-07-01",
    end_date="2024-07-31"
)
```

Returns a DataFrame with:

| Column | Description |
|--------|-------------|
| `dt` | Datetime |
| `load_plan` | Load plan forecast |
| `uecm` | Settlement consumption (UEÇM) |
| `rt_cons` | Real-time consumption |
| `consumption` | Best available consumption (UECM or RT) |

### Price and Cost Data

```python
from eptr2.composite import get_hourly_price_and_cost_data

df = get_hourly_price_and_cost_data(
    start_date="2024-07-01",
    end_date="2024-07-31"
)
```

Returns comprehensive price data including MCP, SMP, and imbalance prices.

### Production Data

```python
from eptr2.composite import get_hourly_production_data

df = get_hourly_production_data(
    start_date="2024-07-01",
    end_date="2024-07-31"
)
```

### Production Plan Data

```python
from eptr2.composite import get_hourly_production_plan_data

df = get_hourly_production_plan_data(
    start_date="2024-07-01",
    end_date="2024-07-31"
)
```

### Imbalance Data

```python
from eptr2.composite import get_imbalance_data

df = get_imbalance_data(
    start_date="2024-07-01",
    end_date="2024-07-31"
)
```

## Using with Custom EPTR2 Instance

All composite functions accept an optional `eptr` parameter:

```python
from eptr2 import EPTR2
from eptr2.composite import get_hourly_consumption_and_forecast_data

# Create your own EPTR2 instance
eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

# Pass it to the composite function
df = get_hourly_consumption_and_forecast_data(
    start_date="2024-07-01",
    end_date="2024-07-31",
    eptr=eptr
)
```

## Verbose Mode

Enable verbose mode to see progress:

```python
df = get_hourly_consumption_and_forecast_data(
    start_date="2024-07-01",
    end_date="2024-07-31",
    verbose=True
)
```

Output:
```
Loading load plan...
Loading UECM...
Loading real time consumption...
```

## Including Contract Symbols

Add contract symbols for easier identification:

```python
df = get_hourly_consumption_and_forecast_data(
    start_date="2024-07-01",
    end_date="2024-07-31",
    include_contract_symbol=True
)
```

## Example: Complete Analysis

Combine consumption and price data for cost analysis:

```python
from eptr2 import EPTR2
from eptr2.composite import (
    get_hourly_consumption_and_forecast_data,
    get_hourly_price_and_cost_data
)
import pandas as pd

# Initialize
eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

# Get consumption data
consumption_df = get_hourly_consumption_and_forecast_data(
    start_date="2024-07-01",
    end_date="2024-07-31",
    eptr=eptr
)

# Get price data
price_df = get_hourly_price_and_cost_data(
    start_date="2024-07-01",
    end_date="2024-07-31",
    eptr=eptr
)

# Merge for analysis
analysis = pd.merge(
    consumption_df,
    price_df,
    on=['dt'],
    how='inner'
)

# Calculate total cost
analysis['total_cost'] = analysis['consumption'] * analysis['mcp']
print(f"Total cost: {analysis['total_cost'].sum():,.2f} TL")
```

## Plant Cost Analysis

```python
from eptr2.composite import calculate_plant_costs

costs = calculate_plant_costs(
    start_date="2024-07-01",
    end_date="2024-07-31",
    pp_id=123,  # Power plant ID
    eptr=eptr
)
```

## IDM (Intraday Market) Log

```python
from eptr2.composite import idm_log_longer

idm_log = idm_log_longer(
    start_date="2024-07-29",
    end_date="2024-07-29",
    eptr=eptr
)
```

`quantity` in the log is in lots (1 lot = 0.1 MWh).

## Organization Estimated Activity

Estimates a company's hourly trading activity from its own matched quantities
only: GÖP, İA and GİP matchings by organization id (`get_dabi_idm_data`, about a
second per week):

```python
from eptr2.composite import get_org_estimated_activity

df = get_org_estimated_activity(
    start_date="2026-10-01",
    end_date="2026-10-07",
    org_id=104000,
    eptr=eptr,
    include_pnl=True,   # + MCP, published WAP and da_id_pnl (fast)
    verbose=True,       # progress with timings on stderr
)
```

`include_day_trade_pnl=True` also adds `idm_tad` and `day_trade_pnl`. TAD needs
the market-wide intraday trade log, fetched day by day, which takes a few
seconds per day (30–50 s for a week).

| Column | Meaning |
|--------|---------|
| `da_id_close` | Day-ahead position reversed in the intraday market: `min(abs(da_net), abs(idm_net))` when they have opposite signs |
| `day_trade` | `min(idm_long, idm_short)`, bought and sold back within the intraday market |
| `dabi_net` | `da_net + bi_net`: day-ahead (GÖP + İA) net position |
| `dabi_idm_net` | `dabi_net + idm_net`; positive must be consumed, negative generated (subtract `bi_net` for GÖP + GİP only) |
| `mcp`, `idm_wap` | With `include_pnl=True`: MCP and the published intraday WAP |
| `idm_tad` | With `include_day_trade_pnl=True`: TAD (quantity-weighted mean of `abs(price - WAP)`) from the trade log |
| `da_id_pnl` | `da_id_close * sign(da_net) * (idm_wap - mcp)` |
| `day_trade_pnl` | `day_trade * idm_tad` (with `include_day_trade_pnl=True`) |
| `total_pnl` | Sum of the PnL columns present |

The PnL is fictitious: the company's own trade prices are not public. To
analyse several companies with day-trade PnL, fetch the log once with
`idm_log_longer` and pass it as `idm_log_df`.

## MMS (Market Management System) Data

```python
from eptr2.composite import get_mms_data

mms = get_mms_data(
    start_date="2024-07-29",
    end_date="2024-07-29",
    eptr=eptr
)
```

## BPM (Balancing Power Market) Data

```python
from eptr2.composite import get_bpm_data

bpm = get_bpm_data(
    start_date="2024-07-29",
    end_date="2024-07-29",
    eptr=eptr
)
```

## Organization Periodic Data

```python
from eptr2.composite import get_periodic_org_data

org_data = get_periodic_org_data(
    start_date="2024-07-01",
    end_date="2024-07-31",
    org_id=123,
    eptr=eptr
)
```

## Function Signatures

All composite functions share a similar signature:

```python
def composite_function(
    start_date: str,           # YYYY-MM-DD format
    end_date: str,             # YYYY-MM-DD format
    eptr: EPTR2 | None = None, # Optional EPTR2 instance
    verbose: bool = False,     # Print progress
    **kwargs                   # Additional parameters
) -> pd.DataFrame:
    ...
```

## Best Practices

1. **Reuse EPTR2 instance** - Pass the same instance to multiple composite calls:
   ```python
   eptr = EPTR2(use_dotenv=True, recycle_tgt=True)
   df1 = get_hourly_consumption_and_forecast_data(..., eptr=eptr)
   df2 = get_hourly_price_and_cost_data(..., eptr=eptr)
   ```

2. **Use reasonable date ranges** - Large date ranges may be slow:
   ```python
   # Good: 1 month
   df = get_hourly_consumption_and_forecast_data(
       start_date="2024-07-01", end_date="2024-07-31", ...
   )
   
   # May be slow: 1 year
   df = get_hourly_consumption_and_forecast_data(
       start_date="2024-01-01", end_date="2024-12-31", ...
   )
   ```

3. **Enable verbose for debugging** - See what's being loaded:
   ```python
   df = get_hourly_consumption_and_forecast_data(..., verbose=True)
   ```

## Next Steps

- [Working with DataFrames](dataframes.md)
- [API Reference - Composite](../api/composite.md)
