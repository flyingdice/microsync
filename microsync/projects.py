"""
    microsync/projects
    ~~~~~~~~~~~~~~~~~~

    Contains functionality for managing projects.
"""
import os
from urllib.parse import urlparse

from . import config, defaults, errors, models, utils
from .hints import Bool, FilePath, Int, Nothing, Str


def new(src: FilePath,
        ref: Str,
        vcs_type: Str,
        template_type: Str,
        comparison_type: Str) -> models.Project:
    """

    :param src: Template source location
    :param ref: Version control reference of the source to checkout
    :param vcs_type: Type of version control system used
    :param template_type: Type of template engine used
    :param comparison_type: Type of comparison used
    :return: New project for the given config
    """
    state = config.new(src, ref, vcs_type, template_type, comparison_type)
    return from_state(state)


def exists(path: FilePath) -> Bool:
    """
    Check to see if project exists at the the given path.

    :param path: Path to project
    :return: True if project exists, False otherwise
    """
    return os.path.exists(path)


def read(path: FilePath) -> models.Project:
    """
    Create project from the given file path.

    :param path: Path to project/project state file to read
    :return: Project at the given file path
    """
    path = config.resolve_path(path)
    state = config.read(path)
    return from_state(state, path)


def write(project: models.Project,
          path: FilePath) -> Int:
    """
    Write microsync project to the given path.

    :param project: Project to write
    :param path: Path to write project
    :return: Number of bytes written
    """
    return config.write(project.state, path)


def delete(project: models.Project) -> Nothing:
    """
    Delete the given microsync project.

    :param project: Project to delete
    :param path: Path to project state
    :return: Nothing
    """
    return config.delete(project.state_path)


def from_state(state: models.State,
               state_path: FilePath = defaults.STATE_FILE) -> models.Project:
    """
    Create project from the given microsync state.

    :param state: State to create project from
    :param state_path: Path where state file was read
    :return: Project
    """
    name = src_to_name(state.template.src)
    path = src_to_path(state.template.src)
    return models.Project(state, state_path, name, path)


def src_to_name(src: Str) -> Str:
    """
    Get name of repository from template src.

    Ex: https://github.com/ahawker/example-cookiecutter -> example-cookiecutter

    :param src: Template src to parse
    :return: Repository name
    """
    return os.path.splitext(os.path.basename(src))[0]


def src_to_path(src: Str,
                root: FilePath = defaults.MICROSYNC_ROOT) -> FilePath:
    """
    Convert a template src value into a file path where it should be saved.

    Supported formats:
    * git@github.com:microsync/example-cookiecutter.git
    * https://github.com/microsync/example-cookiecutter
    * file://some/path/to/repo

    :param src: Template src to parse
    :param root: File path root where template src should be saved
    :return: Absolute file path for template src to be saved
    """
    url = urlparse(src)

    if url.scheme == 'file':
        path = os.path.join(root, 'file', url.path.lstrip('/'))
        return utils.resolve_path(path)

    if url.scheme.startswith('http'):
        path = os.path.join(root, url.netloc, url.path.lstrip('/'))
        return utils.resolve_path(path)

    if url.scheme == '' and url.path.startswith('git@'):
        parts = url.path.strip('.git').split(':')
        netloc = parts[0].split('@')[1]
        path = os.path.join(root, netloc, parts[1])
        return utils.resolve_path(path)

    raise errors.TemplateSourceInvalid(src)
