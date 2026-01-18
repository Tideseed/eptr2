# Working with DataFrames

eptr2 returns pandas DataFrames by default, making it easy to analyze and visualize Turkish electricity market data.

## Basic DataFrame Operations

### Fetching Data

```python
from eptr2 import EPTR2

eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

# Get Market Clearing Price
df = eptr.call("mcp", start_date="2024-07-01", end_date="2024-07-31")
```

### Exploring the Data

```python
# View first rows
print(df.head())

# Check columns
print(df.columns.tolist())

# Data types
print(df.dtypes)

# Summary statistics
print(df.describe())

# Shape
print(f"Rows: {len(df)}, Columns: {len(df.columns)}")
```

## Common Column Names

Different API calls return different columns. Here are common patterns:

### Price Data

| Column | Description |
|--------|-------------|
| `date` | Timestamp |
| `price` | Price in TL/MWh |
| `positiveImbalancePrice` | Positive imbalance price |
| `negativeImbalancePrice` | Negative imbalance price |

### Consumption Data

| Column | Description |
|--------|-------------|
| `date` / `period` | Timestamp |
| `consumption` | Consumption in MWh |
| `swv` | Settlement value (UECM) |
| `lep` | Load plan forecast |

### Generation Data

| Column | Description |
|--------|-------------|
| `date` | Timestamp |
| `total` | Total generation |
| `wind` | Wind generation |
| `solar` | Solar generation |
| `hydro` | Hydro generation |
| `naturalGas` | Natural gas generation |

## Datetime Handling

### Convert to Datetime

```python
# Convert string dates to datetime
df['date'] = pd.to_datetime(df['date'])

# Set as index
df = df.set_index('date')
```

### Extract Components

```python
df['hour'] = df['date'].dt.hour
df['day'] = df['date'].dt.day
df['month'] = df['date'].dt.month
df['weekday'] = df['date'].dt.dayofweek
df['is_weekend'] = df['weekday'].isin([5, 6])
```

### Timezone Handling

eptr2 data uses Turkey timezone (Europe/Istanbul, UTC+3):

```python
import pytz

# Ensure timezone awareness
df['date'] = pd.to_datetime(df['date']).dt.tz_localize('Europe/Istanbul')

# Convert to UTC
df['date_utc'] = df['date'].dt.tz_convert('UTC')
```

## Filtering and Selecting

### By Date Range

```python
# Filter by date
mask = (df['date'] >= '2024-07-15') & (df['date'] <= '2024-07-20')
filtered = df.loc[mask]
```

### By Time

```python
# Peak hours (08:00-20:00)
df['hour'] = df['date'].dt.hour
peak_hours = df[(df['hour'] >= 8) & (df['hour'] < 20)]

# Off-peak hours
off_peak = df[(df['hour'] < 8) | (df['hour'] >= 20)]
```

### By Value

```python
# High price periods
high_price = df[df['price'] > df['price'].quantile(0.9)]

# Specific values
specific = df[df['price'] == 1500.00]
```

## Aggregations

### Daily Aggregations

```python
# Set date index
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')

# Daily statistics
daily = df.resample('D').agg({
    'price': ['mean', 'min', 'max', 'std'],
    'consumption': 'sum'
})
```

### Hourly Patterns

```python
# Average price by hour
hourly_avg = df.groupby(df['date'].dt.hour)['price'].mean()
```

### Monthly Summary

```python
monthly = df.resample('M').agg({
    'price': 'mean',
    'consumption': 'sum'
})
```

## Merging Data

### Merge Price and Consumption

```python
# Get both datasets
mcp = eptr.call("mcp", start_date="2024-07-01", end_date="2024-07-31")
cons = eptr.call("rt-cons", start_date="2024-07-01", end_date="2024-07-31")

# Rename columns for clarity
mcp = mcp.rename(columns={'date': 'datetime', 'price': 'mcp_price'})
cons = cons.rename(columns={'date': 'datetime'})

# Merge on datetime
merged = pd.merge(mcp, cons, on='datetime', how='inner')
```

### Merge Multiple Price Types

```python
mcp = eptr.call("mcp", start_date="2024-07-01", end_date="2024-07-31")
smp = eptr.call("smp", start_date="2024-07-01", end_date="2024-07-31")

mcp = mcp[['date', 'price']].rename(columns={'price': 'mcp'})
smp = smp[['date', 'price']].rename(columns={'price': 'smp'})

prices = pd.merge(mcp, smp, on='date')
prices['spread'] = prices['mcp'] - prices['smp']
```

## Calculations

### Cost Calculation

```python
# Simple cost
df['cost'] = df['consumption'] * df['price']

# Total cost
total_cost = df['cost'].sum()
print(f"Total cost: {total_cost:,.2f} TL")
```

### Rolling Statistics

```python
# 24-hour rolling average
df['price_24h_avg'] = df['price'].rolling(24).mean()

# 7-day rolling average (168 hours)
df['price_7d_avg'] = df['price'].rolling(168).mean()
```

### Percent Change

```python
# Hour-over-hour change
df['price_change'] = df['price'].pct_change()

# Day-over-day change (24 hours)
df['price_daily_change'] = df['price'].pct_change(24)
```

## Visualization

### Basic Plotting

```python
import matplotlib.pyplot as plt

# Price over time
df.plot(x='date', y='price', figsize=(12, 6))
plt.title('Market Clearing Price')
plt.xlabel('Date')
plt.ylabel('Price (TL/MWh)')
plt.show()
```

### Distribution

```python
# Price histogram
df['price'].hist(bins=50, figsize=(10, 6))
plt.title('Price Distribution')
plt.xlabel('Price (TL/MWh)')
plt.ylabel('Frequency')
plt.show()
```

### Hourly Pattern

```python
# Average price by hour
hourly = df.groupby(df['date'].dt.hour)['price'].mean()
hourly.plot(kind='bar', figsize=(12, 6))
plt.title('Average Price by Hour')
plt.xlabel('Hour')
plt.ylabel('Price (TL/MWh)')
plt.show()
```

## Export Options

### To CSV

```python
df.to_csv('electricity_data.csv', index=False)
```

### To Excel

```python
df.to_excel('electricity_data.xlsx', index=False)
```

### To JSON

```python
df.to_json('electricity_data.json', orient='records', date_format='iso')
```

### To Parquet

```python
df.to_parquet('electricity_data.parquet', index=False)
```

## Best Practices

1. **Convert dates early**:
   ```python
   df['date'] = pd.to_datetime(df['date'])
   ```

2. **Use appropriate index**:
   ```python
   df = df.set_index('date').sort_index()
   ```

3. **Handle missing data**:
   ```python
   # Check for missing
   print(df.isnull().sum())
   
   # Fill or drop
   df = df.fillna(method='ffill')  # Forward fill
   ```

4. **Use efficient dtypes**:
   ```python
   # Convert to appropriate types
   df['price'] = df['price'].astype('float32')
   df['hour'] = df['hour'].astype('int8')
   ```

## Next Steps

- [API Reference](../api/eptr2.md)
- [Composite Functions](composite-functions.md)
