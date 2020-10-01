"""
    microsync/defaults
    ~~~~~~~~~~~~~~~~~~

    Contains commonly used default values.
"""
import os
import sys
import tempfile

from . import meta

CLONE_REF = None
COMPARISON_TYPE = 'unidiff'
COMPARISON_IGNORE = tuple()
CONTEXT_INTERACTIVE = sys.stdout.isatty()
MICROSYNC_VERSION = meta.VERSION
MICROSYNC_WORKDIR = '.microsync'
MICROSYNC_HOME = os.environ.get('MICROSYNC_HOME', '.')
PATCH_TYPE = 'git'
PATCH_MESSAGE = ('Update to template ref {ref}\n\n'
                 f'Microsync version: {meta.VERSION}')
RENDER_FORCE = False
RENDER_INTERACTIVE = sys.stdout.isatty()
RESULT_STDOUT = ''
RESULT_STDERR = ''
RESULT_ERROR = None
SCRATCH_PREFIX = 'microsync'
SCRATCH_SUFFIX = '.tmp'
SCRATCH_ROOT = tempfile.gettempdir()
STATE_FILE = '.microsync.state'
STATE_DIR = '.microsync'
TEMPLATE_REF = 'HEAD'
TEMPLATE_TYPE = 'cookiecutter'
TRUNCATE_LENGTH = 80
TRUNCATE_SUFFIX = '...'
VCS_DEPTH = 20
VCS_TYPE = 'git'
