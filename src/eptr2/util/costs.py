from datetime import date, datetime, timedelta, timezone
import warnings
from typing import Literal
import math
from eptr2.util.time import contract_to_floor_ceil_prices, iso_to_contract


def get_time_regulation_params_map():
    """
    Regulation parameters that change over time within the 2026 regulation.

    Same shape and conventions as
    :func:`eptr2.util.time.get_time_min_max_price_map`: one row per regulation
    change, newest first, each row carrying the full set of values so it reads
    standalone. A regulation change that alters only values is a single new row
    here; a change to a *formula* needs a new regulation period instead (see
    :func:`get_regulation_period_by_contract`).

    Rows apply from the first delivery hour of ``date``. Only the 2026
    regulation is covered: pre-2026 uses different formulas and different KUPST
    semantics, and is resolved by regulation period, not by this map.

    Returns:
        list: dictionaries containing
            - 'date': first date the values apply (YYYY-MM-DD)
            - 'V': reference/threshold price (TL/MWh)
            - 'B': reference price for positive imbalance (TL/MWh)
            - 'low_margin' / 'high_margin': imbalance margins
            - 'ceil_margin': additional margin at the price ceiling
            - 'kupst_floor_price': KUPST floor price (TL/MWh)
            - 'kupst': KUPST parameters by category (see KUPST_CATEGORIES),
              each with 'tolerance', 'multiplier' and, where the regulation
              defines one, 'multiplier_maintenance' and
              'maintenance_fault_threshold' (monthly fault entries from which
              the maintenance multiplier applies). 'other' is the fallback.
    """

    ## Categories without a 'multiplier_maintenance' have no maintenance
    ## multiplier; the plain multiplier applies even with the penalty flag.
    def _kupst_2026_01():
        rate = {"multiplier": 0.05, "multiplier_maintenance": 0.08}
        return {
            "wind": {"tolerance": 0.15, **rate},
            "solar": {"tolerance": 0.08, **rate},
            "unlicensed_from_transmission": {"tolerance": 0.20, **rate},
            "other": {"tolerance": 0.05, **rate},
        }

    map_l = [
        {
            ## V lowered from 150 to 100 and KUPST multipliers and tolerances
            ## set per category, effective from the first delivery hour of
            ## 2026-11-01. The imbalance and KUPST formulas are unchanged.
            ## Source: KUPST coefficients table ("Tablo 4, KÜPST katsayıları,
            ## Kasım 2026'dan itibaren") supplied by the maintainer.
            ## TODO: cite the board decision / Resmi Gazete issue.
            ## Consumption unit categories of the same table start in 2027
            ## and are not included yet.
            "date": "2026-11-01",
            "V": 100,
            "B": 100,
            "low_margin": 0.03,
            "high_margin": 0.06,
            "ceil_margin": 0.05,
            "kupst_floor_price": 750.0,
            "kupst": {
                ## Rüzgar
                "wind": {
                    "tolerance": 0.15,
                    "multiplier": 0.05,
                    "multiplier_maintenance": 0.08,
                    "maintenance_fault_threshold": 30,
                },
                ## Güneş
                "solar": {
                    "tolerance": 0.08,
                    "multiplier": 0.05,
                    "multiplier_maintenance": 0.08,
                    "maintenance_fault_threshold": 30,
                },
                ## Depolamalı üretim tesisi
                "plant_w_battery": {"tolerance": 0.05, "multiplier": 0.10},
                ## Diğer kaynaklar
                "other": {
                    "tolerance": 0.05,
                    "multiplier": 0.05,
                    "multiplier_maintenance": 0.08,
                    "maintenance_fault_threshold": 25,
                },
                ## İletime bağlı lisanssız, santral bazında
                "unlicensed_from_transmission": {"tolerance": 0.20, "multiplier": 0.02},
                ## Dağıtıma bağlı lisanssız, katılımcı bazında
                "unlicensed_from_distribution": {"tolerance": 0.25, "multiplier": 0.01},
                ## Müstakil depolama
                "battery": {"tolerance": 0.20, "multiplier": 0.02},
            },
        },
        {
            "date": "2026-01-01",
            "V": 150,
            "B": 100,
            "low_margin": 0.03,
            "high_margin": 0.06,
            "ceil_margin": 0.05,
            "kupst_floor_price": 750.0,
            "kupst": _kupst_2026_01(),
        },
    ]

    return sorted(map_l, key=lambda x: x["date"], reverse=True)


def regulation_date_to_contract(date_str: str) -> str:
    """First hourly contract code of ``date_str`` (YYYY-MM-DD) -> 'PHYYMMDD00'."""
    year, month, day = date_str.split("-")
    return f"PH{year[2:]}{month}{day}00"


def contract_to_regulation_params(contract: str | None = None) -> dict | None:
    """
    Resolve the regulation parameters applying to a contract's delivery hour.

    Contract codes are lexicographically ordered, so the applicable row is the
    newest one whose start contract is not after ``contract``.

    Args:
        contract: Contract code 'PHYYMMDDhh'. If None, the newest row is
            returned (the parameters currently in force).

    Returns:
        dict or None: the parameter row, or None for pre-2026 contracts, which
        are governed by the pre-2026 formulas rather than this map.
    """
    params_map = get_time_regulation_params_map()

    if contract is None:
        return params_map[0]

    for row in params_map:
        if contract >= regulation_date_to_contract(row["date"]):
            return row

    return None


## KUPST categories of the dated map. A category is not exactly the source:
## storage and unlicensed plants have their own categories.
KUPST_CATEGORIES = (
    "wind",
    "solar",
    "plant_w_battery",
    "other",
    "unlicensed_from_transmission",
    "unlicensed_from_distribution",
    "battery",
)

## Exact names (after normalization) that map to a category
KUPST_CATEGORY_ALIASES = {
    "sun": "solar",
    "unlicensed": "unlicensed_from_transmission",
    "lisanssiz": "unlicensed_from_transmission",
    "storage": "battery",
    "depolama": "battery",
    "default": "other",
    "diger": "other",
    "diger_kaynaklar": "other",
    ## Earlier names
    "storage_plant": "plant_w_battery",
    "unlicensed_transmission": "unlicensed_from_transmission",
    "unlicensed_distribution": "unlicensed_from_distribution",
    "standalone_storage": "battery",
}

