"""
    microsync/loggers/stdlib
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Contains logger implementation for `logging`.
"""
import logging

from .. import meta
from ..hints import Args, Kwargs, Nothing, Str
from . import base

LOG = logging.getLogger(meta.NAME)


class Logger(base.Logger):
    """
    Class that represents a logger using the python :mod:`~logging` module.
    """
    def info(self, msg: Str, *args: Args, **kwargs: Kwargs) -> Nothing:
        """
        Log an info message.

        :param msg: Info message to log
        :return: Nothing
        """
        LOG.info(msg)

    def warning(self, msg: Str, *args: Args, **kwargs: Kwargs) -> Nothing:
        """
        Log a warning message.

        :param msg: Warning message to log
        :return: Nothing
        """
        LOG.warning(msg)

    def error(self, msg: Str, *args: Args, **kwargs: Kwargs) -> Nothing:
        """
        Log an error message.

        :param msg: Error message to log
        :return: Nothing
        """
        LOG.error(msg)
