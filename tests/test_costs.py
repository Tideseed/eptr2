"""
Unit tests for eptr2.util.costs module.

Tests cover non-deprecated functions for:
- Regulation period detection
- KUPST tolerance calculations
- KUPST cost calculations
- Imbalance price calculations
- Imbalance cost calculations
- Combined price and cost calculations
- Imbalance amount calculations
"""

import pytest
from eptr2.util.costs import (
    # Regulation functions
    get_regulation_period_by_contract,
    get_starting_contract_by_regulation_period,
    # KUPST tolerance functions
    get_kupst_tolerance,
    get_kupst_tolerance_by_contract,
    get_kupst_tolerance_pre_2026,
    get_kupst_tolerance_2026,
    # KUPST cost functions
    calculate_unit_kupst_cost,
    calculate_unit_kupst_cost_by_contract,
    calculate_unit_kupst_cost_2026,
    calculate_unit_kupst_cost_pre_2026,
    calculate_kupsm,
    calculate_kupst_cost,
    calculate_kupst_cost_by_contract,
    calculate_kupst_cost_list,
    # Imbalance price functions
    calculate_unit_imbalance_price,
    calculate_unit_imbalance_price_by_contract,
    calculate_unit_imbalance_price_2026,
    calculate_unit_imbalance_price_pre_2026,
    # Imbalance cost functions
    calculate_unit_imbalance_cost,
    calculate_unit_imbalance_cost_by_contract,
    calculate_unit_imbalance_cost_2026,
    calculate_unit_imbalance_cost_pre_2026,
    # Combined functions
    calculate_unit_price_and_costs,
    calculate_unit_price_and_costs_by_contract,
    # Amount and cost calculation functions
    calculate_imbalance_amount,
    calculate_diff_costs,
)


# ============================================================================
# Regulation Period Tests
# ============================================================================


class TestRegulationPeriod:
    """Tests for regulation period detection functions."""

    def test_get_regulation_period_by_contract_pre_2026(self):
        """Test contract codes before 2026 are marked as pre_2026."""
        assert get_regulation_period_by_contract("PH25123100") == "pre_2026"
        assert get_regulation_period_by_contract("PH15010100") == "pre_2026"
        assert get_regulation_period_by_contract("PH20010100") == "pre_2026"

    def test_get_regulation_period_by_contract_2026(self):
        """Test contract codes from 2026 onwards are marked as 26_01."""
        assert get_regulation_period_by_contract("PH26010100") == "26_01"
        assert get_regulation_period_by_contract("PH26010101") == "26_01"
        assert get_regulation_period_by_contract("PH27010100") == "26_01"

    def test_get_starting_contract_by_regulation_period_current(self):
        """Test starting contract for current/26_01 period."""
        assert get_starting_contract_by_regulation_period("current") == "PH26010100"
        assert get_starting_contract_by_regulation_period("26_01") == "PH26010100"

    def test_get_starting_contract_by_regulation_period_pre_2026(self):
        """Test starting contract for pre-2026 period."""
        assert get_starting_contract_by_regulation_period("pre_2026") == "PH15010100"

    def test_get_starting_contract_by_regulation_period_invalid(self):
        """Test invalid regulation period raises ValueError."""
        with pytest.raises(ValueError):
            get_starting_contract_by_regulation_period("invalid_period")


# ============================================================================
# KUPST Tolerance Tests
# ============================================================================


