# Compare day-ahead and intraday prices

This example retains missing observations and validates that a join cannot duplicate hours. It does not assume the two endpoints always cover the same range.

```python
from eptr2 import EPTR2
import pandas as pd

eptr = EPTR2(use_dotenv=True, recycle_tgt=True, strict_params=True)
params = {"start_date": "2026-07-01", "end_date": "2026-07-01"}
mcp = eptr.call("mcp", **params)[["date", "price"]]
wap = eptr.call("wap", **params)[["date", "wap"]]
comparison = mcp.merge(wap, on="date", how="outer", validate="one_to_one")
comparison["date"] = pd.to_datetime(comparison["date"], utc=True).dt.tz_convert("Europe/Istanbul")
comparison["dam_minus_idm"] = comparison["price"] - comparison["wap"]
print(comparison)
print("Incomplete hours:", comparison[["price", "wap"]].isna().any(axis=1).sum())
```

For daily or monthly summaries, state the dates, timezone, units, and count of included/missing hours. Weight by energy only when energy weights are part of the requested analysis; an ordinary hourly mean is not a volume-weighted price.
