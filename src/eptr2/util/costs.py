import warnings
from typing import Literal


def get_regulation_period_by_contract(contract: str):
    """
    Get the regulation period based on the contract date.
    Contracts starting from 2026-01-01 are considered under the 2026 regulation.
    """

    if contract < "PH26010100":
        return "pre_2026"
    elif contract >= "PH26010100":
        return "26_01"
    else:
        return "pre_2026"


def get_starting_contract_by_regulation_period(
    regulation_period: Literal["current", "26_01", "pre_2026"] = "current",
):
    """
    Get the starting contract codes based on the regulation period.
    """

    if regulation_period in ["current", "26_01"]:
        return "PH26010100"
    elif regulation_period == "pre_2026":
        return "PH15010100"
    else:
        raise ValueError(
            "Invalid period specified. Use 'current', '26_01' or 'pre_2026'."
        )


### KUPST TOLERANCE FUNCTIONS ###


def get_kupst_tolerance_by_contract(source: str, contract: str):
    """
    Using a contract code, get the KUPST tolerance for the given source.
    """
    regulation_period = get_regulation_period_by_contract(contract)
    return get_kupst_tolerance(source, regulation_period=regulation_period)


def get_kupst_tolerance(
    source: str, regulation_period: Literal["current", "26_01", "pre_2026"] = "current"
):
    """
    Wrapper function to get KUPST tolerance based on regulation period.
    """
    if regulation_period in ["current", "26_01"]:
        return get_kupst_tolerance_2026(source)
    elif regulation_period == "pre_2026":
        return get_kupst_tolerance_pre_2026(source)
    else:
        raise ValueError(
            "Invalid period specified. Use 'current', '26_01' or 'pre_2026'."
        )


def get_kupst_tolerance_pre_2026(source: str):
    """
    Get the tolerance values based on source type according to the EPDK regulation (pre-2026).
    """
    alias_map = {"sun": "solar"}

    tol_source_map = {"wind": 0.17, "solar": 0.10}
    return tol_source_map.get(alias_map.get(source, source), 0.05)


def get_kupst_tolerance_2026(source: str):
    """
    Get the tolerance values based on source type according to the EPDK regulation (valid from Jan 1, 2026).
    """
    alias_map = {"sun": "solar"}

    tol_source_map = {"wind": 0.15, "solar": 0.08, "unlicensed": 0.2}
    return tol_source_map.get(alias_map.get(source, source), 0.05)


### KUPST TOLERANCE FUNCTIONS END###


### KUPST COST FUNCTIONS ###
def calculate_unit_kupst_cost_by_contract(
    contract: str,
    mcp: float,
    smp: float,
    kupst_multiplier: float = None,
    kupst_floor_price: float = None,
    include_maintenance_penalty: bool = False,
):
    """
    Using a contract code, get the KUPST tolerance for the given source.
    """
    regulation_period = get_regulation_period_by_contract(contract)
    return calculate_unit_kupst_cost(
        mcp=mcp,
        smp=smp,
        kupst_multiplier=kupst_multiplier,
        kupst_floor_price=kupst_floor_price,
        include_maintenance_penalty=include_maintenance_penalty,
        regulation_period=regulation_period,
    )


def calculate_unit_kupst_cost(
    mcp: float,
    smp: float,
    kupst_multiplier: float = None,
    kupst_floor_price: float = None,
    include_maintenance_penalty: bool = False,
    regulation_period: Literal["current", "26_01", "pre_2026"] = "current",
    **kwargs,
):
    """
    Wrapper function to calculate unit KUPST costs based on regulation period.
    2026 regulation is effective from Jan 1, 2026.
    """
    if regulation_period in ["current", "26_01"]:
        if kupst_multiplier is None:
            kupst_multiplier = 0.08 if include_maintenance_penalty else 0.05

        if kupst_floor_price is None:
            kupst_floor_price = 750.0

        return calculate_unit_kupst_cost_2026(
            mcp=mcp,
            smp=smp,
            kupst_multiplier_default=kupst_multiplier,
            kupst_floor_price=kupst_floor_price,
            include_maintenance_penalty=include_maintenance_penalty,
        )
    elif regulation_period == "pre_2026":
        if kupst_multiplier is None:
            kupst_multiplier = 0.05 if include_maintenance_penalty else 0.03

        if kupst_floor_price is None:
            kupst_floor_price = 750.0

        return calculate_unit_kupst_cost_pre_2026(
            mcp=mcp,
            smp=smp,
            kupst_multiplier=kupst_multiplier,
            kupst_floor_price=kupst_floor_price,
        )
    else:
        raise ValueError(
            "Invalid period specified. Use 'current', '26_01' or 'pre_2026'."
        )


