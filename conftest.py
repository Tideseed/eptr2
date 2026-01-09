"""
Workspace root indicator for pytest.
This file ensures pytest recognizes the workspace root correctly
and loads conftest.py from the right location.
"""

# This empty conftest.py at workspace root ensures:
# 1. pytest.ini is recognized as config file
# 2. rootdir is set to workspace root
# 3. Fixtures from tests/conftest.py are loaded correctly
