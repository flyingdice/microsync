"""
    microsync/porcelain/repo
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Contains functionality for repositories.
"""
from .. import config, defaults, vcs
from ..hints import OptionalStr, Str


def repo(src: Str,
         dst: Str,
         ref: OptionalStr = defaults.CLONE_REF,
         options: config.VCS = config.VCS()) -> vcs.Repository:
    """
    Use the user selected version control system to retrieve a code repository
    or wrap an existing one on disk and checkout and optional reference.

    The ref is VCS specific but typically a branch name, commit id/hash, or tag.

    :param src: Source location of template repository
    :param dst: Output file path of cloned repository
    :param ref: Version control reference of the source to checkout
    :param options: Options to customize version control system
    :return: Wrapped local repository
    """
    vc = vcs.for_type(options.type)()
    return vc.get(src, dst, ref=ref, options=options)


def remote_url(path: Str,
               options: config.VCS = config.VCS()) -> Str:
    """
    Use the user selected version control system to retrieve a code repository
    remote URL.

    :param path: File path of local repository
    :param options: Options to customize version control system
    :return: Remote URL for the local repository
    """
    vc = vcs.for_type(options.type)()
    return vc.repo_url(path)
