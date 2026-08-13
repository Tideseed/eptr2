"""Machine-readable API schema generation for AI agents.

The schema is generated from the same metadata the library itself uses
(``eptr2.mapping``), so it cannot drift from the code. Output is
deterministic (sorted keys, no timestamps) so committed copies can be
byte-compared against a fresh build.
"""

import inspect
import json
from pathlib import Path
from typing import Optional

SCHEMA_FORMAT_VERSION = "2.0"

# Public, non-deprecated cost utilities from eptr2.util.costs. Curated
# explicitly so internal/deprecated helpers (temp_*, *_pre_2026, *_2026
# period variants) stay out of the agent-facing schema.
COST_UTILITY_NAMES = [
    "get_kupst_tolerance",
    "get_kupst_tolerance_by_contract",
    "calculate_unit_kupst_cost",
    "calculate_unit_kupst_cost_by_contract",
    "calculate_kupst_cost",
    "calculate_kupst_cost_by_contract",
    "calculate_unit_imbalance_price",
    "calculate_unit_imbalance_price_by_contract",
    "calculate_unit_imbalance_cost",
    "calculate_unit_imbalance_cost_by_contract",
    "calculate_unit_price_and_costs",
    "calculate_unit_price_and_costs_by_contract",
    "calculate_unit_price_and_costs_by_datetime",
    "calculate_imbalance_amount",
    "calculate_diff_costs",
    "calculate_diff_costs_by_contract",
    "calculate_diff_costs_by_datetime",
]


def _function_entry(func, module_name: str) -> dict:
    doc = inspect.getdoc(func)
    summary = doc.strip().split("\n")[0] if doc else None
    try:
        signature = str(inspect.signature(func))
    except (TypeError, ValueError):
        signature = None
    return {"module": module_name, "signature": signature, "summary": summary}


def _endpoint_entries() -> dict:
    from eptr2.agentic.discovery import _all_call_info
    from eptr2.mapping.help import get_call_help

    endpoints = {}
    for key, info in _all_call_info().items():
        h = get_call_help(key)
        endpoints[key] = {
            "category": info.get("category"),
            "title": info.get("title"),
            "desc": info.get("desc"),
            "url": info.get("url"),
            "call_path": h.get("call_path"),
            "call_method": h.get("call_method"),
            "required_params": h.get("required_body_params"),
            "optional_params": h.get("optional_body_params"),
        }
    return endpoints


def _composite_entries() -> dict:
    import eptr2.composite as composite

    entries = {}
    for name in dir(composite):
        if name.startswith("_"):
            continue
        obj = getattr(composite, name)
        if not inspect.isfunction(obj):
            continue
        module = getattr(obj, "__module__", "")
        if not module.startswith("eptr2.composite"):
            continue
        entries[name] = _function_entry(obj, module)
    return entries


def _cost_utility_entries() -> dict:
    import eptr2.util.costs as costs

    entries = {}
    for name in COST_UTILITY_NAMES:
        obj = getattr(costs, name, None)
        if obj is None:
            continue
        entries[name] = _function_entry(obj, "eptr2.util.costs")
    return entries


def build_schema() -> dict:
    """Build the full agent-facing schema dictionary."""
    from eptr2 import __version__
    from eptr2.mapping.path import get_alias_map

    endpoints = _endpoint_entries()
    return {
        "schema_format_version": SCHEMA_FORMAT_VERSION,
        "eptr2_version": __version__,
        "description": (
            "Machine-readable schema of the eptr2 Python client for the "
            "EPIAS Transparency Platform (Turkish electricity and natural "
            "gas markets). Generated with `eptr2 schema`; do not edit by hand."
        ),
        "usage": {
            "python": 'EPTR2().call("<key>", start_date=..., end_date=..., ...)',
            "cli": "eptr2 call <key> --start-date ... --end-date ...",
            "discovery": "eptr2 list | eptr2 search <keyword> | eptr2 describe <key>",
        },
        "date_format": "YYYY-MM-DD (ISO 8601); market timezone is Europe/Istanbul",
        "endpoint_count": len(endpoints),
        "endpoints": endpoints,
        "aliases": dict(sorted(get_alias_map().items())),
        "composite_functions": _composite_entries(),
        "cost_utilities": _cost_utility_entries(),
    }


def schema_json(schema: Optional[dict] = None) -> str:
    """Deterministic JSON serialization of the schema."""
    if schema is None:
        schema = build_schema()
    return json.dumps(schema, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def write_schema(path) -> Path:
    """Write the schema JSON to ``path`` and return it."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(schema_json(), encoding="utf-8")
    return p


def check_schema(path) -> bool:
    """True if the file at ``path`` matches a freshly built schema."""
    p = Path(path)
    if not p.exists():
        return False
    return p.read_text(encoding="utf-8") == schema_json()
