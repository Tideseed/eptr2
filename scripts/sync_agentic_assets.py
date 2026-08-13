#!/usr/bin/env python3
"""Sync canonical agentic assets to their repo-local copies.

Canonical sources (shipped in the pip package):
    src/eptr2/assets/skills/            -> .claude/skills/
    src/eptr2/assets/eptr2_api_schema.json -> eptr2_api_schema.json (repo root)

Edit the canonical copies, then run this script from the repo root:
    python scripts/sync_agentic_assets.py
"""

import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CANONICAL_SKILLS = REPO_ROOT / "src" / "eptr2" / "assets" / "skills"
REPO_SKILLS = REPO_ROOT / ".claude" / "skills"
CANONICAL_SCHEMA = REPO_ROOT / "src" / "eptr2" / "assets" / "eptr2_api_schema.json"
ROOT_SCHEMA = REPO_ROOT / "eptr2_api_schema.json"


def main() -> int:
    if not CANONICAL_SKILLS.is_dir():
        print(f"Canonical skills dir missing: {CANONICAL_SKILLS}", file=sys.stderr)
        return 1

    if REPO_SKILLS.exists():
        shutil.rmtree(REPO_SKILLS)
    shutil.copytree(CANONICAL_SKILLS, REPO_SKILLS)
    print(f"Synced skills -> {REPO_SKILLS}")

    if CANONICAL_SCHEMA.exists():
        shutil.copy2(CANONICAL_SCHEMA, ROOT_SCHEMA)
        print(f"Synced schema -> {ROOT_SCHEMA}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
