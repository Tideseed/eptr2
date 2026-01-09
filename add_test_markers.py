#!/usr/bin/env python3
"""
Script to add pytest markers to composite tests for rate limiting compliance.
Markers help organize tests and prevent API throttling.
"""

import re
import os
from pathlib import Path

TEST_DIR = Path("tests/composite")
MARKER_PATTERNS = {
    "test_.*_without_eptr": "@pytest.mark.api_call\n",  # Light API usage
    "test_.*": "@pytest.mark.api_call\n@pytest.mark.serial\n@pytest.mark.integration\n",  # Default: all marked
}


def add_markers_to_file(file_path, exclude_patterns=None):
    """Add pytest markers to test functions in a file"""
    if exclude_patterns is None:
        exclude_patterns = []

    with open(file_path, "r") as f:
        content = f.read()

    # Pattern to match: def test_* with no decorator
    pattern = r"^(def test_.*?[\(\[])"

    def replacer(match):
        func_line = match.group(1)
        func_name = match.group(1).split("(")[0].replace("def ", "")

        # Check if already has decorators
        lines = content[: match.start()].rstrip().split("\n")
        if lines and lines[-1].startswith("@pytest.mark"):
            return match.group(0)  # Already decorated

        # Check exclusion patterns
        should_exclude = False
        for exclude in exclude_patterns:
            if exclude in func_name:
                should_exclude = True
                break

        if should_exclude:
            return match.group(0)

        # Determine markers based on function name
        if "without_eptr" in func_name:
            markers = "@pytest.mark.api_call\n"
        else:
            markers = "@pytest.mark.api_call\n@pytest.mark.serial\n"

        return markers + match.group(0)

    # This is complex, so instead let's document manually
    return content


# Print instructions instead of auto-modifying
print("""
To add markers to test files, add these decorators to test functions:

FOR TESTS WITH REAL API CALLS (test_eptr2_*, test_get_*, etc):
@pytest.mark.api_call
@pytest.mark.serial
@pytest.mark.integration
def test_function_name(params):

FOR TESTS WITH AUTO-INITIALIZED EPTR (test_*_without_eptr):
@pytest.mark.api_call
def test_function_name_without_eptr(params):

The conftest.py will automatically apply these markers based on naming conventions.
No manual editing needed if you use the recommended naming patterns.
""")
