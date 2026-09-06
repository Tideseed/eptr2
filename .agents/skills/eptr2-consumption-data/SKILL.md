---
name: eptr2-consumption-data
description: Retrieve Turkish electricity consumption, settlement UEÇM, and demand forecasts with eptr2. Use to compare demand forecasts with real-time or settled consumption and explain fallback data.
---

# Consumption and demand forecasts

Choose the measurement basis before reporting forecast accuracy: `rt-cons` is real-time consumption, `uecm` is settlement consumption, and `load-plan` is the demand forecast. Publication timing varies; inspect availability rather than promising a fixed delay.

```python
from eptr2 import EPTR2
from eptr2.composite import get_hourly_consumption_and_forecast_data

eptr = EPTR2(use_dotenv=True, recycle_tgt=True, strict_params=True)
df = get_hourly_consumption_and_forecast_data(
    start_date="2026-07-01", end_date="2026-07-01", eptr=eptr,
)
print(df[["dt", "load_plan", "rt_cons", "consumption"]])
```

`consumption` uses UEÇM where present and otherwise real-time consumption; `uecm` may be absent when none is available. This is a fallback series, not uniformly settled demand. Preserve its source in downstream analysis. Hourly quantities are MWh and delivery timestamps use Europe/Istanbul.

Check completeness and duplicate timestamps before aggregating. Do not fill missing demand with zero. For forecast errors, state the actual-data basis and the denominator; avoid percentage division by zero.

Read [examples.md](examples.md) for a source-aware accuracy calculation. Use whichever Python or CLI execution facility the user's runtime provides.
