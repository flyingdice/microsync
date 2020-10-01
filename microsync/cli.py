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


@app.command(short_help='Create a new microsync repository')
def init(
        template: Str = typer.Argument(
            ...,
            metavar='TEMPLATE',
            help='Source template repository, e.g. https://github.com/microsync/example-cookiecutter'
        ),
        path: Str = typer.Option(
            '.',
            '-p',
            '--path',
            help='Path to write rendered template repository, e.g. my_project'
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
    action(template, path, ref, force, interactive=not script)


@app.command(short_help='Show the microsync repository status')
def status(
        path: Str = typer.Argument(
            '.',
            metavar='PATH',
            exists=True,
            help='Path of local repository to get status of, e.g. my_project'
        )
) -> None:
    action = exit_wrapper(results.logger(actions.status))
    action(path)


@app.command(short_help='Show changes between microsync repository refs')
def diff(
        path: Str = typer.Argument(
            '.',
            metavar='PATH',
            exists=True,
            help='Path of local repository to sync, e.g. my_project'
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
    action(path, ref, interactive=not script)


@app.command(short_help='Show changes between local microsync repository and its src ref')
def drift(
        path: Str = typer.Argument(
            '.',
            metavar='PATH',
            exists=True,
            help='Path of local repository to sync, e.g. my_project'
        )
) -> None:
    action = exit_wrapper(results.logger(actions.drift))
    action(path)


@app.command(short_help='Sync local microsync repository with its source template')
def sync(
        path: Str = typer.Argument(
            '.',
            metavar='PATH',
            exists=True,
            help='Path of local repository to sync, e.g. my_project'
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
    action(path, ref, interactive=not script)


@app.command(short_help='Link existing microsync repository to source template that created it')
def link(
        template: Str = typer.Argument(
            ...,
            metavar='TEMPLATE',
            help='Source template repository, e.g. https://github.com/microsync/example-cookiecutter'
        ),
        path: Str = typer.Option(
            '.',
            '-p',
            '--path',
            help='Path of local repository to link, e.g. my_project'
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
    action(template, path, ref, interactive=not script)


@app.command(short_help='Unlink an existing repository from its template')
def unlink(
        path: Str = typer.Option(
            '.',
            '-p',
            '--path',
            help='Path of local repository to unlink, e.g. my_project'
        ),
) -> None:
    action = exit_wrapper(results.logger(actions.unlink))
    action(path)


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
