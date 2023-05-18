from importlib.metadata import distribution
from logging import getLogger

_module = __name__.split(".")[0]

logger = getLogger(_module)
dist = distribution(_module)

HTTP_NAME = f"{dist.metadata['Name']}/{dist.version} (+{dist.metadata['Home-page']})"

# Default values
CONTROL = "/TR_PROXY"
HOST = None
ORIGIN = "http://route.tecomat.com:61682"
PORT = 80
