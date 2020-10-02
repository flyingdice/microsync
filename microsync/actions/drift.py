"""
    microsync/actions/drift
    ~~~~~~~~~~~~~~~~~~~~~~~

    Contains functionality for the `drift` action.
"""
from .. import defaults, loggers, porcelain, projects, results
from ..hints import Bool, Str

LOG = loggers.get_logger()


@results.wrapper
def drift(path: Str,
          interactive: Bool = defaults.RENDER_INTERACTIVE) -> results.Result:
    """
    Responsible for displaying a diff between a local repository and a rendered
    template repository at the same ref.

    The goal of drift is to detect "local" changes made to a child repository
    that haven't been propagated to the parent.

    :param path: Path to project
    :param interactive: Flag indicating execution is interactive and can prompt for user input
    :return: Result of the drift action
    """
    with projects.read(path) as project:
        # Load existing or freshly cloned template source repository.
        repo = porcelain.repo(
            project.state.template.src,
            project.src_dir,
            ref=project.state.template.ref,
            options=project.state.template.vcs
        )

        # Generate context using the current state.
        context = porcelain.context(
            repo,
            project.state.variables,
            interactive=interactive,
            options=project.state.template.engine
        )

        # Render template repo at current ref using generated context.
        rendered = porcelain.render_context(
            repo,
            project.render_dir(),
            context,
            options=project.state.template.engine
        )

        # Graft files defined in template from src to temporary dir.
        graft_dir = porcelain.graft(
            rendered.path,
            path,
            project.graft_dir(),
            options=project.state.template.comparison
        )

        # Generate full diff of file modifications between src and the
        # rendered template both at the state ref.
        diff = porcelain.diff(
            graft_dir,
            rendered.path,
            options=project.state.template.comparison
        )

        return results.success(stdout=diff.content)
