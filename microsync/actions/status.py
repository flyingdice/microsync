"""
    microsync/actions/status
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Contains functionality for the `status` action.
"""
from .. import config, loggers, porcelain, results, scratch
from ..hints import Str

LOG = loggers.get_logger()


@results.wrapper
def status(src: Str) -> results.Result:
    """
    Responsible for listing information about your microsync state
    relative to the source template that created it at your current ref.

    :param src: Source location of template to check status against
    :return: Result of the status action
    """
    # Read state from local repository.
    state = config.read(src)

    with scratch.new() as scratch_dir:
        # Clone template repository locally from source location for state ref.
        current = porcelain.clone(
            state.template.src,
            scratch_dir.wd,
            ref=state.template.ref,
            options=state.template.vcs
        )

        # Determine status of repository.
        # If we're on the latest ref, there's nothing to do.
        status = porcelain.status(current)
        if status.same:
            return results.success(stdout=status.message())

        # If we're not on the latest ref, clone template at latest so we can
        # determine which files have changed.
        latest = porcelain.clone(
            state.template.src,
            scratch_dir.directory(),
            options=state.template.vcs
        )

        # Generate context using the current state and the latest ref.
        context = porcelain.context(
            latest,
            state.variables,
            interactive=False,
            options=state.template.engine
        )

        # Render template repo at current ref using generated context.
        current_rendered = porcelain.render_context(
            current,
            current.path,
            context,
            options=state.template.engine
        )

        # Render template repo at current ref using generated context.
        target_rendered = porcelain.render_context(
            latest,
            latest.path,
            context,
            options=state.template.engine
        )

        # Generate list of file modifications between the refs. If certain situations,
        # it's possible that there aren't any.
        diff = porcelain.diff_files(
            target_rendered.path,
            current_rendered.path,
            options=state.template.comparison
        )

        msg = (f'{status.message()}\n'
               f'{diff.content}\n'
               'Run "diff" to examine changes or "sync" to get latest.')

        return results.failure(stderr=msg)
