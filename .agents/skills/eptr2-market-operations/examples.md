# Inspect transaction metadata and a sample response

```python
from eptr2 import EPTR2
from eptr2.agentic import describe_call

print(describe_call("idm-log"))
eptr = EPTR2(use_dotenv=True, recycle_tgt=True, strict_params=True)
response = eptr.call(
    "idm-log", start_date="2026-07-01", end_date="2026-07-01", postprocess=False,
)
print(type(response).__name__)
if isinstance(response, dict):
    print(response.keys())
```

Inspect the selected quantity field, units, timestamp meaning, and whether the response includes totals or paging metadata before scaling to a long date range. Keep distinct contracts separate and validate completeness. Use a saved dataset or a bounded summary for large results rather than flooding an agent's context with transaction logs.
