"""
    microsync/actions/unlink
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Contains functionality for the `unlink` action.
"""
from .. import projects, results
from ..hints import Str


@results.wrapper
def unlink(path: Str) -> results.Result:
    """
    Responsible for removing the linkage between a repository and
    the template repository it was previously created/updated from.

    Simply put, this destroys the microsync state necessary to maintain the linkage.

    :param path: Path to project
    :return: Result of the unlink action
    """
    with projects.read(path) as project:
        projects.delete(project)

    msg = (f'Repository unlinked from {project.state.template.src} '
           f'at ref {project.state.template.ref}')
    return results.success(stdout=msg)
