"""
    microsync/vcs/base
    ~~~~~~~~~~~~~~~~~~

    Contains functionality for interacting with version control systems.
"""
from .. import errors
from ..hints import Str
from . import base, git
from .base import Repository, VersionControl

__all__ = [
    'VCSType',
    'for_type',
    'Repository',
    'VersionControl'
]


class VCSType:
    """
    Known version control system types.
    """
    Git = 'git'


TYPES = {
    VCSType.Git: git
}


def for_type(vcs_type: Str) -> base.Type[base.VT]:
    """
    Retrieve the VCS implementation for the given type.

    :param vcs_type: VCS type to use
    :return: VCS implementation
    """
    vcs = TYPES.get(vcs_type)
    if not vcs:
        raise errors.VCSTypeNotSupported(vcs_type)

    return vcs.VersionControl
