"""
    microsync/utils
    ~~~~~~~~~~~~~~~

    Contains utility functions that don't have a better place.
"""
import os

from . import defaults
from .hints import FilePath, Int, Str


def mkdir(path: FilePath) -> FilePath:
    """
    Create directory (and all parents) for the given file path.

    :param path: Path to directory
    :return: Path to directory created
    """
    os.makedirs(path, mode=0o755, exist_ok=True)
    return path


def resolve_path(path: FilePath) -> FilePath:
    """
    Resolve the given path into a fully qualified path.

    :param path: File path to resolve
    :return: Absolute path
    """
    if not os.path.isabs(path):
        path = os.path.abspath(path)
    return path


def subject_line(s: Str,
                 n: Int = defaults.TRUNCATE_LENGTH,
                 suffix: Str = defaults.TRUNCATE_SUFFIX) -> Str:
    """
    Find an truncate string for a "subject" line.

    The subject is simply anything up to the first line break. If the subject line
    is longer than the specified 'n', it is truncated.

    :param s: String to truncate
    :param n: Maximum length of the string
    :param suffix: Suffix to add to string to indicate it was truncated
    :return: Truncated string
    """
    try:
        newline = s.index('\n')
    except ValueError:
        return truncate(s, n, suffix)
    else:
        if newline <= n:
            return s[:newline]

        return truncate(s, n, suffix)


def truncate(s: Str,
             n: Int = defaults.TRUNCATE_LENGTH,
             suffix: Str = defaults.TRUNCATE_SUFFIX) -> Str:
    """
    Truncate the given string to 'n' character length.

    :param s: String to truncate
    :param n: Maximum length of the string
    :param suffix: Suffix to add to string to indicate it was truncated
    :return: Truncated string
    """
    if len(s) <= n:
        return s

    s_len = n - len(suffix)
    return s[:s_len] + suffix
