"""
    microsync/porcelain/repo
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Contains functionality for repositories.
"""
from .. import defaults, models, vcs
from ..hints import OptionalStr, Str


def repo(template: Str,
         path: Str,
         ref: OptionalStr = defaults.CLONE_REF,
         options: models.VCS = models.VCS()) -> vcs.Repository:
    """
    Use the user selected version control system to retrieve a code repository
    or wrap an existing one on disk and checkout and optional reference.

    The ref is VCS specific but typically a branch name, commit id/hash, or tag.

    :param template: Source location of template repository
    :param path: Output file path of cloned repository
    :param ref: Version control reference of the source to checkout
    :param options: Options to customize version control system
    :return: Wrapped local repository
    """
    vc = vcs.for_type(options.type)()
    return vc.get(template, path, ref=ref, options=options)
