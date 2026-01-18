# Contributing

Thank you for your interest in contributing to eptr2! This guide will help you get started.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- uv or pip

### Development Setup

1. Fork the repository on GitHub

2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/eptr2.git
   cd eptr2
   ```

3. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate  # Windows
   ```

4. Install development dependencies:
   ```bash
   pip install -e ".[dev,allextras]"
   ```

5. Set up credentials:
   ```bash
   cp .env.example .env
   # Edit .env with your EPIAS credentials
   ```

## Development Workflow

### Running Tests

```bash
pytest
```

Run specific tests:

```bash
pytest tests/test_costs.py -v
```

### Code Style

We follow PEP 8 with some modifications. Use ruff for linting:

```bash
ruff check src/
```

### Type Hints

Use type hints for all public functions:

```python
def get_data(start_date: str, end_date: str) -> pd.DataFrame:
    ...
```

## Making Changes

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

### Commit Messages

Follow conventional commits:

```
type(scope): description

feat(composite): add new consumption function
fix(auth): handle expired TGT correctly
docs(api): update EPTR2 class documentation
```

### Pull Request Process

1. Create a feature branch:
   ```bash
   git checkout -b feature/my-feature
   ```

2. Make your changes and commit:
   ```bash
   git add .
   git commit -m "feat(scope): description"
   ```

3. Push to your fork:
   ```bash
   git push origin feature/my-feature
   ```

4. Open a Pull Request on GitHub

5. Wait for review and address feedback

## Adding New API Endpoints

### 1. Update Mapping

Add the new endpoint to `src/eptr2/mapping/`:

```python
# In path_map.py or similar
"new-endpoint": {
    "path": "/api/v2/new-endpoint",
    "method": "GET",
    "required_params": ["start_date", "end_date"],
}
```

### 2. Add Help Documentation

Update `src/eptr2/mapping/help.py`:

```python
"new-endpoint": {
    "category": "Category",
    "title": {"tr": "Türkçe Başlık", "en": "English Title"},
    "desc": {"tr": "Açıklama", "en": "Description"},
    "url": "https://seffaflik.epias.com.tr/..."
}
```

### 3. Add Tests

Create tests in `tests/`:

```python
def test_new_endpoint():
    eptr = EPTR2(use_dotenv=True)
    result = eptr.call("new-endpoint", start_date="2024-01-01", end_date="2024-01-01")
    assert not result.empty
```

## Documentation

### Building Docs Locally

```bash
pip install mkdocs-material mkdocstrings[python]
mkdocs serve
```

Visit `http://localhost:8000` to preview.

### Documentation Style

- Use clear, concise language
- Include code examples
- Add type hints in docstrings
- Cross-reference related topics

### Docstring Format

Use Google-style docstrings:

```python
def function(param1: str, param2: int) -> pd.DataFrame:
    """Short description.

    Longer description if needed.

    Args:
        param1: Description of param1.
        param2: Description of param2.

    Returns:
        Description of return value.

    Raises:
        ValueError: When something is wrong.

    Example:
        >>> result = function("test", 123)
        >>> print(result)
    """
```

## Reporting Issues

### Bug Reports

Include:
- eptr2 version
- Python version
- Operating system
- Minimal reproducible example
- Expected vs actual behavior
- Full error traceback

### Feature Requests

Include:
- Use case description
- Proposed solution
- Alternative solutions considered

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn

## Questions?

- Open a GitHub Issue
- Check existing issues first
- Provide context and examples

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

## See Also

- [GitHub Repository](https://github.com/Tideseed/eptr2)
- [Issue Tracker](https://github.com/Tideseed/eptr2/issues)
