# Response Cache (experimental)

eptr2 can keep EPİAŞ responses in a local SQLite file and answer repeated requests from it. The cache is **off by default** and **experimental**: its settings and storage rules may change in a later release.

```python
from eptr2 import EPTR2

eptr = EPTR2(use_dotenv=True, cache=True)            # default file
df = eptr.call("mcp", start_date="2026-11-01", end_date="2026-11-03")   # fetched and stored
df = eptr.call("mcp", start_date="2026-11-01", end_date="2026-11-03")   # from the cache
```

A cache hit needs no network and no login. The cache stores the raw JSON response, not the DataFrame. A hit goes through the same postprocessing as a fetch, so `postprocess=True` and `postprocess=False` share one row, and later fixes in eptr2's processing (such as the `idm-qty` relabel in 1.4.1) apply to stored data. Composite functions use the cache through the client, process or environment settings.

## Settings

| Option (`EPTR2(...)` and `eptr.call(...)`) | Environment variable | Default | Meaning |
|---|---|---|---|
| `cache` | `EPTR2_CACHE` (`1`, `true`, `yes`, `on`) | off | use the cache |
| `cache_path` | `EPTR2_CACHE_PATH` | `$XDG_CACHE_HOME/eptr2/responses.sqlite`, else `~/.cache/eptr2/responses.sqlite` | the SQLite file |
| `cache_overwrite` | `EPTR2_CACHE_OVERWRITE` | off | always fetch, and replace the stored row |
| `cache_settle_days` | `EPTR2_CACHE_SETTLE_DAYS` | see below | settle window in days |
| `cache_max_age` | `EPTR2_CACHE_MAX_AGE` | none | refetch rows older than this many days |

The narrowest setting given wins: a call option, then the client, then the process (`eptr2.set_cache(...)`), then the environment. Setting only a path does not turn the cache on.

```python
import eptr2

eptr2.set_cache(True, path="/data/eptr2.sqlite")   # whole process; only the arguments given change
eptr2.set_cache(enabled=None)                       # back to the environment variable
```

The environment variables can also go in the `.env` file read by `EPTR2(use_dotenv=True)`. A variable already set in the environment wins over the file.

```bash
EPTR2_CACHE=1
EPTR2_CACHE_PATH=/data/eptr2.sqlite
```

## What is stored

EPİAŞ keeps revising data after it first publishes it. For example:

- Real-time series are provisional for hours.
- Unpublished hours of KUDÜP and of the DGP instructions come back as **zeros**, not as an empty response.
- Production plans are revised during the day.
- Settlement-month data appears around the 15th of the next month and is revised for about 45 days.

So a response is stored only when the request's last date is outside the call's **settle window**:

| Calls | Settled from |
|---|---|
| most calls | end date + 2 days |
| real-time generation per plant (`rt-gen`, `rt-gen-bulk`, `ren-rt-gen`), DGP instructions (`bpm-*`) | end date + 5 days |
| per-organization matchings (`dam-clearing`, `idm-qty`, `bi-long`, `bi-short`), `capacity-demand`, `line-capacities` | end date + 6 days |
| production plans (`kgup`, `kgup-v1`, `eak`, `dpp-bulk`, `kudup`) | end date + 9 days |
| `bi-euas` | end date + 120 days |
| settlement-month data (`uevm`, `uecm`, `imb-*`, `ren-ul-gen`, `ren-uevm`, `iskk`, ...) | end of the month + 45 days |
| lists by start date (`uevcb-list-bulk`, `gen-uevcb`, `mms-pp-list`, `mms-uevcb-list`) | end of the month + 2 days |

The full table is `eptr2.mapping.settle.SETTLE_RULES`.

- **Requests that reach into the window:** not stored at all, including the settled part of a long range.
- **A month parameter (`period`):** counts as the end of its month.
- **`cache_settle_days`:** given on a call, it replaces the call's rule; `0` stores anything already published. Given on the client, the process or the environment, it replaces only the general 2-day default.
- **A row stored under a shorter window:** not served to a caller whose window it was fetched inside.

Also not stored:

- empty responses: "empty now" often means "not published yet"
- error responses, and bodies that are not JSON with a non-empty `items` list (such as a firewall page sent with HTTP 200)
- requests without a date parameter, such as lists: they change every month
- calls whose value is being live (`page-update-date` and similar, `eptr2.mapping.settle.NEVER_CACHE`)
- `get_raw_response=True` requests

## Refreshing

- **`cache_overwrite=True`:** skips the lookup, fetches, and replaces the row if the new response may be stored. A failed, empty or unsettled refetch keeps the existing row.
- **`cache_max_age=N`:** refetches rows fetched more than N days ago.

Each row records when it was fetched, the eptr2 version and the HTTP status.

```python
from eptr2.cache import cache_info, clear_cache

cache_info()                    # path, rows, size, rows per call key
clear_cache(call_key="uevm")    # delete one call key's rows; clear_cache() deletes all
```

## Notes

- **The file:** several processes can share it (WAL mode, 30 s busy timeout). A cache file that cannot be read or written is logged and skipped; the call still goes to the network.
- **Credentials:** `EPTR2()` still needs credentials and logs in when it is created unless a recycled ticket is valid; only cache hits are free of the network.
- **What the key covers:** the call key, the method, the URL (production or test platform, query parameters) and the request body. Usernames and tickets are not stored.
