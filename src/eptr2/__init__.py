import logging
import sys
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

eptr2_logger = logging.getLogger(__name__)
if not eptr2_logger.handlers:
    ### Diagnostics go to stderr, never stdout. The `eptr2` CLI contract is that
    ### stdout carries only result data (so it can be piped/parsed), and the MCP
    ### stdio transport reserves stdout for protocol frames while allowing
    ### diagnostics on stderr. Writing log records to stdout corrupts both.
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(logging.Formatter("%(message)s"))
    eptr2_logger.addHandler(stderr_handler)
eptr2_logger.setLevel(logging.INFO)
eptr2_logger.propagate = False

### To route eptr2 logs through your own logging configuration instead, clear
### these handlers and re-enable propagation in your application:
#     eptr2_logger = logging.getLogger("eptr2")
#     eptr2_logger.handlers.clear()
#     eptr2_logger.propagate = True


__all__ = [
    "EPTR2",
    "transparency_call",
    "generate_eptr2_credentials_file",
    "eptr_w_tgt_wrapper",
]
