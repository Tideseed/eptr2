from typing import Literal


def get_kupst_tolerance(source: str):
    alias_map = {"sun": "solar"}

    tol_source_map = {"wind": 0.17, "solar": 0.10}
    return tol_source_map.get(alias_map.get(source, source), 0.05)


def temp_get_draft_kupst_tolerance(source: str):
    """
    A temporary function to get the tolerance values based on source type according to the draft EPDK regulation (22 Sep 2025)
    """
    alias_map = {"sun": "solar"}

    tol_source_map = {"wind": 0.15, "solar": 0.08, "unlicensed": 0.2}
    return tol_source_map.get(alias_map.get(source, source), 0.05)


def temp_calculate_draft_unit_kupst_cost(
    mcp: float,
    smp: float,
    source: str | None = None,
    kupst_multiplier_default: float = 0.05,
    kupst_floor_price: float = 750.0,
    include_maintenance_penalty: bool = False,
):
    """
    A temporary function to get the unit kupst costs based on source type according to the draft EPDK regulation (22 Sep 2025)
    """

    kupst_multiplier = 0.08 if include_maintenance_penalty else kupst_multiplier_default
    if source is not None:
        source_map = {"battery": 0.1, "aggregator": 0.05, "unlicensed": 0.02}
        kupst_multiplier = source_map.get(source, kupst_multiplier_default)

    return max(mcp, smp, kupst_floor_price) * kupst_multiplier


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


def calculate_unit_kupst_cost(
    mcp: float,
    smp: float,
    kupst_multiplier: float = 0.03,
    kupst_floor_price: float = 750.0,
):
    return max(mcp, smp, kupst_floor_price) * kupst_multiplier


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


def calculate_kupsm(actual: float, forecast: float, tol: float):
    tol_val = forecast * tol
    kupsm = max(0, abs(forecast - actual) - tol_val)
    return kupsm


def calculate_kupsm_list(actual_values: list, forecast_values: list, tol: float):
    kupsm_list = []
    for a, f in zip(actual_values, forecast_values):
        kupsm_list.append(calculate_kupsm(a, f, tol))
    return kupsm_list


def calculate_kupst_cost(
    actual: float,
    forecast: float,
    mcp: float,
    smp: float,
    tol: float | None = None,
    source: str | None = None,
    kupst_multiplier: float = 0.03,
    kupst_floor_price: float = 750.0,
    return_detail: bool = False,
):
    if tol is None:
        if source is None:
            raise Exception("Either tol(erance) or source parameter must be provided")
        tol = get_kupst_tolerance(source)

    tol_val = forecast * tol
    kupsm = max(0, abs(actual - forecast) - tol_val)
    unit_kupst = calculate_unit_kupst_cost(
        mcp=mcp,
        smp=smp,
        kupst_multiplier=kupst_multiplier,
        kupst_floor_price=kupst_floor_price,
    )
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
    **kwargs,
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
            kupst_floor_price=kwargs.get("kupst_floor_price", 750.0),
            return_detail=kwargs.get("return_detail", True),
        )

        res_d["kupst"] = kupst_d

    return res_d


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
    kupst_floor_price: float = 750.0,
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
        cost = (
            max(abs(x - y) - tol * x, 0)
            * max(m, s, kupst_floor_price)
            * kupst_multiplier
        )

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
    kupst_floor_price: float = 750.0,
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
            kupst_floor_price=kupst_floor_price,
        )

    return res_d


def temp_calculate_imbalance_price_and_costs_new(
    mcp: float,
    smp: float,
    floor_price: float = 0.0,
    ceil_price: float = 3400.0,
    V: float = 150,
    B: float = 100,
    low_margin: float = 0.03,
    high_margin: float = 0.06,
    ceil_margin: float = 0.05,
    regulation: Literal["up", "down", "balanced"] = "balanced",
):
    """
    Temporary function to calculate imbalance prices based on new regulation (2026)

    mcp: Market Clearing Price (Day-ahead price) (PTF)
    smp: System Marginal Price (Real-time price) (SMF)
    floor_price: Price floor (0 TL/MWh)
    ceil_price: Price ceiling (3400 TL/MWh)
    V: Reference price for negative imbalance price calculation and positive imbalance threshold (150 TL/MWh)
    B: Reference price for positive imbalance price calculation (100 TL/MWh)
    low_margin: Margin for the opposite side of the imbalance (3%)
    high_margin: Margin for the same side of the imbalance (6%)
    ceil_margin: Additional margin applied when the maximum of mcp and smp is equal to ceil_price (5%)
    regulation: Direction of system regulation ("up", "down", "balanced") when mcp == smp
    """
    if mcp > smp:  ## system imbalance is positive
        neg_margin = low_margin
        pos_margin = high_margin
    elif mcp < smp:  ## system imbalance is negative
        neg_margin = high_margin
        pos_margin = low_margin
    elif mcp == ceil_price:  ## system imbalance is still negative
        neg_margin = high_margin
        pos_margin = low_margin
    elif mcp == floor_price:  ## system imbalance is still positive
        neg_margin = low_margin
        pos_margin = high_margin
    elif regulation == "up":  ## system imbalance is still negative
        neg_margin = high_margin
        pos_margin = low_margin
    elif regulation == "down":  ## system imbalance is still positive
        neg_margin = low_margin
        pos_margin = high_margin
    else:  ### system is balanced
        neg_margin = low_margin
        pos_margin = low_margin

    if max(mcp, smp) == ceil_price:
        neg_imb_mult = 1 + ceil_margin
    else:
        neg_imb_mult = 1

    neg_imb_price = max(mcp, smp, V) * (1 + neg_margin) * neg_imb_mult

    pos_imb_price_raw = min(mcp, smp)

    if pos_imb_price_raw < V:
        pos_imb_price = -B * (1 - pos_margin)
    else:
        pos_imb_price = pos_imb_price_raw * (1 - pos_margin)

    neg_imb_cost = neg_imb_price - mcp
    pos_imb_cost = mcp - pos_imb_price

    return {
        "mcp": mcp,
        "smp": smp,
        "pos_cost": pos_imb_cost,
        "neg_cost": neg_imb_cost,
        "pos_price": pos_imb_price,
        "neg_price": neg_imb_price,
    }