## Keywords (normalized tokens) used when the name is not an exact match.
## Keywords of 5+ characters also match as prefixes for Turkish suffixes
## (e.g. 'dagitima', 'lisanssizlar', 'bataryali').
_KUPST_UNLICENSED_KEYS = ("unlicensed", "lisanssiz", "licenceless", "licenseless")
_KUPST_DISTRIBUTION_KEYS = ("distribution", "dagitim", "dist", "dso")
_KUPST_BATTERY_KEYS = ("battery", "batteries", "batarya", "bess", "storage", "depolama", "ess")
_KUPST_PLANT_W_BATTERY_KEYS = (
    "depolamali", "plant", "uretim", "tesis", "tesisi", "hybrid", "hibrit", "with",
    "w", "integrated", "entegre", "wind", "ruzgar", "solar", "gunes", "res", "ges",
    "pv", "hes", "hydro",
)
_KUPST_BATTERY_ONLY_KEYS = ("mustakil", "standalone", "stand", "alone", "only")
_KUPST_WIND_KEYS = ("wind", "ruzgar", "res", "wpp", "onshore", "offshore")
_KUPST_SOLAR_KEYS = ("solar", "sun", "gunes", "ges", "pv", "photovoltaic", "fotovoltaik", "spp")
_KUPST_OTHER_KEYS = (
    "other", "diger", "hydro", "hes", "dam", "baraj", "river", "akarsu", "coal",
    "komur", "linyit", "lignite", "gas", "dogalgaz", "natural", "ngcc", "dgkc",
    "geothermal", "jeotermal", "jes", "biomass", "biyokutle", "biogas", "biyogaz",
    "fuel", "fueloil", "nuclear", "nukleer", "thermal", "termik", "import", "ithal",
)
_TR_FOLD = str.maketrans("ıİşŞğĞüÜöÖçÇâÂîÎûÛ", "iissgguuooccaaiiuu")


def _kupst_tokens(name: str) -> list[str]:
    folded = name.translate(_TR_FOLD).lower()
    return [t for t in "".join(c if c.isalnum() else " " for c in folded).split() if t]


def normalize_kupst_category(name: str | None, strict: bool = False) -> str:
    """
    Map a source or category name in any common naming convention to one of
    KUPST_CATEGORIES.

    Matching ignores case, Turkish characters and separators: Turkish
    characters are folded to ASCII (ı/İ -> i, ş -> s, ğ -> g, ü -> u, ö -> o,
    ç -> c), so 'Rüzgar', 'ruzgar' and 'RUZGAR' are the same. 'RES', 'wind', 'Güneş', 'GES', 'PV', 'Depolamalı üretim tesisi',
    'wind + battery', 'Müstakil depolama', 'BESS', 'İletime bağlı lisanssız',
    'Dağıtıma bağlı lisanssız', 'unlicensed', 'HES', 'doğalgaz' all resolve.

    Rules, in order: an exact category name or alias; unlicensed (distribution
    if a distribution keyword is present, transmission otherwise); battery
    (plant_w_battery if it is a generation plant with storage, battery if it is
    standalone storage); wind; solar; other sources.

    Args:
        name: Source or category name. None gives 'other'.
        strict: If True, raise ValueError for names that match no rule instead
            of returning 'other'.

    Returns:
        str: One of KUPST_CATEGORIES.
    """
    if name is None:
        return "other"

    tokens = _kupst_tokens(str(name))
    key = "_".join(tokens)
    if key in KUPST_CATEGORIES:
        return key
    if key in KUPST_CATEGORY_ALIASES:
        return KUPST_CATEGORY_ALIASES[key]

    def has(keys):
        return any(
            t == k or (len(k) >= 5 and t.startswith(k)) for t in tokens for k in keys
        )

    if has(_KUPST_UNLICENSED_KEYS):
        if has(_KUPST_DISTRIBUTION_KEYS):
            return "unlicensed_from_distribution"
        return "unlicensed_from_transmission"
    if has(_KUPST_BATTERY_KEYS):
        if has(_KUPST_BATTERY_ONLY_KEYS):
            return "battery"
        if has(_KUPST_PLANT_W_BATTERY_KEYS):
            return "plant_w_battery"
        return "battery"
    if has(_KUPST_WIND_KEYS):
        return "wind"
    if has(_KUPST_SOLAR_KEYS):
        return "solar"
    if has(_KUPST_OTHER_KEYS) or not strict:
        return "other"

    raise ValueError(
        f"Unknown KUPST category {name!r}. Use one of {', '.join(KUPST_CATEGORIES)}."
    )


def get_kupst_params_by_contract(
    contract: str | None,
    category: str | None = "other",
    include_maintenance_penalty: bool = False,
) -> dict | None:
    """
    Resolve KUPST tolerance, multiplier and floor price for a category and contract.

    Args:
        contract: Contract code 'PHYYMMDDhh'. If None, the newest regulation row
            is used (the latest regulation).
        category: KUPST category or source name in any common convention,
            mapped by normalize_kupst_category (e.g. 'Rüzgar', 'GES', 'BESS').
            'unlicensed' maps to 'unlicensed_from_transmission' (per plant, the
            20% tolerance unlicensed plants had before). Unrecognized names
            (e.g. 'hydro', 'coal') fall back to 'other'. Note that
            'unlicensed_from_distribution' is applied per participant, so the
            deviation should be the participant's aggregate.
        include_maintenance_penalty: Use the maintenance multiplier. Categories
            without one keep their plain multiplier.

    Returns:
        dict with 'category' (resolved), 'tolerance', 'multiplier' and
        'floor_price', or None for pre-2026 contracts.
    """
    params = contract_to_regulation_params(contract)
    if params is None:
        return None

    category = normalize_kupst_category(category)
    if category not in params["kupst"]:
        category = "other"
    cat_d = params["kupst"][category]

    multiplier = cat_d["multiplier"]
    if include_maintenance_penalty:
        multiplier = cat_d.get("multiplier_maintenance", multiplier)

    return {
        "category": category,
        "tolerance": cat_d["tolerance"],
        "multiplier": multiplier,
        "floor_price": params["kupst_floor_price"],
    }


def is_kupst_maintenance_penalty_applicable(
    contract: str | None, category: str | None, monthly_fault_entries: int
) -> bool:
    """
    Whether the KUPST maintenance multiplier applies, given the number of fault
    entries of the plant in the month (e.g. 30 or more for wind and solar, 25 or
    more for other sources from 2026-11-01). False for categories or periods
    without a defined threshold.
    """
    params = contract_to_regulation_params(contract)
    if params is None:
        return False
    category = normalize_kupst_category(category)
    cat_d = params["kupst"].get(category, params["kupst"]["other"])
    threshold = cat_d.get("maintenance_fault_threshold")
    return threshold is not None and monthly_fault_entries >= threshold


## Parameters of the 2026 imbalance-price formula that the dated map supplies.
IMBALANCE_PARAM_KEYS = ("V", "B", "low_margin", "high_margin", "ceil_margin")


def inject_regulation_params(contract: str, kwargs: dict, keys=IMBALANCE_PARAM_KEYS) -> dict:
    """
    Fill ``keys`` in ``kwargs`` from the dated parameters for ``contract``.

    Explicitly supplied values always win; only missing (or None) keys are
    filled, mirroring how floor and ceiling prices are injected.
    """
    params = contract_to_regulation_params(contract)
    if params is None:
        return kwargs

    for key in keys:
        if key in params and kwargs.get(key) is None:
            kwargs[key] = params[key]

    return kwargs


