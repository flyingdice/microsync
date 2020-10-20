"""
    microsync/ignore
    ~~~~~~~~~~~~~~~~

    Contains functionality for ignoring files.
"""
import fnmatch
import os

from . import config
from .hints import (Bool, FilePath, IgnoreNamesFunction, Str, StrIterator,
                    StrList)


def ignore_names_missing(layout: FilePath,
                         src: FilePath,
                         options: config.Comparison) -> IgnoreNamesFunction:
    """
    Returns a function to be used with :func:`~shutil.copytree` that
    ignores files/directories in src that shouldn't be copied.

    A file is ignored if:
    * It doesn't exist in the layout dir
    * It is excluded by a comparison pattern

    :param layout: Directory that defines file/subdir layout of files
    :param src: Directory that contains file/subdir of files to copy
    :param options: Options for configuring comparisons
    :return: Function that ignores files
    """
    def ignore_names(src_dir: Str, names: StrList) -> StrList:
        """
        Ignore files/directories not found in layout or excluded by pattern.

        :param src_dir: Directory to copy
        :param names: Names of file contents in src_dir to copy.
        :return: List of file contents in src_dir to ignore.
        """
        # Get the dir/subdir name relative to src so we can use it to create
        # absolute paths in src and layout for exists comparisons.
        rel_dir = os.path.relpath(src_dir, src)

        # If directory doesn't exist in layout, ignore all files in the dir.
        if not os.path.exists(os.path.abspath(os.path.join(layout, rel_dir))):
            return names

        # Return names for files in src that don't exist in layout or matches
        # one of the ignored files/patterns.
        def ignored(name):
            if not os.path.exists(os.path.abspath(os.path.join(layout, rel_dir, name))):
                return True
            return is_ignored(name, options.ignore)

        return [name
                for name in names
                if ignored(name)]

    return ignore_names


def is_ignored(name: Str, patterns: StrIterator) -> Bool:
    """
    Check if the given name is ignored by the given set of patterns.

    :param name: Name to check if ignored
    :param patterns: Patterns to check against
    :return: True if ignored, False otherwise
    """
    def is_match(pattern):
        return fnmatch.fnmatch(name, pattern)

    return any(map(is_match, patterns))
