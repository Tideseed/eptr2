"""Endpoint discovery helpers for AI agents and the ``eptr2`` CLI.

Pure functions over the static call metadata in ``eptr2.mapping`` — no
network access and no credentials required.
"""

from typing import Optional

from eptr2.mapping.help import get_help_d, get_call_help
from eptr2.mapping.path import get_alias_map, get_path_map

UNCATEGORIZED = "Uncategorized"


def _all_call_info() -> dict[str, dict]:
    """Metadata for every callable key, merging the path map (authoritative
    list of callable keys) with the bilingual help dictionary. Keys without a
    help entry get a minimal record so they are still discoverable."""
    help_d = get_help_d()
    info = {}
    for key in get_path_map(just_call_keys=True):
        entry = help_d.get(key)
        if entry is None:
            entry = {
                "category": UNCATEGORIZED,
                "title": {"tr": "", "en": ""},
                "desc": {"tr": "", "en": ""},
                "url": None,
            }
        info[key] = entry
    return info


def list_calls(category: Optional[str] = None) -> dict[str, dict]:
    """All callable keys with their metadata, optionally filtered by category
    (case-insensitive, e.g. "GÖP", "GİP", "DGP")."""
    info = _all_call_info()
    if category is None:
        return info
    cat = category.lower()
    return {
        k: v for k, v in info.items() if v.get("category", "").lower() == cat
    }


def list_categories() -> dict[str, int]:
    """Category name -> number of endpoints."""
    counts: dict[str, int] = {}
    for v in _all_call_info().values():
        cat = v.get("category") or UNCATEGORIZED
        counts[cat] = counts.get(cat, 0) + 1
    return dict(sorted(counts.items()))


def search_calls(keyword: str, category: Optional[str] = None) -> dict[str, dict]:
    """Case-insensitive keyword search over call keys, titles and
    descriptions (both English and Turkish)."""
    kw = keyword.lower()
    matches = {}
    for key, info in list_calls(category=category).items():
        searchable = [
            key,
            info.get("title", {}).get("en", ""),
            info.get("title", {}).get("tr", ""),
            info.get("desc", {}).get("en", ""),
            info.get("desc", {}).get("tr", ""),
        ]
        if any(kw in s.lower() for s in searchable if s):
            matches[key] = info
    return matches


def describe_call(key: str) -> Optional[dict]:
    """Full description of a single call: metadata plus call path, HTTP
    method, and required/optional parameters. Resolves aliases (e.g. "ptf"
    -> "mcp"). Returns None for unknown keys."""
    alias_map = get_alias_map()
    resolved = alias_map.get(key, key)
    d = get_call_help(resolved)
    if d is None:
        return None
    out = {"key": resolved}
    if resolved != key:
        out["alias_of"] = {"alias": key, "resolves_to": resolved}
    out.update(d)
    if out.get("help") is None:
        out["help"] = _all_call_info().get(resolved)
    return out


def format_calls_table(calls: dict[str, dict]) -> str:
    """Human-readable rendering of a calls dict, grouped by category."""
    if not calls:
        return "No matching endpoints found."
    by_cat: dict[str, list] = {}
    for key, info in calls.items():
        by_cat.setdefault(info.get("category") or UNCATEGORIZED, []).append(
            (key, info)
        )
    lines = []
    for cat in sorted(by_cat):
        lines.append(f"\n## {cat}")
        lines.append("-" * 40)
        for key, info in sorted(by_cat[cat]):
            title = (info.get("title", {}).get("en") or "")[:50]
            lines.append(f"  {key:<28} {title}")
    lines.append("")
    lines.append(f"Total: {len(calls)} endpoints in {len(by_cat)} categories")
    return "\n".join(lines)
