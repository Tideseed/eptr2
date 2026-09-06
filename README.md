![PyPI - Version](https://img.shields.io/pypi/v/eptr2) ![PyPI - Downloads](https://img.shields.io/pypi/dm/eptr2) ![PyPI - Python Version](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Ftideseed%2Feptr2%2Fmain%2Fpyproject.toml
) ![PyPI - License](https://img.shields.io/pypi/l/eptr2)

**!! IMPORTANT: Starting from 1.3.3 there will be some breaking changes due to regulatory changes by EPDK. Overhaul is planned to finish with the next mid release 1.4.0**

**!! CRITICAL: Due to authentication method changes you are strongly recommended to update the eptr2 version to 1.2.4+**

**Note: From 1.3.0 and onwards, eptr2 starts to evolve to be an AI oriented tool. You can use it as an MCP server, directly use them in your LLMs and AI agents to write your code for you.**

# eptr2

`eptr2` (**EP**IAS **Tr**ansparency **2**.0) is a Python client for the [EPIAS Transparency Platform v2.0](https://seffaflik.epias.com.tr/home) API, covering 231 services of the Turkish electricity and natural gas markets. It is an unofficial package by [Robokami](https://robokami.com) / [Tideseed](https://tideseed.com) with Apache License 2.0.

📖 **Full documentation: <https://tideseed.github.io/eptr2/>**

+ Live demo: <https://eptr2demo.streamlit.app/> (or run `eptr2demo` locally after installing)

## Installation

Recommended (includes pandas, MCP server support and other extras):

```bash
pip install "eptr2[allextras]"
```

Minimal install (thin client only): `pip install eptr2`. Both work with `uv pip install` as well.

### Development Versions

Get the latest pre-release from PyPI (pip skips `.devN` versions unless `--pre` is given):

```bash
pip install --pre "eptr2[allextras]"
```

Or install straight from GitHub — a specific dev branch or the default branch:

```bash
pip install "eptr2[allextras] @ git+https://github.com/Tideseed/eptr2.git@dev-1.3.9"
```

```bash
pip install "eptr2[allextras] @ git+https://github.com/Tideseed/eptr2.git"
```

Pin a released version with `eptr2==1.3.8` if you need to stay off dev builds.

## Quickstart

[Register](https://kayit.epias.com.tr/epias-transparency-platform-registration-form) with the EPIAS Transparency Platform, then:

```python
from eptr2 import EPTR2

eptr = EPTR2(username="YOUR_USERNAME", password="YOUR_PASSWORD")
res = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
```

Or keep credentials in a `.env` file (`EPTR_USERNAME=...` / `EPTR_PASSWORD=...`) and reuse authentication tickets:

```python
eptr = EPTR2(use_dotenv=True, recycle_tgt=True)
df = eptr.call("mcp", start_date="2025-08-01", end_date="2025-08-31")
```

All 231 services follow the same pattern — discover them with `eptr.get_available_calls()` or `eptr2 search <keyword>` from the shell. See the docs for [installation](https://tideseed.github.io/eptr2/getting-started/installation/), [authentication](https://tideseed.github.io/eptr2/getting-started/authentication/) and [basic usage](https://tideseed.github.io/eptr2/user-guide/basic-usage/).

## AI Agents & Tooling

`eptr2` ships provider-agnostic tooling for AI assistants and agents:

- **CLI** — `eptr2 list / search / describe / call` for shell-driven agents (data on stdout, JSON or CSV)
- **MCP server** — 18 tools for any Model Context Protocol client (`eptr2-mcp-server`)
- **Agent skills** — 7 bundled skills in the open Agent Skills (SKILL.md) format: `eptr2 install-skills`
- **Agent Plugin** — skills + MCP server packaged in the portable [agent-plugins.org](https://agent-plugins.org) format: `eptr2 plugin-path`
- **Machine-readable schema** — all 231 endpoints with parameters, auto-generated: `eptr2 schema --stdout`

```bash
pip install "eptr2[allextras]"
eptr2 describe mcp                                          # discover (no credentials)
eptr2 call mcp --start-date 2024-07-29 --end-date 2024-07-29 --format csv
eptr2 mcp-config --client vscode                            # MCP config for your client
```

See [AGENTS.md](AGENTS.md) and the AI integration docs: [MCP server](https://tideseed.github.io/eptr2/ai-integration/mcp-server/) · [MCP client setup](https://tideseed.github.io/eptr2/ai-integration/mcp-clients/) · [agent skills](https://tideseed.github.io/eptr2/ai-integration/agent-skills/) · [Agent Plugin](https://tideseed.github.io/eptr2/ai-integration/agent-plugin/) · [CLI](https://tideseed.github.io/eptr2/ai-integration/cli/).

**Teaching an agent this library:** point it at [AGENTS.md](AGENTS.md) (many tools, including VS Code and Claude Code, read it automatically in this repo). Outside the repo, `eptr2 schema --stdout` emits a machine-readable description of every endpoint, and `eptr2 describe <key>` / `eptr2 search <keyword>` answer parameter questions without credentials — AGENTS.md has the full learning path.

## Going Further

| Topic | Documentation |
|-------|---------------|
| All 231 API calls, categories and parameters | [Available API Calls](https://tideseed.github.io/eptr2/user-guide/api-calls/) |
| Typed `get_*` wrapper functions (`eptr2.calls`) | [Convenience Wrappers](https://tideseed.github.io/eptr2/user-guide/convenience-wrappers/) |
| Aliases, bulk calls, DataFrames | [Basic Usage](https://tideseed.github.io/eptr2/user-guide/basic-usage/) · [DataFrames](https://tideseed.github.io/eptr2/user-guide/dataframes/) |
| Composite functions (consumption, prices/costs, production, IDM, BPM, plant costs) | [Composite Functions](https://tideseed.github.io/eptr2/user-guide/composite-functions/) |
| Imbalance / KÜPST cost calculations | [Utilities API](https://tideseed.github.io/eptr2/api/util/) |
| Streamlit demo and calculator tutorials | [Tutorials](https://tideseed.github.io/eptr2/tutorials/demo-app/) |
| Turkish market abbreviations (PTF, SMF, KGÜP, ...) | [Abbreviations](https://tideseed.github.io/eptr2/reference/abbreviations/) |
| Release history | [Changelog](https://tideseed.github.io/eptr2/reference/changelog/) |

## About

🇬🇧 `eptr2` is a thin wrapper around the EPIAS Transparency Platform v2.0 API. Free and permissible use for commercial applications with Apache License 2.0 ([details](https://www.tldrlegal.com/license/apache-license-2-0-apache-2-0)).

🇹🇷 `eptr2`, [Robokami](https://robokami.com) tarafından [EPİAŞ Şeffaflık Platformu 2.0](https://seffaflik.epias.com.tr/home) API'si üzerine geliştirilmiş bir Python paketidir. Apache License 2.0 ile lisanslanmıştır; 231 veri servisine erişim sağlar. Detaylı dokümantasyon: <https://tideseed.github.io/eptr2/>
