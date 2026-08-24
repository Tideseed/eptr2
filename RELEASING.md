# Releasing eptr2

Maintainer checklist for publishing to PyPI. Docs deployment is separate (see below).

## 1. Prepare

```bash
# Set the version in pyproject.toml, then regenerate the API schema,
# which embeds the version string:
uv run --extra allextras eptr2 schema

# Full offline test suite (use --extra allextras, or MCP tests silently skip)
uv run --extra allextras pytest tests/ -m "not integration and not api_call" -q
```

Also update the changelog entry for the release. Note `CHANGELOG.md` uses **CRLF**
line endings and is auto-synced from GitHub Releases by
`.github/workflows/changelog.yml` — preserve the line endings when editing by hand.

## 2. Build

```bash
rm -rf dist
uv build --build-constraints build-constraints.txt
```

The `build-constraints.txt` pin is required: newer hatchling emits
`Metadata-Version: 2.5`, which current twine rejects. See that file for details.

Verify the agentic assets made it into the wheel:

```bash
unzip -l dist/eptr2-*-py3-none-any.whl | grep -E "assets/(skills|plugin.json|mcp.json|eptr2_api_schema)"
```

## 3. Upload

```bash
uvx --from 'twine>=6.1' twine upload dist/*
```

Requires a PyPI API token in `~/.pypirc` (`username = __token__`,
`password = pypi-...`). A `403 Forbidden` almost always means an expired,
wrongly scoped, or non-token credential.

## 4. Verify

```bash
# Dev/pre-releases need --pre; stable releases do not
uv venv /tmp/eptr2check && VIRTUAL_ENV=/tmp/eptr2check uv pip install --pre "eptr2[allextras]"
/tmp/eptr2check/bin/eptr2 version
/tmp/eptr2check/bin/eptr2 plugin-path
```

## 5. Deploy the docs site

The docs workflow triggers on pushes to the **`docs`** branch (not `main`):

```bash
git branch -f docs <release-branch> && git push origin docs
```

`mike` deploys the version read from `pyproject.toml` and moves the `latest` alias.
A brand-new branch does not trigger the workflow's `paths` filter — if nothing runs,
push another commit that touches `docs/**`, `mkdocs.yml`, or `src/eptr2/**`.