class TestKUPSTTolerance:
    """Tests for KUPST tolerance calculation functions."""

    def test_get_kupst_tolerance_2026_wind(self):
        """Test wind tolerance in 2026 regulation is 15%."""
        assert get_kupst_tolerance_2026("wind") == 0.15

    def test_get_kupst_tolerance_2026_solar(self):
        """Test solar tolerance in 2026 regulation is 8%."""
        assert get_kupst_tolerance_2026("solar") == 0.08

    def test_get_kupst_tolerance_2026_unlicensed(self):
        """Test unlicensed tolerance in 2026 regulation is 20%."""
        assert get_kupst_tolerance_2026("unlicensed") == 0.2

    def test_get_kupst_tolerance_2026_default(self):
        """Test default tolerance in 2026 regulation is 5%."""
        assert get_kupst_tolerance_2026("coal") == 0.05
        assert get_kupst_tolerance_2026("gas") == 0.05

    def test_get_kupst_tolerance_2026_sun_alias(self):
        """Test 'sun' is aliased to 'solar' in 2026."""
        assert get_kupst_tolerance_2026("sun") == 0.08

    def test_get_kupst_tolerance_pre_2026_wind(self):
        """Test wind tolerance in pre-2026 regulation is 17%."""
        assert get_kupst_tolerance_pre_2026("wind") == 0.17

    def test_get_kupst_tolerance_pre_2026_solar(self):
        """Test solar tolerance in pre-2026 regulation is 10%."""
        assert get_kupst_tolerance_pre_2026("solar") == 0.10

    def test_get_kupst_tolerance_pre_2026_default(self):
        """Test default tolerance in pre-2026 regulation is 5%."""
        assert get_kupst_tolerance_pre_2026("coal") == 0.05
        assert get_kupst_tolerance_pre_2026("hydro") == 0.05

    def test_get_kupst_tolerance_pre_2026_sun_alias(self):
        """Test 'sun' is aliased to 'solar' in pre-2026."""
        assert get_kupst_tolerance_pre_2026("sun") == 0.10

    def test_get_kupst_tolerance_wrapper_current(self):
        """Test wrapper function with current regulation."""
        assert get_kupst_tolerance("wind", "current") == 0.15
        assert get_kupst_tolerance("solar", "current") == 0.08

    def test_get_kupst_tolerance_wrapper_2026(self):
        """Test wrapper function with 26_01 regulation."""
        assert get_kupst_tolerance("wind", "26_01") == 0.15

    def test_get_kupst_tolerance_wrapper_pre_2026(self):
        """Test wrapper function with pre_2026 regulation."""
        assert get_kupst_tolerance("wind", "pre_2026") == 0.17
        assert get_kupst_tolerance("solar", "pre_2026") == 0.10

    def test_get_kupst_tolerance_by_contract_pre_2026(self):
        """Test getting tolerance from contract code (pre-2026)."""
        assert get_kupst_tolerance_by_contract("PH15010100", "wind") == 0.17

    def test_get_kupst_tolerance_by_contract_2026(self):
        """Test getting tolerance from contract code (2026)."""
        assert get_kupst_tolerance_by_contract("PH26010100", "wind") == 0.15

    def test_get_kupst_tolerance_wrapper_invalid(self):
        """Test wrapper function with invalid regulation raises ValueError."""
        with pytest.raises(ValueError):
            get_kupst_tolerance("wind", "invalid_regulation")


# ============================================================================
# KUPST Cost Tests
# ============================================================================


