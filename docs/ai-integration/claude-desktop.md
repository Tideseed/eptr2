# Claude Desktop Setup

This guide walks you through setting up eptr2 with Claude Desktop for direct electricity market data access.

## Prerequisites

1. [Claude Desktop](https://claude.ai/download) installed
2. eptr2 installed with MCP support:
   ```bash
   pip install "eptr2[allextras]"
   ```
3. EPIAS Transparency Platform credentials

## Configuration

### Step 1: Locate Config File

Find your Claude Desktop configuration file:

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

### Step 2: Add eptr2 Server

Edit `claude_desktop_config.json` to add the eptr2 MCP server:

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

### Alternative: Using UV

If you're using UV for package management:

```json
{
  "mcpServers": {
    "eptr2": {
      "command": "uv",
      "args": [
        "run",
        "--extra", "mcp",
        "eptr2-mcp-server"
      ],
      "env": {
        "EPTR_USERNAME": "your.email@example.com",
        "EPTR_PASSWORD": "yourpassword"
      }
    }
  }
}
```

### Alternative: Using Python Module

```json
{
  "mcpServers": {
    "eptr2": {
      "command": "python",
      "args": ["-m", "eptr2.mcp.server"],
      "env": {
        "EPTR_USERNAME": "your.email@example.com",
        "EPTR_PASSWORD": "yourpassword"
      }
    }
  }
}
```

### Step 3: Restart Claude Desktop

Close and reopen Claude Desktop to load the new configuration.

## Verification

### Check Server Status

In Claude Desktop, you should see the eptr2 tools available. Try asking:

> "What MCP tools do you have available for Turkish electricity market data?"

Claude should list the eptr2 tools.

### Test a Query

Ask Claude:

> "What are today's electricity prices in Turkey?"

Claude will use the `get_market_clearing_price` tool to fetch the data.

## Example Conversations

### Price Analysis

> **You:** What were the electricity prices in Turkey on July 29, 2024?
>
> **Claude:** I'll fetch the market clearing prices for that date...
> [Uses get_market_clearing_price tool]
> 
> The Market Clearing Price (MCP/PTF) on July 29, 2024 ranged from...

### Consumption Data

> **You:** Show me Turkey's real-time electricity consumption for the past week.
>
> **Claude:** I'll get the real-time consumption data...
> [Uses get_real_time_consumption tool]
>
> Here's the hourly consumption data for the past week...

### Generation Mix

> **You:** What's the current generation mix in Turkey? How much comes from renewables?
>
> **Claude:** Let me fetch the real-time generation data by source...
> [Uses get_real_time_generation tool]
>
> Currently, Turkey's electricity generation mix is...

### Complex Analysis

> **You:** Compare the MCP and SMP for July 2024 and tell me about any patterns.
>
> **Claude:** I'll fetch both price series and analyze them...
> [Uses multiple tools]
>
> Here's my analysis of the MCP and SMP comparison...

## Troubleshooting

### Server Not Starting

1. Verify eptr2 is installed:
   ```bash
   pip show eptr2
   ```

2. Test the server manually:
   ```bash
   EPTR_USERNAME=... EPTR_PASSWORD=... eptr2-mcp-server
   ```

3. Check the Claude Desktop logs for errors

### Authentication Errors

1. Verify credentials are correct
2. Test credentials with direct Python:
   ```python
   from eptr2 import EPTR2
   eptr = EPTR2(username="...", password="...")
   print(eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29"))
   ```

### Tools Not Appearing

1. Restart Claude Desktop
2. Check JSON syntax in config file
3. Verify the command path is correct

### Slow Responses

1. Enable TGT recycling to reduce authentication overhead
2. Check your network connection to EPIAS servers

## Security Notes

!!! warning "Credential Security"
    The configuration file stores credentials in plain text. Consider:
    
    - Setting appropriate file permissions
    - Using environment variables from a `.env` file
    - Not sharing your configuration file

### Using .env File Instead

Create a wrapper script that loads from `.env`:

```bash
#!/bin/bash
# eptr2-mcp-wrapper.sh
source /path/to/.env
exec eptr2-mcp-server
```

Then in config:

```json
{
  "mcpServers": {
    "eptr2": {
      "command": "/path/to/eptr2-mcp-wrapper.sh"
    }
  }
}
```

## Advanced Configuration

### Multiple Servers

You can run multiple MCP servers alongside eptr2:

```json
{
  "mcpServers": {
    "eptr2": {
      "command": "eptr2-mcp-server",
      "env": {...}
    },
    "other-server": {
      "command": "other-mcp-server"
    }
  }
}
```

### Custom Settings

```json
{
  "mcpServers": {
    "eptr2": {
      "command": "python",
      "args": [
        "-c",
        "from eptr2.mcp import run_mcp_server; import asyncio; asyncio.run(run_mcp_server(recycle_tgt=True))"
      ],
      "env": {
        "EPTR_USERNAME": "...",
        "EPTR_PASSWORD": "...",
        "EPTR_TGT_PATH": "/custom/path"
      }
    }
  }
}
```

## Next Steps

- [Agent Skills](agent-skills.md)
- [MCP Server Reference](../api/mcp.md)
