"""
Example: Cost functions usage of eptr2 library for AI agents.

This example demonstrates the use cases when calculating costs associated with imbalance in the Turkish electricity market using the internal functions of eptr2.
"""

from eptr2.util.costs import (
    calculate_diff_costs,
    calculate_unit_imbalance_price,
    calculate_unit_imbalance_cost,
    calculate_unit_kupst_cost,
    calculate_kupsm,
    get_regulation_period_by_contract,
    calculate_imbalance_amount,
)


def generate_cost_scenario_output(mcp, smp):
    # Calculate unit imbalance prices
    unit_prices = calculate_unit_imbalance_price(mcp=mcp, smp=smp, include_prices=True)
    print("Unit Imbalance Prices:")
    for k, v in unit_prices.items():
        print(f" - {k}: {round(v, 2)} TL/MWh")

    # Calculate unit imbalance costs
    unit_costs = calculate_unit_imbalance_cost(mcp=mcp, smp=smp, include_prices=True)
    print("\nUnit Imbalance Costs:")
    for k, v in unit_costs.items():
        print(f" - {k}: {round(v, 2)} TL/MWh")

    # Calculate KUPST
    kupst = calculate_unit_kupst_cost(mcp=mcp, smp=smp)
    print(f"\nUnit KUPST: {round(kupst, 2)} TL/MWh")
    return unit_prices, unit_costs, kupst


def example_calculate_imbalance_prices_costs_and_kupst():
    """Calculate imbalance prices, costs, and KUPST for a sample scenario."""

    ### Scenario: System in Negative Imbalance (MCP < SMP)
    mcp = 1500.0  ## Market Clearing Price
    smp = 1800.0  ## System Marginal Price

    print("=====")
    print(f"Scenario 1: MCP ({mcp}) < SMP ({smp}) => System in Negative Imbalance")
    generate_cost_scenario_output(mcp=mcp, smp=smp)
    print("=====")

    ### Scenario: System in Positive Imbalance (MCP > SMP)
    mcp = 2500.0  ## Market Clearing Price
    smp = 2000.0  ## System Marginal Price

    print("=====")
    print(f"Scenario 2: MCP ({mcp}) > SMP ({smp}) => System in Positive Imbalance")
    generate_cost_scenario_output(mcp=mcp, smp=smp)
    print("=====")

    ### Scenario: System in Positive Imbalance (MCP > SMP) and low prices
    mcp = 300.0  ## Market Clearing Price
    smp = 60.0  ## System Marginal Price

    print("=====")
    print(
        f"Scenario 3: MCP ({mcp}) > SMP ({smp}) => System in Positive Imbalance and Low Prices"
    )
    generate_cost_scenario_output(mcp=mcp, smp=smp)
    print("=====")

    ### Scenario: System in Negative Imbalance (MCP < SMP) and ceiling prices (for early 2026)
    mcp = 2000.0
    smp = 3400.0
    print("=====")
    print(
        f"Scenario 4: MCP ({mcp}) < SMP ({smp}) => System in Negative Imbalance and Ceiling Prices"
    )
    generate_cost_scenario_output(mcp=mcp, smp=smp)
    print("=====")

    ### Scenario: System in Negative Imbalance (MCP < SMP) and extreme low/high prices (for early 2026)
    mcp = 100.0
    smp = 3400.0
    print("=====")
    print(
        f"Scenario 5: MCP ({mcp}) < SMP ({smp}) => System in Negative Imbalance and Extreme  Prices"
    )
    generate_cost_scenario_output(mcp=mcp, smp=smp)
    print("=====")

    ### Scenario: System in Negative Imbalance (MCP < SMP) and extreme low/high prices (for early 2026)
    mcp = 3400.0
    smp = 120.0
    print("=====")
    print(
        f"Scenario 6: MCP ({mcp}) > SMP ({smp}) => System in Positive Imbalance and Extreme  Prices"
    )
    generate_cost_scenario_output(mcp=mcp, smp=smp)
    print("=====")

    ### Scenario: System in Negative Imbalance (MCP < SMP) and both low prices (for early 2026)
    mcp = 150.0
    smp = 120.0
    print("=====")
    print(
        f"Scenario 7: MCP ({mcp}) > SMP ({smp}) => System in Positive Imbalance and Both Low Prices"
    )
    generate_cost_scenario_output(mcp=mcp, smp=smp)
    print("=====")

    ### Scenario: System in Negative Imbalance (MCP < SMP) and both ceiling prices (for early 2026) (ps. negative imbalance implied by ceiling SMP price)
    mcp = 3400.0
    smp = 3400.0
    print("=====")
    print(
        f"Scenario 8: MCP ({mcp}) < SMP ({smp}) => System in Negative Imbalance and Ceiling Prices"
    )
    generate_cost_scenario_output(mcp=mcp, smp=smp)
    print("=====")
    return True


