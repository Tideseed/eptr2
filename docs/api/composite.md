# Composite Functions

The `eptr2.composite` module provides pre-built functions that combine multiple API calls for common analysis tasks.

## Overview

Composite functions simplify data retrieval by:

- Combining multiple related API calls
- Merging and transforming data
- Handling missing data gracefully
- Providing consistent output formats

## Import

```python
from eptr2.composite import (
    get_hourly_consumption_and_forecast_data,
    get_hourly_price_and_cost_data,
    get_hourly_production_data,
    get_hourly_production_plan_data,
    get_imbalance_data,
)
```

## Function Reference

### Consumption Functions

::: eptr2.composite.consumption.get_hourly_consumption_and_forecast_data
    options:
      show_root_heading: true
      show_source: true
      heading_level: 4

### Price Functions

::: eptr2.composite.price_and_cost.get_hourly_price_and_cost_data
    options:
      show_root_heading: true
      show_source: true
      heading_level: 4

### Production Functions

::: eptr2.composite.production.get_hourly_production_data
    options:
      show_root_heading: true
      show_source: true
      heading_level: 4

## Quick Reference

### get_hourly_consumption_and_forecast_data

Combines load plan, UECM, and real-time consumption data.

```python
from eptr2.composite import get_hourly_consumption_and_forecast_data

df = get_hourly_consumption_and_forecast_data(
    start_date="2024-07-01",
    end_date="2024-07-31",
    verbose=True
)
```

**Returns:**

| Column | Type | Description |
|--------|------|-------------|
| `dt` | datetime | Timestamp |
| `load_plan` | float | Load plan forecast (MWh) |
| `uecm` | float | Settlement consumption (MWh) |
| `rt_cons` | float | Real-time consumption (MWh) |
| `consumption` | float | Best available consumption |

### get_hourly_price_and_cost_data

Combines MCP, SMP, and imbalance price data.

```python
from eptr2.composite import get_hourly_price_and_cost_data

df = get_hourly_price_and_cost_data(
    start_date="2024-07-01",
    end_date="2024-07-31"
)
```

**Returns:**

| Column | Type | Description |
|--------|------|-------------|
| `dt` | datetime | Timestamp |
| `mcp` | float | Market Clearing Price (TL/MWh) |
| `smp` | float | System Marginal Price (TL/MWh) |
| `positive_imbalance` | float | Positive imbalance price |
| `negative_imbalance` | float | Negative imbalance price |

### get_hourly_production_data

Retrieves hourly production data by source.

```python
from eptr2.composite import get_hourly_production_data

df = get_hourly_production_data(
    start_date="2024-07-01",
    end_date="2024-07-31"
)
```

### get_imbalance_data

Retrieves imbalance-related data for cost calculations.

```python
from eptr2.composite import get_imbalance_data

df = get_imbalance_data(
    start_date="2024-07-01",
    end_date="2024-07-31"
)
```

## Common Parameters

All composite functions share these parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `start_date` | `str` | Required | Start date (YYYY-MM-DD) |
| `end_date` | `str` | Required | End date (YYYY-MM-DD) |
| `eptr` | `EPTR2` | `None` | EPTR2 instance (created if not provided) |
| `verbose` | `bool` | `False` | Print progress messages |
| `**kwargs` | - | - | Additional parameters |

## Examples

### Complete Analysis Pipeline

```python
from eptr2 import EPTR2
from eptr2.composite import (
    get_hourly_consumption_and_forecast_data,
    get_hourly_price_and_cost_data
)
import pandas as pd

# Initialize once
eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

# Get consumption data
consumption = get_hourly_consumption_and_forecast_data(
    start_date="2024-07-01",
    end_date="2024-07-31",
    eptr=eptr,
    verbose=True
)

# Get price data
prices = get_hourly_price_and_cost_data(
    start_date="2024-07-01",
    end_date="2024-07-31",
    eptr=eptr
)

# Merge for analysis
analysis = pd.merge(consumption, prices, on='dt')

# Calculate costs
analysis['total_cost'] = analysis['consumption'] * analysis['mcp']
print(f"Total cost: {analysis['total_cost'].sum():,.2f} TL")
```

### With Verbose Output

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

### Using Custom EPTR2 Instance

```python
from eptr2 import EPTR2
from eptr2.composite import get_hourly_consumption_and_forecast_data

# Custom configuration
eptr = EPTR2(
    use_dotenv=True,
    recycle_tgt=True,
    tgt_path="/custom/path"
)

df = get_hourly_consumption_and_forecast_data(
    start_date="2024-07-01",
    end_date="2024-07-31",
    eptr=eptr
)
```

## See Also

- [Composite Functions Guide](../user-guide/composite-functions.md)
- [Working with DataFrames](../user-guide/dataframes.md)
