"""
    microsync/loggers/base
    ~~~~~~~~~~~~~~~~~~~~~~

    Contains base classes for all logger implementations.
"""
import abc

from ..hints import Args, Kwargs, Str, TypeVar


class Logger(metaclass=abc.ABCMeta):
    """
    Abstract class that represents a logger.
    """
    @abc.abstractmethod
    def info(self: 'LT', msg: Str, *args: Args, **kwargs: Kwargs):
        """
        Log an info message.

        :param msg: Info message to log
        :return: Nothing
        """
        raise NotImplementedError('Derived classes must implement this method')

    @abc.abstractmethod
    def warning(self: 'LT', msg: Str, *args: Args, **kwargs: Kwargs):
        """
        Log a warning message.

        :param msg: Warning message to log
        :return: Nothing
        """
        raise NotImplementedError('Derived classes must implement this method')

    @abc.abstractmethod
    def error(self: 'LT', msg: Str, *args: Args, **kwargs: Kwargs):
        """
        Log an error message.

        :param msg: Error message to log
        :return: Nothing
        """
        raise NotImplementedError('Derived classes must implement this method')


LT = TypeVar('LT', bound=Logger)
