# Changelog

All notable changes to eptr2 are documented here.

## Version 1.4.0 (Development)

Endpoint mappings were reviewed against EPİAŞ's technical documentation
(electricity, natural gas, reporting) and every call key was exercised against
the live API.

### Security
- Minimum versions raised to patched releases: `urllib3>=2.8.0` (runtime
  dependency; chunked-response memory and HTTPS-proxy TLS advisories) and
  `fastmcp>=3.4.10` in the `mcp` / `allextras` extras (component authorization
  advisory). The lock file also moves `mcp` 1.30.0, `PyJWT` 2.15.1, `anyio`
  4.14.2 and `opentelemetry-api` 1.45.2 to their patched versions, staying on
  the same major versions.
- The patched versions are also minimums in `pyproject.toml` (not only in the
  lock file), in the `mcp` / `allextras` extras: `mcp>=1.30.0`,
  `pyjwt>=2.15.0`, `anyio>=4.14.2`, `opentelemetry-api>=1.45.1`.
- `certifi>=2026.10.19` in the `mcp` / `allextras` / `docs` extras and the docs
  dependency group: earlier bundles trust emSign roots whose intermediate CA
  keys were compromised (GHSA-6q48-6c7w-9gw2, critical). certifi reaches eptr2 only through the MCP
  stack (httpx); eptr2's own API calls use the system trust store.

### Fixed
- `calculate_kupst_cost_by_contract`, `calculate_diff_costs_by_contract`
  and `calculate_unit_price_and_costs_by_contract` took KÜPST tolerance or
  multiplier from the regulation period's base table instead of the contract's
  date; `include_maintenance_penalty` overrode a multiplier passed in.
- `gather_and_calculate_plant_costs` applied today's tolerance to every hour
  and the `other` multiplier to every plant type.
- `get_dabi_idm_data` / `get_day_ahead_and_bilateral_matches`: documented columns and signs (nets are long minus short =
  net purchases), the per-organization GİP bid/ask swap (`clearingQuantityAsk` = bought, `clearingQuantityBid` = sold), and
  a new `net_sales` column (positive = net seller). `get_dabi_idm_data_period` and the GİP fetch now pass `**kwargs`
  (retry and timeout options were dropped). Offline regression test with a stubbed client.
