"""
    microsync/actions/sync
    ~~~~~~~~~~~~~~~~~~~~~~

    Contains functionality for the `sync` action.
"""
from .. import config, defaults, loggers, porcelain, results, scratch, utils
from ..hints import Bool, OptionalStr, Str

LOG = loggers.get_logger()


@results.wrapper
def sync(src: Str,
         ref: OptionalStr = defaults.TEMPLATE_REF,
         interactive: Bool = defaults.RENDER_INTERACTIVE) -> results.Result:
    """
    Responsible for updating an existing local repository to a rendered version
    of the template repository at a specific ref.

    This should be run after a `link` for existing local repositories that weren't
    originally created with `init`.

    :param src: Path to local repository to synchronize
    :param ref: Version control reference of the source to link to
    :param interactive: Flag indicating execution is interactive and can prompt for user input
    :return: Result of sync action
    """
    # Read state from local repository.
    state = config.read(src)

    # Grab reference to local repository we're going to synchronize.
    repo = porcelain.repo(
        state.template.src,
        src,
        ref=ref
    )

    # Bail if local repository is dirty as we can't properly
    # apply changes in this case.
    dirty = repo.is_dirty()
    if dirty:
        msg = (f'Repository is dirty and cannot sync until clean.\n\n'
               'Please commit changes and add/ignore untracked files:\n\n'
               f'{dirty.stdout}')
        return results.failure(stderr=msg)

    with scratch.new() as scratch_dir:
        # Clone template repository locally from source location for state ref.
        current = porcelain.clone(
            state.template.src,
            scratch_dir.directory(),
            ref=state.template.ref,
            options=state.template.vcs
        )

        # Determine status of repository.
        # If we're on the latest ref, there's nothing to do.
        status = porcelain.status(current)
        if status.same:
            return results.success(stdout=status.message())

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

        # Apply a patch of changes from target ref to dst repo.
        patch = porcelain.patch(
            repo,
            diff,
            ref=target.commit_id(),
            options=state.template.patch
        )

        msg = f'Repository sync successful with ref {patch.ref}'
        return results.success(stdout=msg)
