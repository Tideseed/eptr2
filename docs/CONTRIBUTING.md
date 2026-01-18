# Documentation

This directory contains the MkDocs documentation for eptr2.

## Building Locally

### Install dependencies

```bash
pip install "eptr2[docs]"
# or
pip install mkdocs-material mkdocstrings[python] mkdocs-autorefs
```

### Serve locally

```bash
mkdocs serve
```

Visit `http://localhost:8000` to preview the documentation.

### Build static site

```bash
mkdocs build
```

The static site will be generated in the `site/` directory.

## Deployment

Documentation is automatically deployed to GitHub Pages when changes are pushed to the `main` branch.

The deployment workflow is defined in `.github/workflows/docs.yml`.

### Manual deployment

```bash
mkdocs gh-deploy
```

## Structure

```
docs/
├── index.md                    # Homepage
├── getting-started/            # Getting started guides
│   ├── installation.md
│   ├── authentication.md
│   └── quickstart.md
├── user-guide/                 # User guides
│   ├── basic-usage.md
│   ├── api-calls.md
│   ├── composite-functions.md
│   └── dataframes.md
├── ai-integration/             # AI integration docs
│   ├── mcp-server.md
│   ├── claude-desktop.md
│   └── agent-skills.md
├── api/                        # API reference
│   ├── eptr2.md
│   ├── main.md
│   ├── composite.md
│   ├── mcp.md
│   └── util.md
├── tutorials/                  # Tutorials
│   ├── demo-app.md
│   └── calculator.md
├── reference/                  # Reference docs
│   ├── abbreviations.md
│   ├── changelog.md
│   └── contributing.md
├── assets/                     # Static assets
│   └── README.md
├── stylesheets/                # Custom CSS
│   └── extra.css
├── javascripts/                # Custom JS
│   └── mathjax.js
└── includes/                   # Included snippets
    └── abbreviations.md
```

## Adding New Pages

1. Create a new `.md` file in the appropriate directory
2. Add the page to the `nav` section in `mkdocs.yml`
3. Use consistent formatting and structure

## Writing Documentation

### Style Guide

- Use clear, concise language
- Include code examples
- Add cross-references to related pages
- Use admonitions for tips, warnings, etc.

### Admonitions

```markdown
!!! note "Title"
    Note content

!!! tip "Tip"
    Tip content

!!! warning "Warning"
    Warning content
```

### Code Blocks

```markdown
```python
from eptr2 import EPTR2
eptr = EPTR2(use_dotenv=True)
```
```

### API Documentation

Use mkdocstrings to generate API docs from docstrings:

```markdown
::: eptr2.main.EPTR2
    options:
      show_root_heading: true
      show_source: true
```
