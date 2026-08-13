"""Command-line interface for eptr2.

Designed to be equally usable by humans and shell-driven AI agents:
data goes to stdout only, diagnostics to stderr, nonzero exit codes on
error. Discovery commands (list, categories, search, describe, schema,
install-skills, mcp-config) need no credentials; only `call` talks to
the EPIAS Transparency API.
"""

import argparse
import json
import sys
from typing import Optional

from eptr2.agentic import discovery


def _err(msg: str) -> None:
    print(msg, file=sys.stderr)


def _cmd_list(args) -> int:
    calls = discovery.list_calls(category=args.category)
    if not calls and args.category:
        _err(f"No category found matching '{args.category}'.")
        _err("Available categories:")
        for cat, count in discovery.list_categories().items():
            _err(f"  {cat} ({count})")
        return 1
    if args.format == "json":
        print(json.dumps(calls, indent=2, ensure_ascii=False))
    else:
        print(discovery.format_calls_table(calls))
    return 0


def _cmd_categories(args) -> int:
    cats = discovery.list_categories()
    if args.format == "json":
        print(json.dumps(cats, indent=2, ensure_ascii=False))
    else:
        for cat, count in cats.items():
            print(f"  {cat:<30} ({count} endpoints)")
    return 0


def _cmd_search(args) -> int:
    matches = discovery.search_calls(args.query, category=args.category)
    if not matches:
        _err(f"No endpoints found matching '{args.query}'.")
        _err("Try: price, consumption, generation, dam, idm, bpm")
        return 1
    if args.format == "json":
        print(json.dumps(matches, indent=2, ensure_ascii=False))
    else:
        print(discovery.format_calls_table(matches))
    return 0


def _cmd_describe(args) -> int:
    d = discovery.describe_call(args.key)
    if d is None:
        _err(f"Unknown call key '{args.key}'.")
        suggestions = discovery.search_calls(args.key)
        if suggestions:
            _err("Did you mean: " + ", ".join(sorted(suggestions)[:10]))
        return 1
    if args.format == "json":
        print(json.dumps(d, indent=2, ensure_ascii=False, default=str))
    else:
        help_d = d.get("help") or {}
        title = (help_d.get("title") or {}).get("en") or d["key"]
        print(f"{d['key']}: {title}")
        if d.get("alias_of"):
            print(f"  (alias '{d['alias_of']['alias']}' resolves to '{d['key']}')")
        print(f"  Category: {help_d.get('category')}")
        desc = (help_d.get("desc") or {}).get("en")
        if desc:
            print(f"  Description: {desc}")
        print(f"  Method: {d.get('call_method')}")
        print(f"  Path: {d.get('call_path')}")
        print(f"  Required params: {d.get('required_body_params') or []}")
        print(f"  Optional params: {d.get('optional_body_params') or []}")
        if help_d.get("url"):
            print(f"  URL: {help_d['url']}")
        print(f"\nExample: eptr2 call {d['key']}"
              + "".join(f" --{p.replace('_', '-')} <value>"
                        for p in (d.get("required_body_params") or [])
                        if p in ("start_date", "end_date")))
    return 0


def _serialize_records(result, fmt: str) -> str:
    """Serialize a call result (DataFrame, list or dict) to json/csv text."""
    if hasattr(result, "to_json"):  # pandas DataFrame
        if fmt == "csv":
            return result.to_csv(index=False)
        return result.to_json(orient="records", date_format="iso", indent=2)
    if fmt == "csv":
        import csv
        import io

        records = result if isinstance(result, list) else [result]
        if not records:
            return ""
        if not all(isinstance(r, dict) for r in records):
            raise ValueError("Result is not tabular; use --format json instead.")
        fieldnames = list(dict.fromkeys(k for r in records for k in r))
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
        return buf.getvalue()
    return json.dumps(result, indent=2, ensure_ascii=False, default=str)


