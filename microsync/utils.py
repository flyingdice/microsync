"""
    microsync/utils
    ~~~~~~~~~~~~~~~

    Contains utility functions that don't have a better place.
"""
import functools
import os
from urllib import parse as urlparse

from . import defaults, errors
from .hints import Bool, FilePath, Int, Str


def within_root(path: FilePath) -> Bool:
    """
    Check to see if the given path is relative to the microsync root path.

    :param path: Path to check
    :return: True if cache path, False otherwise
    """
    path = resolve_path(path)
    root = resolve_path(defaults.MICROSYNC_ROOT)
    return os.path.commonpath([path, root]) == root


def mkdir(path: FilePath) -> FilePath:
    """
    Create directory (and all parents) for the given file path.

    :param path: Path to directory
    :return: Path to directory created
    """
    os.makedirs(path, mode=0o755, exist_ok=True)
    return path


def symlink(src: FilePath,
            dst: FilePath,
            is_dir: Bool = False) -> FilePath:
    """
    Create a symlink between src and dst.

    If the link is for directories, set 'is_dir' to True.

    :param src: Symlink source
    :param dst: Symlink destination
    :param is_dir: Flag indicating if symlink source is a directory
    :return: Symlink destination
    """
    if os.path.exists(dst):
        return dst

    os.symlink(src, dst, target_is_directory=is_dir)
    return dst


symlink_dir = functools.partial(symlink, is_dir=True)


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


def src_to_path(src: Str,
                root: FilePath = defaults.MICROSYNC_ROOT) -> FilePath:
    """
    Convert a template src value into a file path where it should be saved.

    Supported formats:
    * git@github.com:microsync/example-cookiecutter.git
    * git://github.com/microsync/example-cookiecutter.git
    * https://github.com/microsync/example-cookiecutter
    * file://some/path/to/repo

    :param src: Template src to parse
    :param root: File path root where template src should be saved
    :return: Absolute file path for template src to be saved
    """
    url = urlparse.urlparse(src)

    if url.scheme == 'file':
        name = src_to_full_name(url.path.lstrip('/'))
        path = os.path.join(root, 'file', name)
        return resolve_path(path)

    if url.scheme.startswith('http') or url.scheme.startswith('git'):
        name = src_to_full_name(url.path.lstrip('/'))
        path = os.path.join(root, url.netloc, name)
        return resolve_path(path)

    if url.scheme == '' and url.path.startswith('git@'):
        parts = url.path.strip('.git').split(':')
        netloc = parts[0].split('@')[1]
        path = os.path.join(root, netloc, parts[1])
        return resolve_path(path)

    raise errors.TemplateSourceInvalid(src)


def src_to_src_path(src: Str,
                    root: FilePath = defaults.MICROSYNC_ROOT) -> FilePath:
    """
    Convert src value into the 'src' file path within its project path.

    :param src: Template src to parse
    :param root: File path root where template src should be saved
    :return: Absolute file path for template src to be saved
    """
    path = src_to_path(src, root)
    return os.path.join(path, 'src')


def src_to_tmp_path(src: Str,
                    root: FilePath = defaults.MICROSYNC_ROOT) -> FilePath:
    """
    Convert src value into the 'tmp' file path within its project path.

    :param src: Template src to parse
    :param root: File path root where template src should be saved
    :return: Absolute file path for template src to be saved
    """
    path = src_to_path(src, root)
    return os.path.join(path, 'tmp')


def src_to_name(src: Str) -> Str:
    """
    Get name of repository from template src.

    Ex: https://github.com/ahawker/example-cookiecutter -> example-cookiecutter

    :param src: Template src to parse
    :return: Repository name
    """
    return os.path.splitext(os.path.basename(src))[0]


def src_to_full_name(src: Str) -> Str:
    """
    Get the full name of repository from source location.

    Ex: https://github.com/ahawker/example-cookiecutter -> ahawker/example-cookiecutter

    :param src: Source location to parse
    :return: Repository full name
    """
    return os.path.splitext(src)[0]