def inject_kupst_params(contract: str, kwargs: dict, category: str | None = "other") -> dict | None:
    """
    Fill kupst_multiplier and kupst_floor_price in ``kwargs`` for the KUPST
    category from the dated parameters for ``contract``. Explicitly supplied
    values win. Returns the resolved KUPST parameters (None before 2026).
    """
    kupst_d = get_kupst_params_by_contract(
        contract,
        category=category,
        include_maintenance_penalty=kwargs.get("include_maintenance_penalty", False),
    )
    if kupst_d is not None:
        if kwargs.get("kupst_multiplier") is None:
            kwargs["kupst_multiplier"] = kupst_d["multiplier"]
        if kwargs.get("kupst_floor_price") is None:
            kwargs["kupst_floor_price"] = kupst_d["floor_price"]
    return kupst_d


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



def _contract_floor_ceil(contract: str, kwargs: dict) -> dict:
    """Floor and ceiling in force on the CONTRACT's date, unless given explicitly. Without this the helpers below used the
    ceiling in force today (4500 since 2026-04-04), so January-March 2026 hours at the 3400 cap missed the 1.05 surcharge
    (483 of 15,635 published hours 2025-01..2026-10 differed from mcp-smp-imb)."""
    fc_d = contract_to_floor_ceil_prices(contract)
    if fc_d is not None:
        kwargs.setdefault("floor_price", fc_d["min"])
        kwargs.setdefault("ceil_price", fc_d["max"])
    return kwargs

