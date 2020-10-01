"""
    microsync/config
    ~~~~~~~~~~~~~~~~

    Contains functionality for managing microsync state files.
"""
import json
import os

from . import defaults, errors, models, utils
from .hints import FilePath, Int, Nothing, Str


def new(src: FilePath,
        ref: Str,
        vcs_type: Str,
        template_type: Str,
        comparison_type: Str) -> models.State:
    """
    Create a new microsync state with the given values.

    :return: New microsync state
    """
    return models.State(
        models.Template(
            src=src,
            ref=ref,
            comparison=models.Comparison(
                type=comparison_type
            ),
            engine=models.Engine(
                type=template_type
            ),
            vcs=models.VCS(
                type=vcs_type
            )
        )
    )


def read(path: FilePath = defaults.STATE_FILE) -> models.State:
    """
    Read microsync state from the given file path.

    :param path: Path to microsync state file
    :return: Microsync state loaded from file
    """
    try:
        path = resolve_path(path)
        return models.State.read(path)
    except json.JSONDecodeError as ex:
        raise errors.StateFileMalformed(path) from ex
    except FileNotFoundError as ex:
        raise errors.StateFileNotFound(path) from ex


def write(state: models.State,
          path: FilePath = defaults.STATE_FILE) -> Int:
    """
    Write microsync state to the given path.

    :param state: State to write
    :param path: Path to write state
    :return: Number of bytes written
    """
    try:
        path = resolve_path(path)
        return state.write(path)
    except FileNotFoundError as ex:
        raise errors.StateFileNotFound(path) from ex


def delete(path: FilePath = defaults.STATE_FILE) -> Nothing:
    """
    Delete microsync state at the given path.

    :param path: Path to microsync state file
    :return: Nothing
    """
    try:
        path = resolve_path(path)
        return os.remove(path)
    except FileNotFoundError as ex:
        raise errors.StateFileNotFound(path) from ex


def resolve_path(path: FilePath = defaults.STATE_FILE) -> FilePath:
    """
    Resolve the given path into a valid path for a state file.

    If the path is a directory, use the default state file. Ex: /foo/bar/ -> /foo/bar/.microsync.state.
    If the path is relative, resolve it to absolute.

    :param path: File path to resolve for state file
    :return: Absolute path to state file
    """
    if os.path.isdir(path):
        path = os.path.join(path, defaults.STATE_FILE)
    return utils.resolve_path(path)
