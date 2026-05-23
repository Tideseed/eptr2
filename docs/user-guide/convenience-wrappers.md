# Convenience Wrappers (`eptr2.calls`)

Starting with v1.3.8, every endpoint exposed by `EPTR2.call` is also available
as a typed top-level function under `eptr2.calls`. These are thin convenience
wrappers around `eptr.call(...)` that give you:

- **Auto-complete** in editors thanks to explicit parameter signatures.
- **Type hints** for every parameter (`str`, `str | int`, `list`, `bool`).
- **Bilingual docstrings** (EN/TR) with the endpoint category and a reference
  URL to the EPIAS Transparency documentation.
- **Optional `eptr` argument** — pass your own `EPTR2` instance or let the
  wrapper construct one lazily.

There is one `get_*` function per endpoint key, with hyphens replaced by
underscores. Aliases (`ptf`, `smf`) get their own functions that route to the
alias key.

## Basic Usage

```python
from eptr2 import EPTR2
from eptr2.calls import get_mcp, get_smp, get_rt_cons

eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

mcp = get_mcp(start_date="2024-07-29", end_date="2024-07-29", eptr=eptr)
smp = get_smp(start_date="2024-07-29", end_date="2024-07-29", eptr=eptr)
cons = get_rt_cons(start_date="2024-07-29", end_date="2024-07-29", eptr=eptr)
```

## Lazy `EPTR2` Construction

If `eptr` is omitted, the wrapper constructs `EPTR2()` on demand. This honours
`use_dotenv=True` by default, so any `.env` credentials are picked up
automatically:

```python
from eptr2.calls import get_ptf

# No explicit client — wrapper builds EPTR2() internally
df = get_ptf(start_date="2024-07-29", end_date="2024-07-29")
```

For repeated calls, pass an instance so TGT recycling and any custom settings
are preserved:

```python
eptr = EPTR2(use_dotenv=True, recycle_tgt=True)
df1 = get_mcp(start_date="2024-07-29", end_date="2024-07-29", eptr=eptr)
df2 = get_smp(start_date="2024-07-29", end_date="2024-07-29", eptr=eptr)
```

## Function Signature

Each wrapper follows this shape:

```python
def get_<endpoint>(
    <required_param>: <type>,
    ...
    <optional_param>: <type> | None = None,
    ...
    eptr: EPTR2 | None = None,
    **kwargs,
):
    """<EN title> / <TR title>
    ...
    """
```

Extra keyword arguments (e.g. `postprocess=False`) are forwarded straight to
`eptr.call`.

## Forwarding Aliases

Aliases each get a dedicated function that routes to the alias key, so existing
server-side resolution is honoured:

```python
from eptr2.calls import get_mcp, get_ptf, get_smp, get_smf

# All four are real functions; each forwards its own key to eptr.call.
```

## Discovering Wrappers

```python
import eptr2.calls as calls

# Every public name is included in __all__
print(len(calls.__all__))  # 233 (231 endpoints + 2 aliases)

# Get help for any wrapper
help(calls.get_mcp)
```

## Example with Optional Parameters

```python
from eptr2.calls import get_dam_clearing

# org_id is optional and will be sent as null when omitted
df = get_dam_clearing(
    start_date="2024-07-01",
    end_date="2024-07-31",
    org_id=123,
)
```

## When to Use `eptr.call` vs `get_*`

| Use case                                | Recommended |
|-----------------------------------------|-------------|
| Quick scripts / one-off calls           | `get_*`     |
| IDE auto-complete on parameter names    | `get_*`     |
| Reading bilingual docs in your editor   | `get_*`     |
| Dynamic endpoint selection (by string)  | `eptr.call` |
| Iterating over all endpoint keys        | `eptr.call` |

Both APIs use the same underlying request path — pick whichever fits the call
site best.
