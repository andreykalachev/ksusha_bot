import logging
import os
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning


def configure_logging():
    fmt = "%(asctime)s - %(levelname)s - %(message)s"

    # Allow explicit LOG_LEVEL env var (e.g. DEBUG, INFO, WARNING or numeric level).
    level_spec = os.getenv("LOG_LEVEL", "").strip()
    if level_spec:
        try:
            level = int(level_spec)
        except ValueError:
            level = getattr(logging, level_spec.upper(), logging.INFO)
    else:
        level = logging.INFO

    root = logging.getLogger()
    if not root.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(fmt))
        root.addHandler(handler)
    root.setLevel(level)

    # Suppress warning about CallbackQueryHandler without message handler
    filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

    # Quiet noisy libraries while keeping their WARNING logs available
    for lib in ("httpx", "telegram", "asyncio"):
        logging.getLogger(lib).setLevel(logging.WARNING)

    return logging.getLogger(__name__)
