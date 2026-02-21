# EPTR2 Examples

This directory contains example scripts demonstrating how to use the eptr2 library, both for direct usage and for AI agent integration via MCP (Model Context Protocol).

## Files

### 1. `basic_usage.py`
Demonstrates basic usage patterns for the eptr2 library:
- Basic price queries (MCP, SMP)
- Multiple data source queries
- Composite functions
- Discovery of available API calls
- Generation data queries
- Error handling

**Run it:**
```bash
python examples/basic_usage.py
```

**Requirements:**
- Create a `.env` file with your EPIAS credentials:
  ```
  EPTR_USERNAME=your.email@example.com
  EPTR_PASSWORD=yourpassword
  ```

### 2. `mcp_server_example.py`
Shows how to set up and use the MCP server for AI agent integration:
- MCP server configuration
- Available tools documentation
- Example AI agent queries
- Claude Desktop integration

**View information:**
```bash
python examples/mcp_server_example.py
```

**Run the MCP server:**
```bash
python examples/mcp_server_example.py --run
```

Or simply:
```bash
eptr2-mcp-server
```

## Quick Start

### For Direct Library Usage

1. Install eptr2:
   ```bash
   pip install "eptr2[allextras]"
   ```

2. Create `.env` file:
   ```
   EPTR_USERNAME=your.email@example.com
   EPTR_PASSWORD=yourpassword
   ```

3. Run examples:
   ```bash
   python examples/basic_usage.py
   ```

### For AI Agent Integration

1. Install with MCP support:
   ```bash
   pip install "eptr2[allextras,mcp]"
   ```

2. Create `.env` file (same as above)

3. View MCP configuration:
   ```bash
   python examples/mcp_server_example.py
   ```

4. Run MCP server:
   ```bash
   eptr2-mcp-server
   ```

5. Configure your AI assistant (e.g., Claude Desktop) to connect to the server

## Common Use Cases

### Get Market Prices
```python
from eptr2 import EPTR2

eptr = EPTR2(use_dotenv=True, recycle_tgt=True)
mcp = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
```

### Get Consumption Data
```python
consumption = eptr.call("rt-cons", start_date="2024-07-29", end_date="2024-07-29")
```

### Use Composite Functions
```python
from eptr2.composite import get_hourly_price_and_cost_data

df = get_hourly_price_and_cost_data(
    eptr, 
    start_date="2024-07-01", 
    end_date="2024-07-31"
)
```

### Discover Available APIs
```python
calls = eptr.get_available_calls(include_aliases=True)
print(f"Total calls: {len(calls['keys'])}")
```

## Resources

- **Main Documentation**: [../README.md](../README.md)
- **Agent Guide**: [../AGENT_GUIDE.md](../AGENT_GUIDE.md)
- **Quick Reference**: [../QUICK_REFERENCE.md](../QUICK_REFERENCE.md)
- **MCP Documentation**: [../src/eptr2/mcp/README.md](../src/eptr2/mcp/README.md)
- **API Schema**: [../eptr2_api_schema.json](../eptr2_api_schema.json)

## Troubleshooting

### Authentication Errors
- Verify your EPIAS credentials
- Check that `.env` file is in the correct location
- Ensure `use_dotenv=True` is set

### Import Errors
- Make sure eptr2 is installed: `pip install eptr2`
- For all features: `pip install "eptr2[allextras]"`
- For MCP support: `pip install "eptr2[mcp]"`

### MCP Server Issues
- Verify FastMCP is installed: `pip install fastmcp`
- Check Python version (>=3.10 required)
- Ensure credentials are properly configured

## License

Apache License 2.0 - Same as the eptr2 library
