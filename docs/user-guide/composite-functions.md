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
from eptr2.composite import get_idm_log_data

idm_log = get_idm_log_data(
    start_date="2024-07-29",
    end_date="2024-07-29",
    eptr=eptr
)
```

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
