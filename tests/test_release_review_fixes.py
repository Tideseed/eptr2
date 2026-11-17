"""Regression tests for the 1.4.1 pre-release review findings (no credentials needed)."""
import json

import numpy as np
import pandas as pd
import pytest

import eptr2.composite.idm_log as il
from eptr2.util.costs import (
    calculate_imbalance_costs,
    calculate_kupst_cost,
    calculate_kupst_cost_by_contract,
    calculate_unit_kupst_cost_2026,
    normalize_kupst_category,
)


def _prices(contract):
    return [{"contract": contract, "mcp": 1000.0, "smp": 2000.0, "system_direction": -1}]


## --- consumers and consumption categories ---

def test_consumer_without_category_pays_kupst_from_2027():
    row = {"contract": "PH27011010", "actual": 50.0, "forecast": 100.0, "is_producer": False}
    (r,) = calculate_imbalance_costs(data=[row], prices=_prices("PH27011010"), return_df=False)
    assert r["category"] == "consumption_other"
    ## |50 - 100| - 0.30 * 100 = 20 MWh at 0.01 * 2000 TL/MWh
    assert r["kupst_cost"] == pytest.approx(400.0)


@pytest.mark.parametrize("contract, kupst_cost", [("PH26111010", 0.0), ("PH27011010", 400.0)])
def test_consumption_category_makes_a_consumer(contract, kupst_cost):
    row = {"contract": contract, "actual": 50.0, "forecast": 100.0, "category": "Tüketim"}
    (r,) = calculate_imbalance_costs(data=[row], prices=_prices(contract), return_df=False)
    assert r["is_producer"] is False
    assert r["imb_qty"] == pytest.approx(50.0)  # consumer sign convention
    assert r["kupst_cost"] == pytest.approx(kupst_cost)


def test_consumption_source_before_2027_does_not_crash():
    d = calculate_kupst_cost_by_contract(
        contract="PH26110100", actual=50, forecast=100, mcp=1000, smp=2000,
        source="Tüketim", return_detail=True,
    )
    assert d["kupst_cost"] == 0.0 and d["kupsm_tol"] is None


## --- calculate_kupst_cost multiplier follows the source ---

@pytest.mark.parametrize(
    "source, period, unit",
    [
        ("Tüketim", "27_01", 20.0),
        ("plant_w_battery", "26_01", 200.0),
        ("unlicensed", "26_01", 40.0),
        ("battery", "26_02", 40.0),
        ("wind", "26_02", 100.0),
    ],
)
def test_kupst_cost_multiplier_follows_source(source, period, unit):
    d = calculate_kupst_cost(
        actual=50, forecast=100, mcp=1000, smp=2000, source=source,
        regulation_period=period, return_detail=True,
    )
    assert d["unit_kupst_cost"] == pytest.approx(unit)


def test_unit_kupst_cost_2026_unknown_source():
    assert calculate_unit_kupst_cost_2026(1000, 2000, source="wind") == pytest.approx(100.0)


## --- category names ---

@pytest.mark.parametrize(
    "name, category",
    [
        ("dammedHydro", "other_renewable"),
        ("Hidro", "other_renewable"),
        ("Nehir", "other_renewable"),
        ("BES", "other_renewable"),
        ("Depolama tesisi", "battery"),
        ("Elektrik depolama tesisi", "battery"),
        ("Depolamalı üretim tesisi", "plant_w_battery"),
    ],
)
def test_category_names(name, category):
    assert normalize_kupst_category(name) == category


## --- trade log cache ---

KW = dict(start_date="2026-10-20", end_date="2026-10-21")
FULL = pd.DataFrame(
    {"contractName": ["PH26102000", "PH26102100"], "price": [100.0, 120.0], "quantity": [10, 10]}
)


def test_partial_log_is_not_cached(tmp_path, monkeypatch):
    partial = FULL.iloc[:1].copy()  # 2026-10-21 missing, e.g. a failed chunk
    monkeypatch.setattr(il, "idm_log_longer", lambda **kw: partial.copy())
    stats = il.get_idm_contract_stats(**KW, export_dir=str(tmp_path))
    assert list(stats["contract"]) == ["PH26102000"]
    assert list(tmp_path.iterdir()) == []


def test_partial_files_are_not_read(tmp_path, monkeypatch):
    FULL.iloc[:1].to_csv(tmp_path / "idm_log_2026-10-20_2026-10-21.csv", index=False)
    calls = []
    monkeypatch.setattr(il, "idm_log_longer", lambda **kw: calls.append(1) or FULL.copy())
    stats = il.get_idm_contract_stats(**KW, export_dir=str(tmp_path))
    assert calls == [1] and len(stats) == 2


def test_caller_log_is_not_written(tmp_path, monkeypatch):
    monkeypatch.setattr(il, "idm_log_longer", lambda **kw: pytest.fail("must not fetch"))
    il.get_idm_contract_stats(**KW, export_dir=str(tmp_path), idm_log_df=FULL.copy())
    assert list(tmp_path.iterdir()) == []


## --- request bodies with arrays ---

def test_json_default_arrays():
    from eptr2.main import _json_default

    body = {"ids": np.array([5]), "more": np.array([1, 2]), "s": pd.Series([3]), "x": np.int64(4)}
    assert json.loads(json.dumps(body, default=_json_default)) == {"ids": [5], "more": [1, 2], "s": [3], "x": 4}


## --- portfolio cost cache needs no login ---

def test_portfolio_cached_export_without_client(tmp_path, monkeypatch):
    import eptr2.composite.plant_costs as pc

    path = tmp_path / "portfolio_costs_data_2026-10-01_2026-10-02.xlsx"
    with pd.ExcelWriter(path) as w:
        pd.DataFrame({"a": [1]}).to_excel(w, sheet_name="costs_detail", index=False)
        pd.DataFrame({"b": [2]}).to_excel(w, sheet_name="contract_summary", index=False)
    monkeypatch.setattr(pc, "EPTR2", lambda **kw: pytest.fail("must not log in"))
    res = pc.calculate_portfolio_costs(
        "2026-10-01", "2026-10-02", pd.DataFrame(), export_dir=str(tmp_path), check_existing=True
    )
    assert set(res) == {"costs_detail", "contract_summary"}
