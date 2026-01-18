# eptr2 Package

The main eptr2 package provides access to Turkish electricity market data through the EPIAS Transparency Platform.

## Installation

```bash
pip install "eptr2[allextras]"
```

## Quick Start

```python
from eptr2 import EPTR2

eptr = EPTR2(use_dotenv=True, recycle_tgt=True)
df = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
```

## Module Overview

| Module | Description |
|--------|-------------|
| [`eptr2.main`](main.md) | Core EPTR2 class |
| [`eptr2.composite`](composite.md) | Pre-built analysis functions |
| [`eptr2.mcp`](mcp.md) | MCP server for AI integration |
| [`eptr2.util`](util.md) | Utility functions |

## Main Exports

::: eptr2
    options:
      members:
        - EPTR2
        - transparency_call
        - generate_eptr2_credentials_file
        - eptr_w_tgt_wrapper
      show_root_heading: false
      show_source: false
