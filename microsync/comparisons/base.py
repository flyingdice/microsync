"""
    microsync/comparisons/base
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Contains base classes for all comparison implementations.
"""
import abc

from .. import config
from ..hints import FilePath, Str, Type, TypeVar


class Diff(metaclass=abc.ABCMeta):
    """
    Abstract class that represents a diff of contents between two file paths.
    """
    def __init__(self: 'DT', comparison: 'CT', content: Str):
        self.comparison = comparison
        self.content = content


DT = TypeVar('DT', bound=Diff)


class Comparison(metaclass=abc.ABCMeta):
    """
    Abstract class that represents a method of comparison.
    """
    @abc.abstractmethod
    def compare_files(self: 'CT',
                      first: FilePath,
                      second: FilePath,
                      options: config.Comparison = config.Comparison()) -> Type[DT]:
        """
        Compute the diff of contents at two file paths and list the files changed.

        :param first: Path to compare to `second`
        :param second: Path to compare to `first`
        :param options: Options to customize comparison
        :return: Diff of files changed between the two paths
        """
        raise NotImplementedError('Derived classes must implement this method')

    @abc.abstractmethod
    def compare(self: 'CT',
                first: FilePath,
                second: FilePath,
                options: config.Comparison = config.Comparison()) -> Type[DT]:
        """
        Compute the diff of contents at two file paths.

        :param first: Path to compare to `second`
        :param second: Path to compare to `first`
        :param options: Options to customize comparison
        :return: Diff of the two file paths
        """
        raise NotImplementedError('Derived classes must implement this method')


CT = TypeVar('CT', bound=Comparison)
