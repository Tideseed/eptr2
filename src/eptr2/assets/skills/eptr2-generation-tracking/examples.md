# Generation Tracking Examples

## Setup

```python
from eptr2 import EPTR2
from eptr2.composite import get_hourly_production_data, get_hourly_production_plan_data
import pandas as pd

# Initialize client
eptr = EPTR2(use_dotenv=True, recycle_tgt=True)
```

---

## Example 1: Daily Generation Overview

```python
rt_gen = eptr.call("rt-generation", start_date="2024-07-15", end_date="2024-07-15")

# Calculate totals
numeric_cols = rt_gen.select_dtypes(include='number').columns
totals = rt_gen[numeric_cols].sum()

print("Daily Generation by Source (July 15, 2024):")
for col, val in totals.items():
    if val > 0:
        print(f"  {col}: {val:,.0f} MWh")
```

---

## Example 2: Hourly Generation Profile by Fuel Type

```python
rt_gen = eptr.call("rt-generation", start_date="2024-07-15", end_date="2024-07-15")

rt_gen['date'] = pd.to_datetime(rt_gen['date'])
rt_gen['hour'] = rt_gen['date'].dt.hour

# Solar profile (peaks at midday)
solar_profile = rt_gen.groupby('hour')['sun'].mean()
print("Hourly Solar Profile:")
for hour, gen in solar_profile.items():
    bar = '█' * int(gen / 500)
    print(f"{hour:02d}:00 | {bar} {gen:,.0f} MWh")
```

---

## Example 3: Renewable Share Throughout the Day

```python
rt_gen = eptr.call("rt-generation", start_date="2024-07-15", end_date="2024-07-15")

# Define columns
renewable_cols = ['wind', 'sun', 'river', 'dammedHydro', 'geothermal', 'biomass']
available_renewable = [c for c in renewable_cols if c in rt_gen.columns]

rt_gen['renewable'] = rt_gen[available_renewable].sum(axis=1)
rt_gen['total'] = rt_gen.select_dtypes(include='number').drop(columns=['hour'], errors='ignore').sum(axis=1)
rt_gen['renewable_pct'] = (rt_gen['renewable'] / rt_gen['total']) * 100

print("Renewable Share by Hour:")
rt_gen['dt'] = pd.to_datetime(rt_gen['date'])
for _, row in rt_gen.iterrows():
    hour = row['dt'].hour
    pct = row['renewable_pct']
    bar = '█' * int(pct / 5)
    print(f"{hour:02d}:00 | {bar} {pct:.1f}%")
```

---

## Example 4: Monthly Generation Mix

```python
rt_gen = eptr.call("rt-generation", start_date="2024-07-01", end_date="2024-07-31")

# Sum by fuel type
numeric_cols = rt_gen.select_dtypes(include='number').columns
monthly_totals = rt_gen[numeric_cols].sum()
total = monthly_totals.sum()

print("July 2024 Generation Mix:")
for fuel, gen in monthly_totals.sort_values(ascending=False).items():
    if gen > 0:
        pct = (gen / total) * 100
        print(f"  {fuel}: {gen/1000:,.0f} GWh ({pct:.1f}%)")
```

---

## Example 5: Wind Generation Analysis

```python
rt_gen = eptr.call("rt-generation", start_date="2024-07-01", end_date="2024-07-31")

rt_gen['date'] = pd.to_datetime(rt_gen['date'])
rt_gen['hour'] = rt_gen['date'].dt.hour
rt_gen['day'] = rt_gen['date'].dt.date

# Daily wind generation
daily_wind = rt_gen.groupby('day')['wind'].sum()

print("Wind Generation Analysis:")
print(f"  Monthly Total: {daily_wind.sum()/1000:,.0f} GWh")
print(f"  Daily Average: {daily_wind.mean():,.0f} MWh")
print(f"  Best Day: {daily_wind.max():,.0f} MWh on {daily_wind.idxmax()}")
print(f"  Lowest Day: {daily_wind.min():,.0f} MWh on {daily_wind.idxmin()}")
```

---

## Example 6: Solar Capacity Factor Estimation