def temp_calculate_draft_unit_kupst_cost(
    mcp: float,
    smp: float,
    source: str | None = None,
    kupst_multiplier_default: float = 0.05,
    kupst_floor_price: float = 750.0,
    include_maintenance_penalty: bool = False,
):
    """
    .. deprecated:: 1.3.2
        Use :func:`calculate_unit_kupst_cost_2026` instead.
    """
    warnings.warn(
        "temp_calculate_draft_unit_kupst_cost is deprecated, "
        "use calculate_unit_kupst_cost_2026 instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return calculate_unit_kupst_cost_2026(
        mcp=mcp,
        smp=smp,
        source=source,
        kupst_multiplier_default=kupst_multiplier_default,
        kupst_floor_price=kupst_floor_price,
        include_maintenance_penalty=include_maintenance_penalty,
    )


def calculate_unit_kupst_cost_2026(
    mcp: float,
    smp: float,
    source: str | None = None,
    kupst_multiplier_default: float = 0.05,
    kupst_floor_price: float = 750.0,
    include_maintenance_penalty: bool = False,
):
    """
    Calculate unit KUPST costs based on source type according to the EPDK regulation (2026).
    Based on draft regulation published 22 Sep 2025.
    """

    kupst_multiplier = 0.08 if include_maintenance_penalty else kupst_multiplier_default
    if source is not None:
        source_map = {"battery": 0.1, "aggregator": 0.05, "unlicensed": 0.02}
        kupst_multiplier = source_map.get(source, kupst_multiplier_default)

    return max(mcp, smp, kupst_floor_price) * kupst_multiplier


def calculate_unit_kupst_cost_pre_2026(
    mcp: float,
    smp: float,
    kupst_multiplier: float = 0.03,
    kupst_floor_price: float = 750.0,
):
    """
    KUPST unit cost calculation according to EPDK regulation (pre-2026).
    3% of the maximum of MCP, SMP and floor price.
    750 TL/MWh floor price is used if higher.
    """
    return max(mcp, smp, kupst_floor_price) * kupst_multiplier


def calculate_kupsm(actual: float, forecast: float, tol: float):
    """
    Calculate the KÜPSM (Kesinleşmiş Üretim Planından Sapma Miktarı) given actual and forecast values and tolerance.
    """
    tol_val = forecast * tol
    kupsm = max(0, abs(forecast - actual) - tol_val)
    return kupsm


def calculate_kupst_cost_by_contract(
    contract: str,
    actual: float,
    forecast: float,
    mcp: float,
    smp: float,
    tol: float | None = None,
    source: str | None = None,
    kupst_multiplier: float | None = None,
    kupst_floor_price: float | None = None,
    return_detail: bool = False,
    include_maintenance_penalty=False,
):
    """
    Using a contract code, get the KUPST tolerance for the given source.
    """
    regulation_period = get_regulation_period_by_contract(contract)
    return calculate_kupst_cost(
        actual=actual,
        forecast=forecast,
        mcp=mcp,
        smp=smp,
        tol=tol,
        source=source,
        kupst_multiplier=kupst_multiplier,
        kupst_floor_price=kupst_floor_price,
        return_detail=return_detail,
        regulation_period=regulation_period,
        include_maintenance_penalty=include_maintenance_penalty,
    )


