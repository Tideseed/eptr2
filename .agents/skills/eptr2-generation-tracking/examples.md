# Renewable share without double-counting

```python
from eptr2 import EPTR2

eptr = EPTR2(use_dotenv=True, recycle_tgt=True, strict_params=True)
df = eptr.call("rt-gen", start_date="2026-07-01", end_date="2026-07-01")
renewable_columns = ["wind", "sun", "river", "dammedHydro", "geothermal", "biomass"]
# Require all selected sources instead of treating absent data as zero.
renewable = df[renewable_columns].sum(axis=1, min_count=len(renewable_columns))
denominator = df["total"].where(df["total"] > 0)
df["renewable_share_pct"] = renewable / denominator * 100
print(df[["date", "total", "renewable_share_pct"]])
```

# One plant's real-time production

The ID below is an illustration from `pp-list`; resolve the user's plant in that listing first. The settlement ID is different and is intentionally not guessed here.

```python
from eptr2 import EPTR2
from eptr2.composite import get_hourly_production_data

eptr = EPTR2(use_dotenv=True, recycle_tgt=True, strict_params=True)
plant = get_hourly_production_data(
    start_date="2026-07-01", end_date="2026-07-01", eptr=eptr,
    rt_pp_id=641, skip_uevm=True,
)
print(plant[["dt", "total_rt"]])
```

To compare plans with actuals, use the independently resolved UEVCB ID for `get_kgup_bulk_range` and real-time plant ID for `get_rt_gen_bulk_range`. Join timestamps with cardinality validation; do not turn missing hours into zero generation.
