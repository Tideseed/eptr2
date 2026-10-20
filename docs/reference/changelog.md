# Changelog

All notable changes to eptr2 are documented here.

## Version 1.4.0 (Development)

Endpoint mappings were reviewed against EPİAŞ's technical documentation
(electricity, natural gas, reporting) and every call key was exercised against
the live API.

### Fixed
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

### Added
- `ren-capacity-old` — YEKDEM installed capacity up to the YEKDEM deadline.
- `ren-participant-year-list` — years available for `ren-participant-list`.

### Breaking
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
