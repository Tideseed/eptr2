# Imbalance Cost Examples

## Setup

```python
from eptr2 import EPTR2
from eptr2.composite import get_hourly_price_and_cost_data
from eptr2.util.costs import (
    calculate_unit_imbalance_cost,
    calculate_unit_kupst_cost,
    calculate_imb_cost,
    calculate_imbalance_amounts
)
import pandas as pd

# Initialize client
eptr = EPTR2(use_dotenv=True, recycle_tgt=True)
```

---

## Example 1: Basic Unit Cost Calculation

```python
# Sample prices
mcp = 2500  # TL/MWh
smp = 2800  # TL/MWh

# Unit imbalance costs
costs = calculate_unit_imbalance_cost(mcp=mcp, smp=smp)

print(f"MCP: {mcp} TL/MWh, SMP: {smp} TL/MWh")
print(f"Positive Imbalance Cost: {costs['pos']:.2f} TL/MWh")
print(f"Negative Imbalance Cost: {costs['neg']:.2f} TL/MWh")

# KUPST cost
kupst = calculate_unit_kupst_cost(mcp=mcp, smp=smp)
print(f"KUPST Cost: {kupst:.2f} TL/MWh")
```

Output:
```
MCP: 2500 TL/MWh, SMP: 2800 TL/MWh
Positive Imbalance Cost: 75.00 TL/MWh
Negative Imbalance Cost: 384.00 TL/MWh
KUPST Cost: 84.00 TL/MWh
```

---

## Example 2: Full Imbalance Cost for a Generator

```python
# Generator produced more than scheduled
result = calculate_imb_cost(
    actual=105,       # Actually generated
    forecast=100,     # Scheduled (KGÜP)
    mcp=2500,
    smp=2800,
    is_producer=True,
    imb_tol=0.10,     # 10% tolerance
    return_detail=True
)

print("Imbalance Analysis:")
print(f"  Deviation: {result['imbalances']['diff']} MWh")
print(f"  DSG Imbalance: {result['imbalances']['dsg_imbalance']} MWh")
print(f"  Individual Imbalance: {result['imbalances']['individual_imbalance']} MWh")
print(f"  Imbalance Side: {result['imb_side']}")
print(f"  Total Cost: {result['costs']['total_imb_cost']:.2f} TL")
```

---

## Example 3: Daily Imbalance Exposure Analysis

```python
df = get_hourly_price_and_cost_data(eptr, "2024-07-15", "2024-07-15")

# Assume constant 5 MWh positive imbalance per hour
surplus_mwh = 5

# Calculate hourly and daily costs
df['surplus_cost'] = df['pos_imb_cost'] * surplus_mwh

print("Hourly Surplus Cost Analysis:")
print(f"  Min: {df['surplus_cost'].min():.2f} TL")
print(f"  Max: {df['surplus_cost'].max():.2f} TL")
print(f"  Average: {df['surplus_cost'].mean():.2f} TL")
print(f"  Daily Total: {df['surplus_cost'].sum():,.2f} TL")
```

---

## Example 4: Compare Imbalance Costs by System Direction

```python
df = get_hourly_price_and_cost_data(eptr, "2024-07-01", "2024-07-31")

# Group by system direction
analysis = df.groupby('system_direction').agg({
    'pos_imb_cost': ['mean', 'max'],
    'neg_imb_cost': ['mean', 'max'],
    'mcp': 'count'
})

print("Imbalance Costs by System Direction:")
print(analysis)
```

---

## Example 5: Worst-Case Imbalance Cost Days

```python
df = get_hourly_price_and_cost_data(eptr, "2024-07-01", "2024-07-31")

df['date'] = pd.to_datetime(df['date'])
df['day'] = df['date'].dt.date

# Daily max imbalance costs
daily_max = df.groupby('day').agg({
    'pos_imb_cost': 'max',
    'neg_imb_cost': 'max'
})

print("Top 5 Days by Negative Imbalance Cost:")
print(daily_max.nlargest(5, 'neg_imb_cost')[['neg_imb_cost']])
```

---

## Example 6: Cost with DSG Absorption

```python
# DSG absorbs 50% of within-tolerance imbalance
result = calculate_imb_cost(
    actual=108,
    forecast=100,
    mcp=2500,
    smp=2800,
    is_producer=True,
    imb_tol=0.10,
    dsg_absorption_rate=0.5,  # DSG absorbs 50%
    return_detail=True
)

print("With DSG Absorption:")
print(f"  DSG Imbalance: {result['imbalances']['dsg_imbalance']} MWh")
print(f"  Net DSG (after absorption): {result['imbalances']['net_dsg_imbalance']} MWh")
print(f"  Total Cost: {result['costs']['total_imb_cost']:.2f} TL")
```

