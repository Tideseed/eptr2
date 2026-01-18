# EPTR2 Class

The main class for interacting with the EPIAS Transparency Platform API.

## Overview

The `EPTR2` class handles authentication, API calls, and response processing for Turkish electricity market data.

## Basic Usage

```python
from eptr2 import EPTR2

# Using .env file for credentials
eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

# Direct credentials
eptr = EPTR2(username="email@example.com", password="password")

# Make API calls
df = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
```

## Class Reference

::: eptr2.main.EPTR2
    options:
      members:
        - __init__
        - call
        - get_available_calls
        - get_number_of_calls
        - get_aliases
        - get_tgt
        - check_renew_tgt
      show_root_heading: true
      show_source: true
      heading_level: 3

## Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `username` | `str` | `None` | EPIAS platform username (email) |
| `password` | `str` | `None` | EPIAS platform password |
| `recycle_tgt` | `bool` | `True` | Reuse authentication tickets |
| `use_dotenv` | `bool` | `True` | Load credentials from `.env` file |
| `dotenv_path` | `str` | `".env"` | Path to the `.env` file |
| `ssl_verify` | `bool` | `True` | Verify SSL certificates |
| `postprocess` | `bool` | `True` | Return DataFrame instead of raw response |
| `get_raw_response` | `bool` | `False` | Return raw HTTP response |

## The `call` Method

The primary method for making API requests:

```python
result = eptr.call(
    key="mcp",                      # API endpoint key
    start_date="2024-07-29",        # Start date (YYYY-MM-DD)
    end_date="2024-07-29",          # End date (YYYY-MM-DD)
    postprocess=True,               # Return DataFrame
    request_kwargs={"timeout": 10}  # urllib3 request options
)
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `key` | `str` | Yes | API endpoint name or alias |
| `start_date` | `str` | Usually | Start date in YYYY-MM-DD format |
| `end_date` | `str` | Usually | End date in YYYY-MM-DD format |
| `postprocess` | `bool` | No | Return DataFrame (default: True) |
| `request_kwargs` | `dict` | No | Additional request parameters |
| `**kwargs` | - | No | Additional endpoint-specific parameters |

### Returns

- **DataFrame**: When `postprocess=True` (default)
- **dict**: When `postprocess=False`
- **urllib3.HTTPResponse**: When `get_raw_response=True` on EPTR2 instance

## Discovery Methods

### get_available_calls

Returns list of all available API endpoint keys:

```python
calls = eptr.get_available_calls()
print(len(calls))  # 213+
```

### get_number_of_calls

Returns count of available calls:

```python
count = eptr.get_number_of_calls()
print(f"{count} calls available")
```

### get_aliases

Returns dictionary of call aliases:

```python
aliases = eptr.get_aliases()
# {'mcp': 'ptf', 'smp': 'smf', ...}
```

## Authentication Methods

### get_tgt

Manually request a new TGT:

```python
eptr.get_tgt()
```

### check_renew_tgt

Check and renew TGT if expired:

```python
eptr.check_renew_tgt(force_renew_tgt=True)
```

## Examples

### Basic Price Query

```python
from eptr2 import EPTR2

eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

# Market Clearing Price
mcp = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
print(mcp.head())
```

### Multiple Queries

```python
# Reuse instance for multiple queries
eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

mcp = eptr.call("mcp", start_date="2024-07-01", end_date="2024-07-31")
smp = eptr.call("smp", start_date="2024-07-01", end_date="2024-07-31")
consumption = eptr.call("rt-cons", start_date="2024-07-01", end_date="2024-07-31")
```

### With Custom Timeout

```python
df = eptr.call(
    "mcp",
    start_date="2024-07-01",
    end_date="2024-07-31",
    request_kwargs={"timeout": 30}
)
```

### Raw JSON Response

```python
raw = eptr.call(
    "mcp",
    start_date="2024-07-29",
    end_date="2024-07-29",
    postprocess=False
)
print(type(raw))  # dict
```

### With Organization ID

```python
df = eptr.call(
    "bilateral-contracts-org",
    start_date="2024-07-29",
    end_date="2024-07-29",
    org_id=123
)
```

## Error Handling

```python
from eptr2 import EPTR2

eptr = EPTR2(use_dotenv=True)

try:
    df = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
except Exception as e:
    print(f"Error: {e}")
```

## See Also

- [Authentication Guide](../getting-started/authentication.md)
- [Basic Usage Guide](../user-guide/basic-usage.md)
- [Available API Calls](../user-guide/api-calls.md)
