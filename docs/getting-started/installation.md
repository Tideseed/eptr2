# Installation

## Requirements

- Python 3.10 or higher
- An EPIAS Transparency Platform account ([Register here](https://kayit.epias.com.tr/epias-transparency-platform-registration-form))

## Installation Options

### Full Installation (Recommended)

Install with all extras for the complete feature set including pandas, MCP server, and demo app:

=== "pip"
    ```bash
    pip install "eptr2[allextras]"
    ```

=== "uv"
    ```bash
    uv pip install "eptr2[allextras]"
    ```

=== "pipx"
    ```bash
    pipx install "eptr2[allextras]"
    ```

### Minimal Installation

For a lightweight installation with only core dependencies:

=== "pip"
    ```bash
    pip install eptr2
    ```

=== "uv"
    ```bash
    uv pip install eptr2
    ```

### Optional Dependencies

| Extra | Description | Includes |
|-------|-------------|----------|
| `dataframe` | DataFrame support | pandas |
| `mcp` | AI agent integration | pandas, fastmcp |
| `allextras` | All features | pandas, streamlit, fastmcp, openpyxl, xlsxwriter |
| `dev` | Development tools | pytest |

Install specific extras:

```bash
pip install "eptr2[dataframe]"  # Just pandas support
pip install "eptr2[mcp]"        # AI agent features
```

## Verify Installation

After installation, verify it works:

```python
import eptr2
print(eptr2.__version__ if hasattr(eptr2, '__version__') else "Installed!")
```

Or check available calls:

```python
from eptr2 import EPTR2
eptr = EPTR2(username="your@email.com", password="yourpassword")
print(f"Available calls: {len(eptr.get_available_calls())}")
```

## Upgrading

To upgrade to the latest version:

```bash
pip install --upgrade "eptr2[allextras]"
```

## Development Installation

For contributing to eptr2:

```bash
git clone https://github.com/Tideseed/eptr2.git
cd eptr2
pip install -e ".[dev,allextras]"
```

## Troubleshooting

### SSL Certificate Errors

If you encounter SSL certificate errors, you can disable SSL verification (not recommended for production):

```python
eptr = EPTR2(username="...", password="...", ssl_verify=False)
```

### Import Errors

If you see import errors for pandas or other optional dependencies, ensure you installed with the appropriate extras:

```bash
pip install "eptr2[allextras]"
```

## Next Steps

- [Set up authentication](authentication.md)
- [Make your first API call](quickstart.md)