---

## Example 7: Tolerance Calculation

```python
from eptr2.util.costs import get_kupst_tolerance

# Check tolerance by source type
for source in ['wind', 'solar', 'natural_gas', 'hydro']:
    tol = get_kupst_tolerance(source)
    print(f"{source}: {tol*100:.0f}%")
```

Output:
```
wind: 17%
solar: 10%
natural_gas: 5%
hydro: 5%
```

---

## Example 8: Monthly Cost Comparison

```python
july = get_hourly_price_and_cost_data(eptr, "2024-07-01", "2024-07-31")
august = get_hourly_price_and_cost_data(eptr, "2024-08-01", "2024-08-31")

# Assume 10 MWh negative imbalance per hour
deficit_mwh = 10

july_cost = (july['neg_imb_cost'] * deficit_mwh).sum()
august_cost = (august['neg_imb_cost'] * deficit_mwh).sum()

print(f"Monthly Deficit Cost (10 MWh/h):")
print(f"  July: {july_cost:,.0f} TL")
print(f"  August: {august_cost:,.0f} TL")
print(f"  Change: {((august_cost/july_cost)-1)*100:+.1f}%")
```

---

## Example 9: Break-Even Analysis

When is it better to sell surplus in IDM vs take imbalance?

```python
df = get_hourly_price_and_cost_data(eptr, "2024-07-15", "2024-07-15")

# If you have surplus:
# Option 1: Sell in IDM at WAP
# Option 2: Take positive imbalance

df['idm_revenue'] = df['wap']  # Revenue per MWh in IDM
df['imb_revenue'] = df['mcp'] - df['pos_imb_cost']  # Net from imbalance

df['idm_better'] = df['idm_revenue'] > df['imb_revenue']

print(f"Hours where IDM is better: {df['idm_better'].sum()}")
print(f"Average IDM advantage: {(df['idm_revenue'] - df['imb_revenue']).mean():.2f} TL/MWh")
```

---

## Example 10: KUPST Cost Analysis

```python
df = get_hourly_price_and_cost_data(eptr, "2024-07-01", "2024-07-31")

print("KUPST Cost Analysis:")
print(f"  Average: {df['kupst_cost'].mean():.2f} TL/MWh")
print(f"  Min: {df['kupst_cost'].min():.2f} TL/MWh")
print(f"  Max: {df['kupst_cost'].max():.2f} TL/MWh")

# Deviation beyond tolerance
# Example: 20 MWh deviation on 100 MWh plant (20%)
deviation_mwh = 10  # 10% is within tolerance, extra 10 is penalized
extra_deviation = 10

monthly_kupst = df['kupst_cost'].mean() * extra_deviation * 24 * 31
print(f"\nMonthly KUPST for 10 MWh excess deviation: {monthly_kupst:,.0f} TL")
```

---

## Example 11: Simulate Portfolio Imbalance

```python
df = get_hourly_price_and_cost_data(eptr, "2024-07-15", "2024-07-15")

# Simulate portfolio with varying imbalance
import numpy as np
np.random.seed(42)

# Random imbalance between -20 and +20 MWh each hour
df['imbalance'] = np.random.uniform(-20, 20, len(df))

# Calculate cost
df['hour_cost'] = df.apply(
    lambda row: row['neg_imb_cost'] * abs(row['imbalance']) if row['imbalance'] < 0 
                else row['pos_imb_cost'] * row['imbalance'],
    axis=1
)

print(f"Total Daily Imbalance Cost: {df['hour_cost'].sum():,.2f} TL")
print(f"Net Imbalance: {df['imbalance'].sum():.2f} MWh")
```

---

## Example 12: Export for Risk Analysis

```python
df = get_hourly_price_and_cost_data(eptr, "2024-07-01", "2024-07-31")

# Select relevant columns for risk analysis
risk_df = df[['date', 'mcp', 'smp', 'system_direction', 'sd_sign',
              'pos_imb_cost', 'neg_imb_cost', 'kupst_cost']].copy()

# Add volatility metrics
risk_df['cost_spread'] = risk_df['neg_imb_cost'] - risk_df['pos_imb_cost']

# Export
risk_df.to_csv("imbalance_risk_july_2024.csv", index=False)
print(f"Exported {len(risk_df)} rows for risk analysis")
```
