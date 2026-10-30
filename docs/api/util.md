# Utilities

The `eptr2.util` module provides utility functions for common operations.

## Time Utilities

### eptr2.util.time

Utility functions for time and date handling.

```python
from eptr2.util.time import iso_to_contract
```

#### iso_to_contract

Converts ISO datetime to contract symbol format.

```python
from eptr2.util.time import iso_to_contract

contract = iso_to_contract("2024-07-29T10:00:00+03:00")
print(contract)  # e.g., "PH24072910"
```

## Cost Utilities

### eptr2.util.costs

Imbalance and KÜPST (production plan deviation) prices and costs. Start with
the two main functions: they resolve every regulation parameter (floor and
ceiling prices, V, B, margins, KÜPST tolerance and multiplier by category) for
each hour from its delivery date, so a range spanning regulation changes is
priced hour by hour. EPİAŞ's published imbalance prices are used where
available; they are calculated only for hours without them. Hours without SMP
(such as the rest of the current day) are skipped with a warning.

```python
from eptr2.util.costs import calculate_imbalance_prices, calculate_imbalance_costs

## Hourly prices, unit costs and every parameter used (fetches mcp-smp-imb)
prices_df = calculate_imbalance_prices("2026-10-01", "2026-10-07", eptr=eptr)

## Imbalance and KÜPST costs of actual vs forecast rows
costs_df = calculate_imbalance_costs(
    data=[
        {"date": "2026-11-01T10:00:00+03:00", "actual": 80, "forecast": 100},
        {"date": "2026-11-01T11:00:00+03:00", "actual": 95, "forecast": 90},
    ],
    category="Rüzgar",  # any naming convention, see normalize_kupst_category
    eptr=eptr,
)

## Offline or scenario prices: pass them instead of fetching
calculate_imbalance_prices(
    prices=[{"date": "2026-11-01T00:00:00+03:00", "mcp": 120, "smp": 130,
             "system_direction": -1}],
    kupst_category="wind",
)
```

The dated regulation table is `get_time_regulation_params_map()`; each row
names its period (`26_01` from 2026-01-01, `26_02` from 2026-11-01).

::: eptr2.util.costs.calculate_imbalance_prices
    options:
      show_root_heading: true
      show_source: false
      heading_level: 4

::: eptr2.util.costs.calculate_imbalance_costs
    options:
      show_root_heading: true
      show_source: false
      heading_level: 4

::: eptr2.util.costs.normalize_kupst_category
    options:
      show_root_heading: true
      show_source: false
      heading_level: 4

::: eptr2.util.costs.get_regulation_params
    options:
      show_root_heading: true
      show_source: false
      heading_level: 4

## Mapping Utilities

### eptr2.mapping

Utilities for API endpoint mapping and discovery.

```python
from eptr2.mapping import (
    get_path_map,
    alias_to_path,
    get_alias_map,
)
```

#### get_path_map

Returns the complete mapping of API endpoint paths.

```python
from eptr2.mapping import get_path_map

# Get all path keys
paths = get_path_map(just_call_keys=True)
print(len(paths))  # 234
```

#### alias_to_path

Converts an alias to its canonical path.

```python
from eptr2.mapping import alias_to_path

path = alias_to_path("ptf")
print(path)  # "mcp"
```

#### get_alias_map

Returns dictionary of all aliases.

```python
from eptr2.mapping import get_alias_map

aliases = get_alias_map()
# {'ptf': 'mcp', 'smf': 'smp', ...}
```

### eptr2.mapping.help

Help and documentation utilities.

```python
from eptr2.mapping.help import get_help_d
```

#### get_help_d

Get documentation for an API endpoint.

```python
from eptr2.mapping.help import get_help_d

# Get help for specific call
help_info = get_help_d("mcp")
print(help_info['category'])     # "GÖP"
print(help_info['title']['en'])  # "Market Clearing Price"
print(help_info['desc']['en'])   # Description
print(help_info['url'])          # Official docs URL

# Get all help entries
all_help = get_help_d()
```

**Returns:**

| Key | Type | Description |
|-----|------|-------------|
| `category` | `str` | Market category (GÖP, GİP, etc.) |
| `title` | `dict` | Titles in `tr` and `en` |
| `desc` | `dict` | Descriptions in `tr` and `en` |
| `url` | `str` | Link to official documentation |

## Processing Utilities

### eptr2.processing.preprocess

Preprocessing utilities for API parameters.

```python
from eptr2.processing.preprocess import preprocess_parameter
```

These utilities are primarily used internally by the EPTR2 class.

## Examples

### Finding API Endpoints

```python
from eptr2.mapping import get_path_map, alias_to_path

# List all endpoints
all_endpoints = get_path_map(just_call_keys=True)

# Find price-related endpoints
price_endpoints = [e for e in all_endpoints if 'price' in e.lower()]
print(price_endpoints)

# Check if alias exists
canonical = alias_to_path("ptf")
print(f"'ptf' maps to '{canonical}'")
```

### Getting API Documentation

```python
from eptr2.mapping.help import get_help_d

# Get documentation for consumption endpoint
help_info = get_help_d("rt-consumption")

print(f"Category: {help_info['category']}")
print(f"Title (TR): {help_info['title']['tr']}")
print(f"Title (EN): {help_info['title']['en']}")
print(f"Description: {help_info['desc']['en']}")
```

### Working with Contract Symbols

```python
from eptr2.util.time import iso_to_contract

# Convert timestamps to contract symbols
timestamps = [
    "2024-07-29T00:00:00+03:00",
    "2024-07-29T12:00:00+03:00",
    "2024-07-29T23:00:00+03:00",
]

for ts in timestamps:
    contract = iso_to_contract(ts)
    print(f"{ts} -> {contract}")
```

## See Also

- [EPTR2 Class Reference](main.md)
- [Available API Calls](../user-guide/api-calls.md)
