# AGENT_GUIDE

This file is kept as a stable entry point for AI-agent documentation. It is provider-agnostic — everything referenced here works with any agent runtime.

## Primary References

- [AGENTS.md](AGENTS.md) — Main quick-reference guide for AI agents working with `eptr2`
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) — Fast call-key and usage cheatsheet
- [eptr2_api_schema.json](eptr2_api_schema.json) — Machine-readable schema of all 231 endpoints (auto-generated with `eptr2 schema`)
- [src/eptr2/mcp/README.md](src/eptr2/mcp/README.md) — MCP server usage, tools, and troubleshooting
- [docs/ai-integration/mcp-clients.md](docs/ai-integration/mcp-clients.md) — MCP setup for specific clients (VS Code, Claude, Cursor, generic)
- [docs/ai-integration/cli.md](docs/ai-integration/cli.md) — The `eptr2` CLI for shell-driven agents
- [docs/api/mcp.md](docs/api/mcp.md) — API-level MCP reference

## Quick Entry Points

```bash
eptr2 list                  # discover endpoints (no credentials needed)
eptr2 describe mcp          # parameters for one call
eptr2 install-skills        # install bundled agent skills (SKILL.md format)
eptr2 mcp-config --client vscode
```

```python
from eptr2.agentic import list_calls, search_calls, describe_call, build_schema
from eptr2.mcp import create_mcp_server, run_mcp_server
```

## Canonical Call-Key Notes

Use these call keys in code, CLI and MCP generic calls:

- `mcp` (alias: `ptf`)
- `smp` (alias: `smf`)
- `rt-cons`
- `rt-gen`
- `load-plan`
- `mcp-smp-imb`

When in doubt, use discovery:

```bash
eptr2 search <keyword>
```
