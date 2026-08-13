---
name: eptr2-convenience-wrappers
description: Use typed get_* convenience wrapper functions from eptr2.calls instead of eptr.call("key", ...). These wrappers provide type hints, bilingual (EN/TR) docstrings, auto-complete, and an optional eptr argument. Use when writing scripts with typed functions, generating wrapper-based code, asking which get_* function to use, or preferring IDE-friendly code. Triggers on: get_mcp, get_smp, get_rt_cons, get_rt_gen, convenience wrapper, typed function, eptr2.calls, get_ function, wrapper call.
allowed-tools: Read, Bash(python:*)
---

# eptr2 Convenience Wrappers (`eptr2.calls`)

## Overview

Every endpoint exposed by `EPTR2.call` is available as a typed `get_*` function
in `eptr2.calls`. These wrappers give you:

- **Type hints** on every parameter (`str`, `str | int`, `list`, `bool`).
- **Bilingual docstrings** (EN/TR) with category and EPIAS reference URL.
- **Auto-complete** in IDEs.
- **Optional `eptr` argument** — omit it for one-off calls; pass an instance for
  TGT-recycling / batch usage.

There are **233 wrappers** in total (231 endpoint keys + 2 aliases: `ptf`, `smf`),
distributed across **21 per-category modules** (see module layout below for the full
list). The per-module counts shown in section headers below are for reference; use
`python -c "import eptr2.calls as c; print(len(c.__all__))"` to confirm the
total at any time.

---

## Signature shape

```python
def get_<endpoint>(
    <required_param>: <type>,
    ...,
    <optional_param>: <type> | None = None,
    ...,
    eptr: EPTR2 | None = None,
    **kwargs,
):
    """<EN title> / <TR title>

    Category: <GÖP / GİP / DGP / …>

    EN (<EN title>):
        <English description>

    TR (<TR title>):
        <Turkish description>

    Reference: <EPIAS URL>
    """
```

Extra `**kwargs` are forwarded to `EPTR2.call` (e.g. `postprocess=False`).

---

## Basic usage

> **Date parameters** accept `'YYYY-MM-DD'` strings (interpreted in Europe/Istanbul
> timezone). Datetime parameters such as `date_time` accept `'YYYY-MM-DDTHH:MM:SS'`.
>
> **Return type**: by default every `get_*` function returns a **pandas DataFrame**.
> Pass `postprocess=False` to receive the raw JSON (list of dicts) instead.

```python
from eptr2 import EPTR2
from eptr2.calls import get_mcp, get_smp, get_rt_cons, get_rt_gen

eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

# Prices
mcp  = get_mcp(start_date="2024-07-29", end_date="2024-07-29", eptr=eptr)
smp  = get_smp(start_date="2024-07-29", end_date="2024-07-29", eptr=eptr)

# Consumption / generation
cons = get_rt_cons(start_date="2024-07-29", end_date="2024-07-29", eptr=eptr)
gen  = get_rt_gen(start_date="2024-07-29", end_date="2024-07-29", eptr=eptr)
```

## Lazy client (no explicit eptr)

```python
from eptr2.calls import get_ptf

# EPTR2() is constructed automatically, reading credentials from .env
df = get_ptf(start_date="2024-07-29", end_date="2024-07-29")
```

---

## Module layout and key wrappers

Wrappers are grouped into per-category modules.

### Prices – `eptr2.calls.dam` (18 wrappers)

| Function | Required params | Key endpoint |
|----------|----------------|--------------|
| `get_mcp` / `get_ptf` | `start_date`, `end_date` | Market Clearing Price (GÖP) |
| `get_smp` / `get_smf` | `start_date`, `end_date` | System Marginal Price |
| `get_mcp_smp_imb` | `start_date`, `end_date` | Positive/negative imbalance prices |
| `get_interim_mcp` | `start_date`, `end_date` | Interim (pre-final) MCP |
| `get_dam_clearing` | `start_date`, `end_date` | DAM clearing results; optional `org_id` |
| `get_dam_volume` | `start_date`, `end_date` | DAM trade value |
| `get_supply_demand` | `date_time` | Supply-demand curve at a point in time |

```python
from eptr2.calls import get_mcp, get_mcp_smp_imb, get_dam_clearing

mcp = get_mcp(start_date="2024-07-01", end_date="2024-07-31")
imb = get_mcp_smp_imb(start_date="2024-07-01", end_date="2024-07-31")
clr = get_dam_clearing(start_date="2024-07-01", end_date="2024-07-31", org_id=123)
```

### Balancing Power Market – `eptr2.calls.bpm` (5 wrappers)

| Function | Required params |
|----------|----------------|
| `get_bpm_up` | `start_date`, `end_date` |
| `get_bpm_down` | `start_date`, `end_date` |
| `get_smp` (also here) | `start_date`, `end_date` |
| `get_smp_dir` | `start_date`, `end_date` |
| `get_smf` (alias for smp) | `start_date`, `end_date` |

```python
from eptr2.calls import get_bpm_up, get_bpm_down
up   = get_bpm_up(start_date="2024-07-01", end_date="2024-07-31")
down = get_bpm_down(start_date="2024-07-01", end_date="2024-07-31")
```

### Consumption – `eptr2.calls.consumption` (24 wrappers)

| Function | Required params |
|----------|----------------|
| `get_rt_cons` | `start_date`, `end_date` |
| `get_uecm` | `start_date`, `end_date` |
| `get_load_plan` | `start_date`, `end_date` |
| `get_consumption_by_province` | `start_date`, `end_date` |

