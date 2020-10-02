"""
    microsync/cli
    ~~~~~~~~~~~~~

    Contains command line interface (CLI) for `microsync`.
"""
import typer

from . import actions, loggers, meta, results
from .hints import Bool, OptionalStr, Str

__all__ = ['run']


LOG = loggers.get_logger()


app = typer.Typer(
    help=meta.TAGLINE,
    no_args_is_help=True,
    add_completion=False
)


@app.command(help='Create a new project')
def init(
        template: Str = typer.Argument(
            ...,
            metavar='TEMPLATE',
            help='Source template repository, e.g. https://github.com/microsync/example-cookiecutter'
        ),
        project: Str = typer.Option(
            '.',
            '-p',
            '--project',
            help='Path to write new project, e.g. my_project'
        ),
        ref: OptionalStr = typer.Option(
            None,
            '-r',
            '--ref',
            help='VCS reference to use such as commit hash, branch name, or tag'
        ),
        force: Bool = typer.Option(
            False,
            '-f'
            '--force',
            show_default=False,
            help='Force init and overwrite existing dst directory if it exists',
        ),
        script: Bool = typer.Option(
            False,
            '-s',
            '--script',
            show_default=False,
            help='Indicates this is being run as a script and is not interactive',
        ),
) -> None:
    action = exit_wrapper(results.logger(actions.init))
    action(template, project, ref, force, interactive=not script)


@app.command(help='Show project status')
def status(
        project: Str = typer.Argument(
            '.',
            metavar='PROJECT',
            exists=True,
            help='Path of project to use'
        )
) -> None:
    action = exit_wrapper(results.logger(actions.status))
    action(project)


@app.command(help='Show changes between template refs')
def diff(
        project: Str = typer.Argument(
            '.',
            metavar='PROJECT',
            exists=True,
            help='Path of project to use'
        ),
        ref: OptionalStr = typer.Option(
            None,
            '-r',
            '--ref',
            help='VCS reference to use such as commit hash, branch name, or tag'
        ),
        script: Bool = typer.Option(
            False,
            '-s',
            '--script',
            show_default=False,
            help='Indicates this is being run as a script and is not interactive',
        ),
) -> None:
    action = exit_wrapper(results.logger(actions.diff))
    action(project, ref, interactive=not script)


@app.command(help='Show changes between project and template')
def drift(
        project: Str = typer.Argument(
            '.',
            metavar='PROJECT',
            exists=True,
            help='Path of project to use'
        ),
        script: Bool = typer.Option(
            False,
            '-s',
            '--script',
            show_default=False,
            help='Indicates this is being run as a script and is not interactive',
        )
) -> None:
    action = exit_wrapper(results.logger(actions.drift))
    action(project, interactive=not script)


@app.command(help='Sync project with its template')
def sync(
        project: Str = typer.Argument(
            '.',
            metavar='PROJECT',
            exists=True,
            help='Path of project to use'
        ),
        ref: OptionalStr = typer.Option(
            None,
            '-r',
            '--ref',
            help='VCS reference to sync to such as commit hash, branch name, or tag'
        ),
        script: Bool = typer.Option(
            False,
            '-s',
            '--script',
            show_default=False,
            help='Indicates this is being run as a script and is not interactive',
        )
) -> None:
    action = exit_wrapper(results.logger(actions.sync))
    action(project, ref, interactive=not script)


@app.command(help='Link existing project to template that previously created it')
def link(
        template: Str = typer.Argument(
            ...,
            metavar='TEMPLATE',
            help='Source template repository, e.g. https://github.com/microsync/example-cookiecutter'
        ),
        project: Str = typer.Option(
            '.',
            '-p',
            '--project',
            help='Path of project to use'
        ),
        ref: OptionalStr = typer.Option(
            None,
            '-r',
            '--ref',
            help='VCS reference to use such as commit hash, branch name, or tag'
        ),
        script: Bool = typer.Option(
            False,
            '-s',
            '--script',
            show_default=False,
            help='Indicates this is being run as a script and is not interactive',
        )
) -> None:
    action = exit_wrapper(results.logger(actions.link))
    action(template, project, ref, interactive=not script)


@app.command(help='Unlink an existing project from its template')
def unlink(
        project: Str = typer.Option(
            '.',
            '-p',
            '--project',
            help='Path of project to use'
        ),
) -> None:
    action = exit_wrapper(results.logger(actions.unlink))
    action(project)


def exit_wrapper(func):
    """
    Wrap functions that return :class:`~microsync.results.Result` and raise a :class:`~typer.Exit`
    for unsuccessful results so the process exit code is non-zero.
    """
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result.exit_code != 0:
            raise typer.Exit(code=result.exit_code)
        return result
    return wrapper


def run():
    app(prog_name=meta.NAME)


if __name__ == '__main__':
    run()