def _cmd_call(args) -> int:
    from eptr2 import EPTR2

    params = {}
    if args.start_date:
        params["start_date"] = args.start_date
    if args.end_date:
        params["end_date"] = args.end_date
    for item in args.param or []:
        if "=" not in item:
            _err(f"Invalid --param '{item}', expected key=value.")
            return 2
        k, v = item.split("=", 1)
        params[k] = v

    try:
        client = EPTR2(
            use_dotenv=not args.no_dotenv,
            dotenv_path=args.dotenv_path,
            recycle_tgt=True,
        )
        result = client.call(args.key, **params)
    except Exception as e:
        _err(f"Call failed: {e}")
        return 1

    try:
        text = _serialize_records(result, args.format)
    except ValueError as e:
        _err(str(e))
        return 1

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        _err(f"Written to {args.output}")
    else:
        print(text)
    return 0


def _cmd_schema(args) -> int:
    from pathlib import Path

    from eptr2.agentic import schema as schema_mod

    if args.stdout:
        sys.stdout.write(schema_mod.schema_json())
        return 0

    if args.check:
        targets = [args.output] if args.output else _default_schema_targets()
        stale = [str(p) for p in targets if not schema_mod.check_schema(p)]
        if stale:
            _err("Stale schema file(s): " + ", ".join(stale))
            _err("Regenerate with: eptr2 schema")
            return 1
        _err("Schema files are up to date.")
        return 0

    targets = [Path(args.output)] if args.output else _default_schema_targets()
    for p in targets:
        schema_mod.write_schema(p)
        _err(f"Written {p}")
    return 0


def _default_schema_targets():
    """Repo-root and packaged schema copies when run from a source checkout,
    else a single eptr2_api_schema.json in the current directory."""
    from pathlib import Path

    cwd = Path.cwd()
    assets = cwd / "src" / "eptr2" / "assets"
    if assets.is_dir():
        return [cwd / "eptr2_api_schema.json", assets / "eptr2_api_schema.json"]
    return [cwd / "eptr2_api_schema.json"]


def _cmd_install_skills(args) -> int:
    from eptr2.agentic import skills as skills_mod

    if args.list:
        for name in skills_mod.list_bundled_skills():
            print(name)
        return 0

    try:
        installed = skills_mod.install_skills(
            skills_mod.resolve_dest(args.dest),
            skills=args.only or None,
            force=args.force,
        )
    except ValueError as e:
        _err(str(e))
        return 1

    dest = skills_mod.resolve_dest(args.dest)
    if installed:
        _err(f"Installed {len(installed)} skill(s) to {dest}:")
        for p in installed:
            _err(f"  {p.name}")
    else:
        _err(f"Nothing installed (skills already present in {dest}; use --force to overwrite).")
    return 0


MCP_CLIENT_NOTES = {
    "claude-desktop": "Add to claude_desktop_config.json (Settings > Developer > Edit Config).",
    "claude-code": "Or run: claude mcp add eptr2 -e EPTR_USERNAME=... -e EPTR_PASSWORD=... -- eptr2-mcp-server",
    "cursor": "Add to .cursor/mcp.json (project) or ~/.cursor/mcp.json (global).",
    "vscode": "Add to .vscode/mcp.json (workspace) or use MCP: Add Server. VS Code also reads AGENTS.md natively.",
    "generic": "Standard stdio MCP server config; adapt the wrapper key to your client.",
}


def _cmd_mcp_config(args) -> int:
    server = {
        "command": "eptr2-mcp-server",
        "args": [],
        "env": {
            "EPTR_USERNAME": "your.email@example.com",
            "EPTR_PASSWORD": "your-password",
        },
    }
    if args.client == "vscode":
        config = {"servers": {"eptr2": {"type": "stdio", **server}}}
    else:
        config = {"mcpServers": {"eptr2": server}}
    _err(f"# {MCP_CLIENT_NOTES[args.client]}")
    _err("# Replace the EPTR_USERNAME/EPTR_PASSWORD placeholders with your EPIAS")
    _err("# Transparency credentials (most clients do not expand ${VAR} syntax).")
    print(json.dumps(config, indent=2))
    return 0


def _cmd_plugin_path(args) -> int:
    from eptr2.agentic import skills as skills_mod

    print(skills_mod.plugin_root())
    return 0


def _cmd_install_plugin(args) -> int:
    from eptr2.agentic import skills as skills_mod

    try:
        dest = skills_mod.install_plugin(args.dest, force=args.force)
    except FileExistsError as e:
        _err(str(e))
        return 1
    _err(f"Installed Agent Plugin to {dest}")
    return 0


