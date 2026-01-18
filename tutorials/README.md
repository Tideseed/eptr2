# EPTR2 Tutorials

Streamlit-based tutorials and demo applications for the [eptr2](https://pypi.org/project/eptr2/) library.

## Installation

### Option 1: Install from the tutorials directory (Development)

```bash
cd tutorials
pip install -e .
```

### Option 2: Run directly with uv

```bash
cd tutorials
uv run eptr2demo
```

## Running the Apps

After installation, you can run the demo apps using:

```bash
# Main composite functions demo
eptr2demo

# Basic API demo
eptr2-demo

# Imbalance calculator demo
eptr2-calc
```

Or run directly with Python:

```python
from eptr2_tutorials import run_composite_app, run_demo_app, run_calc_app

# Run composite demo (main app)
run_composite_app(username="your@email.com", password="your_password")

# Run basic demo
run_demo_app(username="your@email.com", password="your_password")

# Run calculator demo
run_calc_app(username="your@email.com", password="your_password")
```

## Environment Variables

You can also set credentials via environment variables:

```bash
export EPTR_USERNAME="your@email.com"
export EPTR_PASSWORD="your_password"
```

Or create a `.env` file in the tutorials directory.

## Requirements

- Python 3.10+
- eptr2 >= 1.3.0
- streamlit >= 1.50.0
- pandas >= 2.1.3

## License

Apache License 2.0 - Same as the main eptr2 library.
