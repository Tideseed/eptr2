# CLI for Agents

The `eptr2` command-line interface makes the library usable by shell-driven AI agents and humans alike. Data goes to stdout only, diagnostics to stderr, and exit codes are nonzero on error — so output can be piped and parsed safely.

## Exit codes

| Code | Meaning |
|------|---------|
| `0` | Success; data (if any) is on stdout |
| `1` | The request was well-formed but failed — unknown call key, no results, authentication failure, or an API error |
| `2` | The request was malformed and never sent — invalid parameters, a bad `key=value` pair, or no subcommand |

Code `2` means nothing reached the network, so an agent can retry only after correcting the request; code `1` may be transient.

Installed with the package:

```bash
pip install eptr2          # CLI included; pandas optional but recommended
```

## Discovery (no credentials needed)

```bash
eptr2 list                          # all 232 call keys, grouped by category
eptr2 list --category GÖP           # one category
eptr2 list --format json            # machine-readable
eptr2 categories                    # categories with endpoint counts
eptr2 search imbalance              # keyword search (English and Turkish)
eptr2 describe mcp                  # parameters, method, path, description
eptr2 describe ptf --format json    # aliases resolve automatically
```

## Fetching Data

Requires EPIAS credentials — either a `.env` file with `EPTR_USERNAME`/`EPTR_PASSWORD` in the working directory, or the same variables in the environment.

```bash
eptr2 call mcp --start-date 2024-07-29 --end-date 2024-07-29
eptr2 call mcp --start-date 2024-07-01 --end-date 2024-07-31 --format csv --output july.csv
eptr2 call rt-gen --start-date 2024-07-29 --end-date 2024-07-29 --format csv
eptr2 call some-key -p org_id=123 -p pp_id=456     # extra parameters
```

Output is JSON records by default; `--format csv` produces CSV.

## Machine-Readable Schema

```bash
eptr2 schema --stdout               # print the full API schema as JSON
eptr2 schema                        # regenerate committed schema files (repo checkout)
eptr2 schema --check                # verify the committed schema is fresh (CI-friendly)
```

The schema covers all endpoints with parameters, plus composite functions and cost utilities. See [AGENTS.md](https://github.com/Tideseed/eptr2/blob/main/AGENTS.md) for how agents can use it.

## Agent Skills

```bash
eptr2 install-skills --list          # show bundled skills
eptr2 install-skills                 # install into ./.agents/skills
eptr2 install-skills --dest user     # install into ~/.agents/skills
eptr2 install-skills --client claude  # into ./.claude/skills
eptr2 install-skills --client claude --dest user  # into ~/.claude/skills
eptr2 install-skills --dest /path/to/skills --only eptr2-price-analysis
```

Skills use the provider-agnostic Agent Skills format (`SKILL.md`); any compatible runtime can consume them.

## MCP

```bash
eptr2 mcp-server                    # run the MCP server (stdio)
eptr2 mcp-config --client vscode    # print client config (also: claude-desktop, claude-code, cursor, generic)
```

## Python Module Form

Every command also works as a module invocation:

```bash
python -m eptr2 list
```
