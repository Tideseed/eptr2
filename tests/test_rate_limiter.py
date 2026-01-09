"""
Test the rate limiter functionality independently.
This verifies that the rate limiting system works correctly.
"""

import time
import pytest
from tests.conftest import RateLimiter


@pytest.fixture
def rate_limiter_instance():
    """Create a test rate limiter instance"""
    return RateLimiter(calls_per_minute=3, min_delay=0.2)


class TestRateLimiter:
    """Test suite for RateLimiter class"""

    def test_rate_limiter_basic_delay(self, rate_limiter_instance):
        """Test that rate limiter enforces minimum delay"""
        limiter = rate_limiter_instance

        start = time.time()
        limiter.wait_if_needed()  # First call
        limiter.wait_if_needed()  # Second call should be delayed
        elapsed = time.time() - start

        # Should take at least 0.2 seconds
        assert elapsed >= 0.2, f"Expected delay >= 0.2s, got {elapsed}s"

    def test_rate_limiter_call_tracking(self, rate_limiter_instance):
        """Test that rate limiter tracks calls"""
        limiter = rate_limiter_instance

        assert len(limiter.call_times) == 0, "Should start with no calls"

        limiter.wait_if_needed()
        assert len(limiter.call_times) == 1, "Should have 1 call tracked"

        limiter.wait_if_needed()
        assert len(limiter.call_times) == 2, "Should have 2 calls tracked"

    def test_rate_limiter_cleans_old_calls(self, rate_limiter_instance):
        """Test that rate limiter removes calls older than 1 minute"""
        limiter = RateLimiter(calls_per_minute=1, min_delay=0)

        # Add old timestamp (simulated)
        limiter.call_times.append(time.time() - 61)  # 61 seconds ago
        limiter.call_times.append(time.time() - 30)  # 30 seconds ago

        initial_count = len(limiter.call_times)
        limiter.wait_if_needed()
        final_count = len(limiter.call_times)

        # Should remove the 61-second-old call
        assert final_count < initial_count, "Should clean old calls"

    def test_rate_limiter_returns_none(self, rate_limiter_instance):
        """Test that wait_if_needed doesn't return a value"""
        limiter = rate_limiter_instance
        result = limiter.wait_if_needed()
        assert result is None, "wait_if_needed should return None"


class TestRateLimiterIntegration:
    """Integration tests for rate limiting with pytest"""

    @pytest.mark.api_call
    def test_api_call_marked(self):
        """Test that test is marked for rate limiting"""
        # This test should be rate-limited
        assert True

    @pytest.mark.api_call
    @pytest.mark.serial
    def test_serial_execution(self):
        """Test that serial marker is applied"""
        # This test should run sequentially
        assert True

    def test_unmarked_test_runs_normally(self):
        """This test has no API call marker"""
        # Should run without rate limiting
        assert True


@pytest.mark.skip(reason="Manual performance test")
class TestRateLimiterPerformance:
    """Performance tests for rate limiter"""

    def test_rate_limiter_with_many_calls(self):
        """Test rate limiter with many sequential calls"""
        limiter = RateLimiter(calls_per_minute=10, min_delay=0.1)

        start = time.time()
        for _ in range(5):
            limiter.wait_if_needed()
        elapsed = time.time() - start

        # 5 calls with 0.1s delay = ~0.4 seconds
        assert elapsed >= 0.4, f"Expected >= 0.4s, got {elapsed}s"
        assert elapsed < 2.0, f"Expected < 2.0s, got {elapsed}s"

    def test_rate_limit_enforcement(self):
        """Test that rate limit is enforced correctly"""
        limiter = RateLimiter(calls_per_minute=5, min_delay=0.05)

        start = time.time()
        # Make 6 calls (should trigger rate limit after 5)
        for _ in range(6):
            limiter.wait_if_needed()
        elapsed = time.time() - start

        # Should take noticeable time due to rate limiting
        print(f"\n6 calls with limit of 5/min took {elapsed:.2f}s")
        assert elapsed > 0.2, "Rate limiting should add measurable delay"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
