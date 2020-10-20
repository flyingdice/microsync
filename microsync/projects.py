"""
    microsync/projects
    ~~~~~~~~~~~~~~~~~~

    Contains functionality for managing projects.
"""
import os

from . import config, defaults, descriptors, porcelain, scratch, utils, vcs
from .hints import Bool, FilePath, Int, Nothing, Optional, Str


class Project:
    """
    Represents a microsync project.

    Projects exist in the following environments:

    1) A user-managed directory, e.g. the current working directory.
        In this situation, the user provides a path a local copy of their code repository.
    2) A microsync-managed directory, e.g. .microsync/github.com/my-org/my-template
        In this situation, microsync has made a local copy of a code repository on the file
        system. This repository is either the template for the user-managed directory, or
        one created from a 'src' URI.
    """
    def __init__(self,
                 name: Str,
                 path: FilePath,
                 state: config.State,
                 state_path: FilePath,
                 src: Str = None,
                 src_dir: Optional[FilePath] = None,
                 tmp_dir: Optional[FilePath] = None) -> Nothing:
        self.name = name
        self.path = path
        self.state = state
        self.state_path = state_path
        self.src = src or state.template.src
        self.src_dir = src_dir or os.path.join(path, 'src')
        self.tmp_dir = tmp_dir or os.path.join(path, 'tmp')
        self.scratch = scratch.new(self.tmp_dir)

    def __enter__(self) -> 'Project':
        self.scratch.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> Nothing:
        self.scratch.__exit__(exc_type, exc_val, exc_tb)

    @descriptors.cached
    def repo(self) -> vcs.Repository:
        """
        Repository for the project.

        :return: Repository
        """
        return porcelain.repo(
            src=self.src,
            dst=self.src_dir,
            options=self.state.template.vcs
        )

    @descriptors.cached
    def template(self) -> 'Template':
        """
        Template for the project.

        :return: Template
        """
        return template_from_state(self.state)

    def graft_dir(self) -> Str:
        """
        Create project specific temporary directory used for grafting.

        :return: Path to directory
        """
        return os.path.join(self.scratch.directory(prefix='graft'), self.name)

    def render_dir(self) -> Str:
        """
        Create project specific temporary directory used for rendering.

        :return: Path to directory
        """
        return os.path.join(self.scratch.directory(prefix='render'), self.name)


class Template:
    """

    """
    def __init__(self,
                 name: Str,
                 path: FilePath,
                 state: config.State) -> Nothing:
        self.name = name
        self.path = path
        self.state = state
        self.src_dir = os.path.join(path, 'src')
        self.tmp_dir = os.path.join(path, 'tmp')
        self.scratch = scratch.new(self.tmp_dir)

    def __enter__(self) -> 'Template':
        self.scratch.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> Nothing:
        self.scratch.__exit__(exc_type, exc_val, exc_tb)

    @descriptors.cached
    def repo(self):
        return porcelain.repo(
            self.state.template.src,
            self.src_dir,
            ref=self.state.template.ref,
            options=self.state.template.vcs
        )

    def graft_dir(self) -> Str:
        return os.path.join(self.scratch.directory(prefix='graft'), self.name)

    def render_dir(self) -> Str:
        return os.path.join(self.scratch.directory(prefix='render'), self.name)


def template_from_state(state: config.State) -> Template:
    """

    :param state:
    :return:
    """
    name = utils.src_to_name(state.template.src)
    path = utils.src_to_path(state.template.src)
    return Template(name, path, state)
    # path = os.path.dirname(path)
    # name = os.path.basename(path)
    # template_path = utils.src_to_src_path(state.template.src)
    #
    # #name = src_to_name(state.template.src)
    # #path = src_to_path(state.template.src)
    # return from_state(state, name, path, template_path, state_path)


