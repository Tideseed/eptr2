"""Offline tests for bundled agent skills: repo/package sync, format
validity, and the installer."""

from pathlib import Path

import pytest

from eptr2.agentic import skills as skills_mod

REPO_ROOT = Path(__file__).resolve().parents[1]
CANONICAL = REPO_ROOT / "src" / "eptr2" / "assets" / "skills"
REPO_COPY = REPO_ROOT / ".agents" / "skills"


def _tree(root: Path) -> dict[str, bytes]:
    return {
        str(p.relative_to(root)): p.read_bytes()
        for p in sorted(root.rglob("*"))
        if p.is_file() and "__pycache__" not in p.parts
    }


def test_skills_in_sync():
    """Canonical (src/eptr2/assets/skills) and repo (.agents/skills) copies
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
    assert skills_mod.resolve_dest("user") == Path.home() / ".agents" / "skills"
    assert skills_mod.resolve_dest("project") == Path.cwd() / ".agents" / "skills"
    assert skills_mod.resolve_dest("/x/y") == Path("/x/y")


@pytest.mark.parametrize("client,directory", [("generic", ".agents"), ("claude", ".claude")])
@pytest.mark.parametrize("scope", ["project", "user"])
def test_install_scoped_skills(tmp_path, monkeypatch, client, directory, scope):
    project = tmp_path / "project"
    home = tmp_path / "home"
    project.mkdir()
    home.mkdir()
    monkeypatch.chdir(project)
    monkeypatch.setattr(Path, "home", lambda: home)
    root = project if scope == "project" else home
    installed = skills_mod.install_skills(scope, client=client)
    assert len(installed) == 7
    assert all(p.parent == root / directory / "skills" for p in installed)
    assert not (root / (".claude" if client == "generic" else ".agents")).exists()


def test_explicit_skill_path_wins_and_expands_home(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    assert skills_mod.resolve_dest("~/custom-skills", client="claude") == tmp_path / "custom-skills"
    dest = tmp_path / "explicit"
    assert skills_mod.install_skills(dest, client="claude")[0].parent == dest
    with pytest.raises(ValueError, match="client"):
        skills_mod.resolve_dest("project", client="unknown")


def test_sync_preserves_unrelated_repository_skills(tmp_path, monkeypatch):
    import importlib.util

    spec = importlib.util.spec_from_file_location("sync_assets", REPO_ROOT / "scripts/sync_agentic_assets.py")
    sync = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sync)
    destination = tmp_path / ".agents/skills"
    custom = destination / "my-custom-skill/SKILL.md"
    custom.parent.mkdir(parents=True)
    custom.write_text("Keep my local instructions")
    monkeypatch.setattr(sync, "REPO_SKILLS", destination)
    monkeypatch.setattr(sync, "ROOT_SCHEMA", tmp_path / "schema.json")
    assert sync.main() == 0
    assert custom.read_text() == "Keep my local instructions"
    assert (destination / "eptr2-price-analysis/SKILL.md").read_bytes() == (CANONICAL / "eptr2-price-analysis/SKILL.md").read_bytes()


# --- Agent Plugin (https://agent-plugins.org) ---

import json
import re


def test_plugin_manifest_valid():
    manifest = json.loads((CANONICAL.parent / "plugin.json").read_text(encoding="utf-8"))
    assert manifest["$schema"] == (
        "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
    )
    # name: 1-64 chars, lowercase alphanumeric with hyphens/periods, no -- or ..
    assert re.fullmatch(
        r"(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?", manifest["name"]
    )
    assert len(manifest["name"]) <= 64
    allowed = {
        "$schema", "name", "version", "description", "author", "homepage",
        "repository", "license", "keywords", "extensions",
    }
    assert set(manifest) <= allowed
    author_allowed = {"name", "email", "url"}
    assert set(manifest.get("author", {})) <= author_allowed


def test_plugin_mcp_json_valid():
    mcp = json.loads((CANONICAL.parent / "mcp.json").read_text(encoding="utf-8"))
    assert mcp["$schema"] == "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
    server = mcp["mcpServers"]["eptr2"]
    assert server["type"] == "stdio"
    # command must be a bare name or ./ path
    assert "/" not in server["command"] or server["command"].startswith("./")


def test_plugin_root_is_valid_plugin():
    root = skills_mod.plugin_root()
    assert (root / "plugin.json").is_file()
    assert (root / "mcp.json").is_file()
    skill_dirs = [p for p in (root / "skills").iterdir() if p.is_dir()]
    assert len(skill_dirs) == 7
    for d in skill_dirs:
        assert (d / "SKILL.md").is_file()


def test_install_plugin(tmp_path):
    dest = tmp_path / "eptr2-plugin"
    installed = skills_mod.install_plugin(dest)
    assert installed == dest
    assert (dest / "plugin.json").is_file()
    assert (dest / "mcp.json").is_file()
    assert (dest / "skills" / "eptr2-price-analysis" / "SKILL.md").is_file()
    # no stray python/package files in the installed plugin
    assert not (dest / "__init__.py").exists()
    assert not (dest / "eptr2_api_schema.json").exists()

    import pytest as _pytest

    with _pytest.raises(FileExistsError):
        skills_mod.install_plugin(dest)
    assert skills_mod.install_plugin(dest, force=True) == dest
