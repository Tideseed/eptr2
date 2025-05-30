def get_kupst_tolerance(source: str):
    alias_map = {"sun": "solar"}

    tol_source_map = {"wind": 0.17, "solar": 0.10}
    return tol_source_map.get(alias_map.get(source, source), 0.05)


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


def calculate_imbalance_amounts(
    actual: float,
    forecast: float,
    is_producer: bool,
    imb_tol: float = 0.1,
    dsg_absorption_rate: float = 0.0,
):
    """
    This function returns the imbalance amounts given actual and forecast values, imbalance tolerance and DSG absorption rate. DSG (Dengeden Sorumlu Grup / Balancing Responsible Group) can only absorb imbalances by the imb_tol proportion (default 10% as the regulatory standard). dsg_absorption_rate is the rate at which DSG absorbs imbalances. Anything above 10% imbalance is recorded as individual imbalance.

    For instance if actual is 100, forecast is 50 (current position) and dsg_absorption_rate is 0.5; DSG tolerance is 100*0.1 = 10Mwh (as gross imbalance is 50), DSG absorbed imbalance is 10*0.5 = 5Mwh, individual imbalance is 50-10 = 40 and total penalized imbalance is 5+40 = 45Mwh.
    """
    diff = forecast - actual

    if is_producer:
        diff = -diff

    imb_tol_value = round(actual * imb_tol, 1)

    sign = -1 if diff < 0 else 1

    dsg_imbalance = min(abs(diff), imb_tol_value) * sign
    net_dsg_imbalance = dsg_imbalance * (1 - dsg_absorption_rate)

    individual_imbalance = diff - dsg_imbalance

    res_d = {
        "diff": diff,
        "dsg_imbalance": dsg_imbalance,
        "net_dsg_imbalance": net_dsg_imbalance,
        "individual_imbalance": individual_imbalance,
        "imb_tol_value": imb_tol_value,
    }

    return res_d


def calculate_imb_cost(
    actual: float,
    forecast: float,
    mcp: float,
    smp: float,
    is_producer: bool,
    imb_tol: float = 0.1,
    return_detail: bool = False,
    dsg_absorption_rate: float = 0.0,
):

    ## Get the net costs of per imbalance MWh
    unit_cost_d = calculate_unit_imbalance_cost(mcp=mcp, smp=smp)

    ## Calculate the imbalance amounts
    res_d = calculate_imbalance_amounts(
        actual=actual,
        forecast=forecast,
        is_producer=is_producer,
        imb_tol=imb_tol,
        dsg_absorption_rate=dsg_absorption_rate,
    )

    dsg_imbalance = res_d["dsg_imbalance"]
    net_dsg_imbalance = res_d["net_dsg_imbalance"]
    individual_imbalance = res_d["individual_imbalance"]

    imb_side = "neg" if individual_imbalance < 0 else "pos"
    unit_cost = unit_cost_d[imb_side]

    dsg_imb_cost = abs(dsg_imbalance) * unit_cost
    net_dsg_imb_cost = abs(net_dsg_imbalance) * unit_cost
    individual_imb_cost = abs(individual_imbalance) * unit_cost
    total_imb_cost = individual_imb_cost + net_dsg_imb_cost

    if return_detail:
        return {
            "imbalances": res_d,
            "imb_side": imb_side,
            "costs": {
                "ind_imbalance_cost": individual_imb_cost,
                "dsg_imb_cost": dsg_imb_cost,
                "net_dsg_imb_cost": net_dsg_imb_cost,
                "total_imb_cost": total_imb_cost,
            },
        }
    else:
        return total_imb_cost


def calculate_imbalance_cost_deprecated(
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
    return_detail: bool = False,
):
    if tol is None:
        if source is None:
            raise Exception("Either tol(erance) or source parameter must be provided")
        tol = get_kupst_tolerance(source)

    tol_val = forecast * tol
    kupsm = max(0, abs(actual - forecast) - tol_val)
    unit_kupst = calculate_unit_kupst_cost(mcp, smp, kupst_multiplier)
    kupst_cost = kupsm * unit_kupst
    if return_detail:
        return {
            "kupst_tol_perc": tol,
            "kupsm_tol": tol_val,
            "kupsm": kupsm,
            "unit_kupst_cost": unit_kupst,
            "kupst_cost": kupst_cost,
        }

    return kupst_cost


def calculate_diff_cost(
    actual: float,
    forecast: float,
    mcp: float,
    smp: float,
    prod_source: str | None = None,
    imb_tol: float = 0.1,
    **kwargs
):
    is_producer = prod_source is not None

    res_d = calculate_imb_cost(
        actual=actual,
        forecast=forecast,
        mcp=mcp,
        smp=smp,
        is_producer=is_producer,
        imb_tol=imb_tol,
        dsg_absorption_rate=kwargs.get("dsg_absorption_rate", 0.0),
        return_detail=kwargs.get("return_detail", True),
    )

    if not kwargs.get("return_detail", True):
        res_d = {"total_imb_cost": res_d}

    if is_producer:
        kupst_d = calculate_kupst_cost(
            actual=actual,
            forecast=forecast,
            mcp=mcp,
            smp=smp,
            source=prod_source,
            tol=kwargs.get("kupst_tol", None),
            kupst_multiplier=kwargs.get("kupst_multiplier", 0.03),
            return_detail=kwargs.get("return_detail", True),
        )

        res_d["kupst"] = kupst_d

    return res_d


def calculate_diff_cost_deprecated(
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
    imbalance = calculate_imbalance_cost_deprecated(
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
    min_kupst: float = 750.0,
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
        cost = max(cost, min_kupst)

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
    min_kupst: float = 0.0,
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
            min_kupst=min_kupst,
        )

    return res_d
