#!/usr/bin/env python3
"""
Test execution monitor for composite function tests.
Shows rate limiting status and provides recommendations.
"""

import sys
import subprocess
from pathlib import Path


class TestMonitor:
    """Monitor test execution and provide guidance"""

    @staticmethod
    def get_test_count():
        """Get total number of composite tests"""
        result = subprocess.run(
            ["pytest", "tests/composite/", "--collect-only", "-q"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )
        try:
            # Extract number from output like "31 tests collected"
            output = result.stdout.strip()
            if "test" in output:
                count = int(output.split()[0])
                return count
        except (ValueError, IndexError):
            pass
        return None

    @staticmethod
    def estimate_runtime(test_count, rate_limit=10):
        """Estimate runtime based on test count and rate limit"""
        if not test_count:
            return None

        # Rough estimate: 1 API call per test + overhead
        api_calls = test_count * 0.7  # Not all tests are heavy
        delay_per_call = 0.5  # seconds
        overhead_per_test = 2.0  # seconds (setup, assertion, teardown)

        total_seconds = (api_calls * delay_per_call) + (test_count * overhead_per_test)

        # Add rate limiting wait time
        if api_calls > rate_limit:
            additional_waits = (api_calls - rate_limit) // rate_limit
            total_seconds += additional_waits * 60  # 60 second wait per throttle

        minutes = int(total_seconds / 60)
        return minutes

    @staticmethod
    def show_execution_guide():
        """Display execution guide"""
        test_count = TestMonitor.get_test_count()
        est_time = TestMonitor.estimate_runtime(test_count) if test_count else None

        print("\n" + "=" * 70)
        print("COMPOSITE FUNCTION TEST EXECUTION GUIDE")
        print("=" * 70)
        print()

        if test_count:
            print(f"📊 Tests Found: {test_count} tests")
        if est_time:
            print(
                f"⏱️  Estimated Runtime: {est_time}-{est_time + 10} minutes (with rate limiting)"
            )

        print()
        print("SAFE EXECUTION METHODS:")
        print("-" * 70)
        print()
        print("1️⃣  DEFAULT (Recommended)")
        print("   pytest tests/composite/ -v")
        print("   ✅ Automatically rate-limited")
        print("   ✅ Sequential execution")
        if est_time:
            print(f"   ⏱️  Duration: {est_time}-{est_time + 10} minutes")
        print()

        print("2️⃣  FAST (Skip slow tests)")
        print("   pytest tests/composite/ -v -m 'not slow'")
        print("   ✅ Faster execution")
        fast_time = int((est_time or 15) * 0.5)
        print(f"   ⏱️  Duration: {fast_time}-{fast_time + 5} minutes")
        print()

        print("3️⃣  UNIT TESTS ONLY (Auto-initialized)")
        print("   pytest tests/composite/ -v -k 'without_eptr'")
        print("   ✅ Minimal API calls")
        print("   ⏱️  Duration: 3-5 minutes")
        print()

        print("=" * 70)
        print("FORBIDDEN (Will cause throttling/bans):")
        print("-" * 70)
        print("❌ pytest tests/composite/ -n auto")
        print("❌ pytest tests/composite/ -n 4")
        print("❌ pytest -j auto")
        print()
        print("=" * 70)
        print()
        print("📖 Full guide: helpdocs/compliant_test_execution.md")
        print("🚀 Quick ref:  helpdocs/quick_test_reference.md")
        print()


if __name__ == "__main__":
    try:
        TestMonitor.show_execution_guide()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
