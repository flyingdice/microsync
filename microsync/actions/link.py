"""
    microsync/actions/link
    ~~~~~~~~~~~~~~~~~~~~~~

    Contains functionality for the `link` action.
"""
from .. import config, defaults, porcelain, results, scratch
from ..hints import Bool, OptionalStr, Str


@results.wrapper
def link(src: Str,
         dst: Str,
         ref: OptionalStr = defaults.TEMPLATE_REF,
         interactive: Bool = defaults.RENDER_INTERACTIVE,
         vcs_type: Str = defaults.VCS_TYPE,
         template_type: Str = defaults.TEMPLATE_TYPE,
         comparison_type: Str = defaults.COMPARISON_TYPE) -> results.Result:
    """
    Responsible for linking an existing repository to the template repository
    that originally created it. This is similar to the `init` action except
    we do not modify any files within the existing repository and require
    the user run a `sync` afterwards to apply any template changes that
    occurred after its creation.

    :param src: Source location of template to link
    :param dst: Path of repository to link to src
    :param ref: Version control reference of the source to link to
    :param interactive: Flag indicating execution is interactive and can prompt for user input
    :param vcs_type: Type of version control system used
    :param template_type: Type of template engine used
    :param comparison_type: Type of comparison used
    :return: Result of the link action
    """
    # Create new state based on user provided options and defaults.
    state = config.new(src, ref, vcs_type, template_type, comparison_type)

    with scratch.new() as scratch_dir:
        # Clone template repository locally from source location.
        repo = porcelain.clone(
            src,
            scratch_dir.wd,
            ref=ref,
            options=state.template.vcs
        )

        # Generate context that would be used to render a template.
        context = porcelain.context(
            repo,
            state.variables,
            interactive=interactive,
            options=state.template.engine
        )

        # Update state with dynamic values.
        state.set_ref(repo.commit_id())
        state.set_variables(context.variables)

        # Write state out to disk in the rendered template output directory.
        config.write(state, dst)

        msg = f'Repository linked to {src} at ref {state.template.ref}'
        return results.success(stdout=msg)
