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

## An organization's positions (GÖP + İA + GİP)

`eptr2.composite.get_dabi_idm_data(start_date, end_date, eptr=eptr, org_id=...)` returns them per hour in one frame:
`da_long`/`da_short` (GÖP purchases/sales), `bi_long`/`bi_short` (bilateral), `idm_long`/`idm_short` (GİP), the nets
`dabi_net`, `idm_net`, `dabi_idm_net` (**long minus short = net purchases**) and `net_sales` (positive = net seller).

**EPİAŞ swaps bid/ask on the per-organization GİP endpoint:** in `idm-qty` with `org_id`, `clearingQuantityAsk` is what the
organization BOUGHT and `clearingQuantityBid` what it SOLD. The composite maps this; raw `idm-qty` users must too.
`dam-clearing` per organization is not swapped (`matchedBids` = purchases, `matchedOffers` = sales).

For an organization's estimated trading activity, use `eptr2.composite.get_org_estimated_activity(start_date, end_date, org_id=..., eptr=eptr)`: per hourly contract it splits day-ahead open / intraday close (`da_id_close`), intraday day trade (`min(idm_long, idm_short)`) and the free quantity to be consumed (+) or generated (−), using only the organization's GÖP, İA and GİP matchings (fast). `include_pnl=True` adds a fictitious PnL of day-ahead open / intraday close trades from MCP and the published WAP; `include_day_trade_pnl=True` also adds a day-trade PnL from the TAD of the market-wide `idm-log`, which takes a few seconds per day. `verbose=True` shows progress. `idm-log` quantities are lots of 0.1 MWh. The PnL is an estimate, not the organization's realized result: its own trade prices are not public.

Read [examples.md](examples.md) for discovery and a bounded raw-response query.
