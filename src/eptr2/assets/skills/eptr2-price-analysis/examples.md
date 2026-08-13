# Price Analysis Examples

## Setup

```python
from eptr2 import EPTR2
import pandas as pd

# Initialize client
eptr = EPTR2(use_dotenv=True, recycle_tgt=True)
```

---

## Example 1: Daily Price Summary

Get a summary of all prices for a single day:

```python
from eptr2.composite import get_hourly_price_and_cost_data

df = get_hourly_price_and_cost_data(
    eptr,
    start_date="2024-07-15",
    end_date="2024-07-15"
)

# Summary statistics
print(f"MCP Range: {df['mcp'].min():.2f} - {df['mcp'].max():.2f} TL/MWh")
print(f"SMP Range: {df['smp'].min():.2f} - {df['smp'].max():.2f} TL/MWh")
print(f"WAP Range: {df['wap'].min():.2f} - {df['wap'].max():.2f} TL/MWh")
print(f"Average MCP: {df['mcp'].mean():.2f} TL/MWh")
```

---

## Example 2: Monthly Price Trends

Analyze price patterns over a month:

```python
df = get_hourly_price_and_cost_data(
    eptr,
    start_date="2024-07-01",
    end_date="2024-07-31"
)

# Convert date column
df['date'] = pd.to_datetime(df['date'])
df['hour'] = df['date'].dt.hour
df['day'] = df['date'].dt.date

# Hourly average pattern
hourly_avg = df.groupby('hour')['mcp'].mean()
print("Peak hours (highest average MCP):")
print(hourly_avg.nlargest(5))
```

---

## Example 3: DAM vs IDM Price Spread

Compare Day-Ahead and Intraday market prices:

```python
df = get_hourly_price_and_cost_data(
    eptr,
    start_date="2024-07-15",
    end_date="2024-07-15",
    include_wap=True
)

# Calculate spread
df['dam_idm_spread'] = df['mcp'] - df['wap']

print("DAM-IDM Spread Analysis:")
print(f"  Average: {df['dam_idm_spread'].mean():.2f} TL/MWh")
print(f"  Max (DAM higher): {df['dam_idm_spread'].max():.2f} TL/MWh")
print(f"  Min (IDM higher): {df['dam_idm_spread'].min():.2f} TL/MWh")
```

---

## Example 4: System Direction Analysis

Analyze system regulation patterns:

```python
df = get_hourly_price_and_cost_data(
    eptr,
    start_date="2024-07-01",
    end_date="2024-07-31"
)

# Count hours by system direction
direction_counts = df['system_direction'].value_counts()
print("System Direction Distribution:")
print(direction_counts)
print(f"\nUp-regulation hours: {(df['sd_sign'] == -1).sum()}")
print(f"Down-regulation hours: {(df['sd_sign'] == 1).sum()}")
print(f"Balanced hours: {(df['sd_sign'] == 0).sum()}")
```

---

## Example 5: Imbalance Cost Exposure

Calculate potential imbalance costs:

```python
df = get_hourly_price_and_cost_data(
    eptr,
    start_date="2024-07-15",
    end_date="2024-07-15"
)

# Example: 10 MWh positive imbalance (surplus) each hour
surplus_mwh = 10
df['surplus_cost'] = df['pos_imb_cost'] * surplus_mwh

# Example: 10 MWh negative imbalance (deficit) each hour
deficit_mwh = 10
df['deficit_cost'] = df['neg_imb_cost'] * deficit_mwh

print(f"Daily surplus cost (10 MWh/h): {df['surplus_cost'].sum():.2f} TL")
print(f"Daily deficit cost (10 MWh/h): {df['deficit_cost'].sum():.2f} TL")
```

---

## Example 6: Peak vs Off-Peak Prices

Analyze peak and off-peak price differences:

```python
df = get_hourly_price_and_cost_data(
    eptr,
    start_date="2024-07-01",
    end_date="2024-07-31"
)

df['date'] = pd.to_datetime(df['date'])
df['hour'] = df['date'].dt.hour

# Define peak hours (08:00-20:00)
df['period'] = df['hour'].apply(
    lambda h: 'Peak' if 8 <= h < 20 else 'Off-Peak'
)

# Compare prices
period_avg = df.groupby('period')['mcp'].agg(['mean', 'min', 'max'])
print("Peak vs Off-Peak MCP:")
print(period_avg)

peak_premium = period_avg.loc['Peak', 'mean'] - period_avg.loc['Off-Peak', 'mean']
print(f"\nPeak Premium: {peak_premium:.2f} TL/MWh")
```

---

## Example 7: MCP-SMP Spread (KUPST Basis)

Analyze the basis for KUPST costs:

```python
df = get_hourly_price_and_cost_data(
    eptr,
    start_date="2024-07-01",
    end_date="2024-07-31"
)

df['mcp_smp_spread'] = abs(df['mcp'] - df['smp'])

print("MCP-SMP Spread Analysis:")
print(f"  Average spread: {df['mcp_smp_spread'].mean():.2f} TL/MWh")
print(f"  Max spread: {df['mcp_smp_spread'].max():.2f} TL/MWh")
print(f"  Hours with spread > 100: {(df['mcp_smp_spread'] > 100).sum()}")
```

---

## Example 8: Raw API Calls (Without Composite)

Direct API calls for specific data:

```python
# Market Clearing Price only
mcp_df = eptr.call("mcp", start_date="2024-07-15", end_date="2024-07-15")

# System Marginal Price only
smp_df = eptr.call("smp", start_date="2024-07-15", end_date="2024-07-15")

# Imbalance prices only
imb_df = eptr.call("imbalance-price", start_date="2024-07-15", end_date="2024-07-15")

# Combined in single call
combined = eptr.call("mcp-smp-imb", start_date="2024-07-15", end_date="2024-07-15")
```

---

## Example 9: Historical Price Comparison

Compare prices across different periods:

```python
# Get data for two different months
july_df = get_hourly_price_and_cost_data(eptr, "2024-07-01", "2024-07-31")
august_df = get_hourly_price_and_cost_data(eptr, "2024-08-01", "2024-08-31")

print("Monthly MCP Comparison:")
print(f"  July Average: {july_df['mcp'].mean():.2f} TL/MWh")
print(f"  August Average: {august_df['mcp'].mean():.2f} TL/MWh")
print(f"  Change: {august_df['mcp'].mean() - july_df['mcp'].mean():.2f} TL/MWh")
```

---

## Example 10: Export to CSV

Save price data for further analysis:

```python
df = get_hourly_price_and_cost_data(
    eptr,
    start_date="2024-07-01",
    end_date="2024-07-31"
)

# Export to CSV
df.to_csv("july_2024_prices.csv", index=False)
print(f"Exported {len(df)} rows to july_2024_prices.csv")
```
