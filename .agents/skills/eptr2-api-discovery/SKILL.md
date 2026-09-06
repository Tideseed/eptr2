---
name: eptr2-api-discovery
description: Find eptr2 electricity and natural-gas endpoints, aliases, parameters, and Python helpers without credentials. Use when choosing an API call or exploring available EPIAS data.
---

# Discover eptr2 APIs

Use the installed package's metadata before constructing a client. Discovery does not need credentials or an API request. Match the installed version rather than assuming GitHub main matches the user's environment.

```python
from eptr2.agentic import list_calls, search_calls, describe_call, load_bundled_schema

calls = list_calls()
price_calls = search_calls("price")
description = describe_call("ptf")  # resolves to mcp
schema = load_bundled_schema()     # works without pandas
print(description)
```

For a shell-driven runtime:

```bash
eptr2 search "market clearing"
eptr2 describe mcp --format json
eptr2 list --category GÖP --format json
eptr2 schema --stdout
```

Inspect required and optional parameters, then choose the date range and IDs relevant to the user's question. An alias is not necessarily a wrapper name: inspect `eptr2.calls` before importing a guessed `get_*` function. Raw result types vary by endpoint; inspect the response instead of assuming every call returns a DataFrame.

When executing an authorized data query, reuse a client with `strict_params=True` and automatic `.env` loading. Use the user's existing environment and runtime tools; no particular model vendor, shell-tool name, or skill directory is required.

Read [endpoint-categories.md](endpoint-categories.md) for domain routing and ID lookups. If the console command is unavailable, use `python -m eptr2` or the bundled [discovery script](scripts/list_endpoints.py).
