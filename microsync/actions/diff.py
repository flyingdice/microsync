"""
    microsync/actions/diff
    ~~~~~~~~~~~~~~~~~~~~~~

    Contains functionality for the `diff` action.
"""
from .. import config, defaults, loggers, porcelain, results, scratch
from ..hints import Bool, OptionalStr, Str

LOG = loggers.get_logger()


@results.wrapper
def diff(src: Str,
         ref: OptionalStr = defaults.TEMPLATE_REF,
         interactive: Bool = defaults.RENDER_INTERACTIVE) -> results.Result:
    """
    Responsible displaying a diff between two refs of the template repository.

    :param src: Source location of template to retrieve and render
    :param interactive: Flag indicating execution is interactive and can prompt for user input
    :return: Result of the diff action
    """
    # Read state from local repository.
    state = config.read(src)

    with scratch.new() as scratch_dir:
        # Clone template repository locally from source location for state ref.
        current = porcelain.clone(
            state.template.src,
            scratch_dir.directory(),
            ref=state.template.ref,
            options=state.template.vcs
        )

        # Clone template repository locally from source location for target/latest ref.
        target = porcelain.clone(
            state.template.src,
            scratch_dir.directory(),
            ref=ref,
            options=state.template.vcs
        )

        # Generate context using the current state and the target ref repo.
        context = porcelain.context(
            target,
            state.variables,
            interactive=interactive,
            options=state.template.engine
        )

        # Render template repo at current ref using generated context.
        current_rendered = porcelain.render_context(
            current,
            current.path,
            context,
            options=state.template.engine
        )

        # Render template repo at target ref using generated context.
        target_rendered = porcelain.render_context(
            target,
            target.path,
            context,
            options=state.template.engine
        )

        # Generate full diff of file modifications between the refs.
        diff = porcelain.diff(
            current_rendered.path,
            target_rendered.path,
            options=state.template.comparison
        )

        return results.success(stdout=diff.content)
