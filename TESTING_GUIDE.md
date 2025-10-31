# Testing Guide for AI Agent Integration

This guide helps you test the new AI agent integration features added to eptr2.

## Prerequisites

1. **Valid EPIAS Credentials**
   - Register at: https://kayit.epias.com.tr/epias-transparency-platform-registration-form
   - You'll need your registration email and password

2. **Python Environment**
   - Python >= 3.9.6 (but not 3.9.7)
   - pip or uv package manager

## Installation for Testing

### Option 1: Install from source (recommended for testing)

```bash
# Clone the repository (if not already done)
git clone https://github.com/Tideseed/eptr2.git
cd eptr2

# Checkout the agent branch
git checkout agent-1
# OR
git checkout copilot/prepare-library-for-agentic-ai

# Install in development mode with all extras
pip install -e ".[allextras,mcp,dev]"
```

### Option 2: Install from PyPI (when released)

```bash
pip install "eptr2[allextras,mcp]"
```

## Configuration

Create a `.env` file in your working directory:

```env
EPTR_USERNAME=your.email@example.com
EPTR_PASSWORD=yourpassword
```

You can use `.env.example` as a template:
```bash
cp .env.example .env
# Edit .env with your credentials
```

## Test 1: Basic Library Usage

Test the basic eptr2 functionality:

```bash
python examples/basic_usage.py
```

**Expected Output:**
- 6 examples should run successfully
- Each example should display data from the EPIAS API
- You should see DataFrames with electricity market data
- No authentication errors

**What it tests:**
- ✓ Credential loading from .env
- ✓ TGT authentication
- ✓ Basic API calls (mcp, smp, rt-consumption)
- ✓ Composite functions
- ✓ API discovery
- ✓ Error handling

## Test 2: MCP Server Information

View MCP server configuration and tools:

```bash
python examples/mcp_server_example.py
```

**Expected Output:**
- Configuration guide for MCP server
- List of 10 available tools
- Example queries for AI agents
- Claude Desktop configuration

**What it tests:**
- ✓ Documentation completeness
- ✓ Tool descriptions
- ✓ Configuration examples

## Test 3: MCP Server Execution

Run the MCP server:

### Option A: Using CLI command
```bash
eptr2-mcp-server
```

### Option B: Using Python module
```bash
python -m eptr2.mcp.server
```

### Option C: Using example script
```bash
python examples/mcp_server_example.py --run
```

**Expected Behavior:**
- Server starts without errors
- Waits for MCP client connections
- Press Ctrl+C to stop

**What it tests:**
- ✓ MCP SDK is properly installed
- ✓ Server can start
- ✓ Credentials are loaded correctly

## Test 4: MCP Server with Claude Desktop (Manual)

If you have Claude Desktop:

1. **Configure Claude Desktop**

   Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):
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

2. **Restart Claude Desktop**

3. **Test Queries**
   
   Try these queries in Claude:
   - "What was the market clearing price in Turkey on July 29, 2024?"
   - "Show me the real-time electricity consumption for the last week"
   - "What API endpoints are available in eptr2?"
   - "Get comprehensive pricing data for July 2024"

**Expected Behavior:**
- Claude can access the eptr2 tools
- Queries return actual data from EPIAS
- Data is formatted in JSON/tables

**What it tests:**
- ✓ End-to-end MCP integration
- ✓ Tool invocation
- ✓ Data retrieval and formatting
- ✓ Error handling

## Test 5: Syntax and Import Tests

Check for Python syntax errors:

```bash
# Test imports
python -c "from eptr2 import EPTR2; print('✓ eptr2 imports OK')"
python -c "from eptr2.mcp import run_mcp_server; print('✓ MCP module imports OK')"
python -c "from eptr2.composite import get_hourly_price_and_cost_data; print('✓ Composite imports OK')"

# Test compilation
python -m py_compile src/eptr2/mcp/__init__.py
python -m py_compile src/eptr2/mcp/server.py
python -m py_compile examples/basic_usage.py
python -m py_compile examples/mcp_server_example.py

echo "✓ All files compile successfully"
```

**Expected Output:**
- All import statements succeed
- All files compile without errors

