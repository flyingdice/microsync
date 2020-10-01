"""
    microsync/models
    ~~~~~~~~~~~~~~~~

    Contains microsync models.
"""
import dataclasses

from . import defaults, serde
from .hints import AnyStr, Int, Nothing, Str, StrAnyDict, StrTuple, Type


@dataclasses.dataclass
class VCS:
    """
    Represents template version control specific state.
    """
    depth: Int = defaults.VCS_DEPTH
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
    Represents the state for a repository.
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
