"""
    microsync/porecelain
    ~~~~~~~~~~~~~~~~~~~~

    Contains functionality for user friendly wrappers encapsulating common patterns.
"""
from .context import context
from .diff import diff, diff_files, graft
from .patch import patch, patch_validate
from .render import render, render_context
from .repo import repo
from .status import status


__all__ = ['context', 'diff', 'diff_files', 'graft', 'patch', 'patch_validate',
           'render', 'render_context', 'repo', 'status'],
