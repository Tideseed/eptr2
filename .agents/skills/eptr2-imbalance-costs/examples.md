# Per-contract plant deviation cost

```python
from eptr2.util.costs import calculate_kupst_cost_by_contract, get_kupst_tolerance_by_contract

contract = "PH26070101"
tolerance = get_kupst_tolerance_by_contract(contract, source="wind")
plant_cost = calculate_kupst_cost_by_contract(
    contract=contract, actual=80, forecast=100, mcp=4000, smp=4000,
    source="wind", return_detail=True,
)
print("Tolerance:", tolerance, "Cost breakdown:", plant_cost)
```

# Compare calculations with reported prices

```python
from eptr2 import EPTR2
from eptr2.util.costs import calculate_unit_price_and_costs_by_contract
from eptr2.util.time import iso_to_contract

eptr = EPTR2(use_dotenv=True, recycle_tgt=True, strict_params=True)
df = eptr.call("mcp-smp-imb", start_date="2026-07-01", end_date="2026-07-01")
rows = []
for _, row in df.iterrows():
    calculated = calculate_unit_price_and_costs_by_contract(
        contract=iso_to_contract(row["date"]), mcp=row["ptf"], smp=row["smf"],
        system_direction=row["systemStatus"],
    )
    rows.append({
        "date": row["date"],
        "positive_difference": calculated["pos_imb_price"] - row["positiveImbalance"],
        "negative_difference": calculated["neg_imb_price"] - row["negativeImbalance"],
    })
print(rows)
```

Compare with a declared rounding tolerance (for example 0.01 TL/MWh), retaining missing observations as missing. Agreement with one API sample is not certification of all periods or settlement rules.
