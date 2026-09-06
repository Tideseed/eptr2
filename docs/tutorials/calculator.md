# Calculator App

The calculator tutorial app helps you estimate imbalance and KÜPST (deviation) costs for any date and hour.

## Running the Calculator

The calculator ships in the separate `eptr2-tutorials` project (in the
`tutorials/` directory of the [eptr2 repository](https://github.com/Tideseed/eptr2)),
so that installing `eptr2` itself does not pull in Streamlit:

```bash
git clone https://github.com/Tideseed/eptr2.git
cd eptr2/tutorials
uv run eptr2-calc
```

Or install it first:

```bash
cd eptr2/tutorials
pip install -e .
eptr2-calc
```

Credentials come from `EPTR_USERNAME` / `EPTR_PASSWORD` in your environment or a
`.env` file.

!!! note
    `from eptr2.tutorials import run_calc_app` no longer works: the tutorial
    apps were moved out of the main package.

!!! tip "Calculating costs in your own code"
    You do not need the app to compute these numbers. The cost utilities are
    plain functions that need no API call:

    ```python
    from eptr2.util.costs import calculate_unit_price_and_costs_by_contract

    calculate_unit_price_and_costs_by_contract(
        contract="PH26070101", mcp=4000, smp=4000,
        system_direction="Enerji Açığı",  # required when MCP == SMP
    )
    ```

    See the [Utilities API](../api/util.md) for the full set.

## Features

### Imbalance Cost Calculation

Calculate costs for energy imbalances:

- Input your actual vs. forecast energy
- Select date and hour
- Get positive/negative imbalance costs

### KÜPST (Deviation Cost)

Calculate production plan deviation costs:

- Input planned vs. actual production
- Account for tolerance bands
- Calculate settlement costs

### Interactive Interface

- Real-time price data lookup
- Visual cost breakdown
- Export calculations

## Understanding Imbalance Costs

### Positive Imbalance (Energy Surplus)

When you produce more than planned or consume less:

$$\text{Cost} = \text{Surplus (MWh)} \times \text{Negative Imbalance Price (TL/MWh)}$$

### Negative Imbalance (Energy Deficit)

When you produce less than planned or consume more:

$$\text{Cost} = \text{Deficit (MWh)} \times \text{Positive Imbalance Price (TL/MWh)}$$

## KÜPST Formula

KÜPST (Kesinleşmiş Üretim Planından Sapma Tutarı) is calculated as:

$$\text{KÜPST} = |\text{Deviation}| \times \max(0, \text{SMF} - \text{PTF})$$

Where:

- **Deviation** = Actual - Planned (within tolerance)
- **SMF** = System Marginal Price
- **PTF** = Market Clearing Price

## Example Calculation

```python
# Scenario: 100 MWh deficit on 2024-07-29 at 14:00
# Positive imbalance price: 1500 TL/MWh

deficit = 100  # MWh
price = 1500   # TL/MWh

cost = deficit * price
print(f"Imbalance cost: {cost:,.2f} TL")  # 150,000.00 TL
```

## Using Programmatically

For programmatic cost calculations without the UI:

```python
from eptr2 import EPTR2
from eptr2.composite import get_imbalance_data

eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

# Get imbalance prices
imbalance = eptr.call(
    "imbalance-price",
    start_date="2024-07-29",
    end_date="2024-07-29"
)

# Calculate costs
deficit = 100  # Your deficit in MWh
hour_14 = imbalance[imbalance['date'].dt.hour == 14].iloc[0]
cost = deficit * hour_14['positiveImbalancePrice']
print(f"Cost for 100 MWh deficit at 14:00: {cost:,.2f} TL")
```

## Configuration

### Custom Port

```bash
streamlit run eptr2_tutorials/calc.py --server.port 8503
```

## See Also

- [Demo App](demo-app.md)
- [Imbalance Costs Guide](../user-guide/composite-functions.md)
- [Common Abbreviations](../reference/abbreviations.md)
