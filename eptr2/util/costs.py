def calculate_unit_imbalance_price(mcp: float, smp: float):
    d = {"pos": 0.97 * min(mcp, smp), "neg": 1.03 * max(mcp, smp)}
    return d


def calculate_unit_imbalance_cost(mcp: float, smp: float):
    d = {"pos": mcp - 0.97 * min(mcp, smp), "neg": 1.03 * max(mcp, smp) - mcp}
    return d


def calculate_imbalance_cost(
    actual: float,
    forecast: float,
    mcp: float,
    smp: float,
    producer: bool,
    imbalance_discount: float = 0.0,
):
    if imbalance_discount > 1 or imbalance_discount < 0:
        raise ValueError("Imbalance dampening rate must be between 0 and 1")

    unit_cost_d = calculate_unit_imbalance_cost(mcp=mcp, smp=smp)

    d = {}

    diff = forecast - actual
    if producer:
        cost = abs(diff) * unit_cost_d["neg" if diff > 0 else "pos"]
    else:
        cost = abs(diff) * unit_cost_d["pos" if diff > 0 else "neg"]

    return cost * (1 - imbalance_discount)


def calculate_kupst_cost(
    actual: float,
    forecast: float,
    mcp: float,
    smp: float,
    tol: float = 0.21,
    kupst_multiplier: float = 0.03,
):
    tol_val = forecast * tol
    kupst_cost = (
        max(0, abs(actual - forecast) - tol_val) * max(mcp, smp) * kupst_multiplier
    )
    return kupst_cost


def calculate_diff_cost(
    actual: float,
    forecast: float,
    mcp: float,
    smp: float,
    tol: float = 0.21,
    kupst_multiplier: float = 0.03,
    producer: bool = True,
    imbalance_discount: float = 0.0,
):
    imbalance = calculate_imbalance_cost(
        actual=actual,
        forecast=forecast,
        mcp=mcp,
        smp=smp,
        producer=producer,
        imbalance_discount=imbalance_discount,
    )

    kupst = calculate_kupst_cost(
        actual=actual,
        forecast=forecast,
        mcp=mcp,
        smp=smp,
        tol=tol,
        kupst_multiplier=kupst_multiplier,
    )

    total = imbalance + kupst

    return {"imbalance": imbalance, "kupst": kupst, "total": total}


def calculate_imbalance_prices_list(mcp: list, smp: list):
    """
    Calculates imbalance prices for positive and negative imbalances
    """
    d = {
        "pos": [min(x, y) * 0.97 for x, y in zip(mcp, smp)],
        "neg": [1.03 * max(x, y) for x, y in zip(mcp, smp)],
    }

    return d


def calculate_imbalance_cost_values_list(mcp: list, smp: list):
    """
    Calculates imbalance costs relative to day-ahead prices (MCP) for positive and negative imbalances
    """
    d = calculate_imbalance_prices_list(mcp, smp)
    d["pos"] = [x - y for x, y in zip(mcp, d["pos"])]
    d["neg"] = [y - x for x, y in zip(mcp, d["neg"])]

    return d


def calculate_kupst_cost_list(
    actual_values: list,
    forecast_values: list,
    mcp: list,
    smp: list,
    tol: float = 0.21,
    kupst_multiplier: float = 0.03,
):
    """
    Calculates production plan difference (KUPST) costs.
    """

    kupst_cost_list = []

    for x, y, m, s in zip(forecast_values, actual_values, mcp, smp):
        cost = max(abs(x - y) - tol * x, 0) * max(m, s) * kupst_multiplier

        kupst_cost_list.append(cost)

    return kupst_cost_list


def calculate_imbalance_cost_list(
    actual_values: list,
    forecast_values: list,
    cost_d: dict,
    producer: bool,
    imbalance_discount: float = 0.0,
):
    """
    Calculates imbalance costs for a given forecast and actual values.
    Imbalance dampening reduces imbalance costs by the given rate (<1). It is used to emulate balance responsible party (DSG) effect.
    """

    if imbalance_discount > 1 or imbalance_discount < 0:
        raise ValueError("Imbalance dampening rate must be between 0 and 1")

    if len(actual_values) != len(forecast_values):
        raise ValueError("Actual and forecast values must have the same length")

    imbalance_cost_list = []

    for x, y, n, p in zip(forecast_values, actual_values, cost_d["neg"], cost_d["pos"]):
        if x < y:
            cost = (y - x) * p if producer else n
        else:
            cost = (x - y) * n if producer else p

        imbalance_cost_list.append(cost * (1 - imbalance_discount))

    return imbalance_cost_list


def calculate_diff_costs_list(
    actual_values: list,
    forecast_values: list,
    mcp: list,
    smp: list,
    tol: float,
    kupst_multiplier: float,
    producer: bool,
    imbalance_discount: float = 0,
):
    """
    Wrapper function to calculate all costs related to the difference between actual and forecasted values..
    """
    res_d = {"actual": actual_values, "forecast": forecast_values}

    cost_d = calculate_imbalance_cost_values_list(mcp, smp)
    if producer:
        res_d["kupst_cost"] = calculate_kupst_cost_list(
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

    res_d["imbalance_cost"] = calculate_imbalance_cost_list(
        actual_values, forecast_values, cost_d, producer, imbalance_discount
    )

    return res_d