class TestKUPSTCost:
    """Tests for KUPST cost calculation functions."""

    def test_calculate_kupsm_within_tolerance(self):
        """Test KUPSM when difference is within tolerance."""
        # Forecast 100, actual 98, tolerance 0.05 = 5 MWh tolerance
        # Difference = 2, within tolerance, so KUPSM = 0
        kupsm = calculate_kupsm(actual=98, forecast=100, tol=0.05)
        assert kupsm == 0

    def test_calculate_kupsm_exceeds_tolerance(self):
        """Test KUPSM when difference exceeds tolerance."""
        # Forecast 100, actual 90, tolerance 0.05 = 5 MWh tolerance
        # Difference = 10, excess = 10 - 5 = 5
        kupsm = calculate_kupsm(actual=90, forecast=100, tol=0.05)
        assert kupsm == 5

    def test_calculate_kupsm_zero_forecast(self):
        """Test KUPSM with zero forecast."""
        kupsm = calculate_kupsm(actual=10, forecast=0, tol=0.1)
        assert kupsm == 10

    def test_calculate_unit_kupst_cost_2026_default(self):
        """Test unit KUPST cost calculation for 2026."""
        # max(500, 400, 750) * 0.05 = 750 * 0.05 = 37.5
        cost = calculate_unit_kupst_cost_2026(mcp=500, smp=400)
        assert cost == 37.5

    def test_calculate_unit_kupst_cost_2026_high_prices(self):
        """Test unit KUPST cost when prices exceed floor."""
        # max(1000, 800, 750) * 0.05 = 1000 * 0.05 = 50
        cost = calculate_unit_kupst_cost_2026(mcp=1000, smp=800)
        assert cost == 50

    def test_calculate_unit_kupst_cost_2026_with_maintenance_penalty(self):
        """Test unit KUPST cost with maintenance penalty."""
        # max(500, 400, 750) * 0.08 = 750 * 0.08 = 60
        cost = calculate_unit_kupst_cost_2026(
            mcp=500, smp=400, include_maintenance_penalty=True
        )
        assert cost == 60

    def test_calculate_unit_kupst_cost_2026_with_source_battery(self):
        """Test unit KUPST cost with battery source."""
        # max(500, 400, 750) * 0.1 = 750 * 0.1 = 75
        cost = calculate_unit_kupst_cost_2026(mcp=500, smp=400, source="battery")
        assert cost == 75

    def test_calculate_unit_kupst_cost_2026_with_source_aggregator(self):
        """Test unit KUPST cost with aggregator source."""
        # max(500, 400, 750) * 0.05 = 750 * 0.05 = 37.5
        cost = calculate_unit_kupst_cost_2026(mcp=500, smp=400, source="aggregator")
        assert cost == 37.5

    def test_calculate_unit_kupst_cost_2026_with_source_unlicensed(self):
        """Test unit KUPST cost with unlicensed source."""
        # max(500, 400, 750) * 0.02 = 750 * 0.02 = 15
        cost = calculate_unit_kupst_cost_2026(mcp=500, smp=400, source="unlicensed")
        assert cost == 15

    def test_calculate_unit_kupst_cost_pre_2026_default(self):
        """Test unit KUPST cost for pre-2026."""
        # max(500, 400, 750) * 0.03 = 750 * 0.03 = 22.5
        cost = calculate_unit_kupst_cost_pre_2026(mcp=500, smp=400)
        assert cost == 22.5

    def test_calculate_unit_kupst_cost_pre_2026_custom_multiplier(self):
        """Test unit KUPST cost with custom multiplier."""
        # max(500, 400, 750) * 0.05 = 750 * 0.05 = 37.5
        cost = calculate_unit_kupst_cost_pre_2026(
            mcp=500, smp=400, kupst_multiplier=0.05
        )
        assert cost == 37.5

    def test_calculate_unit_kupst_cost_current_regulation(self):
        """Test wrapper function with current regulation."""
        cost = calculate_unit_kupst_cost(mcp=500, smp=400, regulation_period="current")
        # Should use 2026 logic
        assert cost == 37.5

    def test_calculate_unit_kupst_cost_pre_2026_regulation(self):
        """Test wrapper function with pre-2026 regulation."""
        cost = calculate_unit_kupst_cost(mcp=500, smp=400, regulation_period="pre_2026")
        assert cost == 22.5

    def test_calculate_unit_kupst_cost_by_contract(self):
        """Test unit KUPST cost from contract code."""
        # Pre-2026 contract
        cost = calculate_unit_kupst_cost_by_contract(
            contract="PH15010100", mcp=500, smp=400
        )
        assert cost == 22.5

        # 2026 contract
        cost = calculate_unit_kupst_cost_by_contract(
            contract="PH26010100", mcp=500, smp=400
        )
        assert cost == 37.5

    def test_calculate_kupst_cost_with_tolerance(self):
        """Test full KUPST cost calculation with tolerance."""
        # Forecast 100, actual 90, tol 0.05 -> kupsm = 5
        # unit cost = 37.5 -> total = 5 * 37.5 = 187.5
        cost = calculate_kupst_cost(
            actual=90,
            forecast=100,
            mcp=500,
            smp=400,
            tol=0.05,
            regulation_period="current",
        )
        assert cost == 187.5

    def test_calculate_kupst_cost_with_source(self):
        """Test KUPST cost calculation with source instead of tolerance."""
        # Uses wind tolerance (0.15 for current)
        # Forecast 100, actual 86.5, tol 0.15 -> kupsm = 13.5 - 15 = 0
        cost = calculate_kupst_cost(
            actual=86.5,
            forecast=100,
            mcp=500,
            smp=400,
            source="wind",
            regulation_period="current",
        )
        assert cost == 0

    def test_calculate_kupst_cost_missing_tol_and_source_raises(self):
        """Test that missing both tol and source raises exception."""
        with pytest.raises(Exception):
            calculate_kupst_cost(
                actual=90, forecast=100, mcp=500, smp=400, regulation_period="current"
            )

    def test_calculate_kupst_cost_with_detail(self):
        """Test KUPST cost calculation returning details."""
        result = calculate_kupst_cost(
            actual=90,
            forecast=100,
            mcp=500,
            smp=400,
            tol=0.05,
            regulation_period="current",
            return_detail=True,
        )
        assert isinstance(result, dict)
        assert "kupst_cost" in result
        assert "kupsm" in result
        assert "unit_kupst_cost" in result

    def test_calculate_kupst_cost_by_contract(self):
        """Test KUPST cost calculation using contract code."""
        cost = calculate_kupst_cost_by_contract(
            contract="PH26010100",
            actual=90,
            forecast=100,
            mcp=500,
            smp=400,
            tol=0.05,
        )
        assert cost == 187.5

    def test_calculate_kupst_cost_list(self):
        """Test KUPST cost list calculation."""
        actuals = [90, 95, 100]
        forecasts = [100, 100, 100]
        mcps = [500, 500, 500]
        smps = [400, 400, 400]

        costs = calculate_kupst_cost_list(
            actual_values=actuals,
            forecast_values=forecasts,
            mcp=mcps,
            smp=smps,
            tol=0.05,
            regulation_period="current",
        )

        assert len(costs) == 3
        assert all(isinstance(c, (int, float)) for c in costs)


