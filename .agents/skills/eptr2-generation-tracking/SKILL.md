---
name: eptr2-generation-tracking
description: Retrieve Turkish power generation, KGÜP plans, and UEVM settlement data with eptr2. Use for fuel mix, plant output, or plan-versus-actual analysis while resolving distinct plant and UEVCB IDs.
---

# Generation and production plans

Keep the series and identifiers distinct:

| Data | Call/helper | ID lookup |
|---|---|---|
| Real-time actuals | `rt-gen`, `get_rt_gen_bulk_range` | `pp-list` → `pp_id` / `pp_ids` |
| Settlement actuals | `uevm` | `uevm-pp-list` → settlement `pp_id` |
| Production plans | `kgup`, `get_kgup_bulk_range` | `gen-org` then `gen-uevcb` → `org_id`, `uevcb_id` / `uevcb_ids` |

Do not use the deprecated `get_dpp_bulk_range` name for plans: it is a compatibility alias for actual generation. Verify entity names across namespaces before joining plant datasets.

```python
from eptr2 import EPTR2

eptr = EPTR2(use_dotenv=True, recycle_tgt=True, strict_params=True)
generation = eptr.call("rt-gen", start_date="2026-07-01", end_date="2026-07-01")
print(generation[["date", "total", "wind", "sun"]])
```

The API's `total` already contains generation totals. Never sum it together with fuel columns or recompute it after adding derived renewable totals. Use exact field names such as `importCoal` and `dammedHydro`; do not invent `coal`, `importedCoal`, or `nuclear` columns.

For `get_hourly_production_data`, supply the requested `rt_pp_id` and/or `uevm_pp_id`; omitting both is not an aggregate query. Pass `eptr` by keyword. Check publication status and missing hours rather than claiming fixed real-time/settlement delays.

See [examples.md](examples.md) for renewable share and a plant-specific helper. For capacity factors, obtain capacity applicable to the same plant set and period; do not hard-code national installed capacity.
