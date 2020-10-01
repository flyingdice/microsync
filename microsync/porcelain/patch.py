"""
    microsync/porcelain/patch
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Contains functionality for applying patches.
"""
import dataclasses

from .. import comparisons, models, results, vcs
from ..hints import Str


@dataclasses.dataclass
class Patch:
    repo: vcs.Repository
    diff: comparisons.Diff
    ref: Str


def patch_validate(repo: vcs.Repository,
                   diff: comparisons.Diff) -> results.Result:
    """
    Porcelain function for `patch_validate`.

    This is responsible for checking to see if a patch can be applied to a repository.

    :param repo: Repository to validate patch on
    :param diff: Diff patch to validate
    :return: Result of validation check
    """
    return repo.check_patch(diff.content)


def patch(repo: vcs.Repository,
          diff: comparisons.Diff,
          ref: Str,
          options: models.Patch = models.VCS()) -> Patch:
    """
    Porcelain function for `patch`.

    This is responsible for applying a patch to a repository.

    :param repo: Repository to apply patch
    :param diff: Diff patch to apply
    :param ref: Ref where patch originated from
    :param options: VCS options to configure patching
    :return: Result of patch application
    """
    commit_message = options.message.format(ref=ref)
    repo.apply_patch(diff.content, commit_message)
    return Patch(repo, diff, ref)