- `capacity-demand` and `intl-capacity-demand-direction-list` called the
  line-capacities endpoints ([#6](https://github.com/Tideseed/eptr2/issues/6));
  they now return capacity-auction requests (`auctionCode`,
  `requestedCapacity`, `allocatedCapacity`, `clearencePrice`, …).
- `eligible-consumer-quantity` requires `start_date`/`end_date` (it always
  returned HTTP 400).
- `ra-meters` with `ra_spg_name` (and `get_ra_meters`) raised `TypeError`; the
  filter now maps to `subscriberProfileGroupName`.
- `ra-meter-volumes-period` / `-version`: optional parameters were registered
  under a misspelled key and dropped; the profile-group filter is
  `subscriber_pg`.
- Optional parameters passed as `None` are no longer sent (a `None` date
  crashed the generated wrappers).
- `page-update-date` raised under the default `postprocess=True`.
- Help entries for `idm-order-history` and `ng-physical-realization`.
- `calculate_unit_imbalance_price_by_contract` and
  `calculate_unit_imbalance_cost_by_contract` used the price ceiling in force
  TODAY, not on the contract's date: January–March 2026 hours at the 3400 TL/MWh
  cap missed the 1.05 ceiling surcharge (483 of 15,635 published hours
  2025-01..2026-10 differed from `mcp-smp-imb`; 0 after the fix). They now
  resolve floor and ceiling from the contract like the other `*_by_contract`
  helpers; explicit `floor_price` / `ceil_price` still win.
- `get_time_min_max_price_map`: the 3,000 TL/MWh cap (GİP 3,090) starts on
  **2024-07-01**, not 2024-06-01. In June 2024 PTF and SMF topped out at exactly
  2,700 and GİP trades at exactly 2,781 (= 2,700 × 1.03); the first 3,000 / 3,090
  prices are on 2024-07-01. June 2024 contracts now resolve to the 2,700 cap
  (`contract_to_floor_ceil_prices`, the `*_by_contract` imbalance helpers).
- `get_time_min_max_price_map`: the GİP (IDM) ceiling is **3,760** TL/MWh from
  2023-02-01 (was 3,759.5) and **3,142** from 2023-03-01 (was 3,141.5). EPİAŞ
  rounds 1.03 × the PTF cap up to the lira: February 2023 PH contracts traded at
  most 3,760.00 (121 trades at exactly that price, none above) and March 2023 at
  most 3,142.00 (142 trades, none above).
- `get_uevcb_ids` (and the `periodic_orgs` wrappers that call it) capped the
  current month at the process's local date instead of today's date in
  Istanbul: on a host behind Turkey (e.g. Europe/Berlin, UTC) the last day
  queried was yesterday between Istanbul midnight and local midnight. It now
  uses Istanbul wall-clock time.

### Added
- Main cost functions in `eptr2.util.costs`, working with or without pandas:
  - `calculate_imbalance_prices(start_date, end_date, ...)`: hourly imbalance
    prices, unit costs and every parameter used (regulation period,
    floor/ceiling, V, B, margins, KÜPST tolerance, multiplier and floor),
    resolved per hour. MCP, SMP and system direction are fetched from
    `mcp-smp-imb` unless `prices` is given. EPİAŞ's published imbalance
    prices are used where available (`imb_price_source`); they are calculated
    only for hours without them (scenarios, offline use, unpublished hours).
    `include_calculated=True` adds the calculated prices for comparison.
  - `calculate_imbalance_costs(data, category=..., ...)`: imbalance and KÜPST
    costs of actual vs forecast rows, using `calculate_imbalance_prices`; the
    category (any naming convention) and producer/consumer can be set per row.
- Regulation values that change over time come from one dated table
  (`get_time_regulation_params_map`) and are applied by every `*_by_contract`
  helper; explicit arguments still win. From the first delivery hour of
  2026-11-01: `V` is 100 (was 150), and KÜPST tolerance and multiplier depend
  on the KÜPST category: wind 15% / 0.05, solar 8% / 0.05, generation with
  storage (`plant_w_battery`) 5% / 0.10, other 5% / 0.05, transmission-connected
  unlicensed 20% / 0.02, distribution-connected unlicensed (per participant)
  25% / 0.01, standalone storage (`battery`) 20% / 0.02. The 0.08 maintenance multiplier
  applies to wind and solar from 30, other sources from 25 monthly fault
  entries (`is_kupst_maintenance_penalty_applicable`). `source`/`category`
  accepts these categories; `normalize_kupst_category` maps other naming
  conventions (Turkish labels, RES/GES/HES, BESS, ...) to them, and
  `unlicensed` maps to `unlicensed_from_transmission`.
- `get_org_estimated_activity` composite: a company's estimated hourly activity
  over a date range. Splits day-ahead open / intraday close, intraday day trade
  (`min(idm_long, idm_short)`) and the free quantity to be consumed or
  generated, and adds a fictitious PnL from MCP and the intraday WAP and TAD
  (quantity-weighted mean |price − WAP|) of the trade log. Helpers
  `calculate_idm_contract_stats` and `calculate_org_activity` are pure.
- `ren-capacity-old` — YEKDEM installed capacity up to the YEKDEM deadline.
- `ren-participant-year-list` — years available for `ren-participant-list`.

### Breaking
- Regulation periods: contracts from 2026-11-01 are period `26_02`
  (`get_regulation_period_by_contract`), `26_01` covers 2026-01-01 to
  2026-10-31, and `current` means the newest period. Each period label pins
  its own parameter row (`get_regulation_params`).
- Contract-free 2026 functions take their defaults from the newest parameter
  row instead of literals: `V`, `B`, margins and floor/ceiling in
  `calculate_unit_imbalance_price_2026` / `_cost_2026`, KÜPST multiplier and
  floor, KÜPST tolerance and the 5% DSG tolerance. Calls without a contract or
  period now use V=100 (the 2026-11-01 values); pass `V=150`,
  `regulation_period="26_01"` or a contract to reproduce earlier results.
  Pre-2026 functions keep their fixed values.
- Removed `calculate_imb_cost_pre_2026`, `calculate_diff_cost_pre_2026` and
  `calculate_kupsm_list`, deprecated since 1.3.3 for removal in 1.4.0.
  (`calculate_kupst_cost_list` stays while the deprecated
  `calculate_diff_costs_list` uses it.)
- `capacity-demand` returns different columns (the real endpoint's).
- `interim-mcp` / `get_interim_mcp` take `start_date` only; the endpoint
  ignored `end_date` and returned the start day.
- `eligible-consumer-count` drops `district_name`, `pg_name`, `province_id`;
  the endpoint never applied them.

## Version 1.3.8 (Development)

### Added
- **`eptr2.calls` package** — typed convenience wrappers for every endpoint
  (`get_mcp`, `get_smp`, `get_rt_cons`, …). 231 endpoints + 2 aliases =
  233 top-level functions.
- Bilingual (EN/TR) docstrings on each wrapper, sourced from
  `eptr2.mapping.help.get_help_d`, including category and the EPIAS reference
  URL.
- Type hints on every parameter (`str`, `str | int`, `list`, `bool`).
- Optional `eptr` argument with lazy `EPTR2()` construction when omitted.
- `scripts/generate_call_wrappers.py` regenerator for the wrapper package.
- Parametrised test suite `tests/test_call_wrappers.py` (655 cases) covering
  wrapper existence, parameter forwarding, required-arg enforcement, alias
  routing, and `__all__` coverage.
- New documentation pages: *Convenience Wrappers* (user guide) and
  *Convenience Wrappers* (API reference).

### Changed
- The legacy `src/eptr2/calls/market.py` is superseded by the generated
  per-category modules (`dam.py`, `bpm.py`, `consumption.py`, `generation.py`,
  `idm.py`, …).

## Version 1.3.4 (Development)

### Added
- MkDocs documentation with Material theme
- GitHub Pages deployment workflow

### Changed
- Documentation improvements

## Version 1.3.3

### Important
- Breaking changes due to regulatory changes by EPDK
- Overhaul planned for version 1.4.0

### Changed
- Updated API mappings for regulatory compliance

## Version 1.3.0

### Added
- MCP (Model Context Protocol) server for AI agent integration
- Claude Desktop integration support
- Agent skills for specialized domain queries

### Changed
- eptr2 now evolves to be an AI-oriented tool

## Version 1.2.4

### Critical
- Authentication method changes require update to 1.2.4+

### Added
- MCP server module (`eptr2.mcp`)
- `eptr2-mcp-server` command-line entry point

### Fixed
- Authentication handling improvements

## Version 1.2.3

### Added
- `.env` file support for credentials
- TGT (Ticket Granting Ticket) recycling
- `use_dotenv` parameter
- `recycle_tgt` parameter
- `.eptr2-tgt` file for TGT storage

### Changed
- Improved credential management

## Version 1.2.0

### Added
- Composite functions module
- `get_hourly_consumption_and_forecast_data`
- `get_hourly_price_and_cost_data`

### Changed
- Enhanced DataFrame postprocessing

## Version 1.1.0

### Added
- New login method with automatic TGT management
- `eptr_w_tgt_wrapper` function
- `generate_eptr2_credentials_file` utility

### Deprecated
- Direct credentials file path (use `.env` instead)

## Version 1.0.2

### Added
- Calculator tutorial app (`run_calc_app`)
- Imbalance cost calculation helpers

## Version 1.0.0

### Added
- Initial stable release
- 213+ API endpoints
- Pandas DataFrame integration
- Streamlit demo app
- Live tutorial feature

### Core Features
- EPTR2 class for API access
- Automatic authentication
- Response postprocessing
- Call discovery methods

## Migration Guides

### Migrating from 1.2.x to 1.3.x

1. Update authentication:
   ```python
   # Old
   eptr = EPTR2(username="...", password="...")
   
   # New (recommended)
   eptr = EPTR2(use_dotenv=True, recycle_tgt=True)
   ```

2. Create `.env` file:
   ```env
   EPTR_USERNAME=your.email@example.com
   EPTR_PASSWORD=yourpassword
   ```

### Migrating from 1.1.x to 1.2.x

1. Replace credentials file with `.env`:
   ```python
   # Old
   eptr = EPTR2(credentials_file_path="creds/eptr_credentials.json")
   
   # New
   eptr = EPTR2(use_dotenv=True)
   ```

## Roadmap

### Version 1.4.0 (Planned)
- Complete overhaul for EPDK regulatory changes
- Enhanced composite functions
- Improved documentation

## See Also

- [GitHub Releases](https://github.com/Tideseed/eptr2/releases)
- [PyPI Package](https://pypi.org/project/eptr2/)