def new(src: Str,
        ref: Str = defaults.TEMPLATE_REF,
        vcs_type: Str = defaults.VCS_TYPE,
        template_type: Str = defaults.TEMPLATE_TYPE,
        comparison_type: Str = defaults.COMPARISON_TYPE) -> Project:
    """

    :param src: Template source location
    :param ref: Version control reference of the source to checkout
    :param vcs_type: Type of version control system used
    :param template_type: Type of template engine used
    :param comparison_type: Type of comparison used
    :return: New project for the given config
    """
    state = config.new(src, ref, vcs_type, template_type, comparison_type)
    name = src_to_name(src)
    path = src_to_path(src)
    template_path = src_to_src_path(src)
    return from_state(state, name, path, template_path)


def exists(path: FilePath) -> Bool:
    """
    Check to see if project exists at the the given path.

    :param path: Path to project
    :return: True if project exists, False otherwise
    """
    return os.path.exists(path)


def read(path: FilePath) -> Project:
    """
    Create project from the given file path.

    :param path: Path to project/project state file to read
    :return: Project at the given file path
    """
    reader = read_cache if utils.within_root(path) else read_local
    return reader(path)

    # from cli is will be root path
    # from app it will be src path

    # name = os.path.basename(path)
    # state_path = config.resolve_path(path)
    # state = config.read(state_path)
    # #template_path = utils.src_to_src_path(state.template.src)
    #
    # #name = src_to_name(state.template.src)
    # #path = src_to_path(state.template.src)
    # return from_state(state, name, path, state_path)


def read_local(path: FilePath) -> Project:
    """

    :param path:
    :return:
    """
    print('READING LOCAL PROJECT')
    # TODO - this needs to be given the 'src' to use.
    path = utils.resolve_path(path)
    name = os.path.basename(path)
    state_path = config.resolve_path(path)
    state = config.read(state_path)
    src = porcelain.remote_url(path, state.template.vcs)

#    vc = vcs.vcs(state.template.vcs)
#    print(vc)




    src_dir = path
    #src_dir = utils.src_to_src_path(src)
    tmp_dir = utils.src_to_tmp_path(src)

    print(locals())

    return Project(name, path, state, state_path, src, src_dir, tmp_dir)
    #template_path = utils.src_to_src_path(state.template.src)

    #name = src_to_name(state.template.src)
    #path = src_to_path(state.template.src)
#    return from_state(state, name, path, state_path)


def read_cache(path: FilePath) -> Project:
    """
    ITS ASSUMED GIVEN PATH ../src dir
    :param path:
    :return:
    """
    print('READING CACHE PROJECT')
    path = utils.resolve_path(path)
    state_path = config.resolve_path(path)
    state = config.read(state_path)
    path = os.path.dirname(path)
    name = os.path.basename(path)
    src_dir = os.path.join(path, 'src')
    tmp_dir = os.path.join(path, 'tmp')
    print(locals())
    src = porcelain.remote_url(src_dir, state.template.vcs)
    #template_path = utils.src_to_src_path(state.template.src)

    print(locals())

    return Project(name, path, state, state_path, src, src_dir, tmp_dir)


    #name = src_to_name(state.template.src)
    #path = src_to_path(state.template.src)
    #return from_state(state, name, path, state_path)


def write(project: Project,
          path: FilePath) -> Int:
    """
    Write microsync project to the given path.

    :param project: Project to write
    :param path: Path to write project
    :return: Number of bytes written
    """
    return config.write(project.state, path)


def delete(project: Project) -> Nothing:
    """
    Delete the given microsync project.

    :param project: Project to delete
    :param path: Path to project state
    :return: Nothing
    """
    return config.delete(project.state_path)


def from_state(state: config.State,
               name: Str,
               path: FilePath,
               state_path: FilePath = defaults.STATE_FILE) -> Project:
    """
    Create project from the given microsync state.

    :param state: State to create project from
    :param state_path: Path where state file was read
    :return: Project
    """
    #name = src_to_name(state.template.src)
    #path = src_to_path(state.template.src)
    print(f'projects.from_state {name} {path} {state_path}')
    return Project(name, path, state, state_path)
    #return Project(state, state_path, name, path, template_path)


src_to_name = utils.src_to_name
src_to_full_name = utils.src_to_full_name
src_to_path = utils.src_to_path
src_to_src_path = utils.src_to_src_path



