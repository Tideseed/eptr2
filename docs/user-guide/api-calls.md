# Available API Calls

eptr2 provides access to 213+ API endpoints for Turkish electricity market data. This page lists the most commonly used calls organized by category.

## Price Data

### Day-Ahead Market Prices

| Call Key | Alias | Description |
|----------|-------|-------------|
| `mcp` | `ptf` | Market Clearing Price (Piyasa Takas Fiyatı) |
| `smp` | `smf` | System Marginal Price (Sistem Marjinal Fiyatı) |
| `mcp-smp-imb` | - | Positive and negative imbalance prices |
| `wap` | `aof` | Weighted Average Price (Ağırlıklı Ortalama Fiyat) |

```python
# Market Clearing Price
mcp = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")

# System Marginal Price  
smp = eptr.call("smp", start_date="2024-07-29", end_date="2024-07-29")

# Imbalance prices
imbalance = eptr.call("mcp-smp-imb", start_date="2024-07-29", end_date="2024-07-29")
```

### Intraday Market Prices

| Call Key | Description |
|----------|-------------|
| `idm-wap` | Intraday market weighted average price |
| `idm-volume` | Intraday market volume |
| `idm-summary` | Intraday market summary |

## Consumption Data

| Call Key | Alias | Description |
|----------|-------|-------------|
| `rt-cons` | - | Real-time electricity consumption |
| `uecm` | - | Settlement consumption (Uzlaştırmaya Esas Çekiş Miktarı) |
| `load-plan` | - | Demand forecast |

```python
# Real-time consumption
consumption = eptr.call("rt-cons", start_date="2024-07-29", end_date="2024-07-29")

# Settlement consumption
uecm = eptr.call("uecm", start_date="2024-07-29", end_date="2024-07-29")

# Load forecast
forecast = eptr.call("load-plan", start_date="2024-07-29", end_date="2024-07-29")
```

## Generation Data

### Aggregate Generation

| Call Key | Description |
|----------|-------------|
| `rt-gen` | Real-time generation by resource type |
| `uevm` | Settlement generation (Uzlaştırmaya Esas Veriş Miktarı) |

```python
# Real-time generation by fuel type
generation = eptr.call("rt-gen", start_date="2024-07-29", end_date="2024-07-29")

# Settlement generation
uevm = eptr.call("uevm", start_date="2024-07-29", end_date="2024-07-29")
```

### Plant-Level Data

| Call Key | Description |
|----------|-------------|
| `dpp-pp-list` | List of power plants |
| `rt-gen` | Real-time generation by plant |
| `dpp` / `kgup` | Daily production plan |
| `aic` | Available installed capacity |

```python
# Get list of power plants
plants = eptr.call("dpp-pp-list")

# Daily production plan
dpp = eptr.call("dpp", start_date="2024-07-29", end_date="2024-07-29")
```

## Market Operations

### Day-Ahead Market (GÖP)

| Call Key | Description |
|----------|-------------|
| `dam-volume` | Day-ahead market volume |
| `dam-clearing-qty` | Clearing quantities |
| `dam-block-bid` | Block bid information |

### Intraday Market (GİP)

| Call Key | Description |
|----------|-------------|
| `idm-summary` | Intraday market summary |
| `idm-contract` | Contract information |
| `idm-order-history` | Order book history |

### Balancing Power Market (DGP)

| Call Key | Description |
|----------|-------------|
| `bpm-orders` | Balancing power market orders |
| `bpm-instruction` | Balancing instructions |
| `yal` | Up regulation (Yük Alma) |
| `yat` | Down regulation (Yük Atma) |

## Organization Data

| Call Key | Description |
|----------|-------------|
| `organizations` | List of market participants |
| `dso-list` | Distribution system operators |
| `metering-point-list` | Metering points |

```python
# Get list of organizations
orgs = eptr.call("organizations")
```

## Bilateral Contracts

| Call Key | Description |
|----------|-------------|
| `bilateral-contracts` | Aggregate bilateral contracts |
| `bilateral-contracts-org` | Contracts by organization |

## Ancillary Services

| Call Key | Description |
|----------|-------------|
| `primary-freq-cap` | Primary frequency capacity |
| `secondary-freq-cap` | Secondary frequency capacity |
| `pfc-price` | Primary frequency capacity price |
| `sfc-price` | Secondary frequency capacity price |

## Discovering All Calls

### List All Available Calls

```python
all_calls = eptr.get_available_calls()
print(f"Total: {len(all_calls)} calls")

for call in sorted(all_calls):
    print(f"  - {call}")
```

### Search for Calls

```python
# Find all price-related calls
price_calls = [c for c in eptr.get_available_calls() if 'price' in c.lower()]

# Find all generation calls
gen_calls = [c for c in eptr.get_available_calls() if 'gen' in c.lower()]
```

### Get Call Documentation

```python
from eptr2.mapping.help import get_help_d

# Get help for a specific call
help_info = get_help_d("mcp")
print(f"Category: {help_info['category']}")
print(f"Title: {help_info['title']['en']}")
print(f"Description: {help_info['desc']['en']}")
```

## Call Parameters

Most calls require at minimum:

- `start_date` - Start date in YYYY-MM-DD format
- `end_date` - End date in YYYY-MM-DD format

Some calls require additional parameters:

```python
# Organization-specific calls
df = eptr.call("bilateral-contracts-org", 
               start_date="2024-07-29", 
               end_date="2024-07-29",
               org_id=123)

# Power plant-specific calls  
df = eptr.call("rt-gen",
               start_date="2024-07-29",
               end_date="2024-07-29", 
               pp_id=456)

# UEVCB (production unit) calls
df = eptr.call("uevcb-data",
               start_date="2024-07-29",
               end_date="2024-07-29",
               uevcb_id=789)
```

## Next Steps

- [Composite Functions](composite-functions.md) - Pre-built analysis functions
- [API Reference](../api/eptr2.md) - Complete API documentation
