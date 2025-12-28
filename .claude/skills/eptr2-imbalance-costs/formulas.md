# Imbalance Cost Formulas Reference

## Overview

This document provides comprehensive formulas for calculating imbalance costs in the Turkish electricity market.

---

## 1. Imbalance Price Calculation

### Current Regulation (2024)

The imbalance prices are determined based on MCP (Market Clearing Price) and SMP (System Marginal Price):

```
Penalty Margin (α) = 0.03 (3%)

Positive Imbalance Price = (1 - α) × min(MCP, SMP)
                         = 0.97 × min(MCP, SMP)

Negative Imbalance Price = (1 + α) × max(MCP, SMP)
                         = 1.03 × max(MCP, SMP)
```

### Implementation

```python
def calculate_unit_imbalance_price(mcp: float, smp: float, penalty_margin: float = 0.03):
    return {
        "pos": (1 - penalty_margin) * min(mcp, smp),
        "neg": (1 + penalty_margin) * max(mcp, smp),
    }
```

---

## 2. Imbalance Cost Per MWh

The cost of imbalance is the difference between MCP and imbalance price:

```
Positive Imbalance Cost = MCP - Positive Imbalance Price
                        = MCP - 0.97 × min(MCP, SMP)

Negative Imbalance Cost = Negative Imbalance Price - MCP
                        = 1.03 × max(MCP, SMP) - MCP
```

### Examples

**Scenario 1: MCP < SMP (Up-regulation / Energy Deficit)**
```
MCP = 2500 TL/MWh
SMP = 2800 TL/MWh

Positive Imbalance Price = 0.97 × 2500 = 2425 TL/MWh
Positive Imbalance Cost = 2500 - 2425 = 75 TL/MWh

Negative Imbalance Price = 1.03 × 2800 = 2884 TL/MWh
Negative Imbalance Cost = 2884 - 2500 = 384 TL/MWh
```

**Scenario 2: MCP > SMP (Down-regulation / Energy Surplus)**
```
MCP = 2800 TL/MWh
SMP = 2500 TL/MWh

Positive Imbalance Price = 0.97 × 2500 = 2425 TL/MWh
Positive Imbalance Cost = 2800 - 2425 = 375 TL/MWh

Negative Imbalance Price = 1.03 × 2800 = 2884 TL/MWh
Negative Imbalance Cost = 2884 - 2800 = 84 TL/MWh
```

---

## 3. KUPST (Production Plan Deviation Cost)

KUPST applies to deviations from the production plan (KGÜP).

### Formula

```
KUPST Multiplier (β) = 0.03 (3%)
Floor Price = 750 TL/MWh

KUPST Cost = max(MCP, SMP, Floor Price) × β
```

### Implementation

```python
def calculate_unit_kupst_cost(mcp: float, smp: float, 
                               kupst_multiplier: float = 0.03,
                               kupst_floor_price: float = 750.0):
    return max(mcp, smp, kupst_floor_price) * kupst_multiplier
```

### Example

```
MCP = 2500 TL/MWh
SMP = 2800 TL/MWh
Floor = 750 TL/MWh

KUPST Cost = max(2500, 2800, 750) × 0.03
           = 2800 × 0.03
           = 84 TL/MWh
```

---

## 4. Tolerance Rates (İmbalans Toleransı)

Deviations within tolerance are treated differently:

| Source Type | Tolerance Rate |
|-------------|----------------|
| Wind | 17% |
| Solar | 10% |
| Other (Default) | 5% |

### DSG (Balancing Responsible Group) Mechanics

```
Imbalance Tolerance Value = Actual Generation × Tolerance Rate

If |Deviation| ≤ Tolerance Value:
    → DSG Imbalance (shared within group)
    
If |Deviation| > Tolerance Value:
    → Individual Imbalance (penalized to participant)
```

### Implementation

