"""calculate_portfolio_costs uses each plant's KÜPST multiplier (no credentials needed)."""
import pandas as pd
import pytest

import eptr2.composite.plant_costs as pc


def test_portfolio_unit_kupst_cost_follows_plant_category(tmp_path, monkeypatch):
    contracts = ["PH26101512", "PH26111512"]  # 26_01 and 26_02

    def fake_wrapper(**kw):
        return pd.DataFrame(
            {
                "contract": contracts,
                "toplam_kgup_v1": [100.0, 100.0],
                "toplam_kgup": [100.0, 100.0],
                "total_rt": [50.0, 50.0],
            }
        )

    cost_df = pd.DataFrame(
        {
            "contract": contracts,
            "mcp": [2000.0, 2000.0],
            "smp": [2500.0, 2500.0],
            "sd_sign": [-1, -1],
            "pos_imb_price": [1900.0, 1900.0],
            "neg_imb_price": [2575.0, 2575.0],
            "unit_pos_imb_cost": [100.0, 100.0],
            "unit_neg_imb_cost": [200.0, 200.0],
            "unit_kupst_cost": [125.0, 125.0],  # category 'other' (0.05 * 2500)
        }
    )
    monkeypatch.setattr(pc, "wrapper_hourly_production_plan_and_realized", fake_wrapper)
    monkeypatch.setattr(pc, "get_hourly_price_and_cost_data", lambda **kw: cost_df.copy())

    id_df = pd.DataFrame(
        {
            "plant_name": ["storage plant", "unlicensed plant", "wind plant"],
            "org_id": [1, 2, 3],
            "uevcb_id": [11, 12, 13],
            "rt_id": [21, 22, 23],
            "uevm_id": [31, 32, 33],
            "source": ["Depolamalı üretim tesisi", "İletime bağlı lisanssız", "Rüzgar"],
        }
    )
    res = pc.calculate_portfolio_costs(
        "2026-10-15", "2026-11-15", id_df, eptr=object(), export_dir=str(tmp_path), verbose=False
    )
    detail = res["costs_detail"].set_index(["plant_name", "contract"])["unit_kupst_cost"]
    ## max(MCP, SMP, floor) = 2500 TL/MWh times the plant's multiplier, in both periods
    for contract in contracts:
        assert detail[("storage plant", contract)] == pytest.approx(250.0)  # n = 0.10
        assert detail[("unlicensed plant", contract)] == pytest.approx(50.0)  # n = 0.02
        assert detail[("wind plant", contract)] == pytest.approx(125.0)  # n = 0.05
