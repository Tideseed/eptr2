"""KÜPST coefficients of the 2026 periods against the EPDK decisions (issue #8, no credentials needed).

26_01: Decision 14029 (RG 29/12/2025 No. 33122), 2026-01-01 to 2026-10-31.
26_02: Decision 14907 (RG 19/10/2026 No. 33405), from 2026-11-01.
"""
import pytest

from eptr2.util.costs import (
    calculate_kupst_cost,
    get_kupst_params_by_contract,
    is_kupst_maintenance_penalty_applicable,
)

OCT, NOV = "PH26101512", "PH26111512"


@pytest.mark.parametrize(
    "contract, category, tolerance, multiplier",
    [
        (OCT, "wind", 0.15, 0.05),
        (OCT, "solar", 0.08, 0.05),
        (OCT, "plant_w_battery", 0.05, 0.10),  # Article 2 (a), was 'other' 0.05
        (OCT, "other", 0.05, 0.05),
        (OCT, "unlicensed_from_transmission", 0.20, 0.02),  # Article 2 (c), was 0.05
        (NOV, "plant_w_battery", 0.05, 0.10),
        (NOV, "unlicensed_from_transmission", 0.20, 0.02),
        (NOV, "unlicensed_from_distribution", 0.25, 0.01),
        (NOV, "battery", 0.20, 0.02),
    ],
)
def test_kupst_coefficients(contract, category, tolerance, multiplier):
    params = get_kupst_params_by_contract(contract, category)
    assert params["tolerance"] == tolerance
    assert params["multiplier"] == multiplier


@pytest.mark.parametrize("contract", [OCT, NOV])
@pytest.mark.parametrize(
    "category, threshold", [("wind", 30), ("solar", 30), ("other", 25)]
)
def test_maintenance_threshold(contract, category, threshold):
    assert not is_kupst_maintenance_penalty_applicable(contract, category, threshold - 1)
    assert is_kupst_maintenance_penalty_applicable(contract, category, threshold)


@pytest.mark.parametrize("contract", [OCT, NOV])
def test_no_maintenance_multiplier_for_flat_rates(contract):
    ## Article 2 (a) and (c) are flat rates: no fault-entry table
    for category in ("plant_w_battery", "unlicensed_from_transmission"):
        assert not is_kupst_maintenance_penalty_applicable(contract, category, 100)


def test_kupsm_tol_is_the_tolerance_amount():
    detail = calculate_kupst_cost(
        actual=100, forecast=120, mcp=100, smp=110, source="wind",
        return_detail=True, regulation_period="current",
    )
    assert detail["kupst_tol_perc"] == 0.15
    assert detail["kupsm_tol"] == pytest.approx(18.0)  # MWh, forecast * tolerance
    assert detail["kupsm"] == pytest.approx(2.0)


## --- other renewables, consumption from 2027, portfolio multiplier ---

from eptr2.util.costs import (  # noqa: E402
    calculate_imbalance_costs,
    kupst_applies,
    normalize_kupst_category,
)


@pytest.mark.parametrize(
    "name, category",
    [
        ("HES", "other_renewable"),
        ("Barajlı", "other_renewable"),
        ("Akarsu", "other_renewable"),
        ("Jeotermal", "other_renewable"),
        ("JES", "other_renewable"),
        ("Biyokütle", "other_renewable"),
        ("Biyogaz", "other_renewable"),
        ("Doğalgaz", "other"),
        ("Linyit", "other"),
        ("İthal kömür", "other"),
        ("Tüketim", "consumption_other"),
        ("consumption 17", "consumption_art17"),
        ("RES", "wind"),
        ("HES + BESS", "plant_w_battery"),
    ],
)
def test_category_names(name, category):
    assert normalize_kupst_category(name) == category


@pytest.mark.parametrize("contract", [OCT, NOV])
def test_other_renewable_values(contract):
    params = get_kupst_params_by_contract(contract, "HES")
    assert (params["tolerance"], params["multiplier"]) == (0.05, 0.05)
    assert is_kupst_maintenance_penalty_applicable(contract, "HES", 30)
    assert not is_kupst_maintenance_penalty_applicable(contract, "HES", 29)


JAN27 = "PH27011512"


@pytest.mark.parametrize(
    "category, tolerance", [("consumption_art17", 0.75), ("consumption_other", 0.30)]
)
def test_consumption_from_2027(category, tolerance):
    params = get_kupst_params_by_contract(JAN27, category)
    assert (params["tolerance"], params["multiplier"]) == (tolerance, 0.01)
    assert kupst_applies(JAN27, category, is_producer=False)
    ## Production categories are unchanged from 26_02
    assert get_kupst_params_by_contract(JAN27, "wind") == get_kupst_params_by_contract(NOV, "wind")


@pytest.mark.parametrize("contract", [OCT, NOV])
def test_no_consumption_kupst_before_2027(contract):
    params = get_kupst_params_by_contract(contract, "consumption_other")
    assert params["tolerance"] is None and params["multiplier"] == 0.0
    assert not kupst_applies(contract, "consumption_other", is_producer=False)
    assert not is_kupst_maintenance_penalty_applicable(contract, "consumption_other", 100)


def test_consumer_kupst_in_cost_function():
    prices = [
        {"contract": c, "mcp": 2000.0, "smp": 2500.0, "system_direction": -1}
        for c in ("PH26121512", JAN27)
    ]
    rows = [
        {"contract": c, "actual": 50.0, "forecast": 100.0, "category": "consumption_other", "is_producer": False}
        for c in ("PH26121512", JAN27)
    ]
    dec, jan = calculate_imbalance_costs(data=rows, prices=prices, return_df=False)
    assert dec["kupst_cost"] == 0.0  # no consumption KÜPST in 2026
    ## 2027: |50 - 100| - 0.30 * 100 = 20 MWh at 0.01 * max(2000, 2500, 750) = 25 TL/MWh
    assert jan["kupsm"] == pytest.approx(20.0)
    assert jan["unit_kupst_cost"] == pytest.approx(25.0)
    assert jan["kupst_cost"] == pytest.approx(500.0)


def test_kupsm_with_negative_consumption_plan():
    from eptr2.util.costs import calculate_kupsm

    assert calculate_kupsm(actual=-50, forecast=-100, tol=0.30) == pytest.approx(20.0)
    assert calculate_kupsm(actual=10, forecast=20, tol=None) == 0.0
