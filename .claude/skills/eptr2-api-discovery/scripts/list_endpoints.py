#!/usr/bin/env python3
"""
eptr2 API Endpoint Discovery Script

This script helps you discover and explore available eptr2 API endpoints.
Run it to interactively search for endpoints by keyword or category.

Usage:
    python list_endpoints.py                    # List all endpoints
    python list_endpoints.py price              # Search for 'price' endpoints
    python list_endpoints.py --category GÖP    # List all GÖP endpoints
"""

import sys


def main():
    try:
        from eptr2.mapping.help import get_help_d
    except ImportError:
        print("Error: eptr2 package not installed.")
        print("Install with: pip install eptr2")
        sys.exit(1)

    all_help = get_help_d()

    # Parse arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--category":
            if len(sys.argv) > 2:
                category = sys.argv[2]
                filter_by_category(all_help, category)
            else:
                list_categories(all_help)
        elif sys.argv[1] == "--help":
            print(__doc__)
        else:
            keyword = " ".join(sys.argv[1:])
            search_by_keyword(all_help, keyword)
    else:
        list_all_endpoints(all_help)


def list_all_endpoints(all_help):
    """List all available endpoints."""
    print(f"\n{'=' * 60}")
    print(f"eptr2 Available Endpoints ({len(all_help)} total)")
    print(f"{'=' * 60}\n")

    # Group by category
    categories = {}
    for call, info in all_help.items():
        cat = info.get("category", "Other")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((call, info))

    for cat in sorted(categories.keys()):
        print(f"\n## {cat}")
        print("-" * 40)
        for call, info in sorted(categories[cat]):
            title = info["title"]["en"][:40]
            print(f"  {call:<25} {title}")

    print(f"\n{'=' * 60}")
    print(f"Total: {len(all_help)} endpoints in {len(categories)} categories")
    print(f"{'=' * 60}\n")


def search_by_keyword(all_help, keyword):
    """Search endpoints by keyword."""
    keyword_lower = keyword.lower()

    matches = {}
    for call, info in all_help.items():
        # Search in call name, title (both EN and TR), and description
        searchable = [
            call,
            info["title"].get("en", ""),
            info["title"].get("tr", ""),
            info["desc"].get("en", ""),
            info["desc"].get("tr", ""),
        ]

        if any(keyword_lower in s.lower() for s in searchable):
            matches[call] = info

    if matches:
        print(f"\n{'=' * 60}")
        print(f"Search Results for '{keyword}' ({len(matches)} matches)")
        print(f"{'=' * 60}\n")

        for call, info in sorted(matches.items()):
            print(f"## {call}")
            print(f"   Category: {info['category']}")
            print(f"   Title (EN): {info['title']['en']}")
            print(f"   Title (TR): {info['title']['tr']}")
            print(f"   Description: {info['desc']['en'][:100]}...")
            print(f"   URL: {info['url']}")
            print()
    else:
        print(f"\nNo endpoints found matching '{keyword}'")
        print("Try searching for: price, consumption, generation, dam, idm, bpm")


def filter_by_category(all_help, category):
    """Filter endpoints by category."""
    matches = {
        k: v for k, v in all_help.items() if v["category"].lower() == category.lower()
    }

    if matches:
        print(f"\n{'=' * 60}")
        print(f"Category: {category} ({len(matches)} endpoints)")
        print(f"{'=' * 60}\n")

        for call, info in sorted(matches.items()):
            print(f"  {call:<25} {info['title']['en']}")
    else:
        print(f"\nNo category found matching '{category}'")
        list_categories(all_help)


def list_categories(all_help):
    """List all available categories."""
    categories = {}
    for call, info in all_help.items():
        cat = info.get("category", "Other")
        categories[cat] = categories.get(cat, 0) + 1

    print(f"\n{'=' * 60}")
    print("Available Categories")
    print(f"{'=' * 60}\n")

    for cat, count in sorted(categories.items()):
        print(f"  {cat:<30} ({count} endpoints)")

    print("\nUse: python list_endpoints.py --category <CATEGORY>")


if __name__ == "__main__":
    main()
