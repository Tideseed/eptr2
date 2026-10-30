"""Offline checks for get_dabi_idm_data: column meaning, the GİP ask/bid swap and the signs (no credentials needed)."""
import pandas as pd

from eptr2.composite.dabi_idm import get_dabi_idm_data, get_dabi_idm_data_period


class FakeEPTR2:
    """Returns one delivery hour (2026-10-19 00:00) for every call; records the keyword arguments it got."""

    def __init__(self):
        self.calls = []

    def call(self, key, **kw):
        self.calls.append((key, kw))
        date = "2026-10-19T00:00:00+03:00"
        if key == "dam-clearing":
            return pd.DataFrame([{"date": date, "hour": "00:00", "matchedBids": 2.0, "matchedOffers": 7.0}])
        if key == "bi-long":
            return pd.DataFrame([{"date": date, "hour": "00:00", "quantity": 1.0}])
        if key == "bi-short":
            return pd.DataFrame([{"date": date, "hour": "00:00", "quantity": 40.0}])
        if key == "idm-qty":
            # EPİAŞ naming swap: Ask = BOUGHT (1.1), Bid = SOLD (5.8)
            return pd.DataFrame([{"kontratAdi": "PH26101900", "kontratTuru": "HOURLY",
                                  "clearingQuantityAsk": 1.1, "clearingQuantityBid": 5.8}])
        raise AssertionError(f"unexpected call {key}")


def test_gip_swap_and_signs():
    df = get_dabi_idm_data("2026-10-19", "2026-10-19", eptr=FakeEPTR2(), org_id="103940")
    r = df.iloc[0]
    assert (r.da_long, r.da_short) == (2.0, 7.0)          # GÖP purchases / sales
    assert (r.bi_long, r.bi_short) == (1.0, 40.0)         # bilateral purchases / sales
    assert (r.idm_long, r.idm_short) == (1.1, 5.8)        # Ask -> purchases, Bid -> sales
    assert r.dabi_net == 2.0 - 7.0 + 1.0 - 40.0           # long minus short: net purchases
    assert round(r.idm_net, 2) == -4.7
    assert round(r.dabi_idm_net, 2) == -48.7
    assert round(r.net_sales, 2) == 48.7                  # a net seller
    assert r.org_id == "103940"


def test_period_wrapper_passes_kwargs():
    fake = FakeEPTR2()
    get_dabi_idm_data_period("2026-10-01", eptr=fake, org_id="103940", lives=1)
    assert fake.calls and all(kw.get("retry_attempts") == 1 for _, kw in fake.calls)
