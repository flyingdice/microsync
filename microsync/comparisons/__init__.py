"""
    microsync/comparisons
    ~~~~~~~~~~~~~~~~~~~~~

    Contains functionality for comparisons.
"""
from .. import errors
from ..hints import Str, Type
from . import base, unidiff
from .base import Comparison, Diff

__all__ = [
    'ComparisonType',
    'for_type',
    'Comparison',
    'Diff'
]


class ComparisonType:
    """
    Known comparison types.
    """
    Unidiff = 'unidiff'


TYPES = {
    ComparisonType.Unidiff: unidiff,
}


def for_type(comparison_type: Str) -> Type[base.CT]:
    """
    Retrieve the comparison implementation for the given type.

    :param comparison_type: Logger type to use
    :return: Comparison implementation
    """
    comparison = TYPES.get(comparison_type)
    if not comparison:
        raise errors.ComparisonTypeNotSupported(comparison_type)

    return comparison.Comparison