def example_scenario_1_negative_imbalance_consumer_system_negative():
    """
    This scnenario demonstrates the calculation of costs for a consumer with negative imbalance and the system is also in negative imbalance.
    The consumer has a forecasted consumption of 30 MWh but actually consumes 50 MWh.
    The market clearing price (MCP) is 2000 TL/MWh and the system marginal price (SMP) is 2500 TL/MWh.
    """
    print("Scenario 1: Negative Imbalance Consumer, System in Negative Imbalance")
    mcp = 2000.0  ## Market Clearing Price
    smp = 2500.0  ## System Marginal Price
    is_producer = False
    forecast = 30.0  ## Forecasted consumption
    actual = 50.0  ## Actual consumption

    cost_price_d = calculate_unit_imbalance_cost(mcp=mcp, smp=smp, include_prices=True)

    print("\nUnit Imbalance Prices and Costs")
    for k, v in cost_price_d.items():
        print(f" - {k}: {round(v, 2)} TL/MWh")

    imbalance_quantities_d = calculate_imbalance_amount(
        forecast=forecast, actual=actual, is_producer=is_producer
    )

    print("\nImbalance Quantities")
    for k, v in imbalance_quantities_d.items():
        print(f" - {k}: {round(v, 2)} MWh")

    res_d = calculate_diff_costs(
        forecast=forecast,
        actual=actual,
        mcp=mcp,
        smp=smp,
        is_producer=is_producer,
        include_quantities=True,
    )

    print("\nFinal Cost Calculation")
    for k, v in res_d.items():
        print(f" - {k}: {round(v, 2)}")

    return res_d


def example_scenario_2_negative_imbalance_producer_system_negative():
    """
    This scnenario demonstrates the calculation of costs for a producer (wind power plant) with negative imbalance and the system is also in negative imbalance.
    The producer has a forecasted production of 40 MWh but actually produces 25 MWh.
    The market clearing price (MCP) is 2000 TL/MWh and the system marginal price (SMP) is 2500 TL/MWh.
    """

    print("Example: Scenario 2 - Negative Imbalance Producer, System Negative")
    mcp = 2000.0  ## Market Clearing Price
    smp = 2500.0  ## System Marginal Price
    is_producer = True
    forecast = 40.0  ## Forecasted production
    actual = 25.0  ## Actual production
    source = "wind"

    cost_price_d = calculate_unit_imbalance_cost(mcp=mcp, smp=smp, include_prices=True)

    print("\nUnit Imbalance Prices and Costs")
    for k, v in cost_price_d.items():
        print(f" - {k}: {round(v, 2)} TL/MWh")

    imbalance_quantities_d = calculate_imbalance_amount(
        forecast=forecast, actual=actual, is_producer=is_producer
    )

    print("\nImbalance Quantities")
    for k, v in imbalance_quantities_d.items():
        print(f" - {k}: {round(v, 2)} MWh")

    res_d = calculate_diff_costs(
        forecast=forecast,
        actual=actual,
        mcp=mcp,
        smp=smp,
        is_producer=is_producer,
        include_quantities=True,
        production_source=source,
    )

    print("\nFinal Cost Calculation")
    for k, v in res_d.items():
        print(f" - {k}: {round(v, 2)}")

    return res_d


def main():
    print("*****")
    example_calculate_imbalance_prices_costs_and_kupst()
    print("*****")
    example_scenario_1_negative_imbalance_consumer_system_negative()
    print("*****")
    example_scenario_2_negative_imbalance_producer_system_negative()
    print("*****")


if __name__ == "__main__":
    main()
