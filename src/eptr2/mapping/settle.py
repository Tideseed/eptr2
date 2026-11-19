"""When a response is settled enough to be stored in the (experimental) response cache.

EPİAŞ keeps revising data after first publishing it: real-time series are provisional
for hours, unpublished hours of KUDÜP and DGP instructions come back as zeros rather
than empty, production plans are revised during the day, and settlement-month data
appears around the 15th of the next month and is revised for about 45 days. A cache
that stored "yesterday" would serve such rows as final.

So a response is stored only when the request's last date is outside a settle window:

- ``("days", N)``: settled from ``end_date + N`` days
- ``("month", N)``: settled from ``month_end(end_date) + N`` days

Calls not in :data:`SETTLE_RULES` use :data:`DEFAULT_SETTLE_DAYS`. Requests without a
date parameter are not cached, and :data:`NEVER_CACHE` keys are never cached. The
windows come from the refresh experience of an archive of EPİAŞ data; several are
conservative assumptions (see the comments).
"""

from datetime import date, datetime, timedelta, timezone
import calendar

DEFAULT_SETTLE_DAYS = 2

SETTLE_RULES: dict[str, tuple[str, int]] = {
    ## Production plans (revised during the day; per unit settled after ~9 days).
    ## kudup: unpublished hours are zeros; 9 days is an assumption.
    "kgup": ("days", 9),
    "kgup-v1": ("days", 9),
    "eak": ("days", 9),
    "dpp-bulk": ("days", 9),
    "kudup": ("days", 9),
    ## Per-organization matchings (settled after ~6 days) and late arrivals.
    "dam-clearing": ("days", 6),
    "idm-qty": ("days", 6),
    "bi-long": ("days", 6),
    "bi-short": ("days", 6),
    "capacity-demand": ("days", 6),
    "line-capacities": ("days", 6),
    ## Real-time generation per plant (settled after ~5 days); DGP instructions
    ## lag hours and come back as zeros until published (5 days is an assumption).
    "rt-gen": ("days", 5),
    "rt-gen-bulk": ("days", 5),
    "ren-rt-gen": ("days", 5),
    "bpm-up": ("days", 5),
    "bpm-down": ("days", 5),
    "bpm-orders": ("days", 5),
    "bpm-orders-w-avg": ("days", 5),
    ## Bilateral monthly totals are published late.
    "bi-euas": ("days", 120),
    ## Settlement-month data: month M appears ~15th-17th of M+1 and is revised for
    ## ~45 days. st-uecm, su-uecm, ren-ul-cost and zero-balance are assumed alike.
    "uevm": ("month", 45),
    "uecm": ("month", 45),
    "imb-qty": ("month", 45),
    "imb-vol": ("month", 45),
    "imb-qty-g": ("month", 45),
    "imb-org-list": ("month", 45),
    "ren-ul-gen": ("month", 45),
    "ren-uevm": ("month", 45),
    "iskk": ("month", 45),
    "st-uecm": ("month", 45),
    "su-uecm": ("month", 45),
    "ren-ul-cost": ("month", 45),
    "zero-balance": ("month", 45),
    ## Settlement-based monthly data without archive evidence: assumed like the
    ## settlement month (consumption breakdowns, eligible consumers, YEKDEM costs,
    ## meter volumes, market quantities, congestion cost, natural gas imbalance).
    "consumption-breakdown": ("month", 45),
    "consumer-breakdown": ("month", 45),
    "percentage-consumption-info": ("month", 45),
    "eligible-consumer-count": ("month", 45),
    "eligible-consumer-count-detail": ("month", 45),
    "eligible-consumer-quantity": ("month", 45),
    "electricity-market-quantity": ("month", 45),
    "congestion-cost": ("month", 45),
    "ren-income": ("month", 45),
    "ren-lic-cost": ("month", 45),
    "ren-total-cost": ("month", 45),
    "ren-unit-cost": ("month", 45),
    "ra-meter-volumes-period": ("month", 45),
    "ra-meter-volumes-version": ("month", 45),
    "ra-meters": ("month", 45),
    "ra-sum": ("month", 45),
    "ng-imbalance-amount": ("month", 45),
    "ng-shippers-imbalance-quantity": ("month", 45),
    "ng-bast": ("month", 45),
    ## Natural gas physical and transmission realizations: no evidence, assumed
    ## revised like the per-entity plan series.
    "ng-physical-realization": ("days", 9),
    "ng-virtual-realization": ("days", 9),
    "ng-imbalance-system": ("days", 9),
    "ng-tr-actual-entry-amount": ("days", 9),
    "ng-tr-actual-exit-amount": ("days", 9),
    "ng-tr-daily-transmission": ("days", 9),
    "ng-tr-day-end": ("days", 9),
    "ng-tr-stock-amount": ("days", 9),
    ## Generation by organization (real-time based, like rt-gen).
    "gen-org": ("days", 5),
    ## Lists and notices by month or start date: the current month's list can be
    ## incomplete; past months are stored.
    "uevcb-list-bulk": ("month", 2),
    "gen-uevcb": ("month", 2),
    "mms-pp-list": ("month", 2),
    "mms-uevcb-list": ("month", 2),
    "dam-clearing-org-list": ("month", 2),
    "eic-w-org-list": ("month", 2),
    "eic-w-uevcb-list": ("month", 2),
    "eic-x-org-list": ("month", 2),
    "elig-profile-groups": ("month", 2),
    "mf-distribution": ("month", 2),
    "mf-profile-group": ("month", 2),
    "multiple-factor": ("month", 2),
    "multiple-factor-bulk": ("month", 2),
    "ren-capacity": ("month", 2),
    "ren-capacity-old": ("month", 2),
    "ren-pp-list": ("month", 2),
    ## Outage lists by month: entries are added and changed after the fact.
    "planned-outages": ("month", 9),
    "unplanned-outages": ("month", 9),
}

