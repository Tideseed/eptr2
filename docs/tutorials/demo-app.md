# Demo App

The Streamlit demo app lets you explore Turkish electricity market data
interactively. It lives in the separate `eptr2-tutorials` package, so the core
`eptr2` install stays lightweight (no Streamlit dependency).

## Online Demo

Visit the live demo at: **<https://eptr2demo.streamlit.app/>**

## Running Locally

The apps ship in the `tutorials/` directory of the
[eptr2 repository](https://github.com/Tideseed/eptr2), as their own
`eptr2-tutorials` project:

```bash
git clone https://github.com/Tideseed/eptr2.git
cd eptr2/tutorials
uv run eptr2demo
```

Or install it and use the console scripts:

```bash
cd eptr2/tutorials
pip install -e .

eptr2demo        # composite multi-page app
eptr2-demo       # single-page data explorer
eptr2-calc       # imbalance / KÜPST calculator
```

Credentials are read from `EPTR_USERNAME` / `EPTR_PASSWORD` in your environment
or a `.env` file, exactly as for the library itself.

!!! note
    Earlier versions exposed these apps as `eptr2.tutorials` inside the main
    package. They were moved out so that installing `eptr2` does not pull in
    Streamlit; `from eptr2.tutorials import run_demo_app` no longer works.

## Features

The demo app provides:

### Data Explorer

- Browse all 231 API endpoints
- Filter by category
- View data in tables
- Download as CSV

### Visualizations

- Interactive charts
- Time series plots
- Price comparisons
- Generation mix

### Quick Queries

- Pre-built common queries
- Date range selection
- Real-time data

## Screenshots

!!! note "Coming Soon"
    Screenshots will be added in a future update.

## Configuration

### Custom Port

The apps are ordinary Streamlit apps, so pass Streamlit's own flags:

```bash
streamlit run eptr2_tutorials/composite/Ana_Sayfa.py --server.port 8502
```

### Custom Theme

The demo app uses Streamlit's theming. Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#4F46E5"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F3F4F6"
textColor = "#111827"
```

## Troubleshooting

### Streamlit Not Found

Ensure you installed with extras:

```bash
pip install "eptr2[allextras]"
```

### Authentication Errors

Check your credentials:

```python
from eptr2 import EPTR2

# Test credentials
eptr = EPTR2(username="...", password="...")
print(eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29"))
```

### Port Already in Use

Try a different port:

```bash
streamlit run --server.port 8502 ...
```

## See Also

- [Calculator App](calculator.md)
- [Quick Start Guide](../getting-started/quickstart.md)
