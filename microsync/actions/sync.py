"""
    microsync/actions/sync
    ~~~~~~~~~~~~~~~~~~~~~~

    Contains functionality for the `sync` action.
"""
from .. import defaults, loggers, porcelain, projects, results
from ..hints import Bool, FilePath, OptionalStr

LOG = loggers.get_logger()


@results.wrapper
def sync(path: FilePath,
         ref: OptionalStr = defaults.TEMPLATE_REF,
         interactive: Bool = defaults.RENDER_INTERACTIVE) -> results.Result:
    """
    Responsible for updating an existing local repository to a rendered version
    of the template repository at a specific ref.

    This should be run after a `link` for existing local repositories that weren't
    originally created with `init`.

    :param path: Path to project
    :param ref: Version control reference of the source to link to
    :param interactive: Flag indicating execution is interactive and can prompt for user input
    :return: Result of sync action
    """
    with projects.read(path) as project:
        # Load existing or freshly cloned template source repository.
        repo = porcelain.repo(
            project.state.template.src,
            project.src_dir,
            ref=project.state.template.ref,
            options=project.state.template.vcs
        )

        # Bail if local repository is dirty as we can't properly
        # apply changes in this case.
        dirty = repo.is_dirty()
        if dirty:
            msg = (f'Repository is dirty and cannot sync until clean.\n\n'
                   'Please commit changes and add/ignore untracked files:\n\n'
                   f'{dirty.stdout}')
            return results.failure(stderr=msg)

        # Determine status of repository. If we're on the latest ref, there's nothing to do.
        status = porcelain.status(repo)
        if status.same:
            return results.success(stdout=status.message())

        with repo.switch_to(ref) as target_ref:
            # Generate context using the current state and the target ref.
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
            # Render repo at current ref using generated context.
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

        # Apply a patch of changes from target ref to dst repo.
        patch = porcelain.patch(
            repo,
            diff,
            ref=target_ref,
            options=project.state.template.patch
        )

        msg = f'Repository sync successful with ref {patch.ref}'
        return results.success(stdout=msg)
