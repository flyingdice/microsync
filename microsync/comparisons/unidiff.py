"""
    microsync/comparisons/git
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Contains comparison implementation using the unidiff format.
"""
import sh

from .. import config
from ..hints import FilePath, Str, StrIterator
from . import base


class Diff(base.Diff):
    """
    Represents a diff of contents between two file paths in unidiff format.
    """


class Comparison(base.Comparison):
    """
    Class that represents a unidiff comparison.
    """
    def __init__(self):
        self.git = sh.git.bake('--no-pager', _tty_out=False)

    def compare_files(self,
                      first: FilePath,
                      second: FilePath,
                      options: config.Comparison = config.Comparison()) -> Diff:
        """
        Compute the diff of contents at two file paths and list the files changed.

        :param first: Path to compare to `second`
        :param second: Path to compare to `first`
        :param options: Options to customize comparison
        :return: Diff of files changed between the two paths
        """
        opts = (
            '--stat',
            '--no-index',
            '--no-ext-diff',
            '--no-color'
        )
        stdout = self.run(first, second, opts)
        return Diff(self, stdout)

    def compare(self,
                first: FilePath,
                second: FilePath,
                options: config.Comparison = config.Comparison()) -> Diff:
        """
        Compute the diff of contents at two file paths.

        :param first: Path to compare to `second`
        :param second: Path to compare to `first`
        :param options: Options to customize comparison
        :return: Diff of the two file paths
        """
        opts = (
            '--no-index',
            '--no-ext-diff',
            '--no-color'
        )
        stdout = self.run(first, second, opts)
        return Diff(self, stdout)

    def run(self,
            first: FilePath,
            second: FilePath,
            *args: StrIterator) -> Str:
        """
        Compare contents of two file paths and return diff of changes.

        :param first: Path to compare to `second`
        :param second: Path to compare to `first`
        :param args: Command line options/switches to pass to command
        :return: Diff of the two file paths
        """
        opts = args + tuple(map(str, (first, second)))
        stdout = self.git.diff(*opts, _ok_code=[0, 1]).stdout.decode('utf-8')
        return stdout.replace(first, '').replace(second, '')
