# Agent Plugin

eptr2 ships as a portable [Agent Plugin](https://agent-plugins.org) — the vendor-neutral packaging standard for agent capabilities. The plugin bundles the two component types of the v1 specification:

- **Skills** — the 7 eptr2 agent skills (`SKILL.md` format)
- **MCP server** — the `eptr2-mcp-server` stdio server with 18 tools

## Layout

The plugin root is the packaged `eptr2/assets/` directory:

```
eptr2/assets/            <- plugin root
├── plugin.json          <- Agent Plugins manifest
├── mcp.json             <- MCP server configuration (stdio)
└── skills/
    ├── eptr2-api-discovery/
    ├── eptr2-consumption-data/
    ├── eptr2-convenience-wrappers/
    ├── eptr2-generation-tracking/
    ├── eptr2-imbalance-costs/
    ├── eptr2-market-operations/
    └── eptr2-price-analysis/
```

## Using the Plugin

Any Agent Plugins-compatible client can consume the plugin directly from the installed package:

```bash
pip install "eptr2[allextras]"
eptr2 plugin-path        # prints the plugin root inside site-packages
```

Point your client at that path, or copy the plugin to wherever your client discovers plugins:

```bash
eptr2 install-plugin --dest ~/.your-agent/plugins/eptr2
```

`--force` overwrites an existing copy (useful after upgrading eptr2).

## Credentials

The plugin's `mcp.json` intentionally contains no credentials. The MCP server reads `EPTR_USERNAME` / `EPTR_PASSWORD` from the environment or a `.env` file in its working directory. Configure them in your client's environment, or see [MCP Client Setup](mcp-clients.md) for per-client examples.

## Validation

The plugin is validated in CI: the manifest is checked against the Agent Plugins 1.0.0 constraints (allowed fields, name pattern), `mcp.json` against the stdio transport rules, and every skill directory for a conforming `SKILL.md`.

## Next Steps

- [Agent Skills](agent-skills.md) — what each bundled skill covers
- [MCP Server](mcp-server.md) — the 18 tools in detail
- [MCP Client Setup](mcp-clients.md) — configuring clients without plugin support
