# Demo App

eptr2 includes a built-in Streamlit demo app for exploring Turkish electricity market data interactively.

## Online Demo

Visit the live demo at: **<https://eptr2demo.streamlit.app/>**

## Running Locally

### Prerequisites

Install eptr2 with all extras:

```bash
pip install "eptr2[allextras]"
```

### Command Line

Run the demo app from the terminal:

```bash
eptr2demo
```

### Programmatic

```python
from eptr2.tutorials import run_demo_app

run_demo_app(
    username="your.email@example.com",
    password="yourpassword"
)
```

Or with `.env` file credentials:

```python
from eptr2.tutorials import run_demo_app

run_demo_app()  # Will use EPTR_USERNAME and EPTR_PASSWORD from .env
```

## Features

The demo app provides:

### Data Explorer

- Browse all 213+ API endpoints
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

```python
from eptr2.tutorials import run_demo_app

run_demo_app(
    port=8502  # Default is 8501
)
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
