---
name: eptr2-price-analysis
description: Retrieve and compare Turkish electricity MCP/PTF, SMP/SMF, intraday WAP, and reported imbalance prices with eptr2. Use for price trends and spreads; use cost utilities for deviation-cost calculations.
---

# Electricity prices

Prefer `mcp-smp-imb` when comparing MCP, SMP, imbalance prices, and system direction: the fields already share an hourly timestamp. Use `mcp` for currency variants and `wap` for intraday weighted prices.

```python
from eptr2 import EPTR2
from eptr2.composite import get_hourly_price_and_cost_data

eptr = EPTR2(use_dotenv=True, recycle_tgt=True, strict_params=True)
df = get_hourly_price_and_cost_data(
    start_date="2026-07-01", end_date="2026-07-01", eptr=eptr,
)
print(df[["date", "mcp", "smp", "wap", "system_direction"]])
```

Composite functions take dates first and `eptr` by keyword. Dates are delivery dates in Europe/Istanbul. Check missing/duplicate hours before comparing means or summing exposure. A missing WAP is not a zero price.

Prices and unit costs in this example are TL/MWh. `pos_imb_cost = mcp - pos_imb_price`; `neg_imb_cost = neg_imb_price - mcp`. The composite's `kupst_cost` is a unit deviation cost, not the plant's total KUPST charge.

Use the API's `systemStatus`/composite `system_direction`, especially when MCP equals SMP; equal prices do not prove a balanced system. Describe a chosen peak/off-peak window as an analysis assumption rather than an official market definition.

See [api-reference.md](api-reference.md) for actual column names and [examples.md](examples.md) for a joined comparison. Use the available Python or CLI tools in the user's runtime; no provider-specific integration is required.
