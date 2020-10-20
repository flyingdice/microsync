"""
    microsync/config
    ~~~~~~~~~~~~~~~~

    Contains functionality for managing microsync state files.
"""
import dataclasses
import json
import os

from . import defaults, errors, serde, utils
from .hints import AnyStr, FilePath, Int, Nothing, Str, StrAnyDict, StrTuple, Type


@dataclasses.dataclass
class VCS:
    """
    Represents template version control specific state.
    """
    depth: Int = defaults.VCS_DEPTH
    branch: Str = defaults.VCS_BRANCH
    origin: Str = defaults.VCS_ORIGIN
    type: Str = defaults.VCS_TYPE


@dataclasses.dataclass
class Comparison:
    """
    Represents template comparison specific state.
    """
    type: Str = defaults.COMPARISON_TYPE
    ignore: StrTuple = defaults.COMPARISON_IGNORE


@dataclasses.dataclass
class Patch:
    """
    Represents template patch specific state.
    """
    type: Str = defaults.PATCH_TYPE
    message: Str = defaults.PATCH_MESSAGE


@dataclasses.dataclass
class Engine:
    """
    Represents template engine specific state.
    """
    type: Str = defaults.TEMPLATE_TYPE


@dataclasses.dataclass
class Template:
    """
    Represents the template for a repository.
    """
    src: Str
    ref: Str = defaults.TEMPLATE_REF
    comparison: Comparison = dataclasses.field(default_factory=Comparison)
    engine: Engine = dataclasses.field(default_factory=Engine)
    patch: Patch = dataclasses.field(default_factory=Patch)
    vcs: VCS = dataclasses.field(default_factory=VCS)


@dataclasses.dataclass
class Meta:
    """
    Represents the microsync meta for a repository.
    """
    version: Str = defaults.MICROSYNC_VERSION


@dataclasses.dataclass
class State(serde.SupportsFileSerde):
    """
    Represents the state for a project.
    """
    template: Template
    meta: Meta = dataclasses.field(default_factory=Meta)
    variables: StrAnyDict = dataclasses.field(default_factory=dict)

    def set_ref(self, ref: Str) -> Nothing:
        self.template.ref = ref

    def set_variables(self, variables: StrAnyDict) -> Nothing:
        self.variables = variables

    @classmethod
    def decode(cls: Type['State'], s: AnyStr) -> 'State':
        """
        Decode string to instance.

        :param s: JSON string to decode
        :rtype s: :class:`~microsync.hints.AnyStr`
        :return: Instance created from decoded JSON string
        :rtype: :class:`~microsync.models.State`
        """
        try:
            data = serde.loads(s)
            data['template']['comparison'] = Comparison(**data['template']['comparison'])
            data['template']['engine'] = Engine(**data['template']['engine'])
            data['template']['patch'] = Patch(**data['template']['patch'])
            data['template']['vcs'] = VCS(**data['template']['vcs'])
            data['template'] = Template(**data['template'])
            data['meta'] = Meta(**data['meta'])
        except KeyError as ex:
            raise errors.StateFileFieldMissing(''.join(ex.args))
        else:
            return cls(**data)


def new(src: FilePath,
        ref: Str,
        vcs_type: Str,
        template_type: Str,
        comparison_type: Str) -> State:
    """
    Create a new microsync state with the given values.

    :param src: Template source location
    :param ref: Version control reference of the source to checkout
    :param vcs_type: Type of version control system used
    :param template_type: Type of template engine used
    :param comparison_type: Type of comparison used
    :return: New microsync state
    """
    return State(
        Template(
            src=src,
            ref=ref,
            comparison=Comparison(
                type=comparison_type
            ),
            engine=Engine(
                type=template_type
            ),
            vcs=VCS(
                type=vcs_type
            )
        )
    )


def loads(content: str) -> State:
    """
    Read microsync state from the given string.

    :param content: Microsync state as string
    :return: Microsync state loaded from string
    """
    try:
        return State.decode(content)
    except json.JSONDecodeError as ex:
        raise errors.StateContentMalformed() from ex


def read(path: FilePath = defaults.STATE_FILE) -> State:
    """
    Read microsync state from the given file path.

    :param path: Path to microsync state file
    :return: Microsync state loaded from file
    """
    try:
        path = resolve_path(path)
        return State.read(path)
    except json.JSONDecodeError as ex:
        raise errors.StateFileMalformed(path) from ex
    except FileNotFoundError as ex:
        raise errors.StateFileNotFound(path) from ex


def write(state: State,
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
