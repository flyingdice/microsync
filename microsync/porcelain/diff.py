"""
    microsync/porcelain/diff
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Contains porcelain functions for diffing.
"""
import shutil

from .. import config, comparisons, ignore
from ..hints import FilePath


def diff(first: FilePath,
         second: FilePath,
         options: config.Comparison = config.Comparison()) -> comparisons.Diff:
    """
    Compare contents at two file paths and generating a user
    friendly diff that can be reviewed.

    :param first: Path to compare to `second`
    :param second: Path to compare to `first`
    :param options: Options to customize comparison
    :return: Diff of the two file paths
    """
    comparison = comparisons.for_type(options.type)()
    return comparison.compare(first, second, options=options)


def diff_files(first: FilePath,
               second: FilePath,
               options: config.Comparison = config.Comparison()) -> comparisons.Diff:
    """
    Compare contents at two file paths and generating a user
    friendly list of modified files that can be reviewed.

    :param first: Path to compare to `second`
    :param second: Path to compare to `first`
    :param options: Options to customize comparison
    :return: Diff of the two file paths
    """
    comparison = comparisons.for_type(options.type)()
    return comparison.compare_files(first, second, options=options)


def graft(layout: FilePath,
          src: FilePath,
          dst: FilePath,
          options: config.Comparison) -> FilePath:
    """
    Based on files/directories defined in layout, copy files/directories that exist in src to dst.

    :param layout: Directory that defines file/subdir layout of files
    :param src: Directory that contains files to be copied
    :param dst: Directory to contain copied files
    :param options: Options for configuring comparisons
    :return: Destination directory populated with copied files
    """
    shutil.copytree(
        src,
        dst,
        symlinks=True,
        ignore=ignore.ignore_names_missing(layout, options)
    )
    return dst
