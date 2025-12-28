# Market Operations Examples

## Setup

```python
from eptr2 import EPTR2
import pandas as pd

# Initialize client
eptr = EPTR2(use_dotenv=True, recycle_tgt=True)
```

---

## Example 1: Daily Market Summary

```python
# Get all market activity for a day
dam = eptr.call("dam-clearing", start_date="2024-07-15", end_date="2024-07-15")
idm = eptr.call("idm-qty", start_date="2024-07-15", end_date="2024-07-15")
bi_long = eptr.call("bi-long", start_date="2024-07-15", end_date="2024-07-15")

print("Market Volumes (July 15, 2024):")
print(f"  DAM: {dam['matchedQuantity'].sum():,.0f} MWh")
print(f"  IDM: {idm['matchingQuantity'].sum():,.0f} MWh")
print(f"  Bilateral: {bi_long['quantity'].sum():,.0f} MWh")
```

---

## Example 2: DAM Block Orders Analysis

```python
block_bid = eptr.call("dam-block-bid", start_date="2024-07-15", end_date="2024-07-15")
block_offer = eptr.call("dam-block-offer", start_date="2024-07-15", end_date="2024-07-15")

print("DAM Block Orders:")
print(f"  Total Block Bids: {block_bid['blockBid'].sum():,.0f} MWh")
print(f"  Total Block Offers: {block_offer['blockOffer'].sum():,.0f} MWh")
```

---

## Example 3: IDM Transaction History Analysis

```python
idm_log = eptr.call("idm-log", start_date="2024-07-15", end_date="2024-07-15")

# Convert to DataFrame if needed
idm_log['date'] = pd.to_datetime(idm_log['date'])

# Hourly breakdown
idm_log['hour'] = idm_log['date'].dt.hour
hourly_volume = idm_log.groupby('hour')['quantity'].sum()

print("IDM Hourly Trading Volume:")
print(hourly_volume)
```

---

## Example 4: Price Range Analysis

```python
# IDM min-max matching prices
mm_matching = eptr.call("idm-mm-matching", start_date="2024-07-15", end_date="2024-07-15")

print("IDM Price Range Analysis:")
print(f"  Min Matching Price: {mm_matching['minMatchingPrice'].min():.2f} TL/MWh")
print(f"  Max Matching Price: {mm_matching['maxMatchingPrice'].max():.2f} TL/MWh")
print(f"  Average Range: {(mm_matching['maxMatchingPrice'] - mm_matching['minMatchingPrice']).mean():.2f} TL/MWh")
```

---

## Example 5: Balancing Instructions Analysis

```python
yal = eptr.call("bpm-up", start_date="2024-07-15", end_date="2024-07-15")
yat = eptr.call("bpm-down", start_date="2024-07-15", end_date="2024-07-15")

yal['date'] = pd.to_datetime(yal['date'])
yat['date'] = pd.to_datetime(yat['date'])

# Net regulation by hour
yal['hour'] = yal['date'].dt.hour
yat['hour'] = yat['date'].dt.hour

print("Balancing Instructions Summary:")
print(f"  Total YAL (Up Regulation): {yal['upRegulationNet'].sum():,.0f} MWh")
print(f"  Total YAT (Down Regulation): {yat['downRegulationNet'].sum():,.0f} MWh")
print(f"  Net Direction: {'Up' if yal['upRegulationNet'].sum() > yat['downRegulationNet'].sum() else 'Down'}")
```

---

## Example 6: Supply-Demand Curve

```python
supply_demand = eptr.call("supply-demand", start_date="2024-07-15", end_date="2024-07-15")

# Filter for a specific hour
hour_12 = supply_demand[supply_demand['date'].str.contains('T12:')]

print("Supply-Demand at Hour 12:")
print(hour_12[['price', 'supplyQuantity', 'demandQuantity']].head(20))
```

---

## Example 7: Monthly Market Share