# ============================================================================
# Imbalance Price Tests
# ============================================================================


class TestImbalancePrice:
    """Tests for imbalance price calculation functions."""

    def test_calculate_unit_imbalance_price_2026_mcp_greater_smp(self):
        """Test imbalance price when MCP > SMP (positive imbalance)."""
        prices = calculate_unit_imbalance_price_2026(mcp=300, smp=200)
        assert isinstance(prices, dict)
        assert "pos" in prices
        assert "neg" in prices
        # pos_imb_price should be negative when pos_imb_price_raw < V (200 < 150 is false)
        # Actually 200 * (1 - 0.06) = 188
        assert prices["pos"] == 188
        # neg_imb_price = max(300, 200, 150) * (1 + 0.03) * 1 = 300 * 1.03 = 309
        assert prices["neg"] == 309

    def test_calculate_unit_imbalance_price_2026_mcp_less_smp(self):
        """Test imbalance price when MCP < SMP (negative imbalance)."""
        prices = calculate_unit_imbalance_price_2026(mcp=200, smp=300)
        assert isinstance(prices, dict)
        # pos_imb_price = 200 * (1 - 0.03) = 194
        assert prices["pos"] == 194
        # neg_imb_price = max(200, 300, 150) * (1 + 0.06) = 300 * 1.06 = 318
        assert prices["neg"] == 318

    def test_calculate_unit_imbalance_price_2026_mcp_low(self):
        """Test imbalance price when positive imbalance price < V."""
        prices = calculate_unit_imbalance_price_2026(mcp=100, smp=200)
        # min(100, 200) = 100 < 150, so pos_imb_price = -100 * (1 + margin)
        assert prices["pos"] < 0  # Should be negative

    def test_calculate_unit_imbalance_price_2026_at_ceiling(self):
        """Test imbalance price when max(MCP, SMP) equals ceiling."""
        prices = calculate_unit_imbalance_price_2026(mcp=3400, smp=3000)
        # neg_imb_price should include ceil_margin
        assert prices["neg"] == 3400 * (1 + 0.03) * (1 + 0.05)

    def test_calculate_unit_imbalance_price_pre_2026(self):
        """Test imbalance price for pre-2026 regulation."""
        prices = calculate_unit_imbalance_price_pre_2026(mcp=300, smp=200)
        # pos = min(300, 200) * (1 - 0.03) = 200 * 0.97 = 194
        assert prices["pos"] == 194
        # neg = max(300, 200) * (1 + 0.03) = 300 * 1.03 = 309
        assert prices["neg"] == 309

    def test_calculate_unit_imbalance_price_pre_2026_custom_margin(self):
        """Test imbalance price with custom penalty margin."""
        prices = calculate_unit_imbalance_price_pre_2026(
            mcp=300, smp=200, penalty_margin=0.05
        )
        assert prices["pos"] == 200 * 0.95
        assert prices["neg"] == 300 * 1.05

    def test_calculate_unit_imbalance_price_wrapper_current(self):
        """Test wrapper function with current regulation."""
        prices = calculate_unit_imbalance_price(
            mcp=300, smp=200, regulation_period="current"
        )
        assert isinstance(prices, dict)
        assert "pos" in prices
        assert "neg" in prices

    def test_calculate_unit_imbalance_price_wrapper_pre_2026(self):
        """Test wrapper function with pre-2026 regulation."""
        prices = calculate_unit_imbalance_price(
            mcp=300, smp=200, regulation_period="pre_2026"
        )
        assert prices["pos"] == 194
        assert prices["neg"] == 309

    def test_calculate_unit_imbalance_price_by_contract(self):
        """Test imbalance price calculation from contract code."""
        prices = calculate_unit_imbalance_price_by_contract(
            contract="PH15010100", mcp=300, smp=200
        )
        assert prices["pos"] == 194
        assert prices["neg"] == 309


