"""
    microsync/actions/unlink
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Contains functionality for the `unlink` action.
"""
from .. import config, results
from ..hints import Str


@results.wrapper
def unlink(src: Str) -> results.Result:
    """
    Responsible for removing the linkage between a repository and
    the template repository it was previously created/updated from.

    Simply put, this destroys the microsync state necessary to maintain the linkage.

    :param src: Path to local repository to unlink
    :return: Result of the unlink action
    """
    state = config.read(src)

    config.delete(src)

    msg = f'Repository unlinked from {state.template.src} at ref {state.template.ref}'
    return results.success(stdout=msg)
