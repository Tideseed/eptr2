# Basic Usage

This guide covers the fundamental patterns for using eptr2.

## The EPTR2 Class

The `EPTR2` class is your main interface to the EPIAS Transparency Platform:

```python
from eptr2 import EPTR2

eptr = EPTR2(
    use_dotenv=True,      # Load credentials from .env
    recycle_tgt=True,     # Reuse authentication tickets
    dotenv_path=".env",   # Path to .env file
)
```

## Making API Calls

### The `call` Method

The primary method for fetching data:

```python
result = eptr.call(
    key="mcp",                    # API endpoint name
    start_date="2024-07-29",      # Start date (YYYY-MM-DD)
    end_date="2024-07-29",        # End date (YYYY-MM-DD)
    postprocess=True,             # Return DataFrame (default)
    request_kwargs={"timeout": 10} # Optional request settings
)
```

### Call Aliases

Many endpoints have multiple names (aliases):

```python
# These are equivalent
df1 = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
df2 = eptr.call("ptf", start_date="2024-07-29", end_date="2024-07-29")

# SMP/SMF aliases
df3 = eptr.call("smp", start_date="2024-07-29", end_date="2024-07-29")
df4 = eptr.call("smf", start_date="2024-07-29", end_date="2024-07-29")
```

### View Available Aliases

```python
aliases = eptr.get_aliases()
print(aliases)
```

## Discovery Methods

### List All Available Calls

```python
# Get all available API call keys
all_calls = eptr.get_available_calls()
print(f"Total: {len(all_calls)} calls available")

# Print first 20
for call in all_calls[:20]:
    print(f"  - {call}")
```

### Get Call Count

```python
count = eptr.get_number_of_calls()
print(f"Number of available calls: {count}")
```

### Get Help for a Call

```python
from eptr2.mapping.help import get_help_d

# Get help for MCP endpoint
help_info = get_help_d("mcp")
print(f"Category: {help_info['category']}")
print(f"Title (EN): {help_info['title']['en']}")
print(f"Description: {help_info['desc']['en']}")
```

## Parameters by Endpoint

Different endpoints require different parameters:

### Date-Based Endpoints

Most endpoints just need dates:

```python
# Market prices
df = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")

# Consumption data
df = eptr.call("rt-cons", start_date="2024-07-29", end_date="2024-07-29")
```

### Organization-Based Endpoints

Some endpoints require organization IDs:

```python
# Get organization list first
orgs = eptr.call("organizations")

# Then query for specific organization
df = eptr.call(
    "bilateral-contracts-org",
    start_date="2024-07-29",
    end_date="2024-07-29",
    org_id=123  # Organization ID
)
```

### Power Plant-Based Endpoints

For plant-level data:

```python
# Get power plant list
plants = eptr.call("dpp-pp-list")

# Query for specific plant
df = eptr.call(
    "rt-gen",
    start_date="2024-07-29",
    end_date="2024-07-29",
    pp_id=456  # Power plant ID
)
```

## Response Handling

### DataFrame Output (Default)

```python
df = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")

# Standard pandas operations
print(df.head())
print(df.describe())
print(df.columns)
```

### Raw JSON Output

```python
raw = eptr.call(
    "mcp",
    start_date="2024-07-29",
    end_date="2024-07-29",
    postprocess=False
)
print(type(raw))  # dict
print(raw.keys())
```

### Raw HTTP Response

```python
eptr_raw = EPTR2(use_dotenv=True, get_raw_response=True)
response = eptr_raw.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
print(response.status)
print(response.data)
```

## Request Configuration

### Timeout Settings

```python
df = eptr.call(
    "mcp",
    start_date="2024-07-29",
    end_date="2024-07-29",
    request_kwargs={"timeout": 30}  # 30 second timeout
)
```

### SSL Verification

```python
# Disable SSL verification (not recommended for production)
eptr = EPTR2(use_dotenv=True, ssl_verify=False)
```

## Working with Date Ranges

### Single Day

```python
df = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
```

### Date Range

```python
df = eptr.call("mcp", start_date="2024-07-01", end_date="2024-07-31")
```

### Using Python Dates

```python
from datetime import datetime, timedelta

today = datetime.now()
yesterday = today - timedelta(days=1)

df = eptr.call(
    "mcp",
    start_date=yesterday.strftime("%Y-%m-%d"),
    end_date=yesterday.strftime("%Y-%m-%d")
)
```

## Error Handling

```python
from eptr2 import EPTR2

eptr = EPTR2(use_dotenv=True)

try:
    df = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
except Exception as e:
    print(f"API Error: {e}")
```

## Best Practices

1. **Use TGT recycling** - Reduces authentication overhead:
   ```python
   eptr = EPTR2(use_dotenv=True, recycle_tgt=True)
   ```

2. **Set appropriate timeouts** - Avoid hanging requests:
   ```python
   df = eptr.call("mcp", ..., request_kwargs={"timeout": 10})
   ```

3. **Handle empty responses** - Check DataFrame before processing:
   ```python
   df = eptr.call("mcp", ...)
   if df.empty:
       print("No data returned")
   ```

4. **Reuse EPTR2 instance** - Create once, use multiple times:
   ```python
   eptr = EPTR2(use_dotenv=True, recycle_tgt=True)
   
   # Multiple calls with same instance
   mcp = eptr.call("mcp", ...)
   smp = eptr.call("smp", ...)
   consumption = eptr.call("rt-cons", ...)
   ```

## Next Steps

- [Available API Calls](api-calls.md)
- [Composite Functions](composite-functions.md)
- [Working with DataFrames](dataframes.md)
