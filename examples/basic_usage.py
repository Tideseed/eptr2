"""
Example: Basic usage of eptr2 library for AI agents.

This example demonstrates the most common use cases for querying
Turkish electricity market data through the EPIAS Transparency Platform API.
"""

from eptr2 import EPTR2
from datetime import datetime, timedelta


def example_1_basic_price_query():
    """Get market clearing prices for a specific date range."""
    print("=" * 60)
    print("Example 1: Basic Price Query")
    print("=" * 60)

    # Initialize with credentials from .env file
    eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

    # Get market clearing price for the last 7 days
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    print(f"\nQuerying MCP from {start_date} to {end_date}")

    df = eptr.call("mcp", start_date=start_date, end_date=end_date)

    print(f"\nReturned {len(df)} records")
    print("\nFirst 5 records:")
    print(df.head())

    return df


def example_2_multiple_data_sources():
    """Query multiple related data sources."""
    print("\n" + "=" * 60)
    print("Example 2: Multiple Data Sources")
    print("=" * 60)

    eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

    date = "2024-07-29"

    # Get multiple related datasets
    print(f"\nQuerying multiple data sources for {date}")

    mcp = eptr.call("mcp", start_date=date, end_date=date)
    smp = eptr.call("smp", start_date=date, end_date=date)
    consumption = eptr.call("rt-cons", start_date=date, end_date=date)

    print(f"\n✓ MCP: {len(mcp)} records")
    print(f"✓ SMP: {len(smp)} records")
    print(f"✓ Real-time Consumption: {len(consumption)} records")

    return mcp, smp, consumption


def example_3_composite_functions():
    """Use composite functions for comprehensive data."""
    print("\n" + "=" * 60)
    print("Example 3: Composite Functions")
    print("=" * 60)

    from eptr2.composite import (
        get_hourly_consumption_and_forecast_data,
        get_hourly_price_and_cost_data,
    )

    eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

    date = "2024-07-29"

    print(f"\nQuerying composite data for {date}")

    # Get comprehensive consumption data
    consumption_df = get_hourly_consumption_and_forecast_data(
        eptr, start_date=date, end_date=date
    )

    # Get comprehensive pricing data
    price_df = get_hourly_price_and_cost_data(eptr, start_date=date, end_date=date)

    print(f"\n✓ Consumption & Forecast: {len(consumption_df)} records")
    print(f"  Columns: {list(consumption_df.columns)}")

    print(f"\n✓ Price & Cost Data: {len(price_df)} records")
    print(f"  Columns: {list(price_df.columns)}")

    return consumption_df, price_df


def example_4_discover_available_calls():
    """Discover all available API endpoints."""
    print("\n" + "=" * 60)
    print("Example 4: Discover Available API Calls")
    print("=" * 60)

    eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

    # Get all available calls
    calls = eptr.get_available_calls(include_aliases=True)

    print(f"\nTotal API calls available: {len(calls['keys'])}")
    print(f"Default aliases: {len(calls['default_aliases'])}")

    # Show some examples
    print("\nFirst 10 available calls:")
    for i, call in enumerate(calls["keys"][:10], 1):
        print(f"  {i}. {call}")

    print("\nSome common aliases:")
    for alias, target in list(calls["default_aliases"].items())[:5]:
        print(f"  {alias} → {target}")

    # Get call statistics
    stats = eptr.get_number_of_calls()
    print(f"\nCall Statistics:")
    print(f"  Total calls: {stats['n_total_calls']}")
    print(f"  API calls: {stats['n_api_calls']}")
    print(f"  Derived calls: {stats['n_derived_calls']}")

    return calls


def example_5_generation_data():
    """Query electricity generation data."""
    print("\n" + "=" * 60)
    print("Example 5: Generation Data")
    print("=" * 60)

    eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

    date = "2024-07-29"

    print(f"\nQuerying generation data for {date}")

    # Get real-time generation by resource type
    gen_df = eptr.call("rt-gen", start_date=date, end_date=date)

    print(f"\n✓ Real-time Generation: {len(gen_df)} records")
    print("\nGeneration columns (resource types):")
    for col in gen_df.columns:
        print(f"  - {col}")

    # Show summary statistics
    if len(gen_df) > 0:
        print("\nSample data (first record):")
        print(gen_df.iloc[0])

    return gen_df


def example_6_error_handling():
    """Demonstrate proper error handling."""
    print("\n" + "=" * 60)
    print("Example 6: Error Handling")
    print("=" * 60)

    eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

    # Example 1: Invalid call key
    print("\n1. Handling invalid call key:")
    try:
        df = eptr.call(
            "invalid-call-key", start_date="2024-07-29", end_date="2024-07-29"
        )
    except Exception as e:
        print(f"   ✗ Error caught: {e}")

    # Example 2: Missing required parameters
    print("\n2. Handling missing parameters:")
    try:
        df = eptr.call("mcp")  # Missing start_date and end_date
    except Exception as e:
        print(f"   ✗ Error caught: {type(e).__name__}")

    # Example 3: Proper usage
    print("\n3. Successful call:")
    try:
        df = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
        print(f"   ✓ Success: Retrieved {len(df)} records")
    except Exception as e:
        print(f"   ✗ Unexpected error: {e}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("EPTR2 Library Examples for AI Agents")
    print("=" * 60)
    print("\nThese examples demonstrate common usage patterns for")
    print("querying Turkish electricity market data via EPIAS API.")
    print("\nNote: Make sure you have a .env file with your credentials:")
    print("  EPTR_USERNAME=your.email@example.com")
    print("  EPTR_PASSWORD=yourpassword")
    print("=" * 60)

    try:
        # Run examples
        example_1_basic_price_query()
        example_2_multiple_data_sources()
        example_3_composite_functions()
        example_4_discover_available_calls()
        example_5_generation_data()
        example_6_error_handling()

        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Error running examples: {e}")
        print("\nMake sure:")
        print("1. You have valid EPIAS credentials in .env file")
        print("2. eptr2 library is installed: pip install 'eptr2[allextras]'")
        print("3. You have internet connectivity")


if __name__ == "__main__":
    main()
