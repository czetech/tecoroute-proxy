from importlib.metadata import distribution
from logging import getLogger

_module = __name__.split(".")[0]
_dist = distribution(_module)
_name = _dist.metadata["Name"]

logger = getLogger(_module)

# Distribution metadata
NAME = _name
VERSION = _dist.version
SUMMARY = _dist.metadata["Summary"]
ENTRYPOINT = _dist.entry_points[0].name

# Configuration default values
CONFIG_HOST = None
CONFIG_PORT = 80
CONFIG_CONTROL = "/TR_PROXY"
CONFIG_ORIGIN = "http://route.tecomat.com:61682"

HTTP_NAME = f"{_name}/{_dist.version} (+{_dist.metadata['Home-page']})"
