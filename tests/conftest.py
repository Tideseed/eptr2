"""
Pytest configuration for composite function tests with rate limiting.
Prevents API throttling and bans by controlling test execution.
"""

import time
import pytest

# Rate limiting configuration
RATE_LIMIT_CONFIG = {
    "calls_per_minute": 10,  # Max API calls per minute
    "min_delay_seconds": 0.5,  # Minimum delay between API calls
    "max_concurrent_tests": 1,  # Run tests sequentially by default
}

# Track API calls for rate limiting
api_call_times = []


class RateLimiter:
    """Implements rate limiting to prevent API throttling"""

    def __init__(self, calls_per_minute=10, min_delay=0.5):
        self.calls_per_minute = calls_per_minute
        self.min_delay = min_delay
        self.call_times = []
        self.last_call_time = None

    def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        now = time.time()

        # Remove calls older than 1 minute
        self.call_times = [t for t in self.call_times if now - t < 60]

        # Check if we've hit the rate limit
        if len(self.call_times) >= self.calls_per_minute:
            oldest_call = self.call_times[0]
            wait_time = 60 - (now - oldest_call) + 0.1
            if wait_time > 0:
                print(f"\n⏳ Rate limit reached. Waiting {wait_time:.1f} seconds...")
                time.sleep(wait_time)
                self.call_times = []

        # Enforce minimum delay between calls
        if self.last_call_time is not None:
            elapsed = time.time() - self.last_call_time
            if elapsed < self.min_delay:
                delay = self.min_delay - elapsed
                time.sleep(delay)

        self.last_call_time = time.time()
        self.call_times.append(self.last_call_time)


# Global rate limiter instance
_rate_limiter = RateLimiter(
    calls_per_minute=RATE_LIMIT_CONFIG["calls_per_minute"],
    min_delay=RATE_LIMIT_CONFIG["min_delay_seconds"],
)


@pytest.fixture(scope="session")
def rate_limiter():
    """Provides rate limiter instance for tests"""
    return _rate_limiter


@pytest.fixture(autouse=True)
def enforce_rate_limit(rate_limiter, request):
    """
    Automatically enforce rate limiting for tests marked as 'api_call'.
    Runs before each test that makes API calls.
    """
    if "api_call" in request.keywords:
        rate_limiter.wait_if_needed()
    yield


def pytest_configure(config):
    """Register custom pytest markers"""
    config.addinivalue_line(
        "markers", "api_call: marks test as making API calls (subject to rate limiting)"
    )
    config.addinivalue_line(
        "markers", "slow: marks test as slow (may make multiple API calls)"
    )
    config.addinivalue_line(
        "markers", "integration: marks test as integration test (requires live API)"
    )
    config.addinivalue_line(
        "markers", "serial: marks test that should run serially (not in parallel)"
    )


def pytest_collection_modifyitems(config, items):
    """
    Automatically mark API-calling tests.
    Tests that use EPTR2 are marked as api_call and serial.

    Automatic marking rules:
    - All tests in tests/composite/ are marked @api_call
    - Tests WITHOUT "without_eptr" in name are marked @serial and @integration
    - Tests WITH "without_eptr" in name get minimal marking (lighter API usage)
    """
    for item in items:
        # All composite tests make API calls (EPTR2 initialization)
        if "composite" in str(item.fspath):
            item.add_marker(pytest.mark.api_call)

            # Distinguish between real API calls and auto-initialized calls
            if "without_eptr" in item.name:
                # These are lighter - just minimal API usage for auto-init
                pass
            else:
                # These make real API calls
                item.add_marker(pytest.mark.serial)
                item.add_marker(pytest.mark.integration)
                item.add_marker(pytest.mark.slow)


def get_test_execution_summary():
    """Generate summary of test execution"""
    return {
        "rate_limit_config": RATE_LIMIT_CONFIG,
        "recommended_runners": [
            "pytest tests/composite/ -v -m 'not slow' --maxfail=3",
            "pytest tests/composite/ -v -n 0 (no parallelization)",
            "pytest tests/composite/ -v --tb=short (short tracebacks)",
        ],
    }
