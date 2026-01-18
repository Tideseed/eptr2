# Authentication

eptr2 requires credentials from the [EPIAS Transparency Platform](https://seffaflik.epias.com.tr/) to access market data.

## Getting Credentials

1. Visit the [EPIAS registration page](https://kayit.epias.com.tr/epias-transparency-platform-registration-form)
2. Complete the registration form
3. Verify your email address
4. Use your registration email and password as credentials

## Authentication Methods

### Method 1: Environment File (Recommended)

Create a `.env` file in your project directory:

```env title=".env"
EPTR_USERNAME=your.email@example.com
EPTR_PASSWORD=yourpassword
```

Then initialize without explicit credentials:

```python
from eptr2 import EPTR2

eptr = EPTR2(use_dotenv=True, recycle_tgt=True)
```

!!! tip "TGT Recycling"
    Setting `recycle_tgt=True` stores the authentication ticket locally (`.eptr2-tgt` file) and reuses it until expiration. This reduces API calls and avoids rate limiting.

### Method 2: Direct Credentials

Pass credentials directly (useful for quick testing):

```python
from eptr2 import EPTR2

eptr = EPTR2(
    username="your.email@example.com",
    password="yourpassword"
)
```

!!! warning "Security"
    Never commit credentials to version control. Use environment files or environment variables instead.

### Method 3: Environment Variables

Set system environment variables:

=== "Linux/macOS"
    ```bash
    export EPTR_USERNAME="your.email@example.com"
    export EPTR_PASSWORD="yourpassword"
    ```

=== "Windows"
    ```powershell
    $env:EPTR_USERNAME = "your.email@example.com"
    $env:EPTR_PASSWORD = "yourpassword"
    ```

Then initialize:

```python
from eptr2 import EPTR2

eptr = EPTR2()  # Automatically reads from environment
```

## Configuration Options

The `EPTR2` class accepts several authentication-related options:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `username` | str | None | EPIAS platform username (email) |
| `password` | str | None | EPIAS platform password |
| `use_dotenv` | bool | True | Load credentials from `.env` file |
| `dotenv_path` | str | ".env" | Path to the `.env` file |
| `recycle_tgt` | bool | True | Reuse authentication tickets |
| `tgt_path` | str | "." | Directory to store TGT file |
| `force_renew_tgt` | bool | False | Force renewal of TGT |

## TGT (Ticket Granting Ticket) Management

eptr2 uses a ticket-based authentication system:

1. **Initial Login**: Credentials are exchanged for a TGT
2. **TGT Storage**: With `recycle_tgt=True`, the TGT is saved to `.eptr2-tgt`
3. **TGT Reuse**: Subsequent calls reuse the stored TGT
4. **Auto Renewal**: TGT is automatically renewed when expired

```python
# Custom TGT storage location
eptr = EPTR2(
    use_dotenv=True,
    recycle_tgt=True,
    tgt_path="/path/to/store/tgt"
)
```

## Best Practices

1. **Use `.env` files** - Keep credentials separate from code
2. **Enable TGT recycling** - Reduces authentication overhead
3. **Add `.env` to `.gitignore`** - Never commit credentials
4. **Use `.env.example`** - Document required variables without values

Example `.gitignore`:

```gitignore
.env
.eptr2-tgt
```

Example `.env.example`:

```env
EPTR_USERNAME=
EPTR_PASSWORD=
```

## Troubleshooting

### "Username and password must be provided"

Ensure credentials are properly set:

```python
import os
print("Username set:", "EPTR_USERNAME" in os.environ)
print("Password set:", "EPTR_PASSWORD" in os.environ)
```

### TGT Expiration Issues

Force TGT renewal:

```python
eptr = EPTR2(use_dotenv=True, force_renew_tgt=True)
```

### Rate Limiting

If you encounter rate limiting, ensure `recycle_tgt=True` is set to minimize authentication requests.

## Next Steps

- [Quick Start Guide](quickstart.md)
- [Basic Usage](../user-guide/basic-usage.md)
