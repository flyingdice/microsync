"""
    microsync/templates/base
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Contains functionality common to all template languages.
"""
import abc

from .. import defaults, vcs
from ..hints import Bool, FilePath, Nothing, StrAnyDict, Type, TypeVar


class TemplateContext(metaclass=abc.ABCMeta):
    """
    Abstract class that represents context data necessary to render a template.
    """
    def __init__(self: 'CT', template: 'TT', variables: StrAnyDict) -> Nothing:
        self.template = template
        self.variables = variables


CT = TypeVar('VT', bound=TemplateContext)


class RenderedTemplate(metaclass=abc.ABCMeta):
    """
    Abstract class that represents a template that has been rendered.
    """
    def __init__(self: 'RT', template: 'TT', path: FilePath, context: TemplateContext) -> Nothing:
        self.template = template
        self.path = path
        self.context = context


RT = TypeVar('RT', bound=RenderedTemplate)


class Template(metaclass=abc.ABCMeta):
    """
    Abstract class that represents a template.
    """
    def __init__(self: 'TT', repo: vcs.Repository) -> Nothing:
        self.repo = repo

    @abc.abstractmethod
    def context(self: Type['TT'],
                variables: StrAnyDict,
                interactive: Bool = defaults.RENDER_INTERACTIVE) -> Type[CT]:
        """
        Generate context data necessary to render this template.

        :param variables: User defined variables from microsync state file
        :type variables: :class:`~microsync.hints.StrAnyDict`
        :param interactive: Flag indicating execution is interactive and can prompt for user input
        :type interactive: :class:`~microsync.hints.Bool`
        :return: Context data to use for rendering
        :rtype: :class:`~microsync.templates.base.TemplateContext`
        """
        raise NotImplementedError('Derived classes must implement this method')

    @abc.abstractmethod
    def render(self: Type['TT'],
               path: FilePath,
               context: Type[CT],
               force: Bool = defaults.RENDER_FORCE) -> Type[RT]:
        """
        Render our source code repository template using the given variables and write
        it to the destination path.

        :param path: Path where rendered template should be written
        :type path: :class:`~microsync.hints.FilePath`
        :param context: TemplateContext to use for rendering
        :type context: :class:`~microsync.templates.base.TemplateContext`
        :param force: Flag indicating if output path should be overwritten if it already exists
        :type force: :class:`~microsync.hints.Bool`
        :param interactive: Flag indicating execution is interactive and can prompt for user input
        :type interactive: :class:`~microsync.hints.Bool`
        :return: A template rendered from a local source code repository
        :rtype: :class:`~microsync.templates.base.RenderedTemplate`
        """
        raise NotImplementedError('Derived classes must implement this method')


TT = TypeVar('TT', bound=Template)
