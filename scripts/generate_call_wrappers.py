"""Generate ``get_*`` convenience wrappers for every eptr2 endpoint.

The generated files under ``src/eptr2/calls/`` are checked in and edited like
hand-written code. Re-run this script after adding/removing endpoints in
``src/eptr2/mapping/path.py`` or changing parameters in
``src/eptr2/mapping/parameters.py``.

Usage:
    python scripts/generate_call_wrappers.py
"""

from __future__ import annotations

from pathlib import Path

from eptr2.mapping import get_path_map
from eptr2.mapping.parameters import get_required_parameters, get_optional_parameters
from eptr2.mapping.path import get_alias_map
from eptr2.mapping.help import get_help_d


# (root, prev) -> module filename (without .py)
GROUP_TO_MODULE = {
    ("natural-gas", "general-data"): "ng_general",
    ("natural-gas", "sgp"): "ng_sgp",
    ("natural-gas", "transmission"): "ng_transmission",
    ("natural-gas", "vgp"): "ng_vgp",
    (None, "ancillary-services"): "ancillary",
    (None, "bilateral-contracts"): "bilateral",
    (None, "bpm"): "bpm",
    (None, "consumption"): "consumption",
    (None, "dam"): "dam",
    (None, "dams"): "dams",
    (None, "electricity-service"): "general",
    (None, "general-data"): "general",  # merged with electricity-service
    (None, "generation"): "generation",
    (None, "idm"): "idm",
    (None, "imbalance"): "imbalance",
    (None, "markets"): "mms",
    (None, "pfm"): "vep",
    (None, "renewables"): "renewables",
    (None, "reporting-service"): "reporting",
    (None, "retroactive-adjustment"): "retroactive",
    (None, "transmission"): "transmission",
    (None, "yek-g"): "yek_g",
}


# Explicit per-parameter type hints. Anything not listed falls back to
# ``DEFAULT_PARAM_TYPE`` via :func:`param_type`.
PARAM_TYPES: dict[str, str] = {
    # Date / time
    "start_date": "str",
    "end_date": "str",
    "date": "str",
    "date_time": "str",
    "period": "str",
    "period_start_date": "str",
    "period_end_date": "str",
    "version_start_date": "str",
    "version_end_date": "str",
    "delivery_period": "str",
    "delivery_year": "str | int",
    "year": "str | int",
    # IDs (API accepts both str and int)
    "org_id": "str | int",
    "imb_org_id": "str | int",
    "pp_id": "str | int",
    "uevcb_id": "str | int",
    "region_id": "str | int",
    "province_id": "str | int",
    "message_type_id": "str | int",
    "idm_contract_id": "str | int",
    "dist_org_id": "str | int",
    "profile_group_id": "str | int",
    "distribution_id": "str | int",
    "mr_org_id": "str | int",
    "storage_facility_id": "str | int",
    "point_id": "str | int",
    "menu_id": "str | int",
    "tariff_group_id": "str | int",
    "dist_company_id": "str | int",
    # Plural id lists
    "uevcb_ids": "list",
    "pp_ids": "list",
    "org_ids": "list",
    # Booleans
    "is_txn_period": "bool",
    # Free-form strings
    "region": "str",
    "intl_direction": "str",
    "price_type": "str",
    "order_type": "str",
    "uevcb_name": "str",
    "basin_name": "str",
    "dam_name": "str",
    "spg_name": "str",
    "district_name": "str",
    "pg_name": "str",
    "point_type": "str",
    "load_type": "str",
    "mr_type": "str",
    "subscriber_pg": "str",
}
DEFAULT_PARAM_TYPE = "str"


def param_type(name: str) -> str:
    if name in PARAM_TYPES:
        return PARAM_TYPES[name]
    if name.endswith("_ids"):
        return "list"
    if name.endswith("_id"):
        return "str | int"
    if name.startswith("is_"):
        return "bool"
    if name.endswith("_name"):
        return "str"
    return DEFAULT_PARAM_TYPE


def func_name(key: str) -> str:
    return "get_" + key.replace("-", "_")


def render_docstring(call_key: str, indent: str = "    ") -> str:
    """Render a bilingual docstring block from :func:`get_help_d` metadata.

    Returns an empty string if no help entry exists for ``call_key``.
    """
    h = get_help_d(call_key)
    if not h:
        return ""

    title = h.get("title") or {}
    desc = h.get("desc") or {}
    category = h.get("category")
    url = h.get("url")

    title_en = (title.get("en") or "").strip()
    title_tr = (title.get("tr") or "").strip()
    desc_en = (desc.get("en") or "").strip()
    desc_tr = (desc.get("tr") or "").strip()

    if title_en and title_tr:
        summary = f"{title_en} / {title_tr}"
    else:
        summary = title_en or title_tr or call_key

    def _sanitize(text: str) -> str:
        # Avoid breaking the triple-quoted docstring.
        return text.replace('"""', "'''")

    lines: list[str] = [_sanitize(summary), ""]
    if category:
        lines.append(f"Category: {_sanitize(category)}")
        lines.append("")
    if title_en or desc_en:
        if title_en:
            lines.append(f"EN ({_sanitize(title_en)}):")
        else:
            lines.append("EN:")
        if desc_en:
            lines.append(f"    {_sanitize(desc_en)}")
        lines.append("")
    if title_tr or desc_tr:
        if title_tr:
            lines.append(f"TR ({_sanitize(title_tr)}):")
        else:
            lines.append("TR:")
        if desc_tr:
            lines.append(f"    {_sanitize(desc_tr)}")
        lines.append("")
    if url:
        lines.append(f"Reference: {url}")

    # Trim trailing blank lines.
    while lines and lines[-1] == "":
        lines.pop()

    body = "\n".join(f"{indent}{ln}".rstrip() for ln in lines)
    return f'{indent}"""' + body[len(indent) :] + f'\n{indent}"""\n'


