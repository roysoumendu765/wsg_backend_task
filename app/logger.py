import logging

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s "
        "level=%(levelname)s "
        "module=%(name)s "
        "%(message)s"
    ),
)

logger = logging.getLogger("worker")