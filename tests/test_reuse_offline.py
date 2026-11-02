"""Composites reuse other composites and one client (no credentials needed)."""
import pandas as pd

import eptr2.composite.periodic_orgs as po
from eptr2.composite.price_and_cost import get_reference_imbalance_costs


class _PriceEPTR:
    def __init__(self):
        self.keys = []

    def call(self, key, **kwargs):
        self.keys.append(key)
        assert key == "mcp-smp-imb", key
        return pd.DataFrame(
            {
                "date": ["2026-10-20T00:00:00+03:00"],
                "time": ["00:00"],
                "ptf": [1000.0],
                "smf": [1100.0],
                "positiveImbalance": [970.0],
                "negativeImbalance": [1133.0],
                "systemStatus": ["Enerji Açığı"],
            }
        )


def test_reference_imbalance_costs_uses_price_composite():
    eptr = _PriceEPTR()
    df = get_reference_imbalance_costs("2026-10-20", "2026-10-20", eptr=eptr)
    assert eptr.keys == ["mcp-smp-imb"]  # no WAP call
    r = df.iloc[0]
    assert (r.pos_imb_cost, r.neg_imb_cost) == (30.0, 133.0)
    assert r.ref_imb_cost == 81.5


def test_generation_org_wrappers_create_one_client(monkeypatch):
    created, seen = [], []

    def fake_client(*args, **kwargs):
        created.append(object())
        return created[-1]

    monkeypatch.setattr(po, "EPTR2", fake_client)
    monkeypatch.setattr(
        po,
        "get_generation_organization_list",
        lambda period, **kw: seen.append(kw["eptr"]) or pd.DataFrame({"org_id": [1]}),
    )
    monkeypatch.setattr(
        po,
        "get_uevcb_ids",
        lambda org_df, period, **kw: seen.append(kw["eptr"]) or pd.DataFrame({"org_id": [1], "uevcb_id": [2]}),
    )
    monkeypatch.setattr(po.time, "sleep", lambda s: None)

    po.get_multiperiod_generation_org_and_uevcb_wrapper("2026-08-01", "2026-10-31")
    assert len(created) == 1 and len(seen) == 6 and all(e is created[0] for e in seen)

    created.clear(), seen.clear()
    po.get_periodic_generation_organization_lists("2026-08-01", "2026-10-31")
    assert len(created) == 1 and len(seen) == 3 and all(e is created[0] for e in seen)