def render_function(call_key: str, params_key: str | None = None) -> str:
    """Render a wrapper function for ``call_key``, sourcing parameters from
    ``params_key`` (defaults to ``call_key``). Aliases pass the canonical key
    as ``params_key`` so signatures stay consistent.
    """
    if params_key is None:
        params_key = call_key
    required = list(get_required_parameters(params_key) or [])
    optional = [
        p for p in (get_optional_parameters(params_key) or []) if p not in required
    ]

    params: list[str] = []
    params += [f"{p}: {param_type(p)}" for p in required]
    params += [f"{p}: {param_type(p)} | None = None" for p in optional]
    params.append("eptr: EPTR2 | None = None")
    params.append("**kwargs")
    sig = ", ".join(params)

    call_kwargs_parts = [f'"{call_key}"']
    for p in required + optional:
        call_kwargs_parts.append(f"{p}={p}")
    call_kwargs_parts.append("**kwargs")
    call_kwargs = ", ".join(call_kwargs_parts)

    docstring = render_docstring(call_key)

    return (
        f"def {func_name(call_key)}({sig}):\n"
        f"{docstring}"
        f"    if eptr is None:\n"
        f"        eptr = EPTR2()\n"
        f"    return eptr.call({call_kwargs})\n"
    )


def render_module(
    module: str, keys: list[str], aliases_in_module: dict[str, str]
) -> str:
    header = (
        '"""Auto-generated convenience wrappers. See scripts/generate_call_wrappers.py."""\n'
        "from __future__ import annotations\n\n"
        "from eptr2.main import EPTR2\n\n"
    )

    public_names = [func_name(k) for k in keys]
    public_names += [func_name(a) for a in aliases_in_module]

    all_decl = (
        "__all__ = [\n" + "".join(f'    "{n}",\n' for n in public_names) + "]\n\n"
    )

    body_parts: list[str] = []
    for k in keys:
        body_parts.append(render_function(k))
    for alias_key, canonical_key in aliases_in_module.items():
        # Alias keeps its own call key (so ``eptr.call`` resolves it via the
        # alias map) but reuses the canonical signature.
        body_parts.append(render_function(alias_key, params_key=canonical_key))

    return header + all_decl + "\n\n".join(body_parts) + "\n"


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    out_dir = repo_root / "src" / "eptr2" / "calls"
    out_dir.mkdir(parents=True, exist_ok=True)

    full = get_path_map()
    keys = get_path_map(just_call_keys=True)
    aliases = get_alias_map()  # alias_key -> canonical_key

    # Group keys by module via (root, prev).
    module_keys: dict[str, list[str]] = {}
    for k in keys:
        v = full.get(k, {})
        prev = v.get("prev")
        root = v.get("root")
        module = GROUP_TO_MODULE.get((root, prev))
        if module is None:
            raise SystemExit(
                f"No module mapping for key {k!r} (root={root!r}, prev={prev!r})"
            )
        module_keys.setdefault(module, []).append(k)

    # Place each alias in the same module as its canonical target.
    module_aliases: dict[str, dict[str, str]] = {}
    for alias_key, canonical_key in aliases.items():
        # find module of canonical
        target_module = None
        for module, ks in module_keys.items():
            if canonical_key in ks:
                target_module = module
                break
        if target_module is None:
            raise SystemExit(f"Alias target {canonical_key!r} not found in any module")
        module_aliases.setdefault(target_module, {})[alias_key] = canonical_key

    # Remove stale .py files we previously generated. Keep __init__.py and
    # anything we don't own.
    owned_modules = set(module_keys.keys())
    for f in out_dir.glob("*.py"):
        if f.name == "__init__.py":
            continue
        if f.stem not in owned_modules and f.name != "market.py":
            # leave alone
            continue

    # Write modules.
    written = []
    for module, ks in sorted(module_keys.items()):
        ks_sorted = sorted(ks)
        aliases_for_module = module_aliases.get(module, {})
        text = render_module(module, ks_sorted, aliases_for_module)
        path = out_dir / f"{module}.py"
        path.write_text(text, encoding="utf-8")
        written.append(module)

    # Remove the legacy market.py (superseded by dam.py).
    legacy = out_dir / "market.py"
    if legacy.exists():
        legacy.unlink()

    # Write __init__.py that re-exports everything.
    init_lines = [
        '"""Convenience ``get_*`` wrappers over :meth:`EPTR2.call`."""',
        "from __future__ import annotations",
        "",
    ]
    all_names: list[str] = []
    for module in sorted(written):
        init_lines.append(f"from eptr2.calls.{module} import *  # noqa: F401,F403")
        # Reimport just to collect __all__ for the package-level __all__.
        ns: dict = {}
        exec((out_dir / f"{module}.py").read_text(encoding="utf-8"), ns)
        all_names.extend(ns.get("__all__", []))

    init_lines.append("")
    init_lines.append("__all__ = [")
    for n in sorted(set(all_names)):
        init_lines.append(f'    "{n}",')
    init_lines.append("]")
    init_lines.append("")
    (out_dir / "__init__.py").write_text("\n".join(init_lines), encoding="utf-8")

    print(f"Wrote {len(written)} modules, {len(all_names)} wrappers to {out_dir}")


if __name__ == "__main__":
    main()
