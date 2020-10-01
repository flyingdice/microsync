"""
    microsync/porcelain/context
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Contains functionality for `context`.
"""
from .. import defaults, models, templates, vcs
from ..hints import Bool, StrAnyDict


def context(repo: vcs.Repository,
            variables: StrAnyDict,
            interactive: Bool = defaults.CONTEXT_INTERACTIVE,
            options: models.Engine = models.Engine()) -> templates.TemplateContext:
    """
    Porcelain function for `context`.

    This is responsible for using the user selected template engine to
    generate context (input fed into the template engine) that would be used to render a template.

    :param repo: Template repository to render
    :param variables: Variables to generate context with
    :param interactive: Flag indicating render is interactive and can prompt for user input
    :param options: Options to customize template engine
    :return: Template context
    """
    template = templates.for_type(options.type)(repo)
    return template.context(variables, interactive)
