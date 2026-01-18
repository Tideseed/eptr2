# Quick Start

This guide will help you make your first API call with eptr2.

## Prerequisites

1. [Install eptr2](installation.md)
2. [Set up authentication](authentication.md)

## Your First API Call

```python
from eptr2 import EPTR2

# Initialize the client
eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

# Get Market Clearing Price (MCP/PTF)
df = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
print(df)
```

Output:

```
                       date    price
0   2024-07-29T00:00:00+03:00  1234.56
1   2024-07-29T01:00:00+03:00  1198.23
...
23  2024-07-29T23:00:00+03:00  1156.78
```

## Understanding the `call` Method

The `call` method is the primary way to fetch data:

```python
result = eptr.call(
    key,           # API endpoint name (e.g., "mcp", "smp", "rt-consumption")
    start_date,    # Start date in "YYYY-MM-DD" format
    end_date,      # End date in "YYYY-MM-DD" format
    **kwargs       # Additional parameters (varies by endpoint)
)
```

## Common API Calls

### Prices

```python
# Market Clearing Price (MCP/PTF)
mcp = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")

# System Marginal Price (SMP/SMF)
smp = eptr.call("smp", start_date="2024-07-29", end_date="2024-07-29")

# Imbalance Prices
imbalance = eptr.call("imbalance-price", start_date="2024-07-29", end_date="2024-07-29")
```

### Consumption & Generation

```python
# Real-time Consumption
consumption = eptr.call("rt-cons", start_date="2024-07-29", end_date="2024-07-29")

# Real-time Generation by Source
generation = eptr.call("rt-generation", start_date="2024-07-29", end_date="2024-07-29")

# Load Plan (Demand Forecast)
load_plan = eptr.call("load-plan", start_date="2024-07-29", end_date="2024-07-29")
```

### Production Data

```python
# Daily Production Plan (KGÜP)
dpp = eptr.call("dpp", start_date="2024-07-29", end_date="2024-07-29")

# Generation Forecast (UEVM)
uevm = eptr.call("uevm", start_date="2024-07-29", end_date="2024-07-29")
```

## Discovering Available Calls

List all 213+ available API endpoints:

```python
# Get list of all available calls
calls = eptr.get_available_calls()
print(f"Total available calls: {len(calls)}")

# View first 10 calls
for call in calls[:10]:
    print(call)
```

Search for specific calls:

```python
# Find calls related to price
price_calls = [c for c in calls if 'price' in c.lower()]
print(price_calls)
```

## Using Composite Functions

Composite functions combine multiple API calls for common analysis tasks:

```python
from eptr2.composite import (
    get_hourly_consumption_and_forecast_data,
    get_hourly_price_and_cost_data
)

# Get consumption with forecast
consumption_df = get_hourly_consumption_and_forecast_data(
    start_date="2024-07-01",
    end_date="2024-07-31"
)

# Get comprehensive price data
price_df = get_hourly_price_and_cost_data(
    start_date="2024-07-01",
    end_date="2024-07-31"
)
```

## Date Format

Always use ISO format for dates: `YYYY-MM-DD`

```python
# Correct
df = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")

# Also correct - same day queries
df = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")

# Date ranges
df = eptr.call("mcp", start_date="2024-07-01", end_date="2024-07-31")
```

## Return Types

By default, eptr2 returns pandas DataFrames (if pandas is installed):

```python
df = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
print(type(df))  # <class 'pandas.core.frame.DataFrame'>
```

Get raw JSON response:

```python
raw = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29", postprocess=False)
print(type(raw))  # <class 'dict'>
```

## Error Handling

```python
try:
    df = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
except Exception as e:
    print(f"Error: {e}")
```

## Next Steps

- [Explore Basic Usage](../user-guide/basic-usage.md)
- [Learn about Composite Functions](../user-guide/composite-functions.md)
- [Set up AI Integration](../ai-integration/mcp-server.md)
- [Browse API Reference](../api/eptr2.md)
