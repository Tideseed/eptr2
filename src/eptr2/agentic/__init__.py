"""Agent-facing utilities for eptr2: endpoint discovery, machine-readable
schema generation, and agent-skill installation.

This package is provider-agnostic: it serves any AI assistant or agent
runtime (MCP clients, shell-driven agents, SKILL.md-compatible runtimes).
"""

from eptr2.agentic.discovery import (
    list_calls,
    list_categories,
    search_calls,
    describe_call,
    format_calls_table,
)
from eptr2.agentic.schema import (
    build_schema,
    schema_json,
    write_schema,
    check_schema,
    load_bundled_schema,
    SchemaGenerationUnavailable,
)
from eptr2.agentic.validation import (
    EptrValidationError,
    validate_call,
    validate_call_key,
    validate_date_value,
    validate_params,
)
from eptr2.agentic.skills import (
    list_bundled_skills,
    install_skills,
    resolve_dest,
    plugin_root,
    install_plugin,
)

__all__ = [
    "list_calls",
    "list_categories",
    "search_calls",
    "describe_call",
    "format_calls_table",
    "build_schema",
    "schema_json",
    "write_schema",
    "check_schema",
    "load_bundled_schema",
    "EptrValidationError",
    "validate_call",
    "validate_call_key",
    "validate_date_value",
    "validate_params",
    "SchemaGenerationUnavailable",
    "list_bundled_skills",
    "install_skills",
    "resolve_dest",
    "plugin_root",
    "install_plugin",
]
