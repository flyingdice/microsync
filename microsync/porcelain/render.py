"""
    microsync/porcelain/render
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Contains porcelain functions for rendering.
"""
from .. import defaults, models, templates, vcs
from ..hints import Bool, Str, StrAnyDict


def render(repo: vcs.Repository,
           path: Str,
           variables: StrAnyDict,
           force: Bool = defaults.RENDER_FORCE,
           interactive: Bool = defaults.RENDER_INTERACTIVE,
           options: models.Engine = models.Engine()) -> templates.RenderedTemplate:
    """
    Porcelain function for `render`.

    This is responsible for using the user selected template engine to
    render a local template directory and optionally prompt the user for input to
    define variables.

    :param repo: Template repository to render
    :param path: Output file path where rendered template is saved
    :param variables: Variables to render template with
    :param force: Flag indicating if output path should be overwritten if it already exists
    :param interactive: Flag indicating render is interactive and can prompt for user input
    :param options: Options to customize template engine
    :return: Rendered template
    """
    template = templates.for_type(options.type)(repo)
    context = template.context(variables, interactive)
    return template.render(path, context, force)


def render_context(repo: vcs.Repository,
                   path: Str,
                   context: templates.TemplateContext,
                   force: Bool = defaults.RENDER_FORCE,
                   options: models.Engine = models.Engine()) -> templates.RenderedTemplate:
    """
    Porcelain function for `render_context`.

    This is responsible for using the user selected template engine to
    render a local template directory with the given context.

    :param repo: Template repository to render
    :param path: Output file path where rendered template is saved
    :param context: Generated context to use for rendering.
    :param force: Flag indicating if output path should be overwritten if it already exists
    :param options: Options to customize template engine
    :return: Rendered template
    """
    template = templates.for_type(options.type)(repo)
    return template.render(path, context, force)
