# MCP Client Setup

The eptr2 MCP server works with any Model Context Protocol client. This page shows the canonical configuration and per-client variants.

## Prerequisites

1. eptr2 installed with MCP support:
   ```bash
   pip install "eptr2[allextras]"
   ```
2. EPIAS Transparency Platform credentials ([register here](https://kayit.epias.com.tr/epias-transparency-platform-registration-form))

## Canonical Configuration

The server is a stdio MCP server started with the `eptr2-mcp-server` command. Credentials are passed as environment variables:

```json
{
  "mcpServers": {
    "eptr2": {
      "command": "eptr2-mcp-server",
      "env": {
        "EPTR_USERNAME": "your.email@example.com",
        "EPTR_PASSWORD": "yourpassword"
      }
    }
  }
}
```

!!! warning "Use literal values"
    Most MCP clients do **not** expand `${VAR}` placeholders in config files. Enter your credentials as literal values, or omit the `env` block and keep them in a `.env` file in the server's working directory.

You can print a ready-to-paste snippet for your client at any time:

```bash
eptr2 mcp-config --client vscode        # or: claude-desktop, claude-code, cursor, generic
```

## Per-Client Setup

### VS Code (agent mode)

Add the server to `.vscode/mcp.json` in your workspace (or via the **MCP: Add Server** command). Note VS Code uses a `servers` key:

```json
{
  "servers": {
    "eptr2": {
      "type": "stdio",
      "command": "eptr2-mcp-server",
      "env": {
        "EPTR_USERNAME": "your.email@example.com",
        "EPTR_PASSWORD": "yourpassword"
      }
    }
  }
}
```

VS Code also reads the repository's `AGENTS.md` natively, so agents get eptr2 usage guidance even without MCP.

### Claude Desktop

Edit the config file (Settings → Developer → Edit Config):

=== "macOS"
    ```
    ~/Library/Application Support/Claude/claude_desktop_config.json
    ```

=== "Windows"
    ```
    %APPDATA%\Claude\claude_desktop_config.json
    ```

=== "Linux"
    ```
    ~/.config/Claude/claude_desktop_config.json
    ```

Paste the canonical configuration above, then restart Claude Desktop. The eptr2 tools appear under the tools icon.

### Claude Code

```bash
claude mcp add eptr2 -e EPTR_USERNAME=your.email@example.com -e EPTR_PASSWORD=yourpassword -- eptr2-mcp-server
```

### Cursor

Add the canonical configuration to `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (global).

### Any other stdio client

Point your client at the `eptr2-mcp-server` command with the two environment variables. If your Python environment is not on the client's PATH, use the full path to the executable (find it with `which eptr2-mcp-server`) or launch via `python -m eptr2.mcp.server`.

## Verifying

Ask your assistant something like:

> "What was the Turkish electricity market clearing price yesterday?"

It should call the `get_market_clearing_price` tool. Discovery tools (`search_eptr2_calls`, `describe_eptr2_call`) work even without credentials.

## Troubleshooting

- **Server not found**: the `eptr2-mcp-server` command must be on the PATH the client uses. Use an absolute path if needed.
- **Authentication errors**: check the credential values; test them with `eptr2 call mcp --start-date 2024-01-01 --end-date 2024-01-01` in a shell with the same environment.
- **fastmcp missing**: install with `pip install "eptr2[allextras]"` (or `eptr2[mcp]`).

## Next Steps

- [MCP Server reference](mcp-server.md) — available tools, resources and prompts
- [Agent Skills](agent-skills.md) — bundled SKILL.md skills
- [CLI](cli.md) — the `eptr2` command for shell-driven agents