```python
# Get month of data
dam = eptr.call("dam-clearing", start_date="2024-07-01", end_date="2024-07-31")
idm = eptr.call("idm-qty", start_date="2024-07-01", end_date="2024-07-31")
bi_long = eptr.call("bi-long", start_date="2024-07-01", end_date="2024-07-31")

dam_vol = dam['matchedQuantity'].sum()
idm_vol = idm['matchingQuantity'].sum()
bi_vol = bi_long['quantity'].sum()
total = dam_vol + idm_vol + bi_vol

print("July 2024 Market Share:")
print(f"  DAM: {dam_vol/1000:,.0f} GWh ({dam_vol/total*100:.1f}%)")
print(f"  IDM: {idm_vol/1000:,.0f} GWh ({idm_vol/total*100:.1f}%)")
print(f"  Bilateral: {bi_vol/1000:,.0f} GWh ({bi_vol/total*100:.1f}%)")
```

---

## Example 8: Flexible Orders Matching

```python
flex_bid = eptr.call("dam-flexible-bid", start_date="2024-07-15", end_date="2024-07-15")
flex_offer = eptr.call("dam-flexible-offer", start_date="2024-07-15", end_date="2024-07-15")
flex_match = eptr.call("dam-flexible-matching", start_date="2024-07-15", end_date="2024-07-15")

print("DAM Flexible Orders:")
print(f"  Flexible Bids: {flex_bid.select_dtypes(include='number').sum().sum():,.0f} MWh")
print(f"  Flexible Offers: {flex_offer.select_dtypes(include='number').sum().sum():,.0f} MWh")
print(f"  Matched: {flex_match.select_dtypes(include='number').sum().sum():,.0f} MWh")
```

---

## Example 9: Price Independent Orders

```python
pi_bid = eptr.call("pi-bid", start_date="2024-07-15", end_date="2024-07-15")
pi_offer = eptr.call("pi-offer", start_date="2024-07-15", end_date="2024-07-15")

print("Price Independent Orders (Must-Run):")
print(f"  PI Bids: {pi_bid['quantity'].sum():,.0f} MWh")
print(f"  PI Offers: {pi_offer['quantity'].sum():,.0f} MWh")
```

---

## Example 10: IDM Contract Summary

```python
idm_summary = eptr.call("idm-summary", start_date="2024-07-15", end_date="2024-07-15")

print("IDM Contract Summary:")
print(idm_summary.head(10))
```

---

## Example 11: Trade Value Analysis

```python
dam_vol = eptr.call("dam-volume", start_date="2024-07-01", end_date="2024-07-31")
idm_vol = eptr.call("idm-volume", start_date="2024-07-01", end_date="2024-07-31")

dam_value = dam_vol['volume'].sum()
idm_value = idm_vol['volume'].sum()

print("July 2024 Trade Values:")
print(f"  DAM: {dam_value/1e9:,.2f} Billion TL")
print(f"  IDM: {idm_value/1e9:,.2f} Billion TL")
```

---

## Example 12: EÜAŞ Bilateral Agreements

```python
euas_bi = eptr.call("bi-euas", start_date="2024-01-01", end_date="2024-12-31")

print("EÜAŞ - GTŞ Bilateral Contracts (2024):")
print(euas_bi)
```

---

## Example 13: System Direction Distribution

```python
smp_dir = eptr.call("smp-dir", start_date="2024-07-01", end_date="2024-07-31")

# Count by direction
direction_counts = smp_dir['systemDirection'].value_counts()

print("System Direction Distribution (July 2024):")
print(direction_counts)
```

---

## Example 14: Export Market Data

```python
# Get comprehensive market data
dam = eptr.call("dam-clearing", start_date="2024-07-01", end_date="2024-07-31")
idm = eptr.call("idm-qty", start_date="2024-07-01", end_date="2024-07-31")

# Merge on date
merged = dam.merge(idm, on='date', how='outer', suffixes=('_dam', '_idm'))

# Export
merged.to_csv("market_volumes_july_2024.csv", index=False)
print(f"Exported {len(merged)} rows")
```

---

## Example 15: BPM Instructions with Weighted Average

```python
bpm_avg = eptr.call("bpm-orders-w-avg", start_date="2024-07-15", end_date="2024-07-15")

print("BPM Instructions (Weighted Average):")
print(bpm_avg.head())
```