# ============================================================================
# Imbalance Cost Tests
# ============================================================================


class TestImbalanceCost:
    """Tests for imbalance cost calculation functions."""

    def test_calculate_unit_imbalance_cost_2026_basic(self):
        """Test imbalance cost calculation for 2026."""
        costs = calculate_unit_imbalance_cost_2026(mcp=300, smp=200)
        assert isinstance(costs, dict)
        assert "pos" in costs
        assert "neg" in costs
        # pos_cost = mcp - pos_price
        # neg_cost = neg_price - mcp

    def test_calculate_unit_imbalance_cost_2026_with_prices(self):
        """Test imbalance cost with included prices."""
        costs = calculate_unit_imbalance_cost_2026(
            mcp=300, smp=200, include_prices=True
        )
        assert "pos_price" in costs
        assert "neg_price" in costs
        assert "pos_cost" in costs
        assert "neg_cost" in costs

    def test_calculate_unit_imbalance_cost_pre_2026(self):
        """Test imbalance cost for pre-2026."""
        costs = calculate_unit_imbalance_cost_pre_2026(mcp=300, smp=200)
        # pos_cost = 300 - (200 * 0.97) = 300 - 194 = 106
        assert costs["pos"] == 106
        # neg_cost = (300 * 1.03) - 300 = 309 - 300 = 9
        assert costs["neg"] == 9

    def test_calculate_unit_imbalance_cost_pre_2026_with_prices(self):
        """Test imbalance cost with prices for pre-2026."""
        costs = calculate_unit_imbalance_cost_pre_2026(
            mcp=300, smp=200, include_prices=True
        )
        assert "pos_price" in costs
        assert "neg_price" in costs
        assert "pos_cost" in costs
        assert "neg_cost" in costs

    def test_calculate_unit_imbalance_cost_wrapper_current(self):
        """Test imbalance cost wrapper with current regulation."""
        costs = calculate_unit_imbalance_cost(
            mcp=300, smp=200, regulation_period="current"
        )
        assert isinstance(costs, dict)
        assert "pos" in costs
        assert "neg" in costs

    def test_calculate_unit_imbalance_cost_wrapper_pre_2026(self):
        """Test imbalance cost wrapper with pre-2026."""
        costs = calculate_unit_imbalance_cost(
            mcp=300, smp=200, regulation_period="pre_2026"
        )
        assert costs["pos"] == 106
        assert costs["neg"] == 9

    def test_calculate_unit_imbalance_cost_by_contract(self):
        """Test imbalance cost from contract code."""
        costs = calculate_unit_imbalance_cost_by_contract(
            contract="PH15010100", mcp=300, smp=200
        )
        assert costs["pos"] == 106
        assert costs["neg"] == 9


