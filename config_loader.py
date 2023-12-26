from config import *

try:
    from config_local import *
except ImportError:
    # valid error, no local config
    pass
