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
