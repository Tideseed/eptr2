# Changelog

All notable changes to eptr2 are documented here.

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