## Test 6: Documentation Validation

Check that all documentation files exist and are readable:

```bash
# Check documentation files
for file in README.md AGENT_GUIDE.md QUICK_REFERENCE.md CHANGELOG_MCP.md \
            AI_AGENT_INTEGRATION_SUMMARY.md src/eptr2/mcp/README.md \
            examples/README.md eptr2_api_schema.json mcp-config.json; do
    if [ -f "$file" ]; then
        echo "✓ $file exists"
    else
        echo "✗ $file missing"
    fi
done

# Validate JSON files
python -c "import json; json.load(open('eptr2_api_schema.json')); print('✓ eptr2_api_schema.json is valid JSON')"
python -c "import json; json.load(open('mcp-config.json')); print('✓ mcp-config.json is valid JSON')"
```

**Expected Output:**
- All documentation files exist
- JSON files are valid

## Common Issues and Solutions

### Issue: "MCP SDK not installed"
**Solution:**
```bash
pip install mcp
# or
pip install "eptr2[mcp]"
```

### Issue: "Authentication failed"
**Solution:**
- Check your credentials in `.env` file
- Verify they work on https://seffaflik.epias.com.tr/
- Ensure no extra spaces in credentials

### Issue: "No module named 'eptr2'"
**Solution:**
```bash
# Install the package
pip install -e ".[allextras,mcp]"
# or
pip install eptr2
```

### Issue: "pandas not installed"
**Solution:**
```bash
pip install "eptr2[allextras]"
```

### Issue: "Command 'eptr2-mcp-server' not found"
**Solution:**
```bash
# Reinstall with editable mode
pip install -e ".[allextras,mcp]"
# or use Python module instead
python -m eptr2.mcp.server
```

## Test Results Checklist

- [ ] Basic usage examples run successfully
- [ ] MCP server information displays correctly
- [ ] MCP server starts without errors
- [ ] All imports work correctly
- [ ] All files compile successfully
- [ ] All documentation files exist
- [ ] JSON files are valid
- [ ] (Optional) Claude Desktop integration works

## Performance Tests (Optional)

Test API call performance:

```python
from eptr2 import EPTR2
import time

eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

# First call (with authentication)
start = time.time()
df1 = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
time1 = time.time() - start
print(f"First call: {time1:.2f} seconds")

# Second call (with TGT recycling)
start = time.time()
df2 = eptr.call("smp", start_date="2024-07-29", end_date="2024-07-29")
time2 = time.time() - start
print(f"Second call: {time2:.2f} seconds")

print(f"Speedup: {time1/time2:.2f}x")
```

**Expected:**
- First call: 2-5 seconds (includes authentication)
- Second call: < 2 seconds (reuses TGT)
- Speedup: ~2-3x or better

## Reporting Issues

If you encounter issues, please report with:

1. **Environment information:**
   ```bash
   python --version
   pip list | grep eptr2
   pip list | grep mcp
   ```

2. **Error message** (full traceback)

3. **Steps to reproduce**

4. **Expected vs actual behavior**

## Next Steps After Testing

Once testing is complete:

1. Review test results
2. Fix any issues found
3. Update documentation if needed
4. Prepare for merge/release
5. Update version number in pyproject.toml
6. Create release notes

## Success Criteria

The AI agent integration is ready for release when:

- ✓ All basic usage examples work
- ✓ MCP server starts and runs
- ✓ No syntax or import errors
- ✓ Documentation is complete and accurate
- ✓ JSON files are valid
- ✓ (Optional) Claude Desktop integration confirmed
- ✓ Performance is acceptable
- ✓ No security issues

## Additional Resources

- **Main README**: [README.md](README.md)
- **Agent Guide**: [AGENT_GUIDE.md](AGENT_GUIDE.md)
- **Quick Reference**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **MCP Docs**: [src/eptr2/mcp/README.md](src/eptr2/mcp/README.md)
- **Examples**: [examples/README.md](examples/README.md)
- **Summary**: [AI_AGENT_INTEGRATION_SUMMARY.md](AI_AGENT_INTEGRATION_SUMMARY.md)
