"""
    microsync/loggers
    ~~~~~~~~~~~~~~~~~

    Contains functionality for logging.
"""
import sys

from . import base, stdlib, typer
from .base import Logger

__all__ = [
    'get_logger',
    'Logger'
]


def get_logger() -> base.LT:
    """
    Retrieve the logger implementation for the given environment.

    :return: Logger implementation
    """
    logger = typer if sys.stdout.isatty() else stdlib
    return logger.Logger()
