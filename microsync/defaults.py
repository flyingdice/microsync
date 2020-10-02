"""
    microsync/defaults
    ~~~~~~~~~~~~~~~~~~

    Contains commonly used default values.
"""
import os
import sys

from . import meta

CLONE_REF = None
COMPARISON_TYPE = 'unidiff'
COMPARISON_IGNORE = tuple()
CONTEXT_INTERACTIVE = sys.stdout.isatty()
MICROSYNC_DIR = '.microsync'
MICROSYNC_HOME = os.environ.get('MICROSYNC_HOME', os.path.expanduser('~'))
MICROSYNC_ROOT = os.path.join(MICROSYNC_HOME, MICROSYNC_DIR)
MICROSYNC_VERSION = meta.VERSION
PATCH_TYPE = 'git'
PATCH_MESSAGE = ('Update to template ref {ref}\n\n'
                 'Microsync version: {version}')
RENDER_FORCE = False
RENDER_INTERACTIVE = sys.stdout.isatty()
RESULT_STDOUT = ''
RESULT_STDERR = ''
RESULT_ERROR = None
SCRATCH_PREFIX = 'microsync'
SCRATCH_SUFFIX = '.tmp'
STATE_FILE = '.microsync.state'
TEMPLATE_REF = 'HEAD'
TEMPLATE_TYPE = 'cookiecutter'
TRUNCATE_LENGTH = 80
TRUNCATE_SUFFIX = '...'
VCS_BRANCH = 'master'
VCS_ORIGIN = f'origin/{VCS_BRANCH}'
VCS_DEPTH = 20
VCS_TYPE = 'git'
