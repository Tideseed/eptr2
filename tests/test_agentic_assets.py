"""Offline tests for bundled agent skills: repo/package sync, format
validity, and the installer."""

from pathlib import Path

import pytest

from eptr2.agentic import skills as skills_mod

REPO_ROOT = Path(__file__).resolve().parents[1]
CANONICAL = REPO_ROOT / "src" / "eptr2" / "assets" / "skills"
REPO_COPY = REPO_ROOT / ".claude" / "skills"


def _tree(root: Path) -> dict[str, bytes]:
    return {
        str(p.relative_to(root)): p.read_bytes()
        for p in sorted(root.rglob("*"))
        if p.is_file() and "__pycache__" not in p.parts
    }


def test_skills_in_sync():
    """Canonical (src/eptr2/assets/skills) and repo (.claude/skills) copies
    must be identical. If this fails, edit the canonical copy and run:
    python scripts/sync_agentic_assets.py
    """
    canonical = _tree(CANONICAL)
    repo = _tree(REPO_COPY)
    assert canonical.keys() == repo.keys(), (
        "skill trees differ — run python scripts/sync_agentic_assets.py"
    )
    for rel, content in canonical.items():
        assert content == repo[rel], (
            f"{rel} differs — run python scripts/sync_agentic_assets.py"
        )


def test_every_skill_has_valid_skill_md():
    skill_dirs = [p for p in CANONICAL.iterdir() if p.is_dir()]
    assert len(skill_dirs) == 7
    for d in skill_dirs:
        names = [f.name for f in d.iterdir()]
        assert "SKILL.md" in names, f"{d.name} missing uppercase SKILL.md"
        text = (d / "SKILL.md").read_text(encoding="utf-8")
        assert text.startswith("---"), f"{d.name} SKILL.md missing frontmatter"
        frontmatter = text.split("---")[1]
        assert "name:" in frontmatter, d.name
        assert "description:" in frontmatter, d.name


def test_list_bundled_skills():
    bundled = skills_mod.list_bundled_skills()
    assert len(bundled) == 7
    assert "eptr2-api-discovery" in bundled


def test_install_skills_copies_all(tmp_path):
    installed = skills_mod.install_skills(tmp_path)
    assert len(installed) == 7
    assert (tmp_path / "eptr2-api-discovery" / "SKILL.md").exists()


def test_install_skills_skips_existing_without_force(tmp_path):
    skills_mod.install_skills(tmp_path)
    marker = tmp_path / "eptr2-api-discovery" / "marker.txt"
    marker.write_text("keep")
    installed = skills_mod.install_skills(tmp_path)
    assert installed == []
    assert marker.exists()


def test_install_skills_force_overwrites(tmp_path):
    skills_mod.install_skills(tmp_path)
    marker = tmp_path / "eptr2-api-discovery" / "marker.txt"
    marker.write_text("stale")
    installed = skills_mod.install_skills(tmp_path, force=True)
    assert len(installed) == 7
    assert not marker.exists()


def test_install_skills_subset_and_unknown(tmp_path):
    installed = skills_mod.install_skills(tmp_path, skills=["eptr2-price-analysis"])
    assert [p.name for p in installed] == ["eptr2-price-analysis"]
    with pytest.raises(ValueError, match="Unknown skill"):
        skills_mod.install_skills(tmp_path, skills=["nope"])


def test_resolve_dest():
    assert skills_mod.resolve_dest("user") == Path.home() / ".claude" / "skills"
    assert skills_mod.resolve_dest("project") == Path.cwd() / ".claude" / "skills"
    assert skills_mod.resolve_dest("/x/y") == Path("/x/y")
