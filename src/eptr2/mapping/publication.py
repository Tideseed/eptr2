"""Calls whose data leaves the mandatory Transparency Platform list on 2027-01-01.

EPDK Decision 14968 (15/10/2026, Resmî Gazete 20/10/2026 No. 33406) replaces the
list of data EPİAŞ must publish on the Transparency Platform (Decision 10711) from
1 January 2027. Decision 14967 (same date and issue) moves outage and capacity
notices to the Dâhilî Bilgi Platformu (DBP, inside information platform).

The decisions set what must be published; they do not switch endpoints off. EPİAŞ
may keep serving some of these series voluntarily. Series that identify a single
market participant are a different matter: the Transparency Regulation (RG
14/2/2026 No. 33168, in force from 1/1/2027) Art. 6/4 bars publishing individual
data that reveals a participant's identity, so they are likely to stop.

`eptr.call` warns once per call key and process with
:class:`TransparencyListWarning` (a ``FutureWarning``, shown by default). Silence it
with ``warnings.filterwarnings("ignore", category=TransparencyListWarning)``.
"""

import warnings

EFFECTIVE_DATE = "2027-01-01"
SOURCE_LIST = "EPDK Decision 14968, RG 20/10/2026 No. 33406"
SOURCE_DBP = "EPDK Decision 14967, RG 20/10/2026 No. 33406"
SOURCE_ART64 = "Art. 6/4 of the Transparency Regulation (RG 14/2/2026 No. 33168)"

## kind:
##   participant  - per-participant series; not on the list and barred by Art. 6/4
##   dbp          - moves to the Dâhilî Bilgi Platformu (Decision 14967)
##   not_listed   - not on the 14968 list (no longer mandatory)
##   aggregated   - the list keeps only a total; the per-item breakdown goes
## when_params: the notice applies only when one of these parameters is given
## (the total without them stays on the list).
PUBLICATION_CHANGES: dict[str, dict] = {
    "dam-clearing": {
        "kind": "participant",
        "when_params": ["org_id"],
        "alternative": "the market total (without org_id) stays on the list (row 11)",
    },
    "dam-clearing-org-list": {
        "kind": "participant",
        "when_params": None,
        "alternative": "only market totals of GÖP matching stay on the list (row 11)",
    },
    "idm-qty": {
        "kind": "participant",
        "when_params": ["org_id"],
        "alternative": "the market total per contract (without org_id) stays on the list (row 17)",
    },
    "bi-long": {
        "kind": "participant",
        "when_params": ["org_id"],
        "alternative": "the hourly market total (without org_id) stays on the list (row 49)",
    },
    "bi-short": {
        "kind": "participant",
        "when_params": ["org_id"],
        "alternative": "the hourly market total (without org_id) stays on the list (row 50)",
    },
    "mms": {
        "kind": "dbp",
        "when_params": None,
        "alternative": "outage and maintenance notices move to the Dâhilî Bilgi Platformu "
        "(14967 rows 1-3: 30 MW per facility, 50 MW per portfolio, within 1 hour)",
    },
    "international-line-events": {
        "kind": "dbp",
        "when_params": None,
        "alternative": "transmission and interconnection outage notices move to the "
        "Dâhilî Bilgi Platformu (14967 row 4)",
    },
    "planned-outages": {
        "kind": "not_listed",
        "when_params": None,
        "alternative": None,
    },
    "unplanned-outages": {
        "kind": "not_listed",
        "when_params": None,
        "alternative": None,
    },
    "long-term-demand-forecast": {
        "kind": "not_listed",
        "when_params": None,
        "alternative": "the day-ahead load plan (load-plan, row 71) stays",
    },
    "monthly-index": {
        "kind": "not_listed",
        "when_params": None,
        "alternative": None,
    },
    "consumption-breakdown": {
        "kind": "not_listed",
        "when_params": None,
        "alternative": "consumption by province and profile group is not on the list; "
        "UEÇM (row 73) and eligible consumer consumption (row 79) stay",
    },
    "consumer-breakdown": {
        "kind": "not_listed",
        "when_params": None,
        "alternative": "consumer counts by province and profile group are not on the list; "
        "the eligible consumer count (row 78) stays",
    },
    "percentage-consumption-info": {
        "kind": "not_listed",
        "when_params": None,
        "alternative": None,
    },
    "ren-rt-gen": {
        "kind": "aggregated",
        "when_params": ["pp_id"],
        "alternative": "the list keeps YEKDEM real-time generation by source and "
        "organization (row 81); per plant, use rt-gen (row 66)",
    },
    "dams-active-fullness": {
        "kind": "aggregated",
        "when_params": ["basin_name", "dam_name"],
        "alternative": "only the Türkiye total stays on the list (row 102)",
    },
    "dams-active-volume": {
        "kind": "aggregated",
        "when_params": ["basin_name", "dam_name"],
        "alternative": "only the Türkiye total stays on the list (row 102)",
    },
    "dams-water-energy-provision": {
        "kind": "aggregated",
        "when_params": ["basin_name", "dam_name"],
        "alternative": "only the Türkiye total stays on the list (row 103)",
    },
    "dams-daily-level": {
        "kind": "not_listed",
        "when_params": None,
        "alternative": "dam data on the list are Türkiye totals: active fullness and "
        "volume (row 102) and water energy provision (row 103)",
    },
    "dams-daily-volume": {
        "kind": "not_listed",
        "when_params": None,
        "alternative": "dam data on the list are Türkiye totals: active fullness and "
        "volume (row 102) and water energy provision (row 103)",
    },
    "dams-level-minmax": {
        "kind": "not_listed",
        "when_params": None,
        "alternative": "dam data on the list are Türkiye totals: active fullness and "
        "volume (row 102) and water energy provision (row 103)",
    },
    "dams-volume-minmax": {
        "kind": "not_listed",
        "when_params": None,
        "alternative": "dam data on the list are Türkiye totals: active fullness and "
        "volume (row 102) and water energy provision (row 103)",
    },
    "dams-info": {
        "kind": "not_listed",
        "when_params": None,
        "alternative": "dam data on the list are Türkiye totals: active fullness and "
        "volume (row 102) and water energy provision (row 103)",
    },
}