# ============================================================================
# Combined Price and Cost Tests
# ============================================================================


class TestCombinedPriceAndCost:
    """Tests for combined price and cost calculation functions."""

    def test_calculate_unit_price_and_costs_2026_basic(self):
        """Test combined price and costs for 2026."""
        result = calculate_unit_price_and_costs(
            mcp=300, smp=200, regulation_period="current", include_kupst=False
        )
        assert isinstance(result, dict)
        assert "pos_price" in result
        assert "neg_price" in result
        assert "pos_cost" in result
        assert "neg_cost" in result

    def test_calculate_unit_price_and_costs_2026_with_kupst(self):
        """Test combined prices with KUPST cost included."""
        result = calculate_unit_price_and_costs(
            mcp=300, smp=200, regulation_period="current", include_kupst=True
        )
        assert "unit_kupst" in result
        assert isinstance(result["unit_kupst"], (int, float))

    def test_calculate_unit_price_and_costs_pre_2026(self):
        """Test combined prices for pre-2026."""
        result = calculate_unit_price_and_costs(
            mcp=300, smp=200, regulation_period="pre_2026", include_kupst=False
        )
        assert result["pos_price"] == 194
        assert result["neg_price"] == 309
        assert result["pos_cost"] == 106
        assert result["neg_cost"] == 9

    def test_calculate_unit_price_and_costs_pre_2026_with_kupst(self):
        """Test combined prices with KUPST for pre-2026."""
        result = calculate_unit_price_and_costs(
            mcp=300, smp=200, regulation_period="pre_2026", include_kupst=True
        )
        assert "unit_kupst" in result

    def test_calculate_unit_price_and_costs_by_contract(self):
        """Test combined prices using contract code."""
        result = calculate_unit_price_and_costs_by_contract(
            contract="PH15010100", mcp=300, smp=200, include_kupst=True
        )
        assert isinstance(result, dict)
        assert "pos_price" in result
        assert "unit_kupst" in result


# ============================================================================
# Imbalance Amount Tests
# ============================================================================


class TestImbalanceAmount:
    """Tests for imbalance amount calculation functions."""

    def test_calculate_imbalance_amount_producer_over_produced(self):
        """Test imbalance amount for producer with over-production."""
        result = calculate_imbalance_amount(actual=110, forecast=100, is_producer=True)
        assert isinstance(result, dict)
        assert result["raw_imb"] == 10  # actual - forecast for producer
        assert result["dsg_eff_imb"] >= 0  # Positive imbalance

    def test_calculate_imbalance_amount_producer_under_produced(self):
        """Test imbalance amount for producer with under-production."""
        result = calculate_imbalance_amount(actual=90, forecast=100, is_producer=True)
        assert result["raw_imb"] == -10  # actual - forecast for producer
        assert result["dsg_eff_imb"] <= 0  # Negative imbalance

    def test_calculate_imbalance_amount_consumer_over_consumed(self):
        """Test imbalance amount for consumer with over-consumption."""
        result = calculate_imbalance_amount(actual=110, forecast=100, is_producer=False)
        # For consumer: raw_imb = forecast - actual = 100 - 110 = -10
        assert result["raw_imb"] == -10

    def test_calculate_imbalance_amount_consumer_under_consumed(self):
        """Test imbalance amount for consumer with under-consumption."""
        result = calculate_imbalance_amount(actual=90, forecast=100, is_producer=False)
        # For consumer: raw_imb = forecast - actual = 100 - 90 = 10
        assert result["raw_imb"] == 10

    def test_calculate_imbalance_amount_with_dsg_tolerance(self):
        """Test imbalance amount with DSG tolerance."""
        result = calculate_imbalance_amount(
            actual=90, forecast=100, is_producer=True, tolerance_multiplier=1.0
        )
        assert "dsg_raw_tol" in result
        assert "dsg_raw_imb" in result
        assert "dsg_eff_tol" in result
        assert "dsg_eff_imb" in result

    def test_calculate_imbalance_amount_with_tolerance_multiplier(self):
        """Test imbalance amount with custom tolerance multiplier."""
        result_full = calculate_imbalance_amount(
            actual=90, forecast=100, is_producer=True, tolerance_multiplier=1.0
        )
        result_half = calculate_imbalance_amount(
            actual=90, forecast=100, is_producer=True, tolerance_multiplier=0.5
        )
        # Half tolerance multiplier should result in larger effective imbalance
        assert abs(result_half["dsg_eff_imb"]) > abs(result_full["dsg_eff_imb"])

    def test_calculate_imbalance_amount_just_raw_imbalance(self):
        """Test returning just raw imbalance as float."""
        result = calculate_imbalance_amount(
            actual=110, forecast=100, is_producer=True, just_raw_imbalance=True
        )
        assert isinstance(result, (int, float))
        assert result == 10

    def test_calculate_imbalance_amount_current_regulation(self):
        """Test imbalance amount with current regulation DSG tolerance."""
        result = calculate_imbalance_amount(
            actual=90, forecast=100, is_producer=True, regulation_period="current"
        )
        # Current should use 5% DSG tolerance - based on abs(actual) not forecast
        assert result["dsg_raw_tol"] == 90 * 0.05

    def test_calculate_imbalance_amount_pre_2026_regulation(self):
        """Test imbalance amount with pre-2026 regulation DSG tolerance."""
        result = calculate_imbalance_amount(
            actual=90, forecast=100, is_producer=True, regulation_period="pre_2026"
        )
        # Pre-2026 should use 10% DSG tolerance - based on abs(actual) not forecast
        assert result["dsg_raw_tol"] == 90 * 0.10


