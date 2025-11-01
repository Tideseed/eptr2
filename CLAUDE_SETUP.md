# Claude Desktop MCP Server Setup for eptr2

## ✅ Setup Complete!

The eptr2 MCP server has been added to Claude Desktop.

## Configuration Files

### 1. Claude Desktop Config
**Location:** `YOUR_CLAUDE_PATH/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "eptr2": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "YOUR_EPTR2_PATH",
        "--extra",
        "mcp",
        "eptr2-mcp-server"
      ]
    }
  }
}
```

### 2. Environment Variables
**Location:** `YOUR_EPTR2_PATH/.env`

**⚠️ IMPORTANT:** You need to update the `.env` file with your actual EPIAS credentials:

```bash
# Edit this file with your credentials
nano YOUR_EPTR2_PATH/.env
```

Replace:
- `EPTR_USERNAME=your.email@example.com` → Your actual email
- `EPTR_PASSWORD=yourpassword` → Your actual password

## Next Steps

1. **Update credentials** in `.env` file (required!)
2. **Restart Claude Desktop** to load the MCP server
3. **Look for the 🔌 icon** in Claude Desktop - it should show "eptr2" as connected
4. **Test it** by asking Claude about Turkish electricity market data

## Available Tools in Claude

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
1. Make sure you've restarted Claude Desktop
2. Check that credentials are set in `.env` file
3. Look at Claude Desktop logs: `CLAUDE_LOGS_PATH/Logs/Claude/`

### Authentication Errors
- Verify your EPIAS credentials are correct
- Register at: https://kayit.epias.com.tr/epias-transparency-platform-registration-form

### Testing the Server Manually
```bash
cd YOUR_EPTR2_PATH
uv run --extra mcp eptr2-mcp-server
```

Press Ctrl+C to stop the test.

## Files Created/Modified

- ✅ `YOUR_CLAUDE/PATH/claude_desktop_config.json` - Updated with eptr2 server
- ✅ `YOUR_EPTR2_PATH/.env` - Created (needs your credentials)

## Additional Resources

- [FastMCP Documentation](https://gofastmcp.com)
- [Model Context Protocol Docs](https://modelcontextprotocol.io)
- [eptr2 Documentation](https://github.com/Tideseed/eptr2)