def calculate_kupst_cost(
    actual: float,
    forecast: float,
    mcp: float,
    smp: float,
    tol: float | None = None,
    source: str | None = None,
    kupst_multiplier: float | None = None,
    kupst_floor_price: float | None = None,
    return_detail: bool = False,
    regulation_period: Literal["current", "2026_01", "pre_2026"] = "current",
    include_maintenance_penalty=False,
):
    if tol is None:
        if source is None:
            raise Exception("Either tol(erance) or source parameter must be provided")
        tol = get_kupst_tolerance(source=source, regulation_period=regulation_period)

    kupsm = calculate_kupsm(actual=actual, forecast=forecast, tol=tol)

    unit_kupst = calculate_unit_kupst_cost(
        mcp=mcp,
        smp=smp,
        kupst_multiplier=kupst_multiplier,
        kupst_floor_price=kupst_floor_price,
        regulation_period=regulation_period,
        include_maintenance_penalty=include_maintenance_penalty,
    )
    kupst_cost = kupsm * unit_kupst

    if return_detail:
        detail_d = {
            "kupst_tol_perc": tol,
            "kupsm_tol": tol,
            "kupsm": kupsm,
            "unit_kupst_cost": unit_kupst,
            "kupst_cost": kupst_cost,
        }
        return detail_d

    return kupst_cost


def calculate_kupst_cost_list(
    actual_values: list,
    forecast_values: list,
    mcp: list,
    smp: list,
    tol: float | None = None,
    source: str | None = None,
    kupst_multiplier: float | None = None,
    kupst_floor_price: float | None = None,
    regulation_period: Literal["current", "2026_01", "pre_2026"] = "current",
    **kwargs,
):
    """
    Calculates production plan difference (KUPST) costs.
    """

    if tol is None:
        if source is None:
            raise Exception("Either tol(erance) or source parameter must be provided")
        tol = get_kupst_tolerance(source)

    maintenance_penalty_list = kwargs.get(
        "maintenance_penalty_list", [False] * len(actual_values)
    )

    kupst_cost_list = []

    for x, y, m, s, p in zip(
        forecast_values, actual_values, mcp, smp, maintenance_penalty_list
    ):
        cost = calculate_kupst_cost(
            actual=y,
            forecast=x,
            mcp=m,
            smp=s,
            tol=tol,
            source=source,
            kupst_multiplier=kupst_multiplier,
            kupst_floor_price=kupst_floor_price,
            regulation_period=regulation_period,
            include_maintenance_penalty=p,
            return_detail=False,
        )

        kupst_cost_list.append(cost)

    return kupst_cost_list


### KUPST COST FUNCTIONS END###


### UNIT IMBALANCE PRICE AND COST FUNCTIONS START###
### UNIT IMBALANCE PRICE FUNCTIONS START###
def calculate_unit_imbalance_price_by_contract(
    contract: str,
    mcp: float,
    smp: float,
    **kwargs,
):
    """
    Wrapper function to calculate unit imbalance prices based on contract.
    """

    regulation_period = get_regulation_period_by_contract(contract)

    d = calculate_unit_imbalance_price(
        mcp=mcp,
        smp=smp,
        regulation_period=regulation_period,
        **kwargs,
    )

    return d


def calculate_unit_imbalance_price(
    mcp: float,
    smp: float,
    regulation_period: Literal["current", "2026_01", "pre_2026"] = "current",
    **kwargs,
):
    """
    Wrapper function to calculate unit imbalance prices based on regulation period.
    2026 regulation is effective from Jan 1, 2026.
    """

    if regulation_period in ["current", "26_01"]:
        d = calculate_unit_imbalance_price_2026(mcp=mcp, smp=smp, **kwargs)
    elif regulation_period == "pre_2026":
        d = calculate_unit_imbalance_price_pre_2026(
            mcp=mcp,
            smp=smp,
            **{k: v for k, v in kwargs.items() if k in ["penalty_margin"]},
        )

    return d


