# eptr2

<p align="center">
  <img src="https://img.shields.io/pypi/v/eptr2" alt="PyPI Version">
  <img src="https://img.shields.io/pypi/dm/eptr2" alt="PyPI Downloads">
  <img src="https://img.shields.io/pypi/pyversions/eptr2" alt="Python Version">
  <img src="https://img.shields.io/pypi/l/eptr2" alt="License">
</p>

**eptr2** is a Python client for [EPIAS Transparency Platform v2.0](https://seffaflik.epias.com.tr/home) - the official Turkish electricity market data platform.

!!! tip "Live Demo"
    Try the live demo at <https://eptr2demo.streamlit.app/>

## Features

- 🔌 **213+ API Endpoints** - Access comprehensive Turkish electricity market data
- 📊 **Pandas Integration** - Returns data as DataFrames for easy analysis
- 🤖 **AI Agent Ready** - Built-in MCP server for Claude and other AI assistants
- 🔑 **Easy Authentication** - Simple credential management with `.env` files
- ♻️ **TGT Recycling** - Automatic ticket management for efficient API calls
- 📈 **Composite Functions** - Pre-built functions for common data analysis tasks

## Quick Example

```python
from eptr2 import EPTR2

# Initialize with credentials
eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

# Get Market Clearing Price (MCP/PTF)
df = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
print(df)
```

## What Data is Available?

eptr2 provides access to various Turkish electricity market data:

| Category | Description | Example Calls |
|----------|-------------|---------------|
| **Prices** | Market clearing, system marginal, imbalance prices | `mcp`, `smp`, `mcp-smp-imb` |
| **Consumption** | Real-time consumption, load forecasts | `rt-cons`, `load-plan` |
| **Generation** | Real-time generation by source type | `rt-gen`, `uevm` |
| **Market Operations** | Day-ahead, intraday market data | `dpp`, `kgup` |

## Installation

=== "pip"
    ```bash
    pip install "eptr2[allextras]"
    ```

=== "uv"
    ```bash
    uv pip install "eptr2[allextras]"
    ```

## Next Steps

<div class="grid cards" markdown>

-   :material-clock-fast:{ .lg .middle } __Getting Started__

    ---

    Set up authentication and make your first API call

    [:octicons-arrow-right-24: Quick Start](getting-started/quickstart.md)

-   :material-api:{ .lg .middle } __API Reference__

    ---

    Explore the full API documentation

    [:octicons-arrow-right-24: API Reference](api/eptr2.md)

-   :material-robot:{ .lg .middle } __AI Integration__

    ---

    Use eptr2 with Claude and other AI assistants

    [:octicons-arrow-right-24: MCP Server](ai-integration/mcp-server.md)

-   :material-function:{ .lg .middle } __Composite Functions__

    ---

    Pre-built functions for common analysis tasks

    [:octicons-arrow-right-24: Composite Functions](user-guide/composite-functions.md)

</div>

## License

eptr2 is licensed under the [Apache License 2.0](https://github.com/Tideseed/eptr2/blob/main/LICENSE).