```python
from eptr2.calls import get_rt_cons, get_uecm, get_load_plan

cons     = get_rt_cons(start_date="2024-07-01", end_date="2024-07-31")
uecm     = get_uecm(start_date="2024-07-01", end_date="2024-07-31")
forecast = get_load_plan(start_date="2024-07-01", end_date="2024-07-31")
```

### Generation – `eptr2.calls.generation` (16 wrappers)

| Function | Required params | Optional |
|----------|----------------|----------|
| `get_rt_gen` | `start_date`, `end_date` | `pp_id` |
| `get_uevm` | `start_date`, `end_date` | `pp_id` |
| `get_dpp` | `start_date`, `end_date` | `org_id` |

```python
from eptr2.calls import get_rt_gen, get_uevm, get_dpp

all_gen   = get_rt_gen(start_date="2024-07-01", end_date="2024-07-31")
plant_gen = get_rt_gen(start_date="2024-07-01", end_date="2024-07-31", pp_id=1234)
uevm      = get_uevm(start_date="2024-07-01", end_date="2024-07-31")
dpp       = get_dpp(start_date="2024-07-01", end_date="2024-07-31", org_id=456)
```

### Intraday Market – `eptr2.calls.idm` (8 wrappers)

| Function | Required params |
|----------|----------------|
| `get_idm_wap` | `start_date`, `end_date` |
| `get_idm_volume` | `start_date`, `end_date` |
| `get_idm_summary` | `start_date`, `end_date` |

```python
from eptr2.calls import get_idm_wap, get_idm_volume

wap    = get_idm_wap(start_date="2024-07-01", end_date="2024-07-31")
volume = get_idm_volume(start_date="2024-07-01", end_date="2024-07-31")
```

### Imbalance – `eptr2.calls.imbalance` (4 wrappers)

| Function | Required params |
|----------|----------------|
| `get_imbalance_volume` | `start_date`, `end_date` |
| `get_imbalance_amount` | `start_date`, `end_date` |

```python
from eptr2.calls import get_imbalance_volume, get_imbalance_amount

vol = get_imbalance_volume(start_date="2024-07-01", end_date="2024-07-31")
amt = get_imbalance_amount(start_date="2024-07-01", end_date="2024-07-31")
```

### Renewables – `eptr2.calls.renewables` (12 wrappers)

```python
from eptr2.calls import get_yek_g_amount, get_res_capacity

yek = get_yek_g_amount(start_date="2024-07-01", end_date="2024-07-31")
```

### Bilateral Contracts – `eptr2.calls.bilateral` (3 wrappers)

```python
from eptr2.calls import get_bilateral_contracts
contracts = get_bilateral_contracts(start_date="2024-07-01", end_date="2024-07-31")
```

### Transmission – `eptr2.calls.transmission` (14 wrappers)

```python
# All identifiers use ASCII-only names (no Turkish characters).
from eptr2.calls import get_capacity_demand, get_congestion_cost, get_line_capacities
cap = get_capacity_demand(start_date="2024-07-01", end_date="2024-07-31")
```

### Dams – `eptr2.calls.dams` (10 wrappers)

```python
from eptr2.calls import get_reservoir_level, get_dam_active_fullness
```

### Ancillary Services – `eptr2.calls.ancillary` (4 wrappers)

```python
from eptr2.calls import get_pfk_main, get_sfk_main
```

### Natural Gas Markets

21 modules total; the 6 modules not shown in sections above:
`general` (8), `mms` (5), `reporting` (7), `retroactive` (8), `vep` (12), `yek_g` (10), plus
the 4 natural-gas modules below.

(11 sections × listed counts) + general(8) + mms(5) + reporting(7) + retroactive(8) + vep(12) + yek_g(10) + ng(65) = **233**.

- `eptr2.calls.ng_general` (2), `ng_sgp` (27), `ng_transmission` (15), `ng_vgp` (21)

```python
from eptr2.calls.ng_vgp import get_ng_vgp_matching_quantity
```

---

## Discovering what's available

```python
import eptr2.calls as calls

# All public wrapper names
print(len(calls.__all__))   # 233

# Inspect a specific wrapper (signature + bilingual docstring)
help(calls.get_mcp)
help(calls.get_dam_clearing)

# List all wrappers whose name contains a keyword
print([n for n in calls.__all__ if "cons" in n])
```

---

## When to use `get_*` vs `eptr.call`

| Situation | Use |
|-----------|-----|
| IDE / type-checked code | `get_*` |
| One-off quick script | `get_*` |
| Dynamic endpoint (endpoint key in a variable) | `eptr.call` |
| Iterating over all endpoint keys | `eptr.call` |
| Both approaches call the same underlying API | — |

---

## Forwarding extra kwargs

By default `get_*` functions return a **pandas DataFrame**. Pass
`postprocess=False` to receive the raw JSON (list of dicts).

Anything accepted by `EPTR2.call` can be forwarded:

```python
# Return raw JSON instead of DataFrame
raw = get_mcp(
    start_date="2024-07-29",
    end_date="2024-07-29",
    postprocess=False,
)

# Custom request timeout
df = get_rt_gen(
    start_date="2024-07-29",
    end_date="2024-07-29",
    request_kwargs={"timeout": 30},
)
```

---

## Regenerating wrappers

After adding/changing endpoints in `mapping/path.py` or `mapping/parameters.py`:

```bash
python scripts/generate_call_wrappers.py
```

This rebuilds all 21 per-category modules under `src/eptr2/calls/`.

---

## Reference

- Source: `src/eptr2/calls/`
- Generator: `scripts/generate_call_wrappers.py`
- Help metadata: `eptr2.mapping.help.get_help_d`
- User guide: `docs/user-guide/convenience-wrappers.md`
- API reference: `docs/api/calls.md`
