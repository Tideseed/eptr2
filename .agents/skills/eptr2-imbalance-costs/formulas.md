# Select the maintained calculation

Use the installed implementation and contract date rather than copying numerical regulations into a skill. Check applicable primary rules when a task requires legally authoritative settlement results.

| Need | Utility |
|---|---|
| Hourly prices, unit costs and every resolved parameter over a range (fetched or given prices) | `calculate_imbalance_prices` |
| Imbalance + KÜPST costs of actual vs forecast rows, per-row category | `calculate_imbalance_costs` |
| Unit prices and opportunity costs | `calculate_unit_price_and_costs_by_contract` |
| Source-specific tolerance | `get_kupst_tolerance_by_contract` |
| Unit KÜPST rate | `calculate_unit_kupst_cost_by_contract` |
| Plant KÜPST total | `calculate_kupst_cost_by_contract` |

The price relationship is `unit_pos_imb_cost = mcp - pos_imb_price` and `unit_neg_imb_cost = neg_imb_price - mcp`. These unit amounts are not energy volumes. A total must use the appropriate signed imbalance volume and units.

For production, surplus is actual minus scheduled generation when positive; deficit is the magnitude when negative. Consumption has a different direction convention. DSG tolerance and aggregator treatment are separate from plant KÜPST tolerance; do not substitute one for the other.

From 2026-11-01 KÜPST tolerance and multiplier depend on the KÜPST category, which is not exactly the source: pass e.g. `wind`, `solar`, `plant_w_battery`, `unlicensed_from_transmission`, `unlicensed_from_distribution`, `battery` or `other` as `source`/`category` (see `KUPST_CATEGORIES` and `get_kupst_params_by_contract`). Names in other conventions (`Rüzgar`, `GES`, `Depolamalı üretim tesisi`, `BESS`, `Dağıtıma bağlı lisanssız`, ...) are mapped by `normalize_kupst_category`; pass `strict=True` to reject unrecognized names instead of falling back to `other`. Distribution-connected unlicensed deviation is per participant, so aggregate before applying it.

`PHYYMMDDhh` encodes the delivery hour. Resolve tolerances for each contract and source. Direction inference from prices is ambiguous when MCP=SMP; use observed `systemStatus`, or explicitly identify a hypothetical direction. Inspect function signatures for supported overrides rather than forwarding guessed keyword names.
