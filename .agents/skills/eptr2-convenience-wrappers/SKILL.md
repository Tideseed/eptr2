---
name: eptr2-convenience-wrappers
description: Use and discover typed get_* functions in eptr2.calls when writing Python against EPIAS data. Use for wrapper names and signatures; aliases and composite helpers have different interfaces.
---

# Typed endpoint wrappers

Discover actual exports instead of translating arbitrary aliases into guessed function names. `EPTR2.call` aliases and exported wrapper aliases are not identical sets.

```python
import inspect
import eptr2.calls as calls

print([name for name in calls.__all__ if "kgup" in name or "wap" in name])
print(inspect.signature(calls.get_kgup))
```

Reuse a strict client for multiple calls:

```python
from eptr2 import EPTR2
from eptr2.calls import get_mcp, get_kgup, get_wap

eptr = EPTR2(use_dotenv=True, recycle_tgt=True, strict_params=True)
prices = get_mcp(start_date="2026-07-01", end_date="2026-07-01", eptr=eptr)
wap = get_wap(start_date="2026-07-01", end_date="2026-07-01", eptr=eptr)
plans = get_kgup(
    start_date="2026-07-01", end_date="2026-07-01", region="TR1", eptr=eptr,
)
print(prices.head())
```

`get_kgup` requires the `region` argument even though the generic call can default it. Inspect each wrapper's signature for these differences. Examples of real names include `get_wap`, `get_imb_vol`, `get_imb_qty`, and `get_kgup`; do not invent `get_idm_wap`, `get_imbalance_volume`, or `get_dpp`.

Most tabular endpoints return pandas DataFrames when pandas is installed. Some calls return dictionaries, lists, or scalars; `postprocess=False` preserves the decoded response envelope. Omitting `eptr` constructs a client and authenticates, so discovery should use imports/signatures rather than executing a wrapper.

For composite analysis, import from `eptr2.composite` and pass the client as `eptr=...` after the date arguments. The available Python, shell, or MCP facility is a runtime choice; these examples do not depend on a specific agent vendor.
