"""
    microsync/actions/diff
    ~~~~~~~~~~~~~~~~~~~~~~

    Contains functionality for the `diff` action.
"""
from .. import defaults, loggers, porcelain, projects, results, scratch
from ..hints import Bool, OptionalStr, Str

LOG = loggers.get_logger()


@results.wrapper
def diff(path: Str,
         ref: OptionalStr = defaults.TEMPLATE_REF,
         interactive: Bool = defaults.RENDER_INTERACTIVE) -> results.Result:
    """
    Responsible for displaying a diff between two refs of the template repository.

    :param path: Path to project
    :param ref: Version control reference of the source to diff
    :param interactive: Flag indicating execution is interactive and can prompt for user input
    :return: Result of the diff action
    """
    with projects.read(path) as project:
        # Load existing or freshly cloned template source repository.
        repo = porcelain.repo(
            project.state.template.src,
            project.src_dir,
            ref=ref,
            options=project.state.template.vcs
        )

        with repo.switch_to(ref):
            # Generate context using the current state and the target ref repo.
            context = porcelain.context(
                repo,
                project.state.variables,
                interactive=interactive,
                options=project.state.template.engine
            )

            # Render template repo at target ref using generated context.
            target_rendered = porcelain.render_context(
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

        # Generate full diff of file modifications between the refs.
        diff = porcelain.diff(
            current_rendered.path,
            target_rendered.path,
            options=project.state.template.comparison
        )

        return results.success(stdout=diff.content)
