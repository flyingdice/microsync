"""
    microsync/porcelain
    ~~~~~~~~~~~~~~~~~~~

    Contains functionality for user friendly wrappers encapsulating common patterns.
"""
from .context import context
from .diff import diff, diff_files, graft
from .patch import patch, patch_validate
from .project import project, project_new, project_src
from .render import render, render_context
from .repo import remote_url, repo
from .status import status


__all__ = [
    'context',
    'diff',
    'diff_files',
    'graft',
    'patch',
    'patch_validate',
    'project',
    'project_new',
    'project_src',
    'render',
    'render_context',
    'remote_url',
    'repo',
    'status',
]