```python
def calculate_imbalance_amounts(actual, forecast, is_producer, imb_tol=0.1, dsg_absorption_rate=0.0):
    diff = forecast - actual
    if is_producer:
        diff = -diff
    
    imb_tol_value = actual * imb_tol
    sign = -1 if diff < 0 else 1
    
    dsg_imbalance = min(abs(diff), imb_tol_value) * sign
    net_dsg_imbalance = dsg_imbalance * (1 - dsg_absorption_rate)
    individual_imbalance = diff - dsg_imbalance
    
    return {
        "diff": diff,
        "dsg_imbalance": dsg_imbalance,
        "net_dsg_imbalance": net_dsg_imbalance,
        "individual_imbalance": individual_imbalance,
        "imb_tol_value": imb_tol_value
    }
```

---

## 5. Full Imbalance Cost Calculation

### Algorithm

1. Calculate deviation: `deviation = actual - forecast`
2. Determine direction based on producer/consumer
3. Split into DSG vs individual imbalance using tolerance
4. Calculate unit costs based on MCP/SMP
5. Apply costs to imbalance amounts

### Example Calculation

```
Input:
- Actual Generation = 100 MWh
- Scheduled = 90 MWh (KGÜP)
- MCP = 2500 TL/MWh
- SMP = 2800 TL/MWh
- Tolerance = 10%
- Is Producer = True

Step 1: Deviation = 100 - 90 = 10 MWh surplus (positive imbalance)

Step 2: Tolerance Value = 100 × 0.10 = 10 MWh

Step 3: Since deviation (10) ≤ tolerance (10):
        - DSG Imbalance = 10 MWh
        - Individual Imbalance = 0 MWh

Step 4: Unit Cost (positive) = MCP - 0.97 × min(MCP, SMP)
                              = 2500 - 2425 = 75 TL/MWh

Step 5: Total Cost = 10 × 75 = 750 TL
```

---

## 6. Draft 2026 Regulations (Temporary)

The draft EPDK regulation (September 2025) proposes changes:

### New Tolerance Rates

| Source Type | Current | Proposed 2026 |
|-------------|---------|---------------|
| Wind | 17% | 15% |
| Solar | 10% | 8% |
| Unlicensed | - | 20% |
| Other | 5% | 5% |

### New KUPST Calculation

```
Default Multiplier (β) = 0.05 (5%)
With Maintenance Penalty = 0.08 (8%)
Battery = 0.10 (10%)
Aggregator = 0.05 (5%)
Unlicensed = 0.02 (2%)
Floor Price = 750 TL/MWh

KUPST Cost = max(MCP, SMP, Floor Price) × β
```

### Implementation (Temporary)

```python
def temp_calculate_draft_unit_kupst_cost(mcp, smp, source=None, 
                                          kupst_multiplier_default=0.05,
                                          kupst_floor_price=750.0,
                                          include_maintenance_penalty=False):
    kupst_multiplier = 0.08 if include_maintenance_penalty else kupst_multiplier_default
    if source is not None:
        source_map = {"battery": 0.1, "aggregator": 0.05, "unlicensed": 0.02}
        kupst_multiplier = source_map.get(source, kupst_multiplier_default)
    
    return max(mcp, smp, kupst_floor_price) * kupst_multiplier
```

---

## 7. Summary Table

| Parameter | Symbol | Value | Unit |
|-----------|--------|-------|------|
| Penalty Margin | α | 0.03 | - |
| KUPST Multiplier | β | 0.03 | - |
| KUPST Floor Price | - | 750 | TL/MWh |
| Wind Tolerance | - | 0.17 | - |
| Solar Tolerance | - | 0.10 | - |
| Default Tolerance | - | 0.05 | - |

---

## 8. Key Relationships

```
System Direction     | MCP vs SMP | More Costly Imbalance
---------------------|------------|----------------------
Enerji Açığı (Deficit) | MCP < SMP  | Negative (being short)
Enerji Fazlası (Surplus) | MCP > SMP  | Positive (being long)
Dengede (Balanced)   | MCP ≈ SMP  | Similar both ways
```

**Rule of Thumb**: Imbalance in the same direction as the system is more costly.
- System is short → Your shortage is expensive
- System is long → Your surplus is expensive
