---
name: eptr2-imbalance-costs
description: Calculate Turkish electricity imbalance and KÜPST deviation costs with eptr2 using contract dates, system direction, and plant source. Use for historical cost analysis or explicit scenarios, not order execution.
---

# Imbalance and KÜPST costs

Use contract-aware utilities for historical analysis. The library distinguishes pre-2026 and 2026 rules; do not apply a timeless 3% margin or one tolerance to a range crossing a rule boundary.

```python
from eptr2.util.costs import calculate_unit_price_and_costs_by_contract

costs = calculate_unit_price_and_costs_by_contract(
    contract="PH26070101", mcp=4000, smp=4000,
    system_direction="Enerji Açığı",
)
print(costs)
```

No credentials are required for pure calculations. Fetch `systemStatus` from `mcp-smp-imb` for API-based analyses. Pass direction explicitly, especially when MCP equals SMP: -1 / `Enerji Açığı` means deficit, +1 / `Enerji Fazlası` means surplus, and 0 / `Dengede` means balanced. The MCP calculation tool accepts `system_direction` and requires it for equal prices.

Output `unit_pos_imb_cost` and `unit_neg_imb_cost` are TL/MWh; multiplying by the corresponding imbalance energy gives TL. `unit_kupst` is not the plant's total charge. Distinguish positive/negative imbalance energy, unit prices, unit opportunity costs, and total costs.

Read [formulas.md](formulas.md) for function selection and [examples.md](examples.md) for per-contract KÜPST and API-backed comparisons. State whether the result is historical or a scenario with overridden assumptions. Do not equate a simple plant calculation with every aggregator settlement rule.
