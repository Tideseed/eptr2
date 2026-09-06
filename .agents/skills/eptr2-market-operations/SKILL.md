---
name: eptr2-market-operations
description: Query EPIAS day-ahead, intraday, bilateral, and balancing-market data with eptr2. Use for published volumes, trades, and instructions; this data client does not submit market orders.
---

# Market operations data

Choose the market and measurement before aggregating:

| Market | Starting calls |
|---|---|
| Day-ahead / GÖP | `dam-clearing`, `dam-volume`, `dam-bid`, `dam-offer` |
| Intraday / GİP | `idm-qty`, `idm-volume`, `idm-log`, `wap` |
| Bilateral / İA | `bi-long`, `bi-short` |
| Balancing / DGP | `bpm-up`, `bpm-down`, `bpm-orders-w-avg` |

These expose published data, not permissions or tools for submitting/canceling orders. Use `eptr2 describe <key>` to discover accepted parameters; do not assume similarly named transaction/contract-list endpoints exist.

```python
from eptr2 import EPTR2

eptr = EPTR2(use_dotenv=True, recycle_tgt=True, strict_params=True)
clearing = eptr.call("dam-clearing", start_date="2026-07-01", end_date="2026-07-01")
print(clearing.columns.tolist())
print(clearing.head())
```

A trade value in TL is not a matched quantity in MWh. Do not sum every numeric column: timestamps, IDs, bid/ask sides, prices, and totals can coexist. Avoid adding both sides of the same matched trade. Verify transaction quantity units before converting lots to MWh.

For organization-specific analyses, resolve the organization and pass its ID only to endpoints that accept it. Gate-closure and publication schedules can change; verify them for the requested period instead of treating this skill as a market-rule source.

Read [examples.md](examples.md) for discovery and a bounded raw-response query.