_KIND_TEXT = {
    "participant": (
        f"is not on the Transparency Platform data list from {EFFECTIVE_DATE} "
        f"({SOURCE_LIST}), and {SOURCE_ART64} bars publishing individual data that "
        "identifies a market participant, so EPİAŞ is likely to stop serving it"
    ),
    "dbp": (
        f"moves from the Transparency Platform to the Dâhilî Bilgi Platformu on "
        f"{EFFECTIVE_DATE} ({SOURCE_DBP}) and is not on the Transparency Platform "
        "data list, so EPİAŞ may stop serving it here"
    ),
    "not_listed": (
        f"is not on the Transparency Platform data list from {EFFECTIVE_DATE} "
        f"({SOURCE_LIST}); publishing it is no longer required and EPİAŞ may stop "
        "serving it"
    ),
    "aggregated": (
        f"is not on the Transparency Platform data list from {EFFECTIVE_DATE} at this "
        f"level of detail ({SOURCE_LIST}); EPİAŞ may stop serving it"
    ),
}


class TransparencyListWarning(FutureWarning):
    """The requested data leaves the mandatory Transparency Platform list on
    2027-01-01 (EPDK Decisions 14968 and 14967)."""


_warned: set[str] = set()


def _given(params: dict | None, names: list[str]) -> list[str]:
    params = params or {}
    return [n for n in names if params.get(n) is not None]


def get_publication_change(key: str) -> dict | None:
    """Registry entry for a call key (None if the key's data stays on the list)."""
    entry = PUBLICATION_CHANGES.get(key)
    if entry is None:
        return None
    out = {
        "effective_date": EFFECTIVE_DATE,
        "kind": entry["kind"],
        "when_params": entry["when_params"],
        "source": SOURCE_DBP if entry["kind"] == "dbp" else SOURCE_LIST,
        "alternative": entry["alternative"],
        "notice": publication_notice(key),
    }
    if entry["kind"] == "participant":
        out["source"] = f"{SOURCE_LIST}; {SOURCE_ART64}"
    return out


def publication_notice(key: str, params: dict | None = None) -> str | None:
    """Notice text for a call key, or None if it does not apply.

    With ``params`` given, a parameter-dependent notice applies only when one of
    its parameters is set; with ``params=None`` the general notice is returned.
    """
    entry = PUBLICATION_CHANGES.get(key)
    if entry is None:
        return None
    when = entry["when_params"]
    if when:
        if params is not None and not _given(params, when):
            return None
        subject = f"'{key}' with {' or '.join(when)}"
    else:
        subject = f"'{key}'"
    text = f"{subject} {_KIND_TEXT[entry['kind']]}."
    if entry["alternative"]:
        text += f" Instead: {entry['alternative']}."
    return text + " eptr2 keeps the call while EPİAŞ serves it."


def warn_publication_change(key: str, params: dict | None, stacklevel: int = 3) -> None:
    """Warn once per call key and process if the request's data leaves the list."""
    if key in _warned:
        return
    notice = publication_notice(key, params if params is not None else {})
    if notice is None:
        return
    _warned.add(key)
    warnings.warn(notice, TransparencyListWarning, stacklevel=stacklevel)
