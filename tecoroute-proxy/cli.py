from logging import Formatter, StreamHandler, getLogger
from sys import argv, stdout
from types import SimpleNamespace

from click import group, version_option

from tecoroute import __about__
from tecoroute.connector import Connector


def run(args=None):
    