def calculate_unit_imbalance_price_2026(
    mcp: float,
    smp: float,
    floor_price: float = 0.0,
    ceil_price: float = 3400.0,
    V: float = 150,
    B: float = 100,
    low_margin: float = 0.03,
    high_margin: float = 0.06,
    ceil_margin: float = 0.05,
    **kwargs,
):
    """
    Function to calculate imbalance prices based on new regulation (2026)

    mcp: Market Clearing Price (Day-ahead price) (PTF)
    smp: System Marginal Price (Real-time price) (SMF)
    floor_price: Price floor (0 TL/MWh)
    ceil_price: Price ceiling (3400 TL/MWh)
    V: Reference price for negative imbalance price calculation and positive imbalance threshold (150 TL/MWh)
    B: Reference price for positive imbalance price calculation (100 TL/MWh)
    low_margin: Margin for the opposite side of the imbalance (3%)
    high_margin: Margin for the same side of the imbalance (6%)
    ceil_margin: Additional margin applied when the maximum of mcp and smp is equal to ceil_price (5%)
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

    if max(mcp, smp) == ceil_price:
        neg_imb_mult = 1 + ceil_margin
    else:
        neg_imb_mult = 1

    neg_imb_price = max(mcp, smp, V) * (1 + neg_margin) * neg_imb_mult

    pos_imb_price_raw = min(mcp, smp)

    if pos_imb_price_raw < V:
        pos_imb_price = -B * (1 + pos_margin)
    else:
        pos_imb_price = pos_imb_price_raw * (1 - pos_margin)

    return {
        "pos": pos_imb_price,
        "neg": neg_imb_price,
    }


def calculate_unit_imbalance_price_pre_2026(
    mcp: float, smp: float, penalty_margin: float = 0.03
):
    """
    Calculates imbalance prices for positive and negative imbalances based on pre-2026 regulation. Much simplified compared to 2026 regulation.
    """
    d = {
        "pos": (1 - penalty_margin) * min(mcp, smp),
        "neg": (1 + penalty_margin) * max(mcp, smp),
    }
    return d


### UNIT IMBALANCE PRICE FUNCTIONS END###
### UNIT IMBALANCE COST FUNCTIONS START###


def calculate_unit_imbalance_cost_by_contract(
    contract: str,
    mcp: float,
    smp: float,
    include_prices: bool = False,
    **kwargs,
):
    """
    Using a contract code, get the regulation period and calculate unit imbalance costs automatically.
    """

    regulation_period = get_regulation_period_by_contract(contract)

    return calculate_unit_imbalance_cost(
        mcp=mcp,
        smp=smp,
        include_prices=include_prices,
        regulation_period=regulation_period,
        **kwargs,
    )


def calculate_unit_imbalance_cost(
    mcp: float,
    smp: float,
    include_prices: bool = False,
    regulation_period: Literal["current", "2026_01", "pre_2026"] = "current",
    **kwargs,
):
    """
    Wrapper function to calculate unit imbalance prices based on regulation period.
    2026 regulation is effective from Jan 1, 2026.
    """

    if regulation_period in ["current", "26_01"]:
        d = calculate_unit_imbalance_cost_2026(
            mcp=mcp, smp=smp, include_prices=include_prices, **kwargs
        )
    elif regulation_period == "pre_2026":
        d = calculate_unit_imbalance_cost_pre_2026(
            mcp=mcp,
            smp=smp,
            include_prices=include_prices,
            **{k: v for k, v in kwargs.items() if k in ["penalty_margin"]},
        )

    return d


def calculate_unit_imbalance_cost_2026(
    mcp: float,
    smp: float,
    floor_price: float = 0.0,
    ceil_price: float = 3400.0,
    V: float = 150,
    B: float = 100,
    low_margin: float = 0.03,
    high_margin: float = 0.06,
    ceil_margin: float = 0.05,
    include_prices: bool = False,
    **kwargs,
):
    price_d = calculate_unit_imbalance_price_2026(
        mcp=mcp,
        smp=smp,
        floor_price=floor_price,
        ceil_price=ceil_price,
        V=V,
        B=B,
        low_margin=low_margin,
        high_margin=high_margin,
        ceil_margin=ceil_margin,
        **kwargs,
    )

    neg_imb_cost = price_d["neg"] - mcp
    pos_imb_cost = mcp - price_d["pos"]

    cost_d = {
        "pos": pos_imb_cost,
        "neg": neg_imb_cost,
    }

    if include_prices:
        cost_d = {k + "_cost": v for k, v in cost_d.items()}
        cost_d = {"pos_price": price_d["pos"], "neg_price": price_d["neg"], **cost_d}

    return cost_d


def calculate_unit_imbalance_cost_pre_2026(
    mcp: float, smp: float, penalty_margin: float = 0.03, include_prices: bool = False
):
    """
    Calculates imbalance costs for positive and negative imbalances based on pre-2026 regulation. Much simplified compared to 2026 regulation.
    """

    d = calculate_unit_imbalance_price_pre_2026(
        mcp=mcp, smp=smp, penalty_margin=penalty_margin
    )

    pos_imb_cost = mcp - d["pos"]
    neg_imb_cost = d["neg"] - mcp

    if include_prices:
        cost_d = {"pos_cost": pos_imb_cost, "neg_cost": neg_imb_cost}
        cost_d = {"pos_price": d["pos"], "neg_price": d["neg"], **cost_d}
    else:
        cost_d = {"pos": pos_imb_cost, "neg": neg_imb_cost}

    return cost_d


def calculate_unit_price_and_costs_by_contract(
    contract: str,
    mcp: float,
    smp: float,
    include_kupst: bool = True,
    **kwargs,
):
    """
    Using a contract code, get the regulation period and calculate unit imbalance prices and costs automatically.
    """
    regulation_period = get_regulation_period_by_contract(contract=contract)

    res = calculate_unit_price_and_costs(
        mcp=mcp,
        smp=smp,
        include_kupst=include_kupst,
        regulation_period=regulation_period,
        **kwargs,
    )

    return res


def calculate_unit_price_and_costs(
    mcp: float,
    smp: float,
    include_kupst: bool = True,
    regulation_period: Literal["current", "2026_01", "pre_2026"] = "current",
    **kwargs,
):
    """
    Wrapper function to calculate unit imbalance prices and costs based on regulation period.
    2026 regulation is effective from Jan 1, 2026.
    """

    if regulation_period in ["current", "26_01"]:
        d = calculate_unit_imbalance_cost_2026(
            mcp=mcp, smp=smp, include_prices=True, **kwargs
        )
        if include_kupst:
            unit_kupst = calculate_unit_kupst_cost_2026(
                mcp=mcp,
                smp=smp,
                kupst_floor_price=kwargs.get("kupst_floor_price", 750.0),
                kupst_multiplier_default=kwargs.get("kupst_multiplier", 0.05),
                include_maintenance_penalty=kwargs.get(
                    "include_maintenance_penalty", False
                ),
            )
            d["unit_kupst"] = unit_kupst

    elif regulation_period == "pre_2026":
        d = calculate_unit_imbalance_cost_pre_2026(
            mcp=mcp,
            smp=smp,
            include_prices=True,
            **{k: v for k, v in kwargs.items() if k in ["penalty_margin"]},
        )

        if include_kupst:
            unit_kupst = calculate_unit_kupst_cost_pre_2026(
                mcp=mcp,
                smp=smp,
                kupst_floor_price=kwargs.get("kupst_floor_price", 750.0),
                kupst_multiplier=kwargs.get("kupst_multiplier", 0.03),
            )
            d["unit_kupst"] = unit_kupst

    return d


### UNIT IMBALANCE COST FUNCTIONS END###
### UNIT IMBALANCE PRICE AND COST FUNCTIONS END###


def calculate_imbalance_amount(
    actual: float,
    forecast: float,
    is_producer: bool,
    tolerance_multiplier: float = 1.0,
    just_raw_imbalance: bool = False,
    regulation_period: Literal["current", "2026_01", "pre_2026"] = "current",
    **kwargs,
) -> dict | float:
    """
    This function returns the imbalance amount given actual and forecast values. Imbalance sign is the same with the wording. Positive imbalance means a positive value and negative imbalance means a negative value. If is_producer, then actual > forecast means positive imbalance. Else (i.e. a demand/consumption unit) actual < forecast means positive imbalance. For negative imbalance, the opposite logic applies.

    DSG (Dengeden Sorumlu Grup / Balancing Responsible Group) can absorb imbalances by the dsg_tolerance proportion (default 5% as the regulatory standard). tolerance_multiplier can be used to adjust the effective tolerance. For instance, if tolerance_multiplier is 0.5, then only half of the DSG tolerance is considered effective.

    Parameters:
    actual: Actual measured value (MWh)
    forecast: Forecasted/planned value (MWh)
    is_producer: True if the unit is a producer, False if it is a consumer
    dsg_tolerance: DSG tolerance proportion (default 0.05 for 5%)
    tolerance_multiplier: Multiplier for the DSG tolerance to get effective tolerance (default 1.0)
    just_raw_imbalance: If True, only the raw imbalance is returned (no tolerance calculations)

    Returns:
    dict: A dictionary containing raw imbalance, DSG raw tolerance, DSG raw imbalance, DSG effective tolerance, and DSG effective imbalance.
    float: If just_raw_imbalance is True, returns only the raw imbalance as a float.
    """

    if kwargs.get("dsg_tolerance") is not None:
        dsg_tolerance = kwargs.get("dsg_tolerance")
    else:
        if regulation_period in ["current", "26_01"]:
            dsg_tolerance = 0.05
        elif regulation_period == "pre_2026":
            dsg_tolerance = 0.1

    if is_producer:
        raw_imb = actual - forecast
    else:
        raw_imb = forecast - actual

    if just_raw_imbalance:
        return raw_imb

    dsg_raw_tolerance = abs(actual) * dsg_tolerance
    dsg_effective_tolerance = dsg_raw_tolerance * tolerance_multiplier

    if raw_imb < 0:
        dsg_raw_imb = min(raw_imb + dsg_raw_tolerance, 0)
        dsg_effective_imb = min(raw_imb + dsg_effective_tolerance, 0)
    else:
        dsg_raw_imb = max(raw_imb - dsg_raw_tolerance, 0)
        dsg_effective_imb = max(raw_imb - dsg_effective_tolerance, 0)

    d = {
        "raw_imb": raw_imb,
        "dsg_raw_tol": dsg_raw_tolerance,
        "dsg_raw_imb": dsg_raw_imb,
        "dsg_eff_tol": dsg_effective_tolerance,
        "dsg_eff_imb": dsg_effective_imb,
    }

    return d


def calculate_diff_costs(
    forecast: float,
    actual: float,
    is_producer: bool,
    mcp: float,
    smp: float,
    production_source: str | None = None,
    regulation_period: Literal["current", "2026_01", "pre_2026"] | None = "current",
    include_quantities: bool = False,
    **kwargs,
) -> dict | float:
    """
    Calculates imbalance and kupst costs for given actual and forecast values.
    """

    signed_imb_qty = calculate_imbalance_amount(
        actual=actual,
        forecast=forecast,
        is_producer=is_producer,
        just_raw_imbalance=True,
        regulation_period=regulation_period,
    )

    if is_producer:
        if production_source is None:
            raise Exception("production_source must be provided for producers")

        kupst_tol = get_kupst_tolerance(
            source=production_source if production_source is not None else "default",
            regulation_period=regulation_period,
        )
        kupsm = calculate_kupsm(tol=kupst_tol, actual=actual, forecast=forecast)

    cost_d = calculate_unit_price_and_costs(
        mcp=mcp,
        smp=smp,
        regulation_period=regulation_period,
        include_kupst=True,
        **kwargs,
    )

    imb_cost = (
        abs(signed_imb_qty) * cost_d["neg_cost" if signed_imb_qty < 0 else "pos_cost"]
    )

    ### Hidden option to return only imbalance cost as a float
    if kwargs.get("return_imbalance_cost", False):
        return imb_cost

    d = {
        "imb_cost": imb_cost,
    }

    if is_producer:
        kupst = kupsm * cost_d["unit_kupst"] if is_producer else 0.0
        total_cost = imb_cost + kupst
        d["kupst_cost"] = kupst
        d["total_cost"] = total_cost

    if include_quantities:
        d["imb_qty"] = signed_imb_qty
        if is_producer:
            d["kupsm"] = kupsm

    return d


#####
### DEPRECATED FUNCTIONS BELOW
#####


def calculate_imb_cost_pre_2026(
    actual: float,
    forecast: float,
    mcp: float,
    smp: float,
    is_producer: bool,
    imb_tol: float = 0.1,
    return_detail: bool = False,
    dsg_absorption_rate: float = 0.0,
):
    """
    .. deprecated:: 1.3.3
        This function will be removed in version 1.4.0.
        Use :func:`calculate_unit_imbalance_cost_pre_2026` and :func:`calculate_imbalance_amounts_pre_2026` instead.
    """
    warnings.warn(
        "calculate_imb_cost_pre_2026 is deprecated and will be removed in version 1.4.0. "
        "Use calculate_unit_imbalance_cost_pre_2026 and calculate_imbalance_amounts_pre_2026 instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    ## Get the net costs of per imbalance MWh
    unit_cost_d = calculate_unit_imbalance_cost_pre_2026(mcp=mcp, smp=smp)

    ## Calculate the imbalance amounts
    res_d = calculate_imbalance_amounts_pre_2026(
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


def calculate_imbalance_amounts_pre_2026(
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


def calculate_diff_cost_pre_2026(
    actual: float,
    forecast: float,
    mcp: float,
    smp: float,
    prod_source: str | None = None,
    imb_tol: float = 0.1,
    **kwargs,
):
    """
    .. deprecated:: 1.3.3
        This function will be removed in version 1.4.0.
        Use :func:`calculate_imb_cost_pre_2026` and :func:`calculate_kupst_cost` instead.
    """
    warnings.warn(
        "calculate_diff_cost_pre_2026 is deprecated and will be removed in version 1.4.0. "
        "Use calculate_imb_cost_pre_2026 and calculate_kupst_cost instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    is_producer = prod_source is not None

    res_d = calculate_imb_cost_pre_2026(
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


def calculate_imbalance_cost_list(
    actual_values: list,
    forecast_values: list,
    cost_d: dict,
    is_producer: bool,
    imbalance_discount: float = 0.0,
):
    """
    .. deprecated:: 1.3.3
        Use singular unit functions with list comprehension instead.
        This function will be removed in a future version.

    Calculates imbalance costs for a given forecast and actual values.
    Imbalance dampening reduces imbalance costs by the given rate (<1). It is used to emulate balance responsible party (DSG) effect.
    """
    warnings.warn(
        "calculate_imbalance_cost_list is deprecated and will be removed in a future version. "
        "Use calculate_unit_imbalance_cost with list comprehension instead.",
        DeprecationWarning,
        stacklevel=2,
    )

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
    .. deprecated:: 1.3.3
        Use individual unit functions with list comprehension instead.
        This function will be removed in a future version.

    Wrapper function to calculate all costs related to the difference between actual and forecasted values.
    """
    warnings.warn(
        "calculate_diff_costs_list is deprecated and will be removed in a future version. "
        "Use calculate_unit_imbalance_cost and calculate_kupst_cost with list comprehension instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    res_d = {"actual": actual_values, "forecast": forecast_values}

    cost_d = calculate_imbalance_cost_values_list_pre_2026(mcp, smp)
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


def calculate_imbalance_cost_values_list_pre_2026(mcp: list, smp: list):
    """
    .. deprecated:: 1.3.3
        In further versions, please use the singular unit functions and make your own list comprehension.

    Calculates imbalance costs relative to day-ahead prices (MCP) for positive and negative imbalances
    """
    warnings.warn(
        "calculate_imbalance_cost_values_list_pre_2026 is deprecated, "
        "In further versions, please use the singular unit functions.",
        DeprecationWarning,
        stacklevel=2,
    )

    d = {"pos": [], "neg": []}

    for mcp_x, smp_x in zip(mcp, smp):
        if mcp_x is None or smp_x is None:
            raise ValueError("MCP and SMP lists must not contain None values")
        sub_d = calculate_unit_imbalance_cost_pre_2026(mcp=mcp_x, smp=smp_x)
        d["pos"].append(sub_d["pos"])
        d["neg"].append(sub_d["neg"])

    return d


def temp_get_draft_kupst_tolerance(source: str):
    """
    .. deprecated:: 1.3.2
        Use :func:`get_kupst_tolerance_2026` instead.
    """
    warnings.warn(
        "temp_get_draft_kupst_tolerance is deprecated, "
        "use get_kupst_tolerance_2026 instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return get_kupst_tolerance_2026(source)


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
    .. deprecated:: 1.3.2
        Use :func:`calculate_imbalance_price_and_costs_2026` instead.
    """
    warnings.warn(
        "temp_calculate_imbalance_price_and_costs_new is deprecated, "
        "use calculate_imbalance_price_and_costs_2026 instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return calculate_imbalance_price_and_costs_2026(
        mcp=mcp,
        smp=smp,
        floor_price=floor_price,
        ceil_price=ceil_price,
        V=V,
        B=B,
        low_margin=low_margin,
        high_margin=high_margin,
        ceil_margin=ceil_margin,
        regulation=regulation,
    )


def calculate_imbalance_price_and_costs_2026(
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
    .. deprecated:: 1.3.3
        Use :func:`calculate_unit_price_and_costs` instead.

    Function to calculate imbalance prices based on new regulation (2026)

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
    warnings.warn(
        "calculate_imbalance_price_and_costs_2026 is deprecated, "
        "use calculate_unit_price_and_costs instead",
        DeprecationWarning,
        stacklevel=2,
    )

    price_cost_d = calculate_unit_imbalance_cost_2026(
        mcp=mcp,
        smp=smp,
        floor_price=floor_price,
        ceil_price=ceil_price,
        V=V,
        B=B,
        low_margin=low_margin,
        high_margin=high_margin,
        ceil_margin=ceil_margin,
        imb_side=regulation,
        include_prices=True,
    )

    price_cost_d["mcp"] = mcp
    price_cost_d["smp"] = smp

    return price_cost_d


def calculate_imbalance_prices_list_pre_2026(mcp: list, smp: list):
    """
    .. deprecated:: 1.3.3
        In further versions, please use the singular unit functions and make your own list comprehension.

    Calculates imbalance prices for positive and negative imbalances
    """
    warnings.warn(
        "calculate_imbalance_prices_list_pre_2026 is deprecated, "
        "In further versions, please use the singular unit functions.",
        DeprecationWarning,
        stacklevel=2,
    )
    d = {
        "pos": [min(x, y) * 0.97 for x, y in zip(mcp, smp)],
        "neg": [1.03 * max(x, y) for x, y in zip(mcp, smp)],
    }

    return d


def calculate_kupsm_list(actual_values: list, forecast_values: list, tol: float):
    """
    .. deprecated:: 1.3.3
        Use list comprehension with :func:`calculate_kupsm` instead.
        This function will be removed in version 1.4.0.

    Calculate the KÜPSM (Kesinleşmiş Üretim Planından Sapma Miktarı) list given actual and forecast values and tolerance value.
    """
    warnings.warn(
        "calculate_kupsm_list is deprecated and will be removed in version 1.4.0. "
        "Use list comprehension with calculate_kupsm instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    kupsm_list = []
    for a, f in zip(actual_values, forecast_values):
        kupsm_list.append(calculate_kupsm(a, f, tol))
    return kupsm_list
