# Claude Desktop MCP Server Setup for eptr2

This guide will help you integrate eptr2 with Claude Desktop, allowing Claude to access Turkish electricity market data through the EPIAS Transparency Platform.

## Prerequisites

Before starting, you need:

1. **EPIAS Transparency Platform credentials**
   - Register at: https://kayit.epias.com.tr/epias-transparency-platform-registration-form
   - You'll receive login credentials via email

2. **Install eptr2 with all extras (includes MCP support)**
   ```bash
   pip install "eptr2[allextras]"
   ```

3. **Optional: Install uv (recommended)**
   ```bash
   pip install uv
   ```
   - `uv` provides faster, more reliable Python execution
   - Alternative: You can use standard Python (see below)

## Step 1: Locate Your Claude Desktop Config File

The config file location depends on your operating system:

| Operating System | Config File Location |
|-----------------|---------------------|
| **macOS** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Windows** | `%APPDATA%\Claude\claude_desktop_config.json` |
| **Linux** | `~/.config/Claude/claude_desktop_config.json` |

## Step 2: Add eptr2 to Claude Desktop Config

### Option A: Using uv (Recommended)

Open your `claude_desktop_config.json` file and add the eptr2 server configuration:

```json
{
  "mcpServers": {
    "eptr2": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/FULL/PATH/TO/YOUR/eptr2",
        "--extra",
        "mcp",
        "eptr2-mcp-server"
      ]
    }
  }
}
```

**Important:** Replace `/FULL/PATH/TO/YOUR/eptr2` with the actual path to your eptr2 installation.

### Option B: Using Standard Python

If you don't want to install `uv`, you can use standard Python:

```json
{
  "mcpServers": {
    "eptr2": {
      "command": "python",
      "args": [
        "-m",
        "eptr2.mcp.server"
      ],
      "env": {
        "PYTHONPATH": "/FULL/PATH/TO/YOUR/eptr2/src"
      }
    }
  }
}
```

**Note:** This option requires setting `PYTHONPATH` to the eptr2 source directory.

## Step 3: Set Up Your Credentials

Create a `.env` file in your eptr2 directory with your EPIAS credentials:

**Location:** `/FULL/PATH/TO/YOUR/eptr2/.env`

```bash
EPTR_USERNAME=your.email@example.com
EPTR_PASSWORD=yourpassword
```

**⚠️ IMPORTANT:** Replace with your actual EPIAS credentials:
- `your.email@example.com` → Your registered EPIAS email
- `yourpassword` → Your EPIAS password

**Security Note:** Never commit the `.env` file to version control. It's already in `.gitignore`.

## Step 4: Restart Claude Desktop

**Completely quit and restart Claude Desktop** to load the MCP server.

## Step 5: Verify the Connection

1. **Look for the 🔌 icon** at the bottom of Claude Desktop
2. **Click it** to see connected MCP servers
3. **Confirm "eptr2"** appears in the list with a green indicator

If you see "eptr2" listed, you're ready to go! ✅

## Using eptr2 with Claude

Once connected, Claude will have access to these 10 tools:

1. **get_market_clearing_price** - Day-ahead market prices (MCP/PTF)
2. **get_system_marginal_price** - System marginal prices (SMP/SMF)
3. **get_real_time_consumption** - Real-time consumption data
4. **get_real_time_generation** - Generation by resource type
5. **get_demand_forecast** - Demand forecasts (Load Plan/UECM)
6. **get_imbalance_price** - Imbalance pricing
7. **get_available_eptr2_calls** - List all 213+ API endpoints
8. **call_eptr2_api** - Generic call to any endpoint
9. **get_hourly_consumption_and_forecast** - Composite consumption data
10. **get_price_and_cost_data** - Comprehensive pricing data

## Example Questions for Claude

After setup, try asking Claude:

- "What was the market clearing price yesterday?"
- "Show me real-time electricity consumption for today"
- "What are the system marginal prices for the last week?"
- "Get generation data by resource type for October 2024"
- "What electricity market data sources are available?"

## Troubleshooting

### MCP Server Not Showing Up

1. **Restart Claude Desktop** completely (quit and reopen)
2. **Check config file syntax** - JSON must be valid (no trailing commas)
3. **Verify credentials** are set in `.env` file
4. **Check Claude Desktop logs:**

   | Operating System | Log Location |
   |-----------------|--------------|
   | **macOS** | `~/Library/Logs/Claude/` |
   | **Windows** | `%APPDATA%\Claude\Logs\` |
   | **Linux** | `~/.config/Claude/Logs/` |

### Authentication Errors

- **Verify EPIAS credentials** are correct in `.env` file
- **Check registration status** - account must be approved
- **Re-register if needed:** https://kayit.epias.com.tr/epias-transparency-platform-registration-form

### Testing the Server Manually

You can test the MCP server independently:

**With uv:**
```bash
cd /FULL/PATH/TO/YOUR/eptr2
uv run --extra mcp eptr2-mcp-server
```

**With standard Python:**
```bash
cd /FULL/PATH/TO/YOUR/eptr2
python -m eptr2.mcp.server
```

The server should start and show initialization messages. Press `Ctrl+C` to stop.

If this works but Claude Desktop doesn't connect:
- Double-check your `claude_desktop_config.json` syntax
- Ensure paths are absolute, not relative
- Restart Claude Desktop again

## Summary

**Files you need to modify:**

1. **Claude Desktop Config** (one of):
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. **Environment File:**
   - `/FULL/PATH/TO/YOUR/eptr2/.env` (create with your EPIAS credentials)

**After setup:**
- Restart Claude Desktop
- Look for 🔌 icon showing "eptr2" connected
- Start asking questions about Turkish electricity market data!

## Additional Resources

- **AGENTS.md** - Quick reference for AI agents
- **README.md** - Full documentation
- **Package on PyPI:** https://pypi.org/project/eptr2/
- **Live Demo:** https://eptr2demo.streamlit.app/
- **EPIAS Platform:** https://seffaflik.epias.com.tr/

- [FastMCP Documentation](https://gofastmcp.com)
- [Model Context Protocol Docs](https://modelcontextprotocol.io)
- [eptr2 Documentation](https://github.com/Tideseed/eptr2)
