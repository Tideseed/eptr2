from eptr2.util.costs import calculate_unit_price_and_costs


res = calculate_unit_price_and_costs(mcp=2957.77, smp=2957.77, include_kupst=True)


print("Unit Price and Costs Result: ", res)
