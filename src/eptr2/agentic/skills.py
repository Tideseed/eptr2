"""Installer for the agent skills bundled with the eptr2 package.

Skills follow the provider-agnostic Agent Skills format (a directory with a
``SKILL.md`` file plus optional references/scripts) and can be consumed by
any compatible agent runtime.
"""

import shutil
from importlib.resources import files
from pathlib import Path
from typing import Optional, Union


def plugin_root() -> Path:
    """Root of the bundled Agent Plugin (https://agent-plugins.org):
    the packaged assets directory containing plugin.json, mcp.json and
    skills/."""
    return Path(str(files("eptr2.assets")))


def install_plugin(dest: Union[str, Path], force: bool = False) -> Path:
    """Copy the bundled Agent Plugin (plugin.json, mcp.json, skills/) into
    ``dest``. Refuses to overwrite an existing directory unless ``force``."""
    root = plugin_root()
    dest_path = Path(dest)
    if dest_path.exists():
        if not force:
            raise FileExistsError(
                f"{dest_path} already exists; use force=True to overwrite."
            )
        shutil.rmtree(dest_path)
    dest_path.mkdir(parents=True)
    for name in ("plugin.json", "mcp.json"):
        shutil.copy2(root / name, dest_path / name)
    shutil.copytree(root / "skills", dest_path / "skills")
    return dest_path


def _bundled_skills_root() -> Path:
    return plugin_root() / "skills"


def list_bundled_skills() -> list[str]:
    """Names of the skill directories bundled with the package."""
    root = _bundled_skills_root()
    if not root.is_dir():
        return []
    return sorted(p.name for p in root.iterdir() if p.is_dir())


def resolve_dest(target: Union[str, Path]) -> Path:
    """Resolve an install destination.

    "user" -> ~/.claude/skills (a common agent-skills location),
    "project" -> ./.claude/skills, anything else is used as a path as-is.
    """
    if target == "user":
        return Path.home() / ".claude" / "skills"
    if target == "project":
        return Path.cwd() / ".claude" / "skills"
    return Path(target)


def install_skills(
    dest: Union[str, Path],
    skills: Optional[list[str]] = None,
    force: bool = False,
) -> list[Path]:
    """Copy bundled skills into ``dest`` (created if missing).

    Existing skill directories are skipped unless ``force`` is True.
    Returns the list of installed skill paths.
    """
    root = _bundled_skills_root()
    available = list_bundled_skills()
    if skills is None:
        selected = available
    else:
        unknown = sorted(set(skills) - set(available))
        if unknown:
            raise ValueError(
                f"Unknown skill(s): {', '.join(unknown)}. "
                f"Available: {', '.join(available)}"
            )
        selected = skills

    dest_path = resolve_dest(dest)
    dest_path.mkdir(parents=True, exist_ok=True)

    installed = []
    for name in selected:
        target = dest_path / name
        if target.exists():
            if not force:
                continue
            shutil.rmtree(target)
        shutil.copytree(root / name, target)
        installed.append(target)
    return installed
