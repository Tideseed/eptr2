# Consumption Data Examples

## Setup

```python
from eptr2 import EPTR2
from eptr2.composite import get_hourly_consumption_and_forecast_data
import pandas as pd

# Initialize client
eptr = EPTR2(use_dotenv=True, recycle_tgt=True)
```

---

## Example 1: Daily Consumption Overview

```python
df = get_hourly_consumption_and_forecast_data(
    eptr,
    start_date="2024-07-15",
    end_date="2024-07-15"
)

print("Daily Consumption Summary:")
print(f"  Total: {df['consumption'].sum():,.0f} MWh")
print(f"  Peak: {df['consumption'].max():,.0f} MWh")
print(f"  Minimum: {df['consumption'].min():,.0f} MWh")
print(f"  Average: {df['consumption'].mean():,.0f} MWh")
```

---

## Example 2: Forecast Accuracy Analysis

```python
df = get_hourly_consumption_and_forecast_data(
    eptr,
    start_date="2024-07-01",
    end_date="2024-07-31"
)

# Calculate errors
df['error'] = df['consumption'] - df['load_plan']
df['abs_error'] = df['error'].abs()
df['pct_error'] = (df['error'] / df['load_plan']) * 100

# Error metrics
mae = df['abs_error'].mean()
mape = df['pct_error'].abs().mean()
rmse = (df['error'] ** 2).mean() ** 0.5

print("Forecast Accuracy Metrics (July 2024):")
print(f"  MAE: {mae:.2f} MWh")
print(f"  MAPE: {mape:.2f}%")
print(f"  RMSE: {rmse:.2f} MWh")
```

---

## Example 3: Peak Hour Analysis

```python
df = get_hourly_consumption_and_forecast_data(
    eptr,
    start_date="2024-07-01",
    end_date="2024-07-31"
)

df['dt'] = pd.to_datetime(df['dt'])
df['hour'] = df['dt'].dt.hour
df['day'] = df['dt'].dt.date

# Daily peak hours
daily_peaks = df.loc[df.groupby('day')['consumption'].idxmax()]
peak_hour_dist = daily_peaks['hour'].value_counts().sort_index()

print("Peak Hour Distribution:")
print(peak_hour_dist)
print(f"\nMost Common Peak Hour: {peak_hour_dist.idxmax()}:00")
```

---

## Example 4: Weekday vs Weekend Consumption

```python
df = get_hourly_consumption_and_forecast_data(
    eptr,
    start_date="2024-07-01",
    end_date="2024-07-31"
)

df['dt'] = pd.to_datetime(df['dt'])
df['day_of_week'] = df['dt'].dt.dayofweek
df['is_weekend'] = df['day_of_week'].isin([5, 6])

# Compare
weekday_avg = df[~df['is_weekend']]['consumption'].mean()
weekend_avg = df[df['is_weekend']]['consumption'].mean()

print(f"Weekday Average: {weekday_avg:,.0f} MWh")
print(f"Weekend Average: {weekend_avg:,.0f} MWh")
print(f"Weekend Reduction: {(1 - weekend_avg/weekday_avg)*100:.1f}%")
```

---

## Example 5: Hourly Load Profile

```python
df = get_hourly_consumption_and_forecast_data(
    eptr,
    start_date="2024-07-01",
    end_date="2024-07-31"
)

df['dt'] = pd.to_datetime(df['dt'])
df['hour'] = df['dt'].dt.hour

# Average hourly profile
hourly_profile = df.groupby('hour')['consumption'].mean()

print("Average Hourly Load Profile:")
for hour, consumption in hourly_profile.items():
    bar = '█' * int(consumption / 1000)
    print(f"{hour:02d}:00 | {bar} {consumption:,.0f} MWh")
```

---

## Example 6: Load Factor Calculation

```python
df = get_hourly_consumption_and_forecast_data(
    eptr,
    start_date="2024-07-01",
    end_date="2024-07-31"
)

# Daily load factors
df['dt'] = pd.to_datetime(df['dt'])
df['day'] = df['dt'].dt.date

daily_stats = df.groupby('day')['consumption'].agg(['mean', 'max'])
daily_stats['load_factor'] = daily_stats['mean'] / daily_stats['max']

print("Load Factor Analysis:")
print(f"  Average Load Factor: {daily_stats['load_factor'].mean():.2%}")
print(f"  Min Load Factor: {daily_stats['load_factor'].min():.2%}")
print(f"  Max Load Factor: {daily_stats['load_factor'].max():.2%}")
```

---

## Example 7: Real-Time vs Settlement Comparison

```python
# Get data for a past period (settlement data available)
df = get_hourly_consumption_and_forecast_data(
    eptr,
    start_date="2024-06-15",
    end_date="2024-06-15"
)

# Compare rt_cons with uecm
if 'uecm' in df.columns and not df['uecm'].isna().all():
    df['rt_uecm_diff'] = df['rt_cons'] - df['uecm']
    
    print("Real-Time vs Settlement (UECM) Comparison:")
    print(f"  Average Difference: {df['rt_uecm_diff'].mean():.2f} MWh")
    print(f"  Max Difference: {df['rt_uecm_diff'].abs().max():.2f} MWh")
else:
    print("UECM data not available for this period")
```

---

## Example 8: Direct API Calls (Without Composite)

```python
# Real-time consumption only
rt_df = eptr.call("rt-cons", start_date="2024-07-15", end_date="2024-07-15")
print("Columns:", rt_df.columns.tolist())

# Load plan only
lp_df = eptr.call("load-plan", start_date="2024-07-15", end_date="2024-07-15")
print("Columns:", lp_df.columns.tolist())

# UECM (settlement) only
uecm_df = eptr.call("uecm", start_date="2024-06-15", end_date="2024-06-15")
print("Columns:", uecm_df.columns.tolist())
```

---

## Example 9: Year-over-Year Comparison

```python
# Get data for same week in two different years
week_2024 = get_hourly_consumption_and_forecast_data(
    eptr, "2024-07-15", "2024-07-21"
)
week_2023 = get_hourly_consumption_and_forecast_data(
    eptr, "2023-07-17", "2023-07-23"  # Equivalent week
)

print("Year-over-Year Comparison (same week):")
print(f"  2024 Average: {week_2024['consumption'].mean():,.0f} MWh")
print(f"  2023 Average: {week_2023['consumption'].mean():,.0f} MWh")
print(f"  YoY Change: {((week_2024['consumption'].mean() / week_2023['consumption'].mean()) - 1) * 100:.1f}%")
```

---

## Example 10: Export for Visualization

```python
df = get_hourly_consumption_and_forecast_data(
    eptr,
    start_date="2024-07-01",
    end_date="2024-07-31"
)

# Prepare for export
df['dt'] = pd.to_datetime(df['dt'])
df['date'] = df['dt'].dt.date
df['hour'] = df['dt'].dt.hour

# Save to CSV
df.to_csv("consumption_july_2024.csv", index=False)
print(f"Exported {len(df)} rows")
```

---

## Example 11: Consumption with Contract Symbols

```python
df = get_hourly_consumption_and_forecast_data(
    eptr,
    start_date="2024-07-15",
    end_date="2024-07-15",
    include_contract_symbol=True
)

# Contract symbols like "PH24071500" for first hour of July 15
print(df[['dt', 'contract', 'consumption']].head())
```
