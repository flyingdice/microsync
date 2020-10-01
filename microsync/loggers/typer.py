"""
    microsync/loggers/typer
    ~~~~~~~~~~~~~~~~~~~~~~~

    Contains logger implementation for `typer`.
"""
import typer

from ..hints import Args, Kwargs, Nothing, Str
from . import base


class Logger(base.Logger):
    """
    Class that represents a logger using the :pkg:`~typer` package.
    """
    def info(self, msg: Str, *args: Args, **kwargs: Kwargs) -> Nothing:
        """
        Log an info message.

        :param msg: Info message to log
        :return: Nothing
        """
        typer.echo(msg)

    def warning(self, msg: Str, *args: Args, **kwargs: Kwargs) -> Nothing:
        """
        Log a warning message.

        :param msg: Warning message to log
        :return: Nothing
        """
        typer.secho(msg, fg='yellow')

    def error(self, msg: Str, *args: Args, **kwargs: Kwargs) -> Nothing:
        """
        Log an error message.

        :param msg: Error message to log
        :return: Nothing
        """
        typer.secho(msg, fg='red')
