# Source-aware forecast accuracy

```python
from eptr2 import EPTR2
from eptr2.composite import get_hourly_consumption_and_forecast_data
import pandas as pd

eptr = EPTR2(use_dotenv=True, recycle_tgt=True, strict_params=True)
df = get_hourly_consumption_and_forecast_data(
    start_date="2026-07-01", end_date="2026-07-01", eptr=eptr,
)
settled = df["uecm"] if "uecm" in df else pd.Series(float("nan"), index=df.index)
df["consumption_source"] = "missing"
df.loc[df["rt_cons"].notna(), "consumption_source"] = "real_time"
df.loc[settled.notna(), "consumption_source"] = "settlement"
valid = df[["consumption", "load_plan"]].notna().all(axis=1)
error = df.loc[valid, "consumption"] - df.loc[valid, "load_plan"]
actual_energy = df.loc[valid, "consumption"].abs().sum()
wmape = error.abs().sum() / actual_energy * 100 if actual_energy else float("nan")
print("Included hours:", int(valid.sum()), "Excluded hours:", int((~valid).sum()))
print("MAE (MWh):", error.abs().mean(), "WMAPE (%):", wmape)
print(df["consumption_source"].value_counts())
```

WMAPE here uses absolute actual consumption as the denominator. A mixed settlement/real-time period must be labeled accordingly or split by source. Do not infer that future settlement values equal current real-time measurements.