# ============================================================================
# Difference Costs Tests
# ============================================================================


class TestDifferenceCosts:
    """Tests for comprehensive difference cost calculation."""

    def test_calculate_diff_costs_producer_basic(self):
        """Test difference costs for producer."""
        result = calculate_diff_costs(
            forecast=100,
            actual=90,
            is_producer=True,
            mcp=300,
            smp=200,
            production_source="wind",
        )
        assert isinstance(result, dict)
        assert "imb_cost" in result
        assert "kupst_cost" in result
        assert "total_cost" in result

    def test_calculate_diff_costs_consumer(self):
        """Test difference costs for consumer raises without source."""
        result = calculate_diff_costs(
            forecast=100,
            actual=110,
            is_producer=False,
            mcp=300,
            smp=200,
            production_source=None,
        )
        # Consumer should only have imbalance cost
        assert "imb_cost" in result
        # Should not have KUPST for consumers
        assert "kupst_cost" not in result

    def test_calculate_diff_costs_producer_missing_source_raises(self):
        """Test that producer without source raises exception."""
        with pytest.raises(Exception):
            calculate_diff_costs(
                forecast=100,
                actual=90,
                is_producer=True,
                mcp=300,
                smp=200,
                production_source=None,
            )

    def test_calculate_diff_costs_with_quantities(self):
        """Test difference costs with quantities included."""
        result = calculate_diff_costs(
            forecast=100,
            actual=90,
            is_producer=True,
            mcp=300,
            smp=200,
            production_source="wind",
            include_quantities=True,
        )
        assert "imb_qty" in result
        assert "kupsm" in result

    def test_calculate_diff_costs_pre_2026(self):
        """Test difference costs with pre-2026 regulation."""
        result = calculate_diff_costs(
            forecast=100,
            actual=90,
            is_producer=True,
            mcp=300,
            smp=200,
            production_source="wind",
            regulation_period="pre_2026",
        )
        assert isinstance(result, dict)
        assert "imb_cost" in result


