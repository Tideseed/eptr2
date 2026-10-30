"""Tests for the main cost functions calculate_imbalance_prices and
calculate_imbalance_costs, which resolve every regulation parameter from the
hour's contract."""

import warnings

import pytest

from eptr2.util.costs import (
    calculate_diff_costs_by_contract,
    calculate_imbalance_costs,
    calculate_imbalance_prices,
    calculate_unit_price_and_costs_by_contract,
)

OCT = "2026-10-31T23:00:00+03:00"
NOV = "2026-11-01T00:00:00+03:00"
PRE = "2025-12-31T23:00:00+03:00"


@pytest.fixture
def prices():
    return [
        {"date": OCT, "mcp": 120, "smp": 130, "system_direction": -1},
        {"date": NOV, "mcp": 120, "smp": 130, "system_direction": "Enerji Açığı"},
        {"date": PRE, "mcp": 3000, "smp": 3500, "system_direction": -1},
    ]


def by_contract(rows):
    return {r["contract"]: r for r in rows}


class TestCalculateImbalancePrices:
    def test_parameters_follow_each_hour(self, prices):
        rows = by_contract(
            calculate_imbalance_prices(prices=prices, kupst_category="battery", return_df=False)
        )
        oct_, nov, pre = rows["PH26103123"], rows["PH26110100"], rows["PH25123123"]

        assert (oct_["V"], nov["V"]) == (150, 100)
        assert (oct_["pos_imb_price"], nov["pos_imb_price"]) == (-103.0, 116.4)
        ## Battery has its own KUPST values from November only
        assert (oct_["kupst_tolerance"], nov["kupst_tolerance"]) == (0.05, 0.20)
        assert (oct_["kupst_multiplier"], nov["kupst_multiplier"]) == (0.05, 0.02)
        assert nov["unit_kupst_cost"] == pytest.approx(750 * 0.02)

        assert (oct_["ceil_price"], pre["ceil_price"]) == (4500.0, 3400.0)
        assert pre["regulation_period"] == "pre_2026"
        assert pre["V"] is None
        assert pre["kupst_multiplier"] == 0.03

    def test_sorted_and_filtered_by_range(self, prices):
        rows = calculate_imbalance_prices(
            start_date="2026-10-31", end_date="2026-11-01", prices=prices, return_df=False
        )
        assert [r["contract"] for r in rows] == ["PH26103123", "PH26110100"]

        rows = calculate_imbalance_prices(
            start_date=NOV, end_date=NOV, prices=prices, return_df=False
        )
        assert [r["contract"] for r in rows] == ["PH26110100"]

    def test_agrees_with_by_contract_helper(self, prices):
        for row in calculate_imbalance_prices(prices=prices, return_df=False):
            ref = calculate_unit_price_and_costs_by_contract(
                contract=row["contract"], mcp=row["mcp"], smp=row["smp"],
                system_direction=row["system_direction"],
            )
            assert row["pos_imb_price"] == ref["pos_imb_price"]
            assert row["neg_imb_price"] == ref["neg_imb_price"]
            assert row["unit_kupst_cost"] == ref["unit_kupst"]

    def test_published_prices_are_used(self):
        """mcp-smp-imb rows carry the settlement prices; they replace the
        calculated ones and the unit costs follow from them."""
        raw = [{"date": NOV, "ptf": 120, "smf": 130, "systemStatus": "Enerji Açığı",
                "positiveImbalance": 110.0, "negativeImbalance": 140.0}]
        row = calculate_imbalance_prices(prices=raw, include_calculated=True, return_df=False)[0]
        assert row["imb_price_source"] == "published"
        assert (row["pos_imb_price"], row["neg_imb_price"]) == (110.0, 140.0)
        assert (row["unit_pos_imb_cost"], row["unit_neg_imb_cost"]) == (10.0, 20.0)
        ## The calculation is still available for comparison
        assert (row["calculated_pos_imb_price"], row["calculated_neg_imb_price"]) == (116.4, 137.8)
        assert "published_pos_imb_price" not in row

    def test_calculated_without_published(self, prices):
        for row in calculate_imbalance_prices(prices=prices, return_df=False):
            assert row["imb_price_source"] == "calculated"
            assert "calculated_pos_imb_price" not in row

    def test_published_hours_do_not_warn_on_equal_prices(self):
        raw = [{"date": NOV, "ptf": 100, "smf": 100, "positiveImbalance": 97.0, "negativeImbalance": 106.0}]
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            row = calculate_imbalance_prices(prices=raw, return_df=False)[0]
        assert row["neg_imb_price"] == 106.0

    def test_costs_use_published_prices(self):
        raw = [{"date": NOV, "ptf": 120, "smf": 130, "systemStatus": "Enerji Açığı",
                "positiveImbalance": 110.0, "negativeImbalance": 140.0}]
        row = calculate_imbalance_costs(
            actual=80, forecast=100, date=NOV, prices=raw, return_df=False
        )[0]
        assert row["imb_price_source"] == "published"
        assert row["imb_cost"] == pytest.approx(20 * 20.0)

    def test_overrides_win(self, prices):
        row = by_contract(
            calculate_imbalance_prices(prices=prices, V=150, kupst_multiplier=0.1, return_df=False)
        )["PH26110100"]
        assert row["V"] == 150
        assert row["pos_imb_price"] == -103.0
        assert row["kupst_multiplier"] == 0.1

    def test_equal_prices_without_direction_warn(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            calculate_imbalance_prices(prices=[{"date": NOV, "mcp": 100, "smp": 100}])
        assert any("MCP == SMP" in str(x.message) for x in w)

    def test_range_required_without_prices(self):
        with pytest.raises(ValueError):
            calculate_imbalance_prices()

    def test_returns_dataframe(self, prices):
        pd = pytest.importorskip("pandas")
        assert isinstance(calculate_imbalance_prices(prices=prices), pd.DataFrame)


class TestCalculateImbalanceCosts:
    def test_portfolio_rows(self, prices):
        data = [
            {"date": NOV, "actual": 80, "forecast": 100, "category": "Rüzgar"},
            {"date": NOV, "actual": 80, "forecast": 100, "category": "Müstakil depolama"},
            {"date": OCT, "actual": 120, "forecast": 100, "is_producer": False},
        ]
        wind, battery, consumer = calculate_imbalance_costs(data, prices=prices, return_df=False)

        assert (wind["category"], battery["category"]) == ("wind", "battery")
        ## Same imbalance, different KUPST by category
        assert wind["imb_cost"] == battery["imb_cost"] == pytest.approx(20 * 17.8)
        assert wind["kupsm"] == pytest.approx(5.0)
        assert wind["kupst_cost"] == pytest.approx(5.0 * 750 * 0.05)
        assert battery["kupsm"] == 0.0
        ## Consumers pay no KUPST; over-consumption is a negative imbalance
        assert consumer["imb_qty"] == -20
        assert consumer["kupst_cost"] == 0.0
        for row in (wind, battery, consumer):
            assert row["total_cost"] == pytest.approx(row["imb_cost"] + row["kupst_cost"])

    @pytest.mark.parametrize("date", [OCT, NOV, PRE])
    @pytest.mark.parametrize("category", ["wind", "battery", "plant_w_battery", "other"])
    @pytest.mark.parametrize("actual", [80, 120])
    def test_agrees_with_diff_costs_by_contract(self, prices, date, category, actual):
        row = calculate_imbalance_costs(
            actual=actual, forecast=100, date=date, category=category,
            prices=prices, return_df=False,
        )[0]
        price = next(p for p in prices if p["date"] == date)
        ref = calculate_diff_costs_by_contract(
            forecast=100, actual=actual, is_producer=True, contract=row["contract"],
            mcp=price["mcp"], smp=price["smp"], production_source=category,
            system_direction=-1,
        )
        assert row["imb_cost"] == pytest.approx(ref["imb_cost"])
        assert row["kupst_cost"] == pytest.approx(ref["kupst_cost"])

    def test_single_hour_and_default_category(self, prices):
        row = calculate_imbalance_costs(
            actual=80, forecast=100, date=NOV, prices=prices, return_df=False
        )[0]
        assert row["category"] == "other"
        assert row["kupsm"] == pytest.approx(15.0)

    def test_missing_prices_raise(self, prices):
        with pytest.raises(ValueError):
            calculate_imbalance_costs(
                actual=80, forecast=100, date="2026-11-02T00:00:00+03:00", prices=prices
            )


@pytest.mark.integration
def test_calculated_prices_match_published():
    """Every resolved parameter is right if the calculated prices equal the
    published ones for every hour."""
    from dotenv import load_dotenv
    from eptr2 import EPTR2

    load_dotenv(".env")
    eptr = EPTR2(recycle_tgt=True)
    for start, end in (("2026-10-01", "2026-10-07"), ("2026-02-01", "2026-02-07"), ("2025-11-01", "2025-11-07")):
        rows = calculate_imbalance_prices(
            start, end, eptr=eptr, include_calculated=True, return_df=False
        )
        assert len(rows) == 7 * 24
        for row in rows:
            assert row["imb_price_source"] == "published"
            assert abs(row["calculated_pos_imb_price"] - row["pos_imb_price"]) <= 0.01, row
            assert abs(row["calculated_neg_imb_price"] - row["neg_imb_price"]) <= 0.01, row
