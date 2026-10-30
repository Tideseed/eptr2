"""Regression tests for the historical price floor/ceiling map and Istanbul-time "now" handling.

The cap values are checked against the archived EPİAŞ GİP trade log (eptr2.idm_log, PH contracts):
- June 2024 GİP trades top out at exactly 2,781 (= 2,700 x 1.03); the first 3,000 / 3,090 prices are on 2024-07-01.
- February 2023: max GİP price 3,760.00 (121 trades at exactly 3,760.00, none above), so the IDM cap is 3,760,
  not 3,650 x 1.03 = 3,759.5.
- March 2023: max GİP price 3,142.00 (142 trades at exactly 3,142.00, none above), so the IDM cap is 3,142,
  not 3,050 x 1.03 = 3,141.5.
"""

from datetime import datetime

import pandas as pd
import pytest
import pytz

from eptr2.util.time import contract_to_floor_ceil_prices


@pytest.mark.parametrize(
    "contract, cap_date, dam_max, idm_max",
    [
        ("PH24063023", "2023-07-04", 2700.0, 2781.0),  # last hour before the 3,000 step
        ("PH24070100", "2024-07-01", 3000.0, 3090.0),  # first hour of the 3,000 step
    ],
)
def test_3000_cap_starts_2024_07_01(contract, cap_date, dam_max, idm_max):
    caps = contract_to_floor_ceil_prices(contract)
    assert caps["date"] == cap_date
    assert caps["max"] == dam_max
    assert caps["idm_max"] == idm_max


@pytest.mark.parametrize(
    "contract, dam_max, idm_max",
    [
        ("PH23021512", 3650.0, 3760.0),
        ("PH23031512", 3050.0, 3142.0),
    ],
)
def test_2023_idm_caps_match_the_archived_trade_maximum(contract, dam_max, idm_max):
    caps = contract_to_floor_ceil_prices(contract)
    assert caps["max"] == dam_max
    assert caps["idm_max"] == idm_max


class _RecordingEptr:
    """Stands in for EPTR2: records the dates uevcb-list-bulk is asked for."""

    def __init__(self):
        self.start_dates = []

    def call(self, key, **kwargs):
        assert key == "uevcb-list-bulk"
        self.start_dates.append(kwargs["start_date"])
        return pd.DataFrame(
            {"id": [1], "orgId": [10], "name": ["UNIT"], "eic": [f"EIC-{len(self.start_dates)}"]}
        )


def test_get_uevcb_ids_caps_the_period_at_today_in_istanbul(monkeypatch):
    """00:30 in Istanbul on 2026-10-20 is still 2026-10-19 in Berlin and UTC; the current month must end on the
    Istanbul date whatever the process's local time zone is."""
    import eptr2.composite.periodic_orgs as po

    istanbul_now = pytz.timezone("Europe/Istanbul").localize(datetime(2026, 10, 20, 0, 30))
    monkeypatch.setattr(po, "get_utc3_now", lambda: istanbul_now)
    monkeypatch.setattr(po.time, "sleep", lambda *_: None)

    eptr = _RecordingEptr()
    df = po.get_uevcb_ids(org_df=pd.DataFrame({"org_id": [10]}), period="2026-10-01", eptr=eptr)

    assert eptr.start_dates == ["2026-10-01", "2026-10-20"]
    assert {"uevcb_id", "org_id", "uevcb_name", "uevcb_eic"} <= set(df.columns)


def test_get_uevcb_ids_past_month_uses_its_last_day(monkeypatch):
    import eptr2.composite.periodic_orgs as po

    istanbul_now = pytz.timezone("Europe/Istanbul").localize(datetime(2026, 10, 20, 0, 30))
    monkeypatch.setattr(po, "get_utc3_now", lambda: istanbul_now)
    monkeypatch.setattr(po.time, "sleep", lambda *_: None)

    eptr = _RecordingEptr()
    po.get_uevcb_ids(org_df=pd.DataFrame({"org_id": [10]}), period="2026-09-01", eptr=eptr)

    assert eptr.start_dates == ["2026-09-01", "2026-09-30"]
