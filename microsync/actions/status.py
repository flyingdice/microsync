"""
    microsync/actions/status
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Contains functionality for the `status` action.
"""
from .. import loggers, porcelain, projects, results
from ..hints import FilePath

LOG = loggers.get_logger()


@results.wrapper
def status(path: FilePath) -> results.Result:
    """
    Responsible for listing information about your microsync state
    relative to the source template that created it at your current ref.

    :param path: Path to project
    :return: Result of the status action
    """
    with projects.read(path) as project:
        # Load existing or freshly cloned template source repository.
        repo = porcelain.repo(
            project.state.template.src,
            project.src_dir,
            ref=project.state.template.ref,
            options=project.state.template.vcs
        )

        # Determine status of repository.
        # If we're on the latest ref, there's nothing to do.
        status = porcelain.status(repo)
        if status.same:
            return results.success(stdout=status.message())

        with repo.switch_to():
            # Generate context using the current state and the latest ref.
            context = porcelain.context(
                repo,
                project.state.variables,
                interactive=False,
                options=project.state.template.engine
            )

            # Render template repo at current ref using generated context.
            latest_rendered = porcelain.render_context(
                repo,
                project.render_dir(),
                context,
                options=project.state.template.engine
            )

        with repo.switch_to(project.state.template.ref):
            # Render template repo at current ref using generated context.
            current_rendered = porcelain.render_context(
                repo,
                project.render_dir(),
                context,
                options=project.state.template.engine
            )

        # Generate list of file modifications between the refs. If certain situations,
        # it's possible that there aren't any.
        diff = porcelain.diff_files(
            latest_rendered.path,
            current_rendered.path,
            options=project.state.template.comparison
        )

        msg = (f'{status.message()}\n'
               f'{diff.content}\n'
               'Run "drift" to see local changes, "diff" to see template changes, or "sync" to get latest.')

        return results.failure(stderr=msg)
