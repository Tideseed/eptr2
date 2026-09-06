#!/usr/bin/env python3
"""
eptr2 API Endpoint Discovery Script

Thin wrapper around eptr2.agentic.discovery. Prefer the eptr2 CLI when
available: `eptr2 list`, `eptr2 search <keyword>`, `eptr2 describe <key>`.

Usage:
    python list_endpoints.py                    # List all endpoints
    python list_endpoints.py price              # Search for 'price' endpoints
    python list_endpoints.py --category GÖP    # List all GÖP endpoints
    python list_endpoints.py --category         # List categories
"""

import sys


def main():
    try:
        from eptr2.agentic import discovery
    except ImportError:
        print("Error: eptr2 package not installed.")
        print("Install with: pip install eptr2")
        sys.exit(1)

    args = sys.argv[1:]
    if not args:
        print(discovery.format_calls_table(discovery.list_calls()))
    elif args[0] == "--help":
        print(__doc__)
    elif args[0] == "--category":
        if len(args) > 1:
            calls = discovery.list_calls(category=args[1])
            if calls:
                print(discovery.format_calls_table(calls))
            else:
                print(f"No category found matching '{args[1]}'")
                _print_categories(discovery)
        else:
            _print_categories(discovery)
    else:
        keyword = " ".join(args)
        matches = discovery.search_calls(keyword)
        if matches:
            print(discovery.format_calls_table(matches))
        else:
            print(f"No endpoints found matching '{keyword}'")
            print("Try searching for: price, consumption, generation, dam, idm, bpm")


def _print_categories(discovery):
    print("\nAvailable Categories\n")
    for cat, count in discovery.list_categories().items():
        print(f"  {cat:<30} ({count} endpoints)")
    print("\nUse: python list_endpoints.py --category <CATEGORY>")


if __name__ == "__main__":
    main()