## Calls whose value is being live, or that are not data.
NEVER_CACHE = frozenset(
    {
        "page-update-date",
        "page-settings",
        "interim-mcp-status",
        "date-init",
        "ng-latest-settlement-date",
        "ng-vgp-order-book",
        "menu",
    }
)

## Parameters holding a day; the month parameters stand for their whole month.
_DAY_PARAMS = (
    "start_date",
    "end_date",
    "date",
    "date_time",
    "se_date",
    "version_start_date",
    "version_end_date",
)
_MONTH_PARAMS = ("period", "period_start_date", "period_end_date")

_ISTANBUL = timezone(timedelta(hours=3))


def today_istanbul() -> date:
    """Today in the market time zone (Europe/Istanbul, UTC+3 without DST)."""
    return datetime.now(_ISTANBUL).date()


def _month_end(d: date) -> date:
    return d.replace(day=calendar.monthrange(d.year, d.month)[1])


def _to_date(value) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str) and len(value) >= 10:
        try:
            return date.fromisoformat(value[:10])
        except ValueError:
            return None
    return None


def request_end_date(params: dict) -> date | None:
    """The last day a request covers, or None if it has no date parameter.

    ``params`` are the call's preprocessed parameters (eptr2 names, before the
    EPİAŞ labels). Month parameters count as the end of their month. If a date
    parameter is present but cannot be read, None is returned (not cached).
    """
    found = []
    for name in _DAY_PARAMS + _MONTH_PARAMS:
        if name not in params or params[name] is None:
            continue
        d = _to_date(params[name])
        if d is None:
            return None
        found.append(_month_end(d) if name in _MONTH_PARAMS else d)
    return max(found) if found else None


def settled_from(
    call_key: str,
    end_date: date,
    call_days: int | None = None,
    default_days: int | None = None,
) -> date:
    """First day on which a response for ``call_key`` ending at ``end_date`` counts as settled.

    ``call_days`` (a per-call ``cache_settle_days``) replaces the key's rule;
    ``default_days`` replaces only :data:`DEFAULT_SETTLE_DAYS` for keys without a rule.
    """
    if call_days is not None:
        return end_date + timedelta(days=int(call_days))
    rule = SETTLE_RULES.get(call_key)
    if rule is None:
        n = DEFAULT_SETTLE_DAYS if default_days is None else int(default_days)
        return end_date + timedelta(days=n)
    kind, n = rule
    if kind == "month":
        return _month_end(end_date) + timedelta(days=n)
    return end_date + timedelta(days=n)
