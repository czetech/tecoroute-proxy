from logging import NullHandler, getLogger

from tecoroute.__about__ import __author__, __appname__, __version__
from tecoroute.connector import Connector

__all__ = (Connector.__name__,)  # @UndefinedVariable

getLogger(__name__).addHandler(NullHandler())

del NullHandler, getLogger
