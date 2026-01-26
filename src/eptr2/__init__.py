from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("eptr2")
except PackageNotFoundError:
    __version__ = "unknown"

from eptr2.main import (
    EPTR2,
    transparency_call,
    generate_eptr2_credentials_file,
    eptr_w_tgt_wrapper,
)

__all__ = [
    "EPTR2",
    "transparency_call",
    "generate_eptr2_credentials_file",
    "eptr_w_tgt_wrapper",
]
