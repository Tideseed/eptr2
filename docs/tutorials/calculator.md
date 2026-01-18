# Calculator App

The calculator tutorial app helps you estimate imbalance and KÜPST (deviation) costs for any date and hour.

## Running the Calculator

### Prerequisites

Install eptr2 with all extras:

```bash
pip install "eptr2[allextras]"
```

### Launch

```python
from eptr2.tutorials import run_calc_app

run_calc_app(
    username="your.email@example.com",
    password="yourpassword"
)
```

Or with `.env` credentials:

```python
from eptr2.tutorials import run_calc_app

run_calc_app()  # Uses EPTR_USERNAME and EPTR_PASSWORD
```

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

```python
from eptr2.tutorials import run_calc_app

run_calc_app(port=8503)
```

## See Also

- [Demo App](demo-app.md)
- [Imbalance Costs Guide](../user-guide/composite-functions.md)
- [Common Abbreviations](../reference/abbreviations.md)
