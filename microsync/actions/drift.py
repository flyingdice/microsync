"""
    microsync/actions/drift
    ~~~~~~~~~~~~~~~~~~~~~~~

    Contains functionality for the `drift` action.
"""
from .. import config, defaults, loggers, porcelain, results, scratch
from ..hints import Bool, Str

LOG = loggers.get_logger()


@results.wrapper
def drift(src: Str,
          interactive: Bool = defaults.RENDER_INTERACTIVE) -> results.Result:
    """
    Responsible displaying a diff between a local repository and a rendered
    template repository at the same ref.

    The goal of drift is to detect "local" changes made to a child repository
    that haven't been propagated to the parent.

    :param src: Source location of template to retrieve and render
    :param interactive: Flag indicating execution is interactive and can prompt for user input
    :return: Result of the drift action
    """
    # Read state from local repository.
    state = config.read(src)

    with scratch.new() as scratch_dir:
        # Clone template repository locally from source location for state ref.
        repo = porcelain.clone(
            state.template.src,
            scratch_dir.directory(),
            ref=state.template.ref,
            options=state.template.vcs
        )

        # Generate context using the current state.
        context = porcelain.context(
            repo,
            state.variables,
            interactive=interactive,
            options=state.template.engine
        )

        # Render template repo at current ref using generated context.
        rendered = porcelain.render_context(
            repo,
            repo.path,
            context,
            options=state.template.engine
        )

        # Graft files defined in template from src to temporary dir.
        graft_dir = porcelain.graft(
            rendered.path,
            src,
            scratch_dir.filename(),
            options=state.template.comparison
        )

        # Generate full diff of file modifications between src and the
        # rendered template both at the state ref.
        diff = porcelain.diff(
            graft_dir,
            rendered.path,
            options=state.template.comparison
        )

        return results.success(stdout=diff.content)
