"""
    microsync/actions/init
    ~~~~~~~~~~~~~~~~~~~~~~

    Contains functionality for the `init` action.
"""
from .. import config, defaults, porcelain, results, scratch
from ..hints import Bool, OptionalStr, Str


@results.wrapper
def init(src: Str,
         dst: Str,
         ref: OptionalStr = defaults.TEMPLATE_REF,
         force: Bool = defaults.RENDER_FORCE,
         interactive: Bool = defaults.RENDER_INTERACTIVE,
         vcs_type: Str = defaults.VCS_TYPE,
         template_type: Str = defaults.TEMPLATE_TYPE,
         comparison_type: Str = defaults.COMPARISON_TYPE) -> results.Result:
    """
    Responsible for creating a new local repository on disk
    by the process of rendering a template.

    :param src: Source location of template to retrieve and render
    :param dst: Output path of rendered template
    :param ref: Version control reference of the source to checkout
    :param force: Flag indicating if output path should be overwritten if it already exists
    :param interactive: Flag indicating execution is interactive and can prompt for user input
    :param vcs_type: Type of version control system used
    :param template_type: Type of template engine used
    :param comparison_type: Type of comparison used
    :return: Result of the init action
    """
    # Create new state based on user provided options and defaults.
    state = config.new(src, ref, vcs_type, template_type, comparison_type)

    with scratch.new() as scratch_dir:
        # Load existing or freshly cloned template source repository.
        repo = porcelain.repo(
            src,
            scratch_dir.wd,
            ref=ref,
            options=state.template.vcs
        )

        # Render template repo into destination location.
        rendered = porcelain.render(
            repo,
            dst,
            state.variables,
            force=force,
            interactive=interactive,
            options=state.template.engine
        )

        # Update state with dynamic values.
        state.set_ref(repo.commit_id())
        state.set_variables(rendered.context.variables)

        # Write state out to disk in the rendered template output directory.
        config.write(state, rendered.path)

        msg = ('Initialized microsync repository in'
               f'{rendered.path}'
               f'for {state.template.src} at ref {state.template.ref}')

        return results.success(stdout=msg)