def get_kupst_tolerance_by_contract(
    contract: str,
    source: str = "other",
):
    """
    Get KUPST tolerance for a given source (KUPST category) and contract code.

    KUPST (Kesinlestirilmis Uretim Planından Sapma Tutarı - Production Plan Deviation Cost)
    tolerance determines the allowable deviation between forecasted and actual production
    before deviation costs are applied.

    Parameters
    ----------
    source : str, default 'other'
        KUPST category from 2026 (see KUPST_CATEGORIES and
        get_kupst_params_by_contract), e.g. 'wind', 'solar', 'plant_w_battery',
        'unlicensed_from_transmission', 'battery'. Before 2026 one of
        'wind', 'solar', 'other'. 'sun' is aliased to 'solar'; unknown
        values fall back to 'other'.
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
    - From 2026-11-01 per category, e.g. unlicensed (transmission) 20%,
      unlicensed (distribution) 25%, standalone storage 20%

    Examples
    --------
    >>> get_kupst_tolerance_by_contract('PH26010100', 'wind')
    0.15
    >>> get_kupst_tolerance_by_contract('PH25123100', 'wind')
    0.17
    """
    regulation_period = get_regulation_period_by_contract(contract)
    ## Tolerances can change within a regulation period; pre-2026 keeps its
    ## own table and is resolved by period alone.
    kupst_d = get_kupst_params_by_contract(contract, category=source)
    if kupst_d is not None:
        return kupst_d["tolerance"]
    return get_kupst_tolerance(
        normalize_kupst_category(source), regulation_period=regulation_period
    )


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
    category: str | None = "other",
):
    """
    Unit KUPST cost (TL/MWh) for a contract. Multiplier and floor price are
    resolved from the dated regulation parameters for the KUPST category (see
    get_kupst_params_by_contract) unless given explicitly. category is
    ignored before 2026.
    """
    regulation_period = get_regulation_period_by_contract(contract)
    ## KUPST multipliers and the floor price can change within a regulation
    ## period, so resolve them from the dated parameters when not given.
    kupst_d = get_kupst_params_by_contract(
        contract,
        category=category,
        include_maintenance_penalty=include_maintenance_penalty,
    )
    if kupst_d is not None:
        if kupst_multiplier is None:
            kupst_multiplier = kupst_d["multiplier"]
        if kupst_floor_price is None:
            kupst_floor_price = kupst_d["floor_price"]
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

    if math.isnan(mcp) or math.isnan(smp):
        return None

    if mcp is None or smp is None:
        return None

    if regulation_period in ["current", "26_01"]:
        if kupst_multiplier is None:
            kupst_multiplier = 0.08 if include_maintenance_penalty else 0.05

        if kupst_floor_price is None:
            kupst_floor_price = 750.0

        ## The maintenance penalty is already in kupst_multiplier
        return calculate_unit_kupst_cost_2026(
            mcp=mcp,
            smp=smp,
            kupst_multiplier_default=kupst_multiplier,
            kupst_floor_price=kupst_floor_price,
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
    Calculate unit KUPST costs according to the EPDK regulation (2026).

    Contract-free, so it keeps literal defaults. Multipliers per KUPST category
    and their changes over time (e.g. from 2026-11-01) are resolved by
    calculate_unit_kupst_cost_by_contract (see get_kupst_params_by_contract).
    The source shortcut below is from the draft regulation of 22 Sep 2025
    and its names are not the KUPST categories (its 'battery' rate is the
    plant_w_battery multiplier).
    """

    kupst_multiplier = 0.08 if include_maintenance_penalty else kupst_multiplier_default
    if source is not None:
        source_map = {"battery": 0.1, "aggregator": 0.05, "unlicensed": 0.02}
        kupst_multiplier = source_map.get(source, kupst_multiplier_default)

    return round(max(mcp, smp, kupst_floor_price) * kupst_multiplier, 2)


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
    return round(max(mcp, smp, kupst_floor_price) * kupst_multiplier, 2)


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
    category: str | None = None,
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
    category : str, optional
        KUPST category from 2026 (see get_kupst_params_by_contract). Defaults to
        source, so source='battery' sets both tolerance and
        multiplier.

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
    ## KUPST multipliers and the floor price can change within a regulation
    ## period, so resolve them from the dated parameters when not given.
    category = source if category is None else category
    kupst_d = get_kupst_params_by_contract(
        contract,
        category=category,
        include_maintenance_penalty=include_maintenance_penalty,
    )
    if kupst_d is not None:
        if kupst_multiplier is None:
            kupst_multiplier = kupst_d["multiplier"]
        if kupst_floor_price is None:
            kupst_floor_price = kupst_d["floor_price"]
        ## Tolerance of the dated category, not of the regulation period base table
        if tol is None and category is not None:
            tol = kupst_d["tolerance"]
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
    regulation_period: Literal["current", "26_01", "pre_2026"] = "current",
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
    regulation_period : {'current', '26_01', 'pre_2026'}, default 'current'
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
    ## V, B and the margins can change within a regulation period.
    kwargs = inject_regulation_params(contract, kwargs)
    if regulation_period != "pre_2026":
        kwargs = _contract_floor_ceil(contract, kwargs)

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
    regulation_period: Literal["current", "26_01", "pre_2026"] = "current",
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


SYSTEM_DIRECTION_LABELS = {
    ## EPIAS `systemStatus` values as returned by the mcp-smp-imb endpoint
    "enerji açığı": -1,  ## system is short (deficit)
    "enerji aciği": -1,
    "enerji fazlası": 1,  ## system is long (surplus)
    "enerji fazlasi": 1,
    "dengede": 0,
    "deficit": -1,
    "surplus": 1,
    "balanced": 0,
}


def normalize_system_direction(value):
    """
    Normalize a system imbalance direction to -1, 0, 1 or None.

    Accepts the integer form (-1/0/1), the EPIAS ``systemStatus`` labels
    (e.g. "Enerji Açığı"), and their English equivalents. Returns None when
    ``value`` is None, meaning the direction should be inferred from prices.

    Raises
    ------
    ValueError
        If the value cannot be interpreted as a system direction.
    """
    if value is None:
        return None

    if isinstance(value, str):
        key = value.strip().lower()
        if key in SYSTEM_DIRECTION_LABELS:
            return SYSTEM_DIRECTION_LABELS[key]
        try:
            return int(key)
        except ValueError:
            raise ValueError(
                f"Unrecognized system direction {value!r}. Use -1/0/1 or one of: "
                + ", ".join(sorted(SYSTEM_DIRECTION_LABELS))
            )

    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValueError("system_direction must be convertible to int if not None")


def calculate_unit_imbalance_price_2026(
    mcp: float,
    smp: float,
    floor_price: float = 0.0,
    ceil_price: float | None = None,
    V: float = 150,
    B: float = 100,
    low_margin: float = 0.03,
    high_margin: float = 0.06,
    ceil_margin: float = 0.05,
    sd_sign: int | None = None,
    strict: bool = True,
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
    ceil_price : float or None, default None
        Maximum price ceiling in TL/MWh. When this is reached, additional margins apply.
        If None, the ceiling currently in force is resolved at call time from
        :func:`eptr2.util.time.contract_to_floor_ceil_prices` (4500.0 since 2026-04-04;
        previously 3400.0 from 2025-04-05), so the default tracks EPDK revisions.
        For a historical hour pass the applicable value explicitly, or use the
        ``*_by_contract`` helpers, which resolve floor and ceiling from the contract date.
    V : float, default 150
        Reference/threshold price in TL/MWh. Used for:
        - Calculating negative imbalance price (floor for price calculation)
        - Determining positive imbalance price threshold
        These literal defaults are the values in force from 2026-01-01.
        They are deliberately NOT resolved from the calendar: a call
        without a contract cannot know the delivery hour, so resolving
        'today's value' would silently change results on a regulation
        boundary. The ``*_by_contract`` and ``*_by_datetime`` helpers
        resolve the applicable set from
        :func:`get_time_regulation_params_map` (V is 100 from 2026-11-01).
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
    sd_sign : int or None, optional
        System imbalance direction, needed when MCP == SMP (equal prices do not
        reveal the direction, and assuming a balanced system understates the
        negative imbalance price). Allowed values:
        - 1: positive system imbalance (surplus / "Enerji Fazlası")
        - 0: balanced system ("Dengede")
        - -1: negative system imbalance (deficit / "Enerji Açığı")
        If None, direction is inferred from MCP vs SMP.

        Accepted equivalently as the keyword ``system_direction``, or as the raw
        EPIAS ``systemStatus`` label from the ``mcp-smp-imb`` call (the Turkish
        strings above). ``sd_sign`` is the parameter name and takes precedence
        if both are supplied; ``system_direction`` is kept because it is the
        name used by the ``sd_sign`` column's documentation and by callers
        written against earlier docs. Values are normalized with
        :func:`normalize_system_direction`.
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

    mcp = round(mcp, 2)
    smp = round(smp, 2)

    ## Resolve the ceiling in force today when not given explicitly, so the
    ## default tracks EPDK revisions instead of going stale in the signature.
    if ceil_price is None:
        ceil_price = contract_to_floor_ceil_prices()["max"]

    if strict:
        if mcp < floor_price:
            raise ValueError(f"MCP {mcp} is below floor price {floor_price}")
        if smp < floor_price:
            raise ValueError(f"SMP {smp} is below floor price {floor_price}")
        if mcp > ceil_price:
            raise ValueError(f"MCP {mcp} is above ceiling price {ceil_price}")
        if smp > ceil_price:
            raise ValueError(f"SMP {smp} is above ceiling price {ceil_price}")

    ## Accept the documented `system_direction` spelling (and the raw EPIAS
    ## `systemStatus` label) as aliases for sd_sign. Previously these were
    ## swallowed by **kwargs, silently producing balanced-system prices.
    if sd_sign is None:
        sd_sign = normalize_system_direction(
            kwargs.pop("system_direction", None)
            if "system_direction" in kwargs
            else kwargs.pop("systemStatus", None)
        )
    else:
        sd_sign = normalize_system_direction(sd_sign)

    if sd_sign is not None:
        if sd_sign not in [1, 0, -1]:
            raise ValueError("system_direction must be 1, 0, -1 or None")

    if sd_sign is None:
        if mcp > smp:
            sd_sign = 1
        elif mcp < smp:
            sd_sign = -1
        elif smp == ceil_price:
            sd_sign = -1
        elif smp == floor_price:
            sd_sign = 1
        else:
            sd_sign = 0
    else:
        if mcp > smp and sd_sign != 1:
            warnings.warn(
                "Inconsistent system_direction provided; overriding based on mcp and smp"
            )
            sd_sign = 1
        elif mcp < smp and sd_sign != -1:
            sd_sign = -1
            warnings.warn(
                "Inconsistent system_direction provided; overriding based on mcp and smp"
            )

    if sd_sign == 1:  ## system imbalance is positive
        neg_margin = low_margin
        pos_margin = high_margin
    elif sd_sign == -1:  ## system imbalance is negative
        neg_margin = high_margin
        pos_margin = low_margin
    else:  ## balanced system
        neg_margin = low_margin
        pos_margin = low_margin

    if max(mcp, smp) >= ceil_price:
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
        "pos_imb_price": round(pos_imb_price, 2),
        "neg_imb_price": round(neg_imb_price, 2),
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
        "pos_imb_price": round((1 - penalty_margin) * min(mcp, smp), 2),
        "neg_imb_price": round((1 + penalty_margin) * max(mcp, smp), 2),
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
    ## V, B and the margins can change within a regulation period.
    kwargs = inject_regulation_params(contract, kwargs)
    if regulation_period != "pre_2026":
        kwargs = _contract_floor_ceil(contract, kwargs)

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
    regulation_period: Literal["current", "26_01", "pre_2026"] = "current",
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

    if math.isnan(mcp) or math.isnan(smp) or mcp is None or smp is None:
        if include_prices:
            return {
                "pos_imb_price": None,
                "neg_imb_price": None,
                "unit_pos_imb_cost": None,
                "unit_neg_imb_cost": None,
            }
        else:
            return {"unit_pos_imb_cost": None, "unit_neg_imb_cost": None}

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
    ceil_price: float | None = None,
    V: float = 150,
    B: float = 100,
    low_margin: float = 0.03,
    high_margin: float = 0.06,
    ceil_margin: float = 0.05,
    include_prices: bool = False,
    strict: bool = True,
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
    ceil_price : float or None, default None
        Maximum price ceiling in TL/MWh. If None, the ceiling currently in force is
        resolved at call time (4500.0 since 2026-04-04).
    V : float, default 150
        Reference/threshold price in TL/MWh.
        These literal defaults are the values in force from 2026-01-01.
        They are deliberately NOT resolved from the calendar: a call
        without a contract cannot know the delivery hour, so resolving
        'today's value' would silently change results on a regulation
        boundary. The ``*_by_contract`` and ``*_by_datetime`` helpers
        resolve the applicable set from
        :func:`get_time_regulation_params_map` (V is 100 from 2026-11-01).
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
        strict=strict,
        **kwargs,
    )

    neg_imb_cost = round(price_d["neg_imb_price"] - mcp, 2)
    pos_imb_cost = round(mcp - price_d["pos_imb_price"], 2)

    cost_d = {
        "unit_pos_imb_cost": pos_imb_cost,
        "unit_neg_imb_cost": neg_imb_cost,
    }

    if include_prices:
        # cost_d = {k + "_cost": v for k, v in cost_d.items()}
        cost_d = {
            "pos_imb_price": price_d["pos_imb_price"],
            "neg_imb_price": price_d["neg_imb_price"],
            **cost_d,
        }

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

    pos_imb_cost = round(mcp - d["pos_imb_price"], 2)
    neg_imb_cost = round(d["neg_imb_price"] - mcp, 2)

    if include_prices:
        cost_d = {"unit_pos_imb_cost": pos_imb_cost, "unit_neg_imb_cost": neg_imb_cost}
        cost_d = {
            "pos_imb_price": d["pos_imb_price"],
            "neg_imb_price": d["neg_imb_price"],
            **cost_d,
        }
    else:
        cost_d = {
            "unit_pos_imb_cost": round(pos_imb_cost, 2),
            "unit_neg_imb_cost": round(neg_imb_cost, 2),
        }

    return cost_d


def calculate_unit_price_and_costs_by_datetime(
    dt: str | datetime,
    mcp: float,
    smp: float,
    include_kupst: bool = True,
    include_dynamic_floor_ceil: bool = True,
    **kwargs,
):
    """
    Calculate unit imbalance prices, costs, and optionally KUPST cost using a datetime.
    """
    contract = iso_to_contract(dt)
    res = calculate_unit_price_and_costs_by_contract(
        contract=contract,
        mcp=mcp,
        smp=smp,
        include_kupst=include_kupst,
        include_dynamic_floor_ceil=include_dynamic_floor_ceil,
        **kwargs,
    )

    return res


def calculate_unit_price_and_costs_by_contract(
    contract: str,
    mcp: float,
    smp: float,
    include_kupst: bool = True,
    include_dynamic_floor_ceil: bool = True,
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
        - kupst_category : str, default 'other'. KUPST category for the
          multiplier (see get_kupst_params_by_contract)
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

    if include_dynamic_floor_ceil:
        fc_d = contract_to_floor_ceil_prices(contract)
        ## fc_d is None when the contract predates the dynamic floor/ceil price map;
        ## fall back to the regulation-period defaults in that case
        if fc_d is not None:
            ## Only set floor and ceil if not already provided in kwargs, to allow overrides
            kwargs["floor_price"] = kwargs.get("floor_price", fc_d["min"])
            kwargs["ceil_price"] = kwargs.get("ceil_price", fc_d["max"])

    ## V, B and the margins can change within a regulation period.
    kwargs = inject_regulation_params(contract, kwargs)
    ## So can KUPST multipliers, which depend on the KUPST category.
    inject_kupst_params(contract, kwargs, category=kwargs.pop("kupst_category", "other"))

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
    regulation_period: Literal["current", "26_01", "pre_2026"] = "current",
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
            kupst_multiplier = kwargs.get("kupst_multiplier")
            if kupst_multiplier is None:
                kupst_multiplier = (
                    0.08 if kwargs.get("include_maintenance_penalty", False) else 0.05
                )
            unit_kupst = calculate_unit_kupst_cost_2026(
                mcp=mcp,
                smp=smp,
                kupst_floor_price=kwargs.get("kupst_floor_price", 750.0),
                kupst_multiplier_default=kupst_multiplier,
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
    regulation_period: Literal["current", "26_01", "pre_2026"] = "current",
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


def calculate_diff_costs_by_datetime(
    forecast: float,
    actual: float,
    is_producer: bool,
    dt: str | datetime,
    mcp: float,
    smp: float,
    production_source: str | None = None,
    include_quantities: bool = False,
    include_dynamic_floor_ceil: bool = True,
    **kwargs,
) -> dict | float:
    """
    Calculate total imbalance and KUPST costs for a single period using a datetime with ISO format.
    """

    contract = iso_to_contract(dt)

    return calculate_diff_costs_by_contract(
        forecast=forecast,
        actual=actual,
        is_producer=is_producer,
        contract=contract,
        mcp=mcp,
        smp=smp,
        production_source=production_source,
        include_quantities=include_quantities,
        include_dynamic_floor_ceil=include_dynamic_floor_ceil,
        **kwargs,
    )


def calculate_diff_costs_by_contract(
    forecast: float,
    actual: float,
    is_producer: bool,
    contract: str,
    mcp: float,
    smp: float,
    production_source: str | None = None,
    include_quantities: bool = False,
    include_dynamic_floor_ceil: bool = True,
    **kwargs,
) -> dict | float:
    """
    Calculate total imbalance and KUPST costs for a single period using a contract code.

    This is a convenience function that determines the regulation period from the
    contract code and calculates both imbalance costs and KUPST costs.

    Parameters
    ----------
    forecast : float
        Forecasted/planned quantity in MWh (production for producers, consumption for consumers).
    actual : float
        Actual realized quantity in MWh.
    is_producer : bool
        True if this is a production unit, False if it's a consumption unit.
        This affects how deviations are interpreted (producer surplus vs. consumer deficit).
    contract : str
        Contract code in format 'PHYYMMDDhh' (e.g., 'PH26010100'). Used to determine
        the applicable regulation period.
    mcp : float
        Market Clearing Price in TL/MWh.
    smp : float
        System Marginal Price in TL/MWh.
    production_source : str, optional
        Energy source type, or KUPST category from 2026 (see
        get_kupst_params_by_contract). Required for producers to determine KUPST
        tolerance and multiplier. Not needed for consumers. 'sun' is aliased
        to 'solar'.
    include_quantities : bool, default False
        If True, returned dictionary includes imbalance quantity and KUPST deviation quantity.
    **kwargs
        Additional parameters:
        - All regulation-specific parameters passed to underlying functions
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
    >>> calculate_diff_costs_by_contract(
    ...     forecast=120,
    ...     actual=100,
    ...     is_producer=True,
    ...     contract='PH26010100',
    ...     mcp=100,
    ...     smp=110,
    ...     production_source='wind'
    ... )
    {'imb_cost': 100.0, 'kupst_cost': 90.0, 'total_cost': 190.0}
    >>> calculate_diff_costs_by_contract(
    ...     forecast=120,
    ...     actual=100,
    ...     is_producer=True,
    ...     contract='PH26010100',
    ...     mcp=100,
    ...     smp=110,
    ...     production_source='wind',
    ...     include_quantities=True
    ... )
    {'imb_cost': 100.0, 'kupst_cost': 90.0, 'total_cost': 190.0, 'imb_qty': -20.0, 'kupsm': 2.0}
    """
    regulation_period = get_regulation_period_by_contract(contract)

    if include_dynamic_floor_ceil:
        fc_d = contract_to_floor_ceil_prices(contract)
        # fc_d is None when the contract predates the dynamic floor/ceil price map;
        # fall back to the regulation-period defaults in that case
        if fc_d is not None:
            # Only set floor and ceil if not already provided in kwargs, to allow overrides
            kwargs["floor_price"] = kwargs.get("floor_price", fc_d["min"])
            kwargs["ceil_price"] = kwargs.get("ceil_price", fc_d["max"])

    ## V, B and the margins can change within a regulation period.
    kwargs = inject_regulation_params(contract, kwargs)
    ## So can KUPST multipliers and tolerances, which depend on the category.
    kupst_d = inject_kupst_params(contract, kwargs, category=production_source)
    if kupst_d is not None and production_source is not None:
        kwargs.setdefault("kupst_tol", kupst_d["tolerance"])

    return calculate_diff_costs(
        forecast=forecast,
        actual=actual,
        is_producer=is_producer,
        mcp=mcp,
        smp=smp,
        production_source=production_source,
        regulation_period=regulation_period,
        include_quantities=include_quantities,
        **kwargs,
    )


def calculate_diff_costs(
    forecast: float,
    actual: float,
    is_producer: bool,
    mcp: float,
    smp: float,
    production_source: str | None = None,
    regulation_period: Literal["current", "26_01", "pre_2026"] | None = "current",
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
    regulation_period : {'current', '26_01', 'pre_2026'}, default 'current'
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

    kupst_tol = kwargs.pop("kupst_tol", None)

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

        if kupst_tol is None:
            kupst_tol = get_kupst_tolerance(
                source=production_source if production_source is not None else "default",
                regulation_period=regulation_period,
            )
        kupsm = calculate_kupsm(tol=kupst_tol, actual=actual, forecast=forecast)

    cost_d = calculate_unit_price_and_costs(
        mcp=mcp,
        smp=smp,
        regulation_period=regulation_period,
        include_kupst=kwargs.pop("include_kupst", True),
        **kwargs,
    )

    imb_cost = round(
        abs(signed_imb_qty)
        * cost_d["unit_neg_imb_cost" if signed_imb_qty < 0 else "unit_pos_imb_cost"],
        2,
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

    imb_side = "unit_neg_imb_cost" if individual_imbalance < 0 else "unit_pos_imb_cost"
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

    for x, y, n, p in zip(
        forecast_values,
        actual_values,
        cost_d["unit_neg_imb_cost"],
        cost_d["unit_pos_imb_cost"],
    ):
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
            "unit_pos_imb_cost" if x < 0 else "unit_neg_imb_cost" for x in res_d["diff"]
        ]
    else:
        res_d["imbalance_direction"] = [
            "unit_pos_imb_cost" if x > 0 else "unit_neg_imb_cost" for x in res_d["diff"]
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

    d = {"unit_pos_imb_cost": [], "unit_neg_imb_cost": []}

    for mcp_x, smp_x in zip(mcp, smp):
        if mcp_x is None or smp_x is None:
            raise ValueError("MCP and SMP lists must not contain None values")
        sub_d = calculate_unit_imbalance_cost_pre_2026(mcp=mcp_x, smp=smp_x)
        d["unit_pos_imb_cost"].append(sub_d["unit_pos_imb_cost"])
        d["unit_neg_imb_cost"].append(sub_d["unit_neg_imb_cost"])

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
    ceil_price: float | None = None,
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
    ceil_price: float | None = None,
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
    ceil_price: Price ceiling (None = ceiling in force, 4500 TL/MWh since 2026-04-04)
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
        "pos_imb_price": [min(x, y) * 0.97 for x, y in zip(mcp, smp)],
        "neg_imb_price": [1.03 * max(x, y) for x, y in zip(mcp, smp)],
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


def calculate_kupst_cost_list(
    actual_values: list,
    forecast_values: list,
    mcp: list,
    smp: list,
    tol: float | None = None,
    source: str | None = None,
    kupst_multiplier: float | None = None,
    kupst_floor_price: float | None = None,
    regulation_period: Literal["current", "26_01", "pre_2026"] = "current",
    **kwargs,
):
    """
    .. deprecated:: 1.3.3
        Use list comprehension with :func:`calculate_kupsm` instead.
        This function will be removed in version 1.4.0.

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
    regulation_period : {'current', '26_01', 'pre_2026'}, default 'current'
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

    warnings.warn(
        "calculate_kupst_cost_list is deprecated, "
        "In further versions, please use the singular unit functions.",
        DeprecationWarning,
        stacklevel=2,
    )

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


### MAIN FUNCTIONS ###
## calculate_imbalance_prices and calculate_imbalance_costs resolve every
## regulation parameter (regulation period, floor and ceiling prices, V, B,
## margins, KUPST tolerance, multiplier and floor) from each hour's contract, so
## callers only supply market prices (or let them be fetched) and quantities.
## They work without pandas and return a DataFrame when pandas is installed.

_ISTANBUL_TZ = timezone(timedelta(hours=3))

## Accepted input names, in order of preference, for each field
_PRICE_FIELD_NAMES = {
    "mcp": ("mcp", "ptf"),
    "smp": ("smp", "smf"),
    "system_direction": ("system_direction", "systemStatus", "sd_sign"),
    "published_pos_imb_price": ("published_pos_imb_price", "positiveImbalance"),
    "published_neg_imb_price": ("published_neg_imb_price", "negativeImbalance"),
}


def _to_contract(value, end: bool = False) -> str | None:
    """Contract of a contract code, date ('YYYY-MM-DD', start or end hour of
    the day), ISO datetime string or datetime/date object."""
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        if value.startswith("PH"):
            return value
        if len(value) == 10:
            value = datetime.strptime(value, "%Y-%m-%d").date()
        else:
            value = datetime.fromisoformat(value)
    if isinstance(value, datetime):
        if value.tzinfo is not None:
            value = value.astimezone(_ISTANBUL_TZ)
        return value.strftime("PH%y%m%d%H")
    if isinstance(value, date):
        return value.strftime("PH%y%m%d") + ("23" if end else "00")
    raise ValueError(f"Cannot convert {value!r} to a contract")


def _contract_to_date_str(contract: str) -> str:
    return f"20{contract[2:4]}-{contract[4:6]}-{contract[6:8]}"


def _to_records(data) -> list[dict]:
    """List of dicts from a DataFrame, a list of dicts or an API response."""
    if data is None:
        return []
    if hasattr(data, "to_dict"):
        return data.to_dict("records")
    if isinstance(data, dict):
        return list(data.get("items", [data]))
    return [dict(row) for row in data]


def _get_field(row: dict, field: str):
    for name in _PRICE_FIELD_NAMES[field]:
        value = row.get(name)
        if value is not None and not (isinstance(value, float) and math.isnan(value)):
            return value
    return None


def _row_contract(row: dict) -> str:
    if row.get("contract") is not None:
        return row["contract"]
    if row.get("date") is not None:
        return _to_contract(row["date"])
    raise ValueError("Each row needs a 'date' or 'contract'")


def _maybe_df(rows: list[dict], return_df: bool):
    if not return_df:
        return rows
    try:
        import pandas as pd
    except ImportError:
        return rows
    return pd.DataFrame(rows)


def _fetch_mcp_smp_imb(start_contract: str, end_contract: str, eptr=None, **kwargs) -> list[dict]:
    if eptr is None:
        from eptr2 import EPTR2

        eptr = EPTR2(dotenv_path=kwargs.get("dotenv_path", ".env"))

    res = eptr.call(
        "mcp-smp-imb",
        start_date=_contract_to_date_str(start_contract),
        end_date=_contract_to_date_str(end_contract),
    )
    rows = _to_records(res)
    if len(rows) == 0:
        raise ValueError(
            "No MCP/SMP data returned for the period. SMP and system direction are "
            "published after delivery; for future hours pass prices explicitly."
        )
    return rows


def _kupst_params_for_row(contract, category, include_maintenance_penalty, kupst_multiplier=None, kupst_floor_price=None):
    """Tolerance, multiplier and floor applying to a contract and category."""
    kupst_d = get_kupst_params_by_contract(
        contract,
        category=category,
        include_maintenance_penalty=include_maintenance_penalty,
    )
    if kupst_d is None:
        ## Pre-2026 values, the same defaults as calculate_unit_kupst_cost
        category = normalize_kupst_category(category)
        kupst_d = {
            "category": category if category in ("wind", "solar") else "other",
            "tolerance": get_kupst_tolerance_by_contract(contract, category),
            "multiplier": 0.05 if include_maintenance_penalty else 0.03,
            "floor_price": 750.0,
        }
    if kupst_multiplier is not None:
        kupst_d["multiplier"] = kupst_multiplier
    if kupst_floor_price is not None:
        kupst_d["floor_price"] = kupst_floor_price
    return kupst_d


def calculate_imbalance_prices(
    start_date=None,
    end_date=None,
    prices=None,
    eptr=None,
    kupst_category: str = "other",
    include_maintenance_penalty: bool = False,
    return_df: bool = True,
    **kwargs,
):
    """
    Hourly imbalance prices, unit costs and every regulation parameter used to
    calculate them, resolved automatically from each hour's delivery date.

    For each hour the regulation period, price floor and ceiling, V, B, low,
    high and ceiling margins and the KUPST tolerance, multiplier and floor price
    are looked up (see get_time_regulation_params_map and
    contract_to_floor_ceil_prices), so a range spanning regulation changes is
    priced correctly hour by hour.

    Market prices come from ``prices`` if given, otherwise they are fetched
    from EPİAŞ (mcp-smp-imb) for the range. Fetched hours also carry the
    published imbalance prices, so calculated and published prices can be
    compared.

    Args:
        start_date: Start of the range: 'YYYY-MM-DD', ISO datetime, contract
            code or datetime. Required unless ``prices`` is given.
        end_date: End of the range (inclusive). A date means its last hour.
        prices: Hourly prices as a DataFrame or list of dicts with 'date' (or
            'contract'), 'mcp' (or 'ptf') and 'smp' (or 'smf'), and optionally
            'system_direction' (-1/0/1, or EPİAŞ 'systemStatus' labels such as
            'Enerji Açığı'). The raw mcp-smp-imb response is accepted as is.
            Rows outside start_date/end_date are dropped.
        eptr: EPTR2 client for fetching. Created from .env if needed.
        kupst_category: KUPST category or source name for the KUPST columns
            (see normalize_kupst_category).
        include_maintenance_penalty: Use the KUPST maintenance multiplier.
        return_df: Return a pandas DataFrame if pandas is installed, otherwise
            (or if False) a list of dicts.
        **kwargs: Explicit parameter overrides that win over the resolved ones:
            floor_price, ceil_price, V, B, low_margin, high_margin,
            ceil_margin, kupst_multiplier, kupst_floor_price.

    Returns:
        One row per hour with: date, contract, regulation_period, mcp, smp,
        system_direction, floor_price, ceil_price, V, B, low_margin,
        high_margin, ceil_margin (None before 2026, whose formula does not use
        them), pos_imb_price, neg_imb_price, unit_pos_imb_cost,
        unit_neg_imb_cost, kupst_category, kupst_tolerance, kupst_multiplier,
        kupst_floor_price, unit_kupst_cost and, when available,
        published_pos_imb_price and published_neg_imb_price.

    Notes:
        When MCP equals SMP the system direction cannot be inferred from
        prices. Fetched data carries the published direction; for given prices
        without a direction such hours are priced as balanced and a warning is
        raised.

    Examples:
        >>> calculate_imbalance_prices("2026-10-01", "2026-10-07", eptr=eptr)
        >>> calculate_imbalance_prices(prices=[
        ...     {"date": "2026-11-01T00:00:00+03:00", "mcp": 120, "smp": 130,
        ...      "system_direction": -1}], kupst_category="Rüzgar")
    """
    start_contract = _to_contract(start_date)
    end_contract = _to_contract(end_date, end=True)

    if prices is None:
        if start_contract is None or end_contract is None:
            raise ValueError("start_date and end_date are required unless prices are given")
        rows = _fetch_mcp_smp_imb(start_contract, end_contract, eptr=eptr, **kwargs)
    else:
        rows = _to_records(prices)

    overrides = {
        k: kwargs[k]
        for k in ("floor_price", "ceil_price") + IMBALANCE_PARAM_KEYS
        if kwargs.get(k) is not None
    }

    result = []
    n_ambiguous = 0
    for row in rows:
        contract = _row_contract(row)
        if start_contract is not None and contract < start_contract:
            continue
        if end_contract is not None and contract > end_contract:
            continue

        mcp = _get_field(row, "mcp")
        smp = _get_field(row, "smp")
        system_direction = normalize_system_direction(_get_field(row, "system_direction"))
        if system_direction is None and mcp == smp:
            n_ambiguous += 1

        regulation_period = get_regulation_period_by_contract(contract)
        params = {}
        fc_d = contract_to_floor_ceil_prices(contract)
        if fc_d is not None:
            params["floor_price"] = fc_d["min"]
            params["ceil_price"] = fc_d["max"]
        reg_params = contract_to_regulation_params(contract)
        for key in IMBALANCE_PARAM_KEYS:
            params[key] = reg_params[key] if reg_params is not None else None
        params.update(overrides)

        kupst_d = _kupst_params_for_row(
            contract,
            kupst_category,
            include_maintenance_penalty,
            kupst_multiplier=kwargs.get("kupst_multiplier"),
            kupst_floor_price=kwargs.get("kupst_floor_price"),
        )

        cost_d = calculate_unit_price_and_costs_by_contract(
            contract=contract,
            mcp=mcp,
            smp=smp,
            system_direction=system_direction,
            kupst_multiplier=kupst_d["multiplier"],
            kupst_floor_price=kupst_d["floor_price"],
            **{k: v for k, v in params.items() if v is not None},
        )

        out = {
            "date": row.get("date"),
            "contract": contract,
            "regulation_period": regulation_period,
            "mcp": mcp,
            "smp": smp,
            "system_direction": system_direction,
            "floor_price": params.get("floor_price"),
            "ceil_price": params.get("ceil_price"),
            **{key: params[key] for key in IMBALANCE_PARAM_KEYS},
            "pos_imb_price": cost_d["pos_imb_price"],
            "neg_imb_price": cost_d["neg_imb_price"],
            "unit_pos_imb_cost": cost_d["unit_pos_imb_cost"],
            "unit_neg_imb_cost": cost_d["unit_neg_imb_cost"],
            "kupst_category": kupst_d["category"],
            "kupst_tolerance": kupst_d["tolerance"],
            "kupst_multiplier": kupst_d["multiplier"],
            "kupst_floor_price": kupst_d["floor_price"],
            "unit_kupst_cost": cost_d["unit_kupst"],
        }
        for field in ("published_pos_imb_price", "published_neg_imb_price"):
            value = _get_field(row, field)
            if value is not None:
                out[field] = value
        result.append(out)

    if n_ambiguous > 0:
        warnings.warn(
            f"{n_ambiguous} hour(s) have MCP == SMP and no system direction; they are "
            "priced as balanced. Pass system_direction (or EPİAŞ systemStatus) to "
            "price them correctly.",
            stacklevel=2,
        )

    result.sort(key=lambda x: x["contract"])
    return _maybe_df(result, return_df)


def calculate_imbalance_costs(
    data=None,
    actual: float | None = None,
    forecast: float | None = None,
    date=None,
    category: str = "other",
    is_producer: bool = True,
    prices=None,
    eptr=None,
    include_maintenance_penalty: bool = False,
    return_df: bool = True,
    **kwargs,
):
    """
    Imbalance and KUPST costs of actual vs forecast quantities, with every
    price and regulation parameter pulled automatically.

    The hours of ``data`` define the range; calculate_imbalance_prices supplies
    the hourly prices, unit costs and parameters (fetched from EPİAŞ unless
    ``prices`` is given). KUPST tolerance and multiplier follow each row's
    category and date.

    Args:
        data: Hourly quantities as a DataFrame or list of dicts with 'date' (or
            'contract'), 'actual' and 'forecast' in MWh. Optional per row
            columns 'category' (or 'source') and 'is_producer' override the
            function arguments, so a portfolio can mix plant types.
        actual, forecast, date: A single hour instead of ``data``.
        category: KUPST category or source name in any common convention
            (e.g. 'wind', 'Rüzgar', 'GES', 'Müstakil depolama'), see
            normalize_kupst_category.
        is_producer: Production (True) or consumption (False) unit. KUPST
            applies to producers only.
        prices: Hourly prices passed to calculate_imbalance_prices. Fetched
            from EPİAŞ if None.
        eptr: EPTR2 client for fetching.
        include_maintenance_penalty: Use the KUPST maintenance multiplier.
        return_df: Return a pandas DataFrame if pandas is installed.
        **kwargs: Parameter overrides passed to calculate_imbalance_prices.

    Returns:
        One row per input row with the input columns and contract, category,
        is_producer, mcp, smp, system_direction, pos_imb_price, neg_imb_price,
        imb_qty (positive surplus, negative deficit), unit_imb_cost, imb_cost,
        kupst_tolerance, kupsm, unit_kupst_cost, kupst_cost (0 for consumers)
        and total_cost, in TL.

    Notes:
        Imbalance is the raw deviation of the unit; balancing group (DSG)
        tolerance and netting are not applied.

    Examples:
        >>> calculate_imbalance_costs(
        ...     actual=80, forecast=100, date="2026-11-01T10:00:00+03:00",
        ...     category="Rüzgar", eptr=eptr)
    """
    if data is None:
        if actual is None or forecast is None or date is None:
            raise ValueError("Provide data, or actual, forecast and date")
        rows = [{"date": date, "actual": actual, "forecast": forecast}]
    else:
        rows = _to_records(data)
    if len(rows) == 0:
        return _maybe_df([], return_df)

    contracts = [_row_contract(row) for row in rows]
    price_rows = calculate_imbalance_prices(
        start_date=min(contracts),
        end_date=max(contracts),
        prices=prices,
        eptr=eptr,
        return_df=False,
        **kwargs,
    )
    price_by_contract = {p["contract"]: p for p in price_rows}

    result = []
    for row, contract in zip(rows, contracts):
        price = price_by_contract.get(contract)
        if price is None:
            raise ValueError(f"No prices for {contract}")

        row_category = row.get("category", row.get("source")) or category
        row_is_producer = row.get("is_producer")
        row_is_producer = is_producer if row_is_producer is None else bool(row_is_producer)

        imb_qty = calculate_imbalance_amount(
            actual=row["actual"],
            forecast=row["forecast"],
            is_producer=row_is_producer,
            just_raw_imbalance=True,
            regulation_period=price["regulation_period"],
        )
        unit_imb_cost = price["unit_neg_imb_cost" if imb_qty < 0 else "unit_pos_imb_cost"]
        imb_cost = round(abs(imb_qty) * unit_imb_cost, 2)

        kupst = {"kupst_tolerance": None, "kupsm": 0.0, "unit_kupst_cost": None, "kupst_cost": 0.0}
        if row_is_producer:
            kupst_d = _kupst_params_for_row(
                contract,
                row_category,
                include_maintenance_penalty,
                kupst_multiplier=kwargs.get("kupst_multiplier"),
                kupst_floor_price=kwargs.get("kupst_floor_price"),
            )
            detail = calculate_kupst_cost(
                actual=row["actual"],
                forecast=row["forecast"],
                mcp=price["mcp"],
                smp=price["smp"],
                tol=kupst_d["tolerance"],
                kupst_multiplier=kupst_d["multiplier"],
                kupst_floor_price=kupst_d["floor_price"],
                regulation_period=price["regulation_period"],
                return_detail=True,
            )
            kupst = {
                "kupst_tolerance": kupst_d["tolerance"],
                "kupsm": detail["kupsm"],
                "unit_kupst_cost": detail["unit_kupst_cost"],
                "kupst_cost": round(detail["kupst_cost"], 2),
            }

        result.append(
            {
                **row,
                "contract": contract,
                "category": normalize_kupst_category(row_category),
                "is_producer": row_is_producer,
                "mcp": price["mcp"],
                "smp": price["smp"],
                "system_direction": price["system_direction"],
                "pos_imb_price": price["pos_imb_price"],
                "neg_imb_price": price["neg_imb_price"],
                "imb_qty": imb_qty,
                "unit_imb_cost": unit_imb_cost,
                "imb_cost": imb_cost,
                **kupst,
                "total_cost": round(imb_cost + kupst["kupst_cost"], 2),
            }
        )

    return _maybe_df(result, return_df)


### MAIN FUNCTIONS END ###
