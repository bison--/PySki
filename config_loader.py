import logging
from config import *


def setup_logging():
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT
    )


try:
    from config_local import *
except ImportError:
    # valid error, no local config
    pass

setup_logging()
