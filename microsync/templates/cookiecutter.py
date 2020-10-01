"""
    microsync/templates/cookiecutter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Contains functionality for Cookiecutter templates.
"""
import os

from cookiecutter import config, exceptions, generate, prompt

from .. import defaults, errors
from ..hints import Bool, FilePath, StrAnyDict
from . import base


class TemplateContext(base.TemplateContext):
    """
    Represents cookiecutter context used for rendering.
    """


class RenderedTemplate(base.RenderedTemplate):
    """
    Represents a rendered cookiecutter template.
    """


class Template(base.Template):
    """
    Represents a cookiecutter template.
    """
    def context(self,
                variables: StrAnyDict,
                interactive: Bool = defaults.RENDER_INTERACTIVE) -> TemplateContext:
        """
        Generate context data necessary to render this template.

        :param variables: User defined variables from microsync state file
        :param interactive: Flag indicating execution is interactive and can prompt for user input
        :return: Context data to use for rendering
        """
        # Load default cookiecutter config.
        user_config = config.get_user_config(default_config=True)

        # Generate cookiecutter context based on defaults, cookiecutter.json file, and user provided variables
        # that originate from the the microsync state file.
        context = generate.generate_context(
            context_file=os.path.join(self.repo.path, 'cookiecutter.json'),
            default_context=user_config['default_context'],
            extra_context=variables
        )

        # Render context so variables like '{{ cookiecutter.foo.bar }}' are converted to field values.
        variables = prompt.prompt_for_config(context, no_input=not interactive)
        return TemplateContext(self, variables)

    def render(self,
               path: FilePath,
               context: TemplateContext,
               force: Bool = defaults.RENDER_FORCE) -> RenderedTemplate:
        """
        Render our source code repository template using the given template context and write
        it to the destination path.

        :param path: Path where rendered template should be written
        :param context: TemplateContext to use for rendering
        :param force: Flag indicating if output path should be overwritten if it already exists
        :return: A template rendered from a local source code repository
        """
        try:
            # Generate files using context and write them into a directory in the output path.
            path = generate.generate_files(
                self.repo.path,
                context=dict(cookiecutter=context.variables),
                output_dir=path,
                overwrite_if_exists=force
            )
        except exceptions.OutputDirExistsException as ex:
            raise errors.RenderedTemplateDirectoryExists(path) from ex
        else:
            return RenderedTemplate(self, path, context)
