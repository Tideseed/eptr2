# Local Archive (experimental)

eptr2 can keep the responses it fetches in a local SQLite file and answer repeated requests from it. This builds an archive of EPİAŞ data as a side effect of ordinary use, with no separate job. The archive is **off by default** and **experimental**: its settings and rules may change in a later release.

```python
from eptr2 import EPTR2

eptr = EPTR2(use_dotenv=True, archive=True)   # default file
df = eptr.call("mcp", start_date="2026-10-01", end_date="2026-10-31")   # fetched and kept
df = eptr.call("mcp", start_date="2026-10-01", end_date="2026-10-31")   # from the archive
```

- **Reading from the archive:** needs no network and no login.
- **What is kept:** the raw JSON response, not the DataFrame. Reading from the archive goes through the same postprocessing as a fetch, so `postprocess=True` and `postprocess=False` share one row. Later fixes in eptr2's processing (such as the `idm-qty` relabel in 1.4.1) also apply to archived data.
- **No expiry:** archived rows are kept until you delete them.
- **Composite functions:** use the archive through the client, process or environment settings.

## Settings

| Option (`EPTR2(...)` and `eptr.call(...)`) | Environment variable | Default | Meaning |
|---|---|---|---|
| `archive` | `EPTR2_ARCHIVE` (`1`, `true`, `yes`, `on`) | off | use the archive |
| `archive_path` | `EPTR2_ARCHIVE_PATH` | `$XDG_DATA_HOME/eptr2/archive.sqlite`, else `~/.local/share/eptr2/archive.sqlite` | the SQLite file |
| `archive_overwrite` | `EPTR2_ARCHIVE_OVERWRITE` | off | always fetch, and replace the archived row |
| `archive_settle_days` | `EPTR2_ARCHIVE_SETTLE_DAYS` | see below | settle window in days |

The narrowest setting given wins: a call option, then the client, then the process (`eptr2.set_archive(...)`), then the environment. Setting only a path does not turn the archive on. The default file is in a data directory, not a cache directory, because cleanup tools may empty cache directories.

```python
import eptr2

eptr2.set_archive(True, path="/data/eptr2_archive.sqlite")   # whole process; only the arguments given change
eptr2.set_archive(enabled=None)                               # back to the environment variable
```

The environment variables can also go in the `.env` file read by `EPTR2(use_dotenv=True)`. A variable already set in the environment wins over the file.

```bash
EPTR2_ARCHIVE=1
EPTR2_ARCHIVE_PATH=/data/eptr2_archive.sqlite
```

## What is kept

EPİAŞ keeps revising data after it first publishes it. For example:

- Real-time series are provisional for hours.
- Unpublished hours of KUDÜP and of the DGP instructions come back as **zeros**, not as an empty response.
- Production plans are revised during the day.
- Settlement-month data appears around the 15th of the next month and is revised for about 45 days.

So a response is kept only when the request's last date is outside the call's **settle window**:

| Calls | Settled from |
|---|---|
| most calls | end date + 2 days |
| real-time generation per plant or organization (`rt-gen`, `rt-gen-bulk`, `ren-rt-gen`, `gen-org`), DGP instructions (`bpm-*`) | end date + 5 days |
| per-organization matchings (`dam-clearing`, `idm-qty`, `bi-long`, `bi-short`), `capacity-demand`, `line-capacities` | end date + 6 days |
| production plans (`kgup`, `kgup-v1`, `eak`, `dpp-bulk`, `kudup`); natural gas realizations and transmission actuals | end date + 9 days |
| `bi-euas` | end date + 120 days |
| settlement-month data: `uevm`, `uecm`, `imb-qty`, `imb-vol`, `imb-qty-g`, `imb-org-list`, `ren-ul-gen`, `ren-uevm`, `iskk`, and alike (`st-uecm`, `su-uecm`, consumption breakdowns, eligible consumers, YEKDEM costs, meter volumes, market quantities, congestion cost, natural gas imbalance) | end of the month + 45 days |
| outage lists (`planned-outages`, `unplanned-outages`) | end of the month + 9 days |
| lists by month or start date (UEVÇB, EIC, organization and plant lists, multiple factors, renewable capacity) | end of the month + 2 days |

Several windows are assumptions rather than measurements: `kudup`, `bpm-*`, `gen-org`, the natural gas rules and the settlement siblings. A call that takes a month parameter always has a month rule.

The full table is `eptr2.mapping.settle.SETTLE_RULES`.

- **Requests that reach into the window:** not stored at all, including the settled part of a long range.
- **A month parameter (`period`):** counts as the end of its month.
- **`cache_settle_days`:** given on a call, it replaces the call's rule; `0` keeps anything already published. Given on the client, the process or the environment, it replaces only the general 2-day default.
- **A row stored under a shorter window:** not served to a caller whose window it was fetched inside.

Also not kept:

- empty responses: "empty now" often means "not published yet"
- error responses, and bodies that are not JSON with a non-empty `items` list (such as a firewall page sent with HTTP 200)
- requests without a date parameter, such as lists: they change every month
- calls whose value is being live (`page-update-date` and similar, `eptr2.mapping.settle.NEVER_ARCHIVE`)
- `get_raw_response=True` requests

## Refreshing

`archive_overwrite=True` skips the lookup, fetches, and replaces the row if the new response may be kept. A failed, empty or unsettled refetch keeps the existing row. Each row records when it was fetched, the eptr2 version and the HTTP status.

```python
from eptr2.archive import archive_info, clear_archive

archive_info()                    # path, size, rows; per call key: rows and first/last archived end date
clear_archive(call_key="uevm")    # delete one call key's rows; clear_archive() deletes all
```

## Size

Responses are kept compressed. As a guide, measured on October 2026:

| Data | Per year (compressed) |
|---|---|
| hourly market-wide series (`mcp`, `smp`, `rt-cons`) | about 70–110 KB each |
| real-time generation by source (`rt-gen`) | about 600 KB |
| GİP matching of one organization (`idm-qty` with `org_id`) | about 85 KB |
| GİP trade log (`idm-log`) | about 100 MB |

There is no size limit: the archive only adds the convenience of keeping what you fetch, and grows with what you request. A year of market-wide data plus per-organization series is a few hundred MB at most, which SQLite handles without trouble. To shrink it, delete rows with `clear_archive`.

## Notes

- **Rows are keyed by the exact request:** the call key, the method, the URL (production or test platform, query parameters) and the request body.
  - The same period asked as one month and as single days is kept twice.
  - A range that was never asked as such is fetched, even if its days are archived.
  - For a reusable archive, request in a fixed rhythm, for example one day or one month at a time.
- **Usernames and tickets** are not kept.
- **Sharing the file:** several processes can share it (WAL mode, 30 s busy timeout). An archive file that cannot be read or written is logged and skipped; the call still goes to the network.
- **Credentials:** `EPTR2()` still needs credentials and logs in when it is created unless a recycled ticket is valid. Only reads from the archive are free of the network.