```python
rt_gen = eptr.call("rt-generation", start_date="2024-07-01", end_date="2024-07-31")

# Assuming ~20 GW installed solar capacity
installed_capacity_mw = 20000
hours_in_month = 24 * 31

total_solar_mwh = rt_gen['sun'].sum()
max_possible_mwh = installed_capacity_mw * hours_in_month
capacity_factor = total_solar_mwh / max_possible_mwh

print(f"Solar Generation: {total_solar_mwh/1000:,.0f} GWh")
print(f"Estimated Capacity Factor: {capacity_factor*100:.1f}%")
```

---

## Example 7: Compare Real-Time with Settlement (UEVM)

```python
from eptr2.composite import get_hourly_production_data

# Get data for a settled period
df = get_hourly_production_data(
    eptr,
    start_date="2024-06-15",
    end_date="2024-06-15"
)

# Compare rt vs uevm
if 'total_uevm' in df.columns:
    df['diff'] = df['total_rt'] - df['total_uevm']
    print("Real-Time vs Settlement Comparison:")
    print(f"  Average Difference: {df['diff'].mean():.2f} MWh")
    print(f"  Max Difference: {df['diff'].abs().max():.2f} MWh")
```

---

## Example 8: Plant-Level Production

```python
from eptr2.composite import get_hourly_production_data

# Get data for a specific power plant
# Example IDs (you need to look up actual IDs)
df = get_hourly_production_data(
    eptr,
    start_date="2024-07-15",
    end_date="2024-07-15",
    rt_pp_id=641,     # Real-time plant ID
    uevm_pp_id=142    # UEVM plant ID
)

print(f"Plant Daily Generation: {df['total_rt'].sum():,.0f} MWh")
```

---

## Example 9: Organization Production Plan Analysis

```python
from eptr2.composite import get_hourly_production_plan_data

# Get production plan for an organization
df = get_hourly_production_plan_data(
    eptr,
    start_date="2024-07-15",
    end_date="2024-07-15",
    org_id=195,  # Organization ID (e.g., EÜAŞ)
)

print(df.columns.tolist())
print(f"Total Planned Generation: {df.select_dtypes(include='number').sum().sum():,.0f} MWh")
```

---

## Example 10: Cross-Border Generation Context

```python
# Generation data combined with cross-border flows
rt_gen = eptr.call("rt-generation", start_date="2024-07-15", end_date="2024-07-15")

# Total generation
total_gen = rt_gen.select_dtypes(include='number').drop(columns=['hour'], errors='ignore').sum(axis=1)

# Note: Cross-border data requires separate endpoint
# This shows generation context for understanding net position
print(f"Total Generation Range: {total_gen.min():,.0f} - {total_gen.max():,.0f} MWh")
```

---

## Example 11: Export Generation Data

```python
rt_gen = eptr.call("rt-generation", start_date="2024-07-01", end_date="2024-07-31")

# Export to CSV
rt_gen.to_csv("generation_july_2024.csv", index=False)
print(f"Exported {len(rt_gen)} rows")
```

---

## Example 12: Compare Two Months

```python
july = eptr.call("rt-generation", start_date="2024-07-01", end_date="2024-07-31")
june = eptr.call("rt-generation", start_date="2024-06-01", end_date="2024-06-30")

july_total = july.select_dtypes(include='number').sum().sum()
june_total = june.select_dtypes(include='number').sum().sum()

print(f"June Total: {june_total/1000:,.0f} GWh")
print(f"July Total: {july_total/1000:,.0f} GWh")
print(f"Change: {((july_total/june_total)-1)*100:+.1f}%")
```

---

## Power Plant ID Reference

To get plant-specific data, you need the appropriate IDs. Common approaches:

```python
# List available power plants (requires org_id lookup first)
orgs = eptr.call("pp-list")  # Power plant listing

# Or use the real-time generation organization listing
rt_org_list = eptr.call("rt-gen-org-list")
print(rt_org_list.head())
```

Note: Power plant IDs differ between real-time (`rt_pp_id`) and settlement (`uevm_pp_id`) systems.
