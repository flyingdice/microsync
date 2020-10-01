"""
    microsync/exceptions
    ~~~~~~~~~~~~~~~~~~~~

    Contains microsync specific exceptions.
"""
from . import hints, loggers

LOG = loggers.get_logger()


class MicrosyncException(Exception):
    """
    Base exception class for all microsync related exceptions.
    """


class StateFileException(MicrosyncException):
    """
    Base exception class for all state file related exceptions.
    """
    template = 'State file error using "{}"'

    def __init__(self, path: hints.FilePath):
        self.path = str(path)
        super().__init__(self.template.format(self.path))


class StateFileMalformed(StateFileException):
    """
    Exception raised when the state file cannot be properly read.
    """
    template = 'State file malformed at "{}"'


class StateFileNotFound(StateFileException):
    """
    Exception raised when the state file cannot be found.
    """
    template = 'State file not found at "{}"'


class TemplateException(MicrosyncException):
    """
    Base exception class for all template related exceptions.
    """


class TemplateTypeNotSupported(TemplateException):
    """
    Exception raised when trying to use a template type that is not supported.
    """
    template = 'Template type "{}" is not supported'

    def __init__(self, template_type: hints.Str) -> hints.Nothing:
        self.template_type = template_type
        super().__init__(self.template.format(self.template_type))


class TemplateSourceInvalid(TemplateException):
    """
    Exception raised when using an invalid template 'src' value.
    """
    template = 'Template src "{}" is not invalid'

    def __init__(self, src: hints.Str) -> hints.Nothing:
        self.src = src
        super().__init__(self.template.format(self.src))


class RenderedTemplateException(MicrosyncException):
    """
    Base exception class for all rendered template related exceptions.
    """


class RenderedTemplateDirectoryExists(RenderedTemplateException):
    """
    Exception raised when the output directory for rendering a template already exists
    and overwriting is not enabled.
    """
    template = 'Rendered template output directory "{}" already exists'

    def __init__(self, path: hints.FilePath):
        self.path = str(path)
        super().__init__(self.template.format(self.path))


class VCSException(MicrosyncException):
    """
    Base exception class for all VCS related exceptions.
    """


class VCSTypeNotSupported(VCSException):
    """
    Exception raised when trying to use a VCS type that is not supported.
    """
    template = 'VCS type "{}" is not supported'

    def __init__(self, vcs_type: hints.Str) -> hints.Nothing:
        self.vcs_type = vcs_type
        super().__init__(self.template.format(self.vcs_type))


class ComparisonException(MicrosyncException):
    """
    Base exception class for all comparison related exceptions.
    """


class ComparisonTypeNotSupported(ComparisonException):
    """
    Exception raised when trying to use a comparison type that is not supported.
    """
    template = 'Comparison type "{}" is not supported'

    def __init__(self, comparison_type: hints.Str) -> hints.Nothing:
        self.comparison_type = comparison_type
        super().__init__(self.template.format(self.comparison_type))


def error_logger(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except StateFileNotFound as ex:
            LOG.error(f'Not a microsync repository; state file not found "{ex.path}"')
        except Exception as ex:
            LOG.error(str(ex))
    return wrapper