def _cmd_mcp_server(args) -> int:
    from eptr2.mcp.server import main as mcp_main

    mcp_main()
    return 0


def _cmd_version(args) -> int:
    from eptr2 import __version__

    print(__version__)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="eptr2",
        description="eptr2 CLI: EPIAS Transparency Platform data for humans and AI agents.",
    )
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("list", help="List all API call keys (optionally by category)")
    p.add_argument("--category", help="Filter by category, e.g. GÖP, GİP, DGP")
    p.add_argument("--format", choices=["table", "json"], default="table")
    p.set_defaults(func=_cmd_list)

    p = sub.add_parser("categories", help="List endpoint categories with counts")
    p.add_argument("--format", choices=["table", "json"], default="table")
    p.set_defaults(func=_cmd_categories)

    p = sub.add_parser("search", help="Search endpoints by keyword (EN/TR)")
    p.add_argument("query")
    p.add_argument("--category", help="Restrict search to a category")
    p.add_argument("--format", choices=["table", "json"], default="table")
    p.set_defaults(func=_cmd_search)

    p = sub.add_parser("describe", help="Show parameters and metadata for a call key")
    p.add_argument("key")
    p.add_argument("--format", choices=["text", "json"], default="text")
    p.set_defaults(func=_cmd_describe)

    p = sub.add_parser("call", help="Call an API endpoint (requires credentials)")
    p.add_argument("key")
    p.add_argument("--start-date", help="YYYY-MM-DD")
    p.add_argument("--end-date", help="YYYY-MM-DD")
    p.add_argument(
        "-p",
        "--param",
        action="append",
        metavar="KEY=VALUE",
        help="Additional call parameter (repeatable)",
    )
    p.add_argument("--format", choices=["json", "csv"], default="json")
    p.add_argument("--output", help="Write result to file instead of stdout")
    p.add_argument("--no-dotenv", action="store_true", help="Do not read a .env file")
    p.add_argument("--dotenv-path", default=".env")
    p.set_defaults(func=_cmd_call)

    p = sub.add_parser("schema", help="Generate or check the machine-readable API schema")
    p.add_argument("--output", help="Write to a specific path")
    p.add_argument("--check", action="store_true", help="Verify committed schema is fresh")
    p.add_argument("--stdout", action="store_true", help="Print schema JSON to stdout")
    p.set_defaults(func=_cmd_schema)

    p = sub.add_parser("install-skills", help="Install bundled agent skills (SKILL.md format)")
    p.add_argument(
        "--dest",
        default="project",
        help="'user' (~/.claude/skills), 'project' (./.claude/skills) or a path",
    )
    p.add_argument("--list", action="store_true", help="List bundled skills and exit")
    p.add_argument("--only", action="append", metavar="SKILL", help="Install only these skills")
    p.add_argument("--force", action="store_true", help="Overwrite existing skill directories")
    p.set_defaults(func=_cmd_install_skills)

    p = sub.add_parser(
        "plugin-path",
        help="Print the path of the bundled Agent Plugin (agent-plugins.org format)",
    )
    p.set_defaults(func=_cmd_plugin_path)

    p = sub.add_parser(
        "install-plugin",
        help="Copy the bundled Agent Plugin (plugin.json, mcp.json, skills/) to a directory",
    )
    p.add_argument("--dest", required=True, help="Target directory for the plugin")
    p.add_argument("--force", action="store_true", help="Overwrite an existing directory")
    p.set_defaults(func=_cmd_install_plugin)

    p = sub.add_parser("mcp-config", help="Print MCP client configuration for eptr2")
    p.add_argument(
        "--client",
        choices=sorted(MCP_CLIENT_NOTES),
        default="generic",
    )
    p.set_defaults(func=_cmd_mcp_config)

    p = sub.add_parser("mcp-server", help="Run the eptr2 MCP server (stdio)")
    p.set_defaults(func=_cmd_mcp_server)

    p = sub.add_parser("version", help="Print the eptr2 version")
    p.set_defaults(func=_cmd_version)

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
