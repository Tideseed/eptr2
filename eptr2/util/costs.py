def calculate_imbalance_prices(mcp: float, smp: float):
    """
    Calculates imbalance prices for positive and negative imbalances
    """
    d = {
        "pos": min(mcp, smp) * 0.97,
        "neg": 1.03 * max(mcp, smp),
    }

    return d


def calculate_imbalance_cost_values(mcp: float, smp: float):
    """
    Calculates imbalance costs relative to day-ahead prices (MCP) for positive and negative imbalances
    """
    d = calculate_imbalance_prices(mcp, smp)
    d["pos"] = mcp - d["pos"]
    d["neg"] = d["neg"] - mcp

    return d


def calculate_kupst_cost(
    actual_values: list,
    forecast_values: list,
    mcp: float,
    smp: float,
    tol: float = 0.21,
    kupst_multiplier: float = 0.03,
):
    """
    Calculates production plan difference (KUPST) costs.
    """

    kupst_cost_list = []

    for x, y in zip(forecast_values, actual_values):
        error = abs(x - y)
        if error > tol * y:
            cost = round(error - tol * y, 1) * max(mcp, smp) * kupst_multiplier
        else:
            cost = 0

        kupst_cost_list.append(cost)

    return kupst_cost_list


def calculate_imbalance_cost(
    actual_values: list,
    forecast_values: list,
    cost_d: dict,
    producer: bool,
    imbalance_dampening_rate: float = 0.0,
):
    """
    Calculates imbalance costs for a given forecast and actual values.
    Imbalance dampening reduces imbalance costs by the given rate (<1). It is used to emulate balance responsible party (DSG) effect.
    """

    if imbalance_dampening_rate > 1 or imbalance_dampening_rate < 0:
        raise ValueError("Imbalance dampening rate must be between 0 and 1")

    if len(actual_values) != len(forecast_values):
        raise ValueError("Actual and forecast values must have the same length")

    imbalance_cost_list = []

    for x, y in zip(forecast_values, actual_values):
        if x < y:
            cost = (y - x) * cost_d["pos" if producer else "neg"]
        else:
            cost = (x - y) * cost_d["neg" if producer else "pos"]

        imbalance_cost_list.append(cost * (1 - imbalance_dampening_rate))

    return imbalance_cost_list


def calculate_diff_costs(
    actual_values: list,
    forecast_values: list,
    mcp: float,
    smp: float,
    tol: float,
    kupst_multiplier: float,
    producer: bool,
    imbalance_dampening_rate: float = 0,
):
    """
    Wrapper function to calculate all costs related to the difference between actual and forecasted values..
    """
    res_d = {"actual": actual_values, "forecast": forecast_values}

    cost_d = calculate_imbalance_cost_values(mcp, smp)
    if producer:
        res_d["kupst_cost"] = calculate_kupst_cost(
            actual_values, forecast_values, mcp, smp, tol, kupst_multiplier
        )

    if producer:
        res_d["imbalance_direction"] = [
            "pos" if x < y else "neg" for x, y in zip(forecast_values, actual_values)
        ]
    else:
        res_d["imbalance_direction"] = [
            "neg" if x < y else "pos" for x, y in zip(forecast_values, actual_values)
        ]

    res_d["imbalance_cost"] = calculate_imbalance_cost(
        actual_values, forecast_values, cost_d, producer, imbalance_dampening_rate
    )

    return res_d
