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
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(logging.Formatter("%(message)s"))
    eptr2_logger.addHandler(stdout_handler)
eptr2_logger.setLevel(logging.INFO)
eptr2_logger.propagate = False

### NOTE: In order to integrate eptr2 logging with the user's logging configuration, we set propagate to True and do not add any handlers to the eptr2 logger. This way, log messages from eptr2 will be handled by the user's logging configuration. If the user has not configured logging, they will not see any log messages from eptr2. If they have configured logging, they will see log messages according to their configuration.
# import logging
# eptr2_logger = logging.getLogger("eptr2")
# eptr2_logger.handlers.clear()
# eptr2_logger.propagate = True


__all__ = [
    "EPTR2",
    "transparency_call",
    "generate_eptr2_credentials_file",
    "eptr_w_tgt_wrapper",
]