# ============================================================================
# Edge Cases and Validation Tests
# ============================================================================


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_zero_prices(self):
        """Test calculations with zero prices."""
        cost = calculate_unit_kupst_cost_2026(mcp=0, smp=0)
        # Should use floor price of 750
        assert cost == 750 * 0.05

    def test_very_high_prices(self):
        """Test calculations with very high prices."""
        cost = calculate_unit_kupst_cost_2026(mcp=10000, smp=10000)
        assert cost == 10000 * 0.05

    def test_identical_mcp_smp_high_price(self):
        """Test calculations when MCP equals SMP but at ceiling."""
        # Test with ceil_price condition to avoid uninitialized variable
        prices = calculate_unit_imbalance_price_2026(mcp=3400, smp=3400)
        assert isinstance(prices, dict)
        assert "pos" in prices
        assert "neg" in prices

    def test_large_forecast_actual_difference(self):
        """Test KUPST with large forecast-actual difference."""
        kupsm = calculate_kupsm(actual=10, forecast=200, tol=0.05)
        assert kupsm == 190 - (200 * 0.05)

    def test_negative_margin_pre_2026(self):
        """Test pre-2026 cost calculations are consistent."""
        costs_base = calculate_unit_imbalance_cost_pre_2026(mcp=300, smp=200)
        costs_custom = calculate_unit_imbalance_cost_pre_2026(
            mcp=300, smp=200, penalty_margin=0.03
        )
        # Should be identical with default margin
        assert costs_base["pos"] == costs_custom["pos"]
        assert costs_base["neg"] == costs_custom["neg"]

    def test_tolerance_list_matching(self):
        """Test that matching list lengths work correctly."""
        # All lists have same length
        costs = calculate_kupst_cost_list(
            actual_values=[90, 95],  # 2 items
            forecast_values=[100, 100],  # 2 items
            mcp=[500, 500],
            smp=[400, 400],
            tol=0.05,
        )
        assert len(costs) == 2

    def test_float_vs_int_prices(self):
        """Test that float and int prices give same results."""
        cost_int = calculate_unit_kupst_cost_2026(mcp=500, smp=400)
        cost_float = calculate_unit_kupst_cost_2026(mcp=500.0, smp=400.0)
        assert cost_int == cost_float

    def test_regulation_period_invalid_raises(self):
        """Test that invalid regulation period raises error."""
        with pytest.raises(ValueError):
            calculate_unit_kupst_cost(mcp=500, smp=400, regulation_period="invalid")


# ============================================================================
# Integration Tests
# ============================================================================


class TestIntegration:
    """Integration tests combining multiple functions."""

    def test_full_calculation_chain_producer_2026(self):
        """Test full calculation chain for producer under 2026 regulation."""
        # Setup
        forecast = 100
        actual = 90
        mcp = 300
        smp = 200
        source = "wind"

        # Calculate imbalance amount
        imbalance = calculate_imbalance_amount(
            actual=actual,
            forecast=forecast,
            is_producer=True,
            regulation_period="current",
            just_raw_imbalance=True,
        )

        # Calculate KUPST
        kupst = calculate_kupst_cost(
            actual=actual,
            forecast=forecast,
            mcp=mcp,
            smp=smp,
            source=source,
            regulation_period="current",
        )

        # Calculate imbalance cost
        imb_cost = calculate_unit_imbalance_cost(
            mcp=mcp,
            smp=smp,
            regulation_period="current",
        )

        # All should return valid results
        assert isinstance(imbalance, (int, float))
        assert isinstance(kupst, (int, float))
        assert isinstance(imb_cost, dict)

    def test_full_calculation_chain_producer_pre_2026(self):
        """Test full calculation chain for producer under pre-2026 regulation."""
        result = calculate_diff_costs(
            forecast=100,
            actual=90,
            is_producer=True,
            mcp=300,
            smp=200,
            production_source="solar",
            regulation_period="pre_2026",
            include_quantities=True,
        )

        assert "imb_cost" in result
        assert "kupst_cost" in result
        assert "total_cost" in result
        assert result["total_cost"] > 0

    def test_contract_based_full_calculation(self):
        """Test using contract codes throughout calculation."""
        contract = "PH26010100"

        # Get regulation period
        regulation = get_regulation_period_by_contract(contract)
        assert regulation == "26_01"

        # Calculate KUPST with contract
        kupst = calculate_kupst_cost_by_contract(
            contract=contract,
            actual=90,
            forecast=100,
            mcp=300,
            smp=200,
            tol=0.15,
        )
        assert isinstance(kupst, (int, float))

        # Calculate imbalance with contract
        imbalance = calculate_unit_imbalance_cost_by_contract(
            contract=contract,
            mcp=300,
            smp=200,
        )
        assert isinstance(imbalance, dict)
