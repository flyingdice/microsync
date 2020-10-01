"""
    microsync/templates
    ~~~~~~~~~~~~~~~~~~~

    Contains functionality for interacting with template engines.
"""
from .. import errors
from ..hints import Str, Type
from . import base, cookiecutter
from .base import RenderedTemplate, Template, TemplateContext

__all__ = [
    'TemplateType',
    'for_type',
    'RenderedTemplate',
    'TemplateContext',
    'Template'
]


class TemplateType:
    """
    Known template types.
    """
    Cookiecutter = 'cookiecutter'


TYPES = {
    TemplateType.Cookiecutter: cookiecutter
}


def for_type(template_type: Str) -> Type[base.TT]:
    """
    Retrieve the template implementation for the given type.

    :param template_type: Template type to use
    :return: Template implementation
    """
    template = TYPES.get(template_type)
    if not template:
        raise errors.TemplateTypeNotSupported(template_type)

    return template.Template
