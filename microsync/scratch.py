"""
    microsync/scratch
    ~~~~~~~~~~~~~~~~~

    Contains functionality for managing scratch files/directories.
"""
from scratchdir import ScratchDir

from . import defaults, utils
from .hints import FilePath


def new(wd: FilePath) -> ScratchDir:
    """
    Create a new scratch directory for managing temporary files/directories.

    :param wd: Directory to bind scratchdir to
    :return: Scratch directory
    """
    return ScratchDir(wd=utils.mkdir(wd),
                      prefix=defaults.SCRATCH_PREFIX,
                      suffix=defaults.SCRATCH_SUFFIX)


def child(parent: ScratchDir) -> ScratchDir:
    """
    Create a new scratch directory for managing temporary files/directories
    that is a child directory of the given scratchdir.

    :param parent: Parent scratchdir
    :return: Scratch directory
    """
    return parent.child(suffix=defaults.SCRATCH_SUFFIX)
