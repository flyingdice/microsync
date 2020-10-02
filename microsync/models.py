"""
    microsync/models
    ~~~~~~~~~~~~~~~~

    Contains microsync models.
"""
import dataclasses
import os

from . import defaults, scratch, serde, utils
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
class Config:
    """
    Represents the microsync config for a repository.
    """
    version: Str = defaults.MICROSYNC_VERSION


@dataclasses.dataclass
class State(serde.SupportsFileSerde):
    """
    Represents the state for a project.
    """
    template: Template
    config: Config = dataclasses.field(default_factory=Config)
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
        data = serde.loads(s)
        data['template']['comparison'] = Comparison(**data['template']['comparison'])
        data['template']['engine'] = Engine(**data['template']['engine'])
        data['template']['patch'] = Patch(**data['template']['patch'])
        data['template']['vcs'] = VCS(**data['template']['vcs'])
        data['template'] = Template(**data['template'])
        data['config'] = Config(**data['config'])
        return cls(**data)


class Project:
    """
    Represents a project that is managed by microsync.

    Projects track the template source repository, temporary space
    for rendering/grafting and the project (child) state file.
    """
    def __init__(self,
                 state: State,
                 state_path: FilePath,
                 name: Str,
                 path: FilePath) -> Nothing:
        self.state = state
        self.state_path = state_path
        self.name = name
        self.path = utils.mkdir(path)
        self.src_dir = os.path.join(path, 'src')
        self.tmp_dir = os.path.join(path, 'tmp')
        self.scratch = scratch.new(self.tmp_dir)

    def __enter__(self) -> 'Project':
        self.scratch.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> Nothing:
        self.scratch.__exit__(exc_type, exc_val, exc_tb)

    def graft_dir(self) -> Str:
        return os.path.join(self.scratch.directory(prefix='graft'), self.name)

    def render_dir(self) -> Str:
        return os.path.join(self.scratch.directory(prefix='render'), self.name)
