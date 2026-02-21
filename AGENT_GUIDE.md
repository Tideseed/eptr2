# AGENT_GUIDE

This file is kept as a stable entry point for AI-agent documentation.

## Primary References

- [AGENTS.md](AGENTS.md) — Main quick-reference guide for AI agents working with `eptr2`
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) — Fast call-key and usage cheatsheet
- [src/eptr2/mcp/README.md](src/eptr2/mcp/README.md) — MCP server usage, tools, and troubleshooting
- [docs/ai-integration/mcp-server.md](docs/ai-integration/mcp-server.md) — Integration guide for MCP clients
- [docs/api/mcp.md](docs/api/mcp.md) — API-level MCP reference

## MCP Programmatic Entry Points

```python
from eptr2.mcp import create_mcp_server, run_mcp_server
```

- `run_mcp_server(...)`: async helper that creates and runs the server
- `create_mcp_server(...)`: returns a configured FastMCP server for explicit lifecycle control

## Canonical Call-Key Notes

Use these call keys in code and MCP generic calls:

- `mcp` (alias: `ptf`)
- `smp` (alias: `smf`)
- `rt-cons`
- `rt-gen`
- `load-plan`
- `mcp-smp-imb`

When in doubt, use discovery:

```python
from eptr2 import EPTR2

eptr = EPTR2(use_dotenv=True, recycle_tgt=True)
calls = eptr.get_available_calls(include_aliases=True)
```
