import warnings
from typing import Literal


def get_regulation_period_by_contract(contract: str):
    """
    Determine the regulation period from a contract code.

    The Turkish electricity market regulations changed on January 1, 2026.
    Contract codes are lexicographically ordered by date, allowing for direct comparison.

    Parameters
    ----------
    contract : str
        Contract code in format 'PHYYMMDDhh' (e.g., 'PH26010100' for 2026-01-01 00:00).

    Returns
    -------
    str
        Either 'pre_2026' for contracts before 2026-01-01, or '26_01' for 2026 onwards.

    Examples
    --------
    >>> get_regulation_period_by_contract('PH25123100')
    'pre_2026'
    >>> get_regulation_period_by_contract('PH26010100')
    '26_01'
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
    Get the first contract code for a given regulation period.

    Parameters
    ----------
    regulation_period : {'current', '26_01', 'pre_2026'}, default 'current'
        The regulation period. 'current' and '26_01' both refer to 2026 regulation.

    Returns
    -------
    str
        The first contract code of the period:
        - '26_01'/'current': 'PH26010100' (2026 regulation)
        - 'pre_2026': 'PH15010100' (pre-2026 regulation)

    Raises
    ------
    ValueError
        If regulation_period is invalid.

    Examples
    --------
    >>> get_starting_contract_by_regulation_period('current')
    'PH26010100'
    >>> get_starting_contract_by_regulation_period('pre_2026')
    'PH15010100'
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


def get_kupst_tolerance_by_contract(
    contract: str,
    source: Literal["wind", "solar", "sun", "unlicensed", "other"] = "other",
):
    """
    Get KUPST tolerance for a given source and contract code.

    KUPST (Kesinlestirilmis Uretim Planından Sapma Tutarı - Production Plan Deviation Cost)
    tolerance determines the allowable deviation between forecasted and actual production
    before deviation costs are applied.

    Parameters
    ----------
    source : {'wind', 'solar', 'sun', 'unlicensed', 'other'}, default 'other'
        Energy source type. 'sun' is aliased to 'solar'.
    contract : str
        Contract code to determine the applicable regulation period.

    Returns
    -------
    float
        Tolerance as a decimal (e.g., 0.15 for 15%). Higher values allow larger deviations.

    Notes
    -----
    Tolerance values differ by regulation period:
    - Wind: 17% (pre-2026) → 15% (2026+)
    - Solar: 10% (pre-2026) → 8% (2026+)
    - Default: 5% for sources not specifically listed

    Examples
    --------
    >>> get_kupst_tolerance_by_contract('wind', 'PH26010100')
    0.15
    >>> get_kupst_tolerance_by_contract('wind', 'PH25123100')
    0.17
    """
    regulation_period = get_regulation_period_by_contract(contract)
    return get_kupst_tolerance(source, regulation_period=regulation_period)


def get_kupst_tolerance(
    source: Literal["wind", "solar", "sun", "unlicensed", "other"] = "other",
    regulation_period: Literal["current", "26_01", "pre_2026"] = "current",
):
    """
    Get KUPST tolerance for a given source and regulation period.

    This is a dispatcher function that selects the appropriate tolerance calculation
    based on the regulation period and delegates to regulation-specific implementations.

    Parameters
    ----------
    source : {'wind', 'solar', 'sun', 'unlicensed', 'other'}, default 'other'
        Energy source type. 'sun' is aliased to 'solar'.
    regulation_period : {'current', '26_01', 'pre_2026'}, default 'current'
        The regulation period. 'current' and '26_01' both refer to 2026 regulation.

    Returns
    -------
    float
        Tolerance as a decimal (e.g., 0.15 for 15%).

    Raises
    ------
    ValueError
        If regulation_period is not one of the valid values.

    Examples
    --------
    >>> get_kupst_tolerance('wind', 'current')
    0.15
    >>> get_kupst_tolerance('wind', 'pre_2026')
    0.17
    """
    if regulation_period in ["current", "26_01"]:
        return get_kupst_tolerance_2026(source)
    elif regulation_period == "pre_2026":
        return get_kupst_tolerance_pre_2026(source)
    else:
        raise ValueError(
            "Invalid period specified. Use 'current', '26_01' or 'pre_2026'."
        )


def get_kupst_tolerance_pre_2026(
    source: Literal["wind", "solar", "sun", "other"] = "other",
):
    """
    Get KUPST tolerance for pre-2026 EPDK regulation.

    Parameters
    ----------
    source : {'wind', 'solar', 'sun', 'other'}, default 'other'
        Energy source type.

    Returns
    -------
    float
        Tolerance value as decimal:
        - Wind: 17% (0.17)
        - Solar/Sun: 10% (0.10)
        - Other sources: 5% (0.05, default)

    Notes
    -----
    Source 'sun' is aliased to 'solar' for convenience.
    """
    alias_map = {"sun": "solar"}

    tol_source_map = {"wind": 0.17, "solar": 0.10}
    return tol_source_map.get(alias_map.get(source, source), 0.05)


def get_kupst_tolerance_2026(
    source: Literal["wind", "solar", "sun", "unlicensed", "other"] = "other",
):
    """
    Get KUPST tolerance for 2026 EPDK regulation (effective 2026-01-01).

    Parameters
    ----------
    source : {'wind', 'solar', 'sun', 'unlicensed', 'other'}, default 'other'
        Energy source type.

    Returns
    -------
    float
        Tolerance value as decimal:
        - Wind: 15% (0.15)
        - Solar/Sun: 8% (0.08)
        - Unlicensed: 20% (0.20)
        - Other sources: 5% (0.05, default)

    Notes
    -----
    Source 'sun' is aliased to 'solar' for convenience.
    The 2026 regulation tightened tolerances for wind and solar,
    while introducing a higher tolerance for unlicensed production.
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
    Calculate unit KUPST (Production Plan Deviation Cost) per MWh based on regulation period.

    This function dispatches to regulation-specific implementations and returns the cost per
    MWh of deviation. The cost is calculated as a multiplier of the maximum of MCP and SMP,
    with a floor price applied.

    Parameters
    ----------
    mcp : float
        Market Clearing Price (day-ahead market price) in TL/MWh.
    smp : float
        System Marginal Price (real-time/balancing price) in TL/MWh.
    kupst_multiplier : float, optional
        Multiplier for KUPST cost calculation. Defaults based on regulation period and
        maintenance penalty status:
        - 2026 regulation: 0.05 (0.08 with maintenance penalty)
        - Pre-2026 regulation: 0.03 (0.05 with maintenance penalty)
    kupst_floor_price : float, optional
        Floor price for KUPST calculation in TL/MWh. Default is 750.0 TL/MWh.
    include_maintenance_penalty : bool, default False
        If True, applies higher multiplier (maintenance penalty rate) to reflect
        additional deviation costs from lack of maintenance.
    regulation_period : {'current', '26_01', 'pre_2026'}, default 'current'
        Regulation period. 'current' and '26_01' both refer to 2026 regulation.
    **kwargs
        Additional keyword arguments (unused, for compatibility).

    Returns
    -------
    float
        Unit KUPST cost in TL/MWh.

    Raises
    ------
    ValueError
        If regulation_period is not one of the valid values.

    Notes
    -----
    The calculation follows:
    unit_kupst = max(mcp, smp, floor_price) * multiplier

    Multiplier values differ by regulation period and maintenance penalty:
    - 2026 regulation: 5% (8% maintenance) of the maximum reference price
    - Pre-2026 regulation: 3% (5% maintenance) of the maximum reference price

    Examples
    --------
    >>> calculate_unit_kupst_cost(mcp=100, smp=110, regulation_period='current')
    5.5
    >>> calculate_unit_kupst_cost(mcp=100, smp=110, include_maintenance_penalty=True, regulation_period='current')
    8.8
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
    Calculate KUPST (Production Plan Deviation Cost) using a contract code.

    This function determines the regulation period from the contract code and calculates
    the total KUPST cost based on the deviation between actual and forecasted production.

    Parameters
    ----------
    contract : str
        Contract code in format 'PHYYMMDDhh' (e.g., 'PH26010100'). Used to determine
        the applicable regulation period.
    actual : float
        Actual generated production in MWh.
    forecast : float
        Forecasted/planned production in MWh.
    mcp : float
        Market Clearing Price in TL/MWh.
    smp : float
        System Marginal Price in TL/MWh.
    tol : float, optional
        KUPST tolerance as a decimal (e.g., 0.15 for 15%). If None, calculated from source.
    source : str, optional
        Energy source type (e.g., 'wind', 'solar', 'hydro'). Required if tol is None.
    kupst_multiplier : float, optional
        Multiplier for unit KUPST calculation. If None, uses regulation default.
    kupst_floor_price : float, optional
        Floor price for KUPST calculation in TL/MWh. Default 750.0 TL/MWh.
    return_detail : bool, default False
        If True, returns dictionary with breakdown of tolerance, deviation, unit cost, and total cost.
        If False, returns only the total KUPST cost.
    include_maintenance_penalty : bool, default False
        If True, applies maintenance penalty to multiplier.

    Returns
    -------
    float or dict
        If return_detail=False: Total KUPST cost in TL.
        If return_detail=True: Dictionary with keys:
        - 'kupst_tol_perc': Applied tolerance percentage
        - 'kupsm': Production plan deviation (after tolerance) in MWh
        - 'unit_kupst_cost': KUPST cost per MWh in TL/MWh
        - 'kupst_cost': Total KUPST cost in TL

    Raises
    ------
    Exception
        If neither tol nor source is provided.
    ValueError
        If contract code is invalid.

    Examples
    --------
    >>> calculate_kupst_cost_by_contract(
    ...     contract='PH26010100',
    ...     actual=100,
    ...     forecast=120,
    ...     mcp=100,
    ...     smp=110,
    ...     source='wind'
    ... )
    90.0
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
    """
    Calculate KUPST (Production Plan Deviation Cost) for a single period.

    This function calculates the total deviation cost based on the difference between
    actual and forecasted production. The deviation is only penalized if it exceeds
    the source-specific tolerance level.

    Parameters
    ----------
    actual : float
        Actual generated production in MWh.
    forecast : float
        Forecasted/planned production in MWh.
    mcp : float
        Market Clearing Price in TL/MWh.
    smp : float
        System Marginal Price in TL/MWh.
    tol : float, optional
        KUPST tolerance as a decimal (e.g., 0.15 for 15%). If None, retrieved from source.
        Tolerance is applied as: tolerance_amount = forecast * tol
    source : str, optional
        Energy source type (e.g., 'wind', 'solar', 'hydro'). Required if tol is None.
    kupst_multiplier : float, optional
        Multiplier for unit KUPST calculation. If None, uses regulation default.
    kupst_floor_price : float, optional
        Floor price for KUPST calculation in TL/MWh. Default 750.0 TL/MWh.
    return_detail : bool, default False
        If True, returns dictionary with detailed breakdown of calculation.
        If False, returns only total cost.
    regulation_period : {'current', '2026_01', 'pre_2026'}, default 'current'
        Regulation period for determining multiplier and tolerance values.
    include_maintenance_penalty : bool, default False
        If True, applies maintenance penalty rate to multiplier.

    Returns
    -------
    float or dict
        If return_detail=False: Total KUPST cost in TL.
        If return_detail=True: Dictionary with:
        - 'kupst_tol_perc': Applied tolerance percentage (decimal)
        - 'kupsm_tol': Tolerance amount in MWh (forecast * tol)
        - 'kupsm': Deviation after tolerance in MWh (max(0, |deviation| - tolerance))
        - 'unit_kupst_cost': Cost per MWh of deviation in TL/MWh
        - 'kupst_cost': Total KUPST cost in TL

    Raises
    ------
    Exception
        If neither tol nor source parameter is provided.
    ValueError
        If regulation_period is invalid.

    Notes
    -----
    Calculation steps:
    1. Determine tolerance: tol_amount = forecast * tolerance_percentage
    2. Calculate deviation: deviation = |actual - forecast|
    3. Calculate penalized deviation: KUPSM = max(0, deviation - tol_amount)
    4. Calculate unit cost: unit_kupst = max(mcp, smp, floor_price) * multiplier
    5. Total cost: KUPST = KUPSM * unit_kupst

    Examples
    --------
    >>> calculate_kupst_cost(
    ...     actual=100,
    ...     forecast=120,
    ...     mcp=100,
    ...     smp=110,
    ...     source='wind',
    ...     regulation_period='current'
    ... )
    90.0

    >>> calculate_kupst_cost(
    ...     actual=100,
    ...     forecast=120,
    ...     mcp=100,
    ...     smp=110,
    ...     source='wind',
    ...     return_detail=True,
    ...     regulation_period='current'
    ... )
    {'kupst_tol_perc': 0.15, 'kupsm_tol': 18.0, 'kupsm': 2.0, 'unit_kupst_cost': 5.5, 'kupst_cost': 11.0}
    """
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
    Calculate KUPST (Production Plan Deviation Cost) for multiple periods.

    This function efficiently calculates KUPST costs for a list of periods, allowing
    per-period variations in MCP, SMP, and optionally maintenance penalty status.

    Parameters
    ----------
    actual_values : list
        List of actual generated production values in MWh for each period.
    forecast_values : list
        List of forecasted/planned production values in MWh for each period.
    mcp : list
        List of Market Clearing Prices in TL/MWh for each period.
    smp : list
        List of System Marginal Prices in TL/MWh for each period.
    tol : float, optional
        KUPST tolerance as a decimal (e.g., 0.15 for 15%). Applied uniformly to all periods.
        If None, retrieved from source parameter.
    source : {'wind', 'solar', 'sun', 'unlicensed', 'other'}, optional
        Energy source type. Required if tol is None. 'sun' is aliased to 'solar'.
    kupst_multiplier : float, optional
        Multiplier for unit KUPST calculation. If None, uses regulation default.
    kupst_floor_price : float, optional
        Floor price for KUPST calculation in TL/MWh. Default 750.0 TL/MWh.
    regulation_period : {'current', '2026_01', 'pre_2026'}, default 'current'
        Regulation period for determining multiplier and tolerance values.
    **kwargs
        Additional keyword arguments:
        - maintenance_penalty_list : list of bool
            Per-period maintenance penalty flags. Defaults to [False] * num_periods.

    Returns
    -------
    list
        List of KUPST costs in TL for each period. List length matches input lists.

    Raises
    ------
    Exception
        If neither tol nor source parameter is provided.
    ValueError
        If input lists have mismatched lengths.

    Notes
    -----
    Each period's cost is calculated independently using calculate_kupst_cost().
    The tolerance value is fixed across all periods, but MCP, SMP, and maintenance
    penalty status can vary by period.

    Examples
    --------
    >>> calculate_kupst_cost_list(
    ...     actual_values=[100, 105],
    ...     forecast_values=[120, 110],
    ...     mcp=[100, 95],
    ...     smp=[110, 105],
    ...     source='wind',
    ...     regulation_period='current'
    ... )
    [90.0, 12.5]
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
    Calculate unit imbalance prices using a contract code.

    This function determines the regulation period from the contract code and calculates
    the imbalance prices for positive and negative imbalances according to the applicable rules.

    Parameters
    ----------
    contract : str
        Contract code in format 'PHYYMMDDhh' (e.g., 'PH26010100'). Used to determine
        the applicable regulation period.
    mcp : float
        Market Clearing Price in TL/MWh.
    smp : float
        System Marginal Price in TL/MWh.
    **kwargs
        Regulation-specific parameters passed to underlying functions:
        - For 2026 regulation: floor_price, ceil_price, V, B, low_margin, high_margin, ceil_margin
        - For pre-2026 regulation: penalty_margin

    Returns
    -------
    dict
        Dictionary with keys:
        - 'pos': Price for positive imbalance (sell at this price) in TL/MWh
        - 'neg': Price for negative imbalance (buy at this price) in TL/MWh

    Notes
    -----
    The interpretation of 'pos' and 'neg' depends on whether you have a surplus
    or deficit relative to your plan. This is a price, not a cost.

    Examples
    --------
    >>> calculate_unit_imbalance_price_by_contract(
    ...     contract='PH26010100',
    ...     mcp=100,
    ...     smp=110
    ... )
    {'pos': 94.0, 'neg': 116.5}
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
    Calculate unit imbalance prices based on regulation period.

    This dispatcher function routes to regulation-specific implementations to calculate
    the prices at which imbalances are traded (positive and negative).

    Parameters
    ----------
    mcp : float
        Market Clearing Price in TL/MWh.
    smp : float
        System Marginal Price in TL/MWh.
    regulation_period : {'current', '26_01', 'pre_2026'}, default 'current'
        Regulation period. 'current' and '26_01' both refer to 2026 regulation.
    **kwargs
        Regulation-specific parameters passed to underlying functions:
        - For 2026 regulation: floor_price, ceil_price, V, B, low_margin, high_margin, ceil_margin
        - For pre-2026 regulation: penalty_margin

    Returns
    -------
    dict
        Dictionary with keys:
        - 'pos': Price for positive imbalance in TL/MWh
        - 'neg': Price for negative imbalance in TL/MWh

    Raises
    ------
    ValueError
        If regulation_period is not one of the valid values.

    Notes
    -----
    The 2026 regulation uses a more complex pricing model with multiple parameters,
    while pre-2026 uses a simplified margin-based approach.

    Examples
    --------
    >>> calculate_unit_imbalance_price(mcp=100, smp=110, regulation_period='current')
    {'pos': 94.0, 'neg': 116.5}
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
    Calculate imbalance prices under 2026 EPDK regulation (effective 2026-01-01).

    This function implements the complex 2026 imbalance pricing model which applies
    different margins based on system imbalance direction and price levels.

    Parameters
    ----------
    mcp : float
        Market Clearing Price (day-ahead price) in TL/MWh.
    smp : float
        System Marginal Price (real-time balancing price) in TL/MWh.
    floor_price : float, default 0.0
        Minimum price floor in TL/MWh. Prices cannot fall below this value.
    ceil_price : float, default 3400.0
        Maximum price ceiling in TL/MWh. When this is reached, additional margins apply.
    V : float, default 150
        Reference/threshold price in TL/MWh. Used for:
        - Calculating negative imbalance price (floor for price calculation)
        - Determining positive imbalance price threshold
    B : float, default 100
        Reference price for positive imbalance in TL/MWh. Applied when imbalance price
        would fall below V.
    low_margin : float, default 0.03
        Margin (3%) applied to the opposite side of system imbalance.
        - If SMP > MCP (negative system imbalance), applied to positive imbalance price
        - If MCP > SMP (positive system imbalance), applied to negative imbalance price
    high_margin : float, default 0.06
        Margin (6%) applied to the same side as system imbalance.
        - If SMP > MCP, applied to negative imbalance price
        - If MCP > SMP, applied to positive imbalance price
    ceil_margin : float, default 0.05
        Additional margin (5%) applied when max(MCP, SMP) equals ceil_price,
        only to negative imbalance price.
    **kwargs
        Additional keyword arguments (unused, for compatibility).

    Returns
    -------
    dict
        Dictionary with keys:
        - 'pos': Price for positive imbalance (TL/MWh) - price at which positive imbalances are settled
        - 'neg': Price for negative imbalance (TL/MWh) - price at which negative imbalances are settled

    Notes
    -----
    Margin assignment depends on system imbalance direction:
    - Positive system imbalance (MCP > SMP): System has surplus
      - Producers with surplus (positive imbalance) get low margin (less penalty)
      - Consumers needing energy (negative imbalance) pay high margin (higher cost)
    - Negative system imbalance (SMP > MCP): System has deficit
      - Producers needed (negative imbalance) get high margin (incentive)
      - Consumers with surplus (positive imbalance) get low margin (less reward)

    The negative imbalance price has a floor at max(MCP, SMP, V).
    The positive imbalance price has a special rule: if less than V, it becomes -B.

    Examples
    --------
    >>> calculate_unit_imbalance_price_2026(mcp=100, smp=110)
    {'pos': 94.0, 'neg': 116.5}

    >>> calculate_unit_imbalance_price_2026(mcp=100, smp=90)
    {'pos': 84.3, 'neg': 109.0}
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
    Calculate imbalance prices under pre-2026 EPDK regulation.

    This function implements the simplified pre-2026 imbalance pricing model where
    a uniform penalty margin is applied to both positive and negative imbalances.

    Parameters
    ----------
    mcp : float
        Market Clearing Price (day-ahead price) in TL/MWh.
    smp : float
        System Marginal Price (real-time balancing price) in TL/MWh.
    penalty_margin : float, default 0.03
        Penalty margin (3%) applied symmetrically to both imbalance sides:
        - Positive imbalance price: min(MCP, SMP) * (1 - margin)
        - Negative imbalance price: max(MCP, SMP) * (1 + margin)

    Returns
    -------
    dict
        Dictionary with keys:
        - 'pos': Price for positive imbalance in TL/MWh = min(mcp, smp) * (1 - penalty_margin)
        - 'neg': Price for negative imbalance in TL/MWh = max(mcp, smp) * (1 + penalty_margin)

    Notes
    -----
    This simplified model applies:
    - Positive imbalances (surplus): Penalized at lower of MCP or SMP, with 3% discount
    - Negative imbalances (deficit): Penalized at higher of MCP or SMP, with 3% surcharge

    This approach is much simpler than 2026 regulation, which uses directional margins
    and price thresholds.

    Examples
    --------
    >>> calculate_unit_imbalance_price_pre_2026(mcp=100, smp=110)
    {'pos': 97.0, 'neg': 113.3}
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
    Calculate unit imbalance costs using a contract code.

    This function determines the regulation period from the contract code and calculates
    the imbalance costs (price differential from MCP) for positive and negative imbalances.

    Parameters
    ----------
    contract : str
        Contract code in format 'PHYYMMDDhh' (e.g., 'PH26010100'). Used to determine
        the applicable regulation period.
    mcp : float
        Market Clearing Price in TL/MWh.
    smp : float
        System Marginal Price in TL/MWh.
    include_prices : bool, default False
        If True, returned dictionary includes both prices and costs.
        If False, returns only costs.
    **kwargs
        Regulation-specific parameters passed to underlying functions.

    Returns
    -------
    dict
        If include_prices=False:
        - 'pos': Cost of positive imbalance in TL/MWh (MCP - positive_imbalance_price)
        - 'neg': Cost of negative imbalance in TL/MWh (negative_imbalance_price - MCP)

        If include_prices=True, also includes:
        - 'pos_price': Price for positive imbalance in TL/MWh
        - 'neg_price': Price for negative imbalance in TL/MWh
        - 'pos_cost': Cost of positive imbalance in TL/MWh
        - 'neg_cost': Cost of negative imbalance in TL/MWh

    Notes
    -----
    Cost is defined as the difference between the imbalance price and MCP:
    - Positive imbalance cost = MCP - (positive imbalance price)
    - Negative imbalance cost = (negative imbalance price) - MCP

    A positive cost indicates the imbalance is penalized (unfavorable).

    Examples
    --------
    >>> calculate_unit_imbalance_cost_by_contract(
    ...     contract='PH26010100',
    ...     mcp=100,
    ...     smp=110,
    ...     include_prices=True
    ... )
    {'pos_price': 94.0, 'neg_price': 116.5, 'pos_cost': 6.0, 'neg_cost': 16.5}
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
    Calculate unit imbalance costs based on regulation period.

    This dispatcher function routes to regulation-specific implementations to calculate
    the imbalance costs (penalty or benefit) relative to the day-ahead market price.

    Parameters
    ----------
    mcp : float
        Market Clearing Price in TL/MWh.
    smp : float
        System Marginal Price in TL/MWh.
    include_prices : bool, default False
        If True, returned dictionary includes both prices and costs.
        If False, returns only costs.
    regulation_period : {'current', '26_01', 'pre_2026'}, default 'current'
        Regulation period. 'current' and '26_01' both refer to 2026 regulation.
    **kwargs
        Regulation-specific parameters passed to underlying functions.

    Returns
    -------
    dict
        Dictionary with imbalance costs. Format depends on include_prices parameter.

    Raises
    ------
    ValueError
        If regulation_period is not one of the valid values.

    Notes
    -----
    The 2026 regulation is effective from January 1, 2026. Before that date,
    the pre-2026 regulation applies.

    Examples
    --------
    >>> calculate_unit_imbalance_cost(mcp=100, smp=110, regulation_period='current')
    {'pos': 6.0, 'neg': 16.5}
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
    """
    Calculate unit imbalance costs under 2026 EPDK regulation.

    This function calculates the cost differential between the imbalance price and
    the day-ahead market clearing price (MCP) for both positive and negative imbalances.

    Parameters
    ----------
    mcp : float
        Market Clearing Price in TL/MWh.
    smp : float
        System Marginal Price in TL/MWh.
    floor_price : float, default 0.0
        Minimum price floor in TL/MWh.
    ceil_price : float, default 3400.0
        Maximum price ceiling in TL/MWh.
    V : float, default 150
        Reference/threshold price in TL/MWh.
    B : float, default 100
        Reference price for positive imbalance in TL/MWh.
    low_margin : float, default 0.03
        Margin for opposite imbalance side (3%).
    high_margin : float, default 0.06
        Margin for same imbalance side (6%).
    ceil_margin : float, default 0.05
        Additional margin when max(MCP, SMP) equals ceil_price (5%).
    include_prices : bool, default False
        If True, returned dictionary includes both prices and costs.
    **kwargs
        Additional keyword arguments (unused, for compatibility).

    Returns
    -------
    dict
        If include_prices=False:
        - 'pos': Positive imbalance cost in TL/MWh (MCP - positive_price)
        - 'neg': Negative imbalance cost in TL/MWh (negative_price - MCP)

        If include_prices=True:
        - 'pos_price': Positive imbalance price in TL/MWh
        - 'neg_price': Negative imbalance price in TL/MWh
        - 'pos_cost': Positive imbalance cost in TL/MWh
        - 'neg_cost': Negative imbalance cost in TL/MWh

    Notes
    -----
    Costs are derived from prices:
    - pos_cost = MCP - pos_price (positive is costlier if result > 0)
    - neg_cost = neg_price - MCP (negative is costlier if result > 0)

    See calculate_unit_imbalance_price_2026() for details on price calculation.

    Examples
    --------
    >>> calculate_unit_imbalance_cost_2026(mcp=100, smp=110)
    {'pos': 6.0, 'neg': 16.5}

    >>> calculate_unit_imbalance_cost_2026(mcp=100, smp=110, include_prices=True)
    {'pos_price': 94.0, 'neg_price': 116.5, 'pos_cost': 6.0, 'neg_cost': 16.5}
    """
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
    Calculate unit imbalance costs under pre-2026 EPDK regulation.

    This function calculates the cost differential between the imbalance price and
    the day-ahead market clearing price (MCP) using the simplified pre-2026 model.

    Parameters
    ----------
    mcp : float
        Market Clearing Price in TL/MWh.
    smp : float
        System Marginal Price in TL/MWh.
    penalty_margin : float, default 0.03
        Penalty margin (3%) applied symmetrically to both imbalance sides.
    include_prices : bool, default False
        If True, returned dictionary includes both prices and costs.
        If False, returns only costs.

    Returns
    -------
    dict
        If include_prices=False:
        - 'pos': Positive imbalance cost in TL/MWh
        - 'neg': Negative imbalance cost in TL/MWh

        If include_prices=True:
        - 'pos_price': Positive imbalance price in TL/MWh
        - 'neg_price': Negative imbalance price in TL/MWh
        - 'pos_cost': Positive imbalance cost in TL/MWh
        - 'neg_cost': Negative imbalance cost in TL/MWh

    Notes
    -----
    The pre-2026 model applies uniform margins:
    - Positive imbalance: min(MCP, SMP) * (1 - margin)
    - Negative imbalance: max(MCP, SMP) * (1 + margin)

    This is significantly simpler than the 2026 regulation which uses directional margins.

    Examples
    --------
    >>> calculate_unit_imbalance_cost_pre_2026(mcp=100, smp=110)
    {'pos': 3.0, 'neg': 3.3}

    >>> calculate_unit_imbalance_cost_pre_2026(mcp=100, smp=110, include_prices=True)
    {'pos_price': 97.0, 'neg_price': 113.3, 'pos_cost': 3.0, 'neg_cost': 3.3}
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
    Calculate unit imbalance prices, costs, and optionally KUPST cost using a contract code.

    This function determines the regulation period from the contract code and provides
    a comprehensive breakdown of both imbalance and production plan deviation costs.

    Parameters
    ----------
    contract : str
        Contract code in format 'PHYYMMDDhh' (e.g., 'PH26010100'). Used to determine
        the applicable regulation period.
    mcp : float
        Market Clearing Price in TL/MWh.
    smp : float
        System Marginal Price in TL/MWh.
    include_kupst : bool, default True
        If True, includes unit KUPST cost in the result.
    **kwargs
        Regulation-specific parameters and KUPST parameters:
        - kupst_floor_price : float, default 750.0
        - kupst_multiplier : float, default varies by regulation
        - include_maintenance_penalty : bool, default False
        - For 2026: floor_price, ceil_price, V, B, low_margin, high_margin, ceil_margin
        - For pre-2026: penalty_margin

    Returns
    -------
    dict
        Dictionary containing:
        - 'pos_price': Price for positive imbalance in TL/MWh
        - 'neg_price': Price for negative imbalance in TL/MWh
        - 'pos_cost': Cost of positive imbalance in TL/MWh
        - 'neg_cost': Cost of negative imbalance in TL/MWh
        - 'unit_kupst': Unit KUPST cost in TL/MWh (only if include_kupst=True)

    Notes
    -----
    This is a convenience function that returns both imbalance and KUPST costs
    in a single call. Useful for analyzing total deviation costs.

    Examples
    --------
    >>> calculate_unit_price_and_costs_by_contract(
    ...     contract='PH26010100',
    ...     mcp=100,
    ...     smp=110
    ... )
    {'pos_price': 94.0, 'neg_price': 116.5, 'pos_cost': 6.0, 'neg_cost': 16.5, 'unit_kupst': 5.5}
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
    Calculate unit imbalance prices, costs, and optionally KUPST cost by regulation period.

    This dispatcher function calculates both imbalance prices/costs and optionally
    production plan deviation costs in a single comprehensive call.

    Parameters
    ----------
    mcp : float
        Market Clearing Price in TL/MWh.
    smp : float
        System Marginal Price in TL/MWh.
    include_kupst : bool, default True
        If True, includes unit KUPST cost in the result dictionary.
    regulation_period : {'current', '26_01', 'pre_2026'}, default 'current'
        Regulation period. 'current' and '26_01' both refer to 2026 regulation.
    **kwargs
        Regulation-specific parameters and KUPST parameters:
        - kupst_floor_price : float, default 750.0
        - kupst_multiplier : float, default varies by regulation
        - include_maintenance_penalty : bool, default False
        - For 2026: floor_price, ceil_price, V, B, low_margin, high_margin, ceil_margin
        - For pre-2026: penalty_margin

    Returns
    -------
    dict
        Dictionary containing imbalance prices, costs, and optionally KUPST:
        - 'pos_price': Price for positive imbalance in TL/MWh
        - 'neg_price': Price for negative imbalance in TL/MWh
        - 'pos_cost': Cost of positive imbalance in TL/MWh
        - 'neg_cost': Cost of negative imbalance in TL/MWh
        - 'unit_kupst': Unit KUPST cost in TL/MWh (only if include_kupst=True)

    Raises
    ------
    ValueError
        If regulation_period is not one of the valid values.

    Notes
    -----
    This function provides a comprehensive breakdown of all unit-level costs that apply
    to deviations from a production or consumption plan. It's useful for cost modeling
    and total cost analysis.

    Examples
    --------
    >>> calculate_unit_price_and_costs(mcp=100, smp=110, regulation_period='current')
    {'pos_price': 94.0, 'neg_price': 116.5, 'pos_cost': 6.0, 'neg_cost': 16.5, 'unit_kupst': 5.5}
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
    Calculate the imbalance amount and DSG (Balancing Responsible Group) tolerance effects.

    This function calculates how much deviation from plan constitutes an imbalance
    that must be settled, accounting for DSG tolerance absorption (regulatory protection).

    Parameters
    ----------
    actual : float
        Actual measured value in MWh.
    forecast : float
        Forecasted/planned value in MWh.
    is_producer : bool
        True if the unit is a producer, False if it is a consumer.
        Determines how deviation sign is interpreted.
    tolerance_multiplier : float, default 1.0
        Multiplier for DSG tolerance to get effective tolerance (0.0 to 1.0+).
        E.g., 0.5 means only 50% of DSG tolerance is effective.
    just_raw_imbalance : bool, default False
        If True, only returns the raw imbalance as float (faster, for internal use).
    regulation_period : {'current', '26_01', 'pre_2026'}, default 'current'
        Regulation period determining DSG tolerance:
        - 2026 regulation: 5% DSG tolerance
        - Pre-2026 regulation: 10% DSG tolerance
    **kwargs
        Additional parameters:
        - dsg_tolerance : float
            Override default DSG tolerance value.

    Returns
    -------
    float or dict
        If just_raw_imbalance=True: Raw imbalance amount (float) in MWh.

        Otherwise, returns dict with:
        - 'raw_imb': Raw imbalance (actual - forecast for producers, inverse for consumers) in MWh
        - 'dsg_raw_tol': DSG tolerance amount (raw, without multiplier) in MWh = |actual| * tolerance
        - 'dsg_raw_imb': Imbalance after raw DSG tolerance absorption in MWh
        - 'dsg_eff_tol': DSG tolerance amount (after multiplier) in MWh = dsg_raw_tol * multiplier
        - 'dsg_eff_imb': Imbalance after effective DSG tolerance absorption in MWh (penalized imbalance)

    Notes
    -----
    Imbalance sign interpretation:
    - For producers: positive if actual > forecast (surplus), negative if actual < forecast (deficit)
    - For consumers: positive if actual < forecast (deficit), negative if actual > forecast (surplus)

    DSG tolerance is applied to reduce the penalized imbalance:
    - If imbalance is positive (surplus/deficit depending on producer/consumer):
        effective_imbalance = max(0, raw_imbalance - dsg_effective_tolerance)
    - If imbalance is negative (deficit/surplus depending on producer/consumer):
        effective_imbalance = min(0, raw_imbalance + dsg_effective_tolerance)

    Examples
    --------
    For a producer with actual=105, forecast=100, tolerance_multiplier=1.0:
    >>> calculate_imbalance_amount(actual=105, forecast=100, is_producer=True)
    {'raw_imb': 5.0, 'dsg_raw_tol': 5.25, 'dsg_raw_imb': 0.0, 'dsg_eff_tol': 5.25, 'dsg_eff_imb': 0.0}

    >>> calculate_imbalance_amount(actual=105, forecast=100, is_producer=True, just_raw_imbalance=True)
    5.0
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
    Calculate total imbalance and KUPST costs for a single period.

    This is a comprehensive function that calculates both imbalance costs (from deviations
    relative to the day-ahead plan) and KUPST costs (for production plan deviations that
    exceed tolerance). It's the highest-level cost calculation function.

    Parameters
    ----------
    forecast : float
        Forecasted/planned quantity in MWh (production for producers, consumption for consumers).
    actual : float
        Actual realized quantity in MWh.
    is_producer : bool
        True if this is a production unit, False if it's a consumption unit.
        This affects how deviations are interpreted (producer surplus vs. consumer deficit).
    mcp : float
        Market Clearing Price in TL/MWh.
    smp : float
        System Marginal Price in TL/MWh.
    production_source : {'wind', 'solar', 'sun', 'unlicensed', 'other'}, optional
        Energy source type. Required for producers to determine KUPST tolerance.
        Not needed for consumers. 'sun' is aliased to 'solar'.
    regulation_period : {'current', '2026_01', 'pre_2026'}, default 'current'
        Regulation period for cost calculations.
    include_quantities : bool, default False
        If True, returned dictionary includes imbalance quantity and KUPST deviation quantity.
    **kwargs
        Additional parameters:
        - return_imbalance_cost : bool (hidden option to return only imbalance cost as float)
        - All other regulation-specific parameters passed to underlying functions

    Returns
    -------
    dict or float
        If return_imbalance_cost=True: Returns only imbalance cost as float (hidden option).

        Otherwise, returns dict with:
        - 'imb_cost': Total imbalance cost in TL
        - 'kupst_cost': KUPST cost in TL (only for producers)
        - 'total_cost': Total cost = imb_cost + kupst_cost (only for producers)

        If include_quantities=True, also includes:
        - 'imb_qty': Signed imbalance quantity in MWh (positive/negative)
        - 'kupsm': Production plan deviation after tolerance in MWh (only for producers)

    Raises
    ------
    Exception
        If is_producer=True but production_source is not provided (when KUPST tolerance cannot be determined).
    ValueError
        If regulation_period is invalid.

    Notes
    -----
    For producers:
    - Imbalance sign: positive if actual > forecast (surplus), negative if actual < forecast (deficit)
    - KUPST applies to both positive and negative deviations beyond tolerance
    - Total cost = imbalance cost + KUPST cost

    For consumers:
    - Imbalance sign: positive if actual < forecast (deficit), negative if actual > forecast (surplus)
    - No KUPST applied (only imbalance cost calculated)

    Examples
    --------
    >>> calculate_diff_costs(
    ...     forecast=120,
    ...     actual=100,
    ...     is_producer=True,
    ...     mcp=100,
    ...     smp=110,
    ...     production_source='wind',
    ...     regulation_period='current'
    ... )
    {'imb_cost': 100.0, 'kupst_cost': 90.0, 'total_cost': 190.0}

    >>> calculate_diff_costs(
    ...     forecast=120,
    ...     actual=100,
    ...     is_producer=True,
    ...     mcp=100,
    ...     smp=110,
    ...     production_source='wind',
    ...     include_quantities=True,
    ...     regulation_period='current'
    ... )
    {'imb_cost': 100.0, 'kupst_cost': 90.0, 'total_cost': 190.0, 'imb_qty': -20.0, 'kupsm': 2.0}
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
