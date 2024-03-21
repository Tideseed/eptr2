def get_kupst_tolerance(source: str):
    tol_source_map = {"wind": 0.21, "solar": 0.12}
    return tol_source_map.get(source, 0.05)


def calculate_unit_imbalance_price(
    mcp: float, smp: float, penalty_margin: float = 0.03
):
    d = {
        "pos": (1 - penalty_margin) * min(mcp, smp),
        "neg": (1 + penalty_margin) * max(mcp, smp),
    }
    return d


def calculate_unit_imbalance_cost(mcp: float, smp: float, penalty_margin: float = 0.03):
    d = calculate_unit_imbalance_price(mcp=mcp, smp=smp, penalty_margin=penalty_margin)

    d["pos"] = mcp - d["pos"]
    d["neg"] = d["neg"] - mcp

    return d


def calculate_unit_kupst_cost(mcp: float, smp: float, kupst_multiplier: float = 0.03):
    return max(mcp, smp) * kupst_multiplier


def calculate_imbalance_cost(
    actual: float,
    forecast: float,
    mcp: float,
    smp: float,
    is_producer: bool,
    imbalance_discount: float = 0.0,
):
    if imbalance_discount > 1 or imbalance_discount < 0:
        raise ValueError("Imbalance dampening rate must be between 0 and 1")

    unit_cost_d = calculate_unit_imbalance_cost(mcp=mcp, smp=smp)

    d = {}

    diff = forecast - actual
    if is_producer:
        cost = abs(diff) * unit_cost_d["neg" if diff > 0 else "pos"]
    else:
        cost = abs(diff) * unit_cost_d["pos" if diff > 0 else "neg"]

    return cost * (1 - imbalance_discount)


def calculate_kupst_cost(
    actual: float,
    forecast: float,
    mcp: float,
    smp: float,
    tol: float | None = None,
    source: str | None = None,
    kupst_multiplier: float = 0.03,
):
    if tol is None:
        if source is None:
            raise Exception("Either tol(erance) or source parameter must be provided")
        tol = get_kupst_tolerance(source)

    tol_val = forecast * tol
    kupst_cost = max(0, abs(actual - forecast) - tol_val) * calculate_unit_kupst_cost(
        mcp, smp, kupst_multiplier
    )
    return kupst_cost


def calculate_diff_cost(
    actual: float,
    forecast: float,
    mcp: float,
    smp: float,
    tol: float | None = None,
    kupst_multiplier: float = 0.03,
    is_producer: bool = True,
    source: str | None = None,
    imbalance_discount: float = 0.0,
):
    imbalance = calculate_imbalance_cost(
        actual=actual,
        forecast=forecast,
        mcp=mcp,
        smp=smp,
        is_producer=is_producer,
        imbalance_discount=imbalance_discount,
    )

    kupst = calculate_kupst_cost(
        actual=actual,
        forecast=forecast,
        mcp=mcp,
        smp=smp,
        tol=tol,
        source=source,
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
    tol: float | None = None,
    source: str | None = None,
    kupst_multiplier: float = 0.03,
):
    """
    Calculates production plan difference (KUPST) costs.
    """

    if tol is None:
        if source is None:
            raise Exception("Either tol(erance) or source parameter must be provided")
        tol = get_kupst_tolerance(source)

    kupst_cost_list = []

    for x, y, m, s in zip(forecast_values, actual_values, mcp, smp):
        cost = max(abs(x - y) - tol * x, 0) * max(m, s) * kupst_multiplier

        kupst_cost_list.append(cost)

    return kupst_cost_list


def calculate_imbalance_cost_list(
    actual_values: list,
    forecast_values: list,
    cost_d: dict,
    is_producer: bool,
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
            cost = (y - x) * p if is_producer else n
        else:
            cost = (x - y) * n if is_producer else p

        imbalance_cost_list.append(cost * (1 - imbalance_discount))

    return imbalance_cost_list


def calculate_diff_costs_list(
    actual_values: list,
    forecast_values: list,
    mcp: list,
    smp: list,
    is_producer: bool,
    tol: float | None = None,
    source: str | None = None,
    kupst_multiplier: float = 0.03,
    imbalance_discount: float = 0,
):
    """
    Wrapper function to calculate all costs related to the difference between actual and forecasted values..
    """
    res_d = {"actual": actual_values, "forecast": forecast_values}

    cost_d = calculate_imbalance_cost_values_list(mcp, smp)
    res_d["diff"] = [x - y for x, y in zip(forecast_values, actual_values)]

    if is_producer:
        res_d["imbalance_direction"] = [
            "pos" if x < 0 else "neg" for x in res_d["diff"]
        ]
    else:
        res_d["imbalance_direction"] = [
            "pos" if x > 0 else "neg" for x in res_d["diff"]
        ]

    res_d["imbalance_cost"] = calculate_imbalance_cost_list(
        actual_values=actual_values,
        forecast_values=forecast_values,
        cost_d=cost_d,
        is_producer=is_producer,
        imbalance_discount=imbalance_discount,
    )

    if is_producer:
        res_d["kupst_cost"] = calculate_kupst_cost_list(
            actual_values=actual_values,
            forecast_values=forecast_values,
            mcp=mcp,
            smp=smp,
            tol=tol,
            source=source,
            kupst_multiplier=kupst_multiplier,
        )

    return res_d
