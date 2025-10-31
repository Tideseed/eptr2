# Changelog - AI Agent Integration (MCP Server)

## Added for AI Agent Integration

### MCP Server Implementation
- **New Module**: `eptr2.mcp` - Model Context Protocol server for AI agents
- **CLI Command**: `eptr2-mcp-server` - Easy-to-run MCP server
- **10 MCP Tools** exposed for AI agent queries:
  1. `get_market_clearing_price` - Day-ahead market prices
  2. `get_system_marginal_price` - System marginal prices  
  3. `get_real_time_consumption` - Real-time consumption data
  4. `get_real_time_generation` - Generation by resource type
  5. `get_demand_forecast` - Demand forecasts
  6. `get_imbalance_price` - Imbalance pricing
  7. `get_available_eptr2_calls` - List all 213+ API endpoints
  8. `call_eptr2_api` - Generic API call to any endpoint
  9. `get_hourly_consumption_and_forecast` - Composite consumption data
  10. `get_price_and_cost_data` - Comprehensive pricing data

### Agent-Friendly Documentation
- **AGENT_GUIDE.md** - Comprehensive guide for AI agents working with eptr2
- **QUICK_REFERENCE.md** - Quick reference card with common patterns
- **eptr2_api_schema.json** - Structured JSON schema for easy parsing
- **src/eptr2/mcp/README.md** - Detailed MCP server documentation
- **mcp-config.json** - Ready-to-use MCP configuration file

### Examples
- **examples/basic_usage.py** - 6 comprehensive examples covering:
  - Basic price queries
  - Multiple data sources
  - Composite functions
  - API discovery
  - Generation data
  - Error handling
- **examples/mcp_server_example.py** - MCP server setup and usage guide
- **examples/README.md** - Examples documentation

### Configuration
- **.env.example** - Template for environment configuration
- **Optional dependency**: `mcp` (install with `pip install "eptr2[mcp]"`)
- **Updated README.md** with MCP installation and usage instructions

## Technical Details

### MCP Server Features
- Async/await support for efficient operation
- Automatic credential management via .env files
- TGT (Ticket Granting Ticket) recycling for optimal performance
- Error handling with descriptive messages
- JSON output format compatible with all MCP clients
- Support for all major eptr2 API endpoints
- Integration with composite functions

### Integration Points
- **Claude Desktop**: Configuration examples provided
- **Generic MCP Clients**: Standard stdio-based protocol
- **Programmatic Access**: Can be run as Python module or CLI command

### Dependencies
- Core: urllib3, pytz (existing)
- MCP Support: `mcp>=0.9.0` (new optional)
- All Extras: pandas, streamlit, tornado, requests (existing)

## Usage Examples

### Basic MCP Server Usage
```bash
# Install with MCP support
pip install "eptr2[allextras,mcp]"

# Run the server
eptr2-mcp-server
```

### Programmatic Usage
```python
from eptr2.mcp import run_mcp_server
import asyncio

asyncio.run(run_mcp_server(use_dotenv=True, recycle_tgt=True))
```

### Claude Desktop Configuration
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

## Benefits for AI Agents

1. **Standardized Access**: Model Context Protocol ensures compatibility
2. **Rich Tool Set**: 10 pre-configured tools covering most use cases
3. **Discovery**: Agents can query available endpoints dynamically
4. **Efficiency**: TGT recycling minimizes authentication overhead
5. **Documentation**: Multiple documentation formats for quick learning
6. **Examples**: Comprehensive examples for common patterns

## Files Modified

### Changed
- `README.md` - Added MCP installation and usage instructions
- `pyproject.toml` - Added MCP optional dependency and CLI command

### New Files
- `src/eptr2/mcp/__init__.py`
- `src/eptr2/mcp/server.py`
- `src/eptr2/mcp/README.md`
- `AGENT_GUIDE.md`
- `QUICK_REFERENCE.md`
- `eptr2_api_schema.json`
- `mcp-config.json`
- `.env.example`
- `examples/basic_usage.py`
- `examples/mcp_server_example.py`
- `examples/README.md`
- `CHANGELOG_MCP.md` (this file)

## Backward Compatibility

All changes are backward compatible:
- MCP support is optional (`pip install "eptr2[mcp]"`)
- No changes to existing API
- No breaking changes to core functionality
- Existing code continues to work unchanged

## Future Enhancements

Potential future additions:
- Additional MCP tools for specialized queries
- Support for MCP resources and prompts
- Batch query optimization
- Caching layer for frequently accessed data
- WebSocket support for real-time updates
- Additional agent-friendly output formats

## Documentation Links

- Main README: [README.md](README.md)
- Agent Guide: [AGENT_GUIDE.md](AGENT_GUIDE.md)
- Quick Reference: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- MCP Server Docs: [src/eptr2/mcp/README.md](src/eptr2/mcp/README.md)
- Examples: [examples/README.md](examples/README.md)
- API Schema: [eptr2_api_schema.json](eptr2_api_schema.json)

## Support

For questions or issues:
- GitHub: https://github.com/Tideseed/eptr2
- Email: info@tideseed.com
- PyPI: https://pypi.org/project/eptr2/
