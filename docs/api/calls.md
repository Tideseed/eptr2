# `eptr2.calls`

Typed convenience wrappers for every endpoint exposed by `EPTR2.call`.

Each function follows the shape:

```python
get_<endpoint>(
    <required_param>: <type>,
    ...,
    <optional_param>: <type> | None = None,
    ...,
    eptr: EPTR2 | None = None,
    **kwargs,
)
```

If `eptr` is omitted the wrapper instantiates `EPTR2()` on demand. Extra
keyword arguments are forwarded to `EPTR2.call`. See the
[Convenience Wrappers guide](../user-guide/convenience-wrappers.md) for usage
patterns.

## Package contents

```python
import eptr2.calls as calls
print(len(calls.__all__))   # 233 (231 endpoints + 2 aliases)
```

The wrappers are auto-generated from
[`src/eptr2/mapping/path.py`](https://github.com/Tideseed/eptr2/blob/main/src/eptr2/mapping/path.py),
[`src/eptr2/mapping/parameters.py`](https://github.com/Tideseed/eptr2/blob/main/src/eptr2/mapping/parameters.py),
and
[`src/eptr2/mapping/help.py`](https://github.com/Tideseed/eptr2/blob/main/src/eptr2/mapping/help.py)
by [`scripts/generate_call_wrappers.py`](https://github.com/Tideseed/eptr2/blob/main/scripts/generate_call_wrappers.py).
Re-run the generator after adding or modifying endpoints:

```bash
python scripts/generate_call_wrappers.py
```

## Module layout

Functions are grouped by market category into per-module files under
`src/eptr2/calls/`:

| Module | Topic |
|--------|-------|
| `dam` | Day-Ahead Market (GÖP), MCP, supply/demand, block & flexible bids |
| `idm` | Intraday Market (GİP) orders, transactions, matching |
| `bpm` | Balancing Power Market (DGP), SMP, YAL/YAT |
| `bilateral` | Bilateral contracts (İA) |
| `imbalance` | Imbalance volumes & prices |
| `consumption` | Demand forecasts, real-time consumption, UEÇM |
| `generation` | Real-time generation, UEVM, plant production |
| `renewables` | YEK-DEM and renewable-specific endpoints |
| `transmission` | Cross-border flows, ATC, IDP |
| `dams` | Hydro reservoirs and dam metering |
| `ancillary` | Ancillary services (PFK/SFK) |
| `vep` | Pre-financial market settlement (VEP / PFM) |
| `mms` | Market message system |
| `reporting` | Reporting-service endpoints |
| `retroactive` | Retroactive adjustments |
| `yek_g` | YEK-G certificates |
| `ng_general`, `ng_sgp`, `ng_transmission`, `ng_vgp` | Natural gas market endpoints |
| `general` | Cross-cutting service and reference data |

## Top-level exports

```python
from eptr2.calls import (
    get_mcp,
    get_ptf,
    get_smp,
    get_smf,
    get_rt_cons,
    get_rt_gen,
    get_load_plan,
    get_dam_clearing,
    get_uevm,
    # ... 233 in total
)
```
