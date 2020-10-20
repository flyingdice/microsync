"""
    microsync/vcs/git
    ~~~~~~~~~~~~~~~~~

    Contains version control system implementation for `git`.
"""
import logging
import os

import sh

from .. import config, defaults, results, utils
from ..hints import Bool, FilePath, Nothing, OptionalStr, Str
from . import base

LOG = logging.getLogger(__name__)


class Repository(base.Repository):
    """
    Class that represents a `git` code repository.
    """
    def __init__(self,
                 vc: 'VersionControl',
                 src: Str,
                 path: FilePath,
                 ref: OptionalStr,
                 options: config.VCS) -> Nothing:
        super().__init__(vc, src, path, ref, options)
        self.git = sh.git.bake('--no-pager', _cwd=self.path, _tty_out=False)

    def is_valid(self) -> Bool:
        """
        Check to see if the repository is valid.

        :return: True if valid, False otherwise.
        """
        return os.path.exists(os.path.join(self.path, '.git'))

    @results.wrapper
    def is_clean(self) -> results.Result:
        """
        Check to see if the repository working tree is clean.

        :return: True if clean, False otherwise.
        """
        return results.inverse(self.is_dirty())

    @results.wrapper
    def is_dirty(self) -> results.Result:
        """
        Check to see if the repository working tree is dirty.

        :return: True if dirty, False otherwise.
        """
        LOG.info('Checking working tree dirty status for %s', self.path)
        stdout = self.git.status('--porcelain').stdout.decode('utf-8').strip()
        return results.Result(success=bool(stdout),
                              stdout=stdout)

    @results.wrapper
    def check_patch(self, patch: Str) -> results.Result:
        """
         Check to see if the given patch can be applied without conflicts.

         :param patch: Patch to check
         :return: Result indicating check status
         """
        LOG.info('Checking patch for %s', self.path)
        return self.git.apply('--check', _in=patch)

    @results.wrapper
    def apply_patch(self, patch: Str, commit_message: Str) -> results.Result:
        """
        Apply the given patch and commit with the given message.

        :param patch: Patch to apply
        :param commit_message: Message of commit for patch
        :return: Result indicating apply status
        """
        LOG.info('Applying patch for %s', self.path)
        self.git.apply('--3way', _in=patch)
        return self.git.commit('-m', commit_message, '--signoff')

    def remote_url(self) -> Str:
        """
        Retrieve the URL for the remote server where this repository is stored.

        This value should be identical to 'src' but can be leveraged for retrieving
        the value from the local file system when not available.

        :return: Repository remote URL.
        """
        return self.git.remote('get-url', 'origin').stdout.decode('utf-8').strip()

    def commit_id(self) -> Str:
        """
        Retrieve identifier for the current commit.

        :return: Commit identifier
        """
        LOG.info('Retrieving HEAD commit for local %s', self.path)
        return self.git('rev-parse', 'HEAD').stdout.decode('utf-8').strip()

    def commit_subject(self, ref: Str) -> Str:
        """
        Retrieve commit message "subject" (short version) for the given ref.

        :param ref: Commit identifier to get subject for
        :return: Commit message subject line
        """
        LOG.info('Retrieving commit message subject for %s', ref)
        entry = self.git.log('--format=%B', '-n 1', ref).stdout.decode('utf-8').strip()
        return utils.subject_line(entry)

    def remote_commit_id(self) -> Str:
        """
        Retrieve identifier for the latest commit on the remote.

        :return: Commit identifier
        """
        LOG.info('Retrieving HEAD commit for remote %s', self.src)
        return self.git('rev-parse', 'origin/master').stdout.decode('utf-8').strip()

    def reset(self) -> Nothing:
        """
        Undo any local modifications/commits and reset to previous state.

        :return: Nothing
        """
        LOG.info('Hard reset for %s', self)
        self.git.clean('--force', '-d', '-x')
        self.git.reset('--hard', self.options.origin)

    def update(self) -> Nothing:
        """
        Pull down and merge any remote modifications.

        :return: Nothing
        """
        LOG.info('Checkout and pull master for %s', self)
        self.git.checkout(self.options.branch)
        self.git.pull()

    def create_branch(self,
                      name: Str) -> results.Result:
        """
        Create a new branch in the repository.

        :param name: Name of the branch
        :return: Result indicating branch creation status
        """
        LOG.info('Checking out new branch %s for %s', name, self)
        self.reset()
        return self.git.checkout('-b', name)

    def push_branch(self,
                    remote: Str,
                    name: Str) -> results.Result:
        """
        Push a new branch to the remote repository.

        :param remote: Remote repository name
        :param name: Name of the branch
        :return: Result indicating branch push status
        """
        LOG.info('Pushing branch %s to %s/%s for %s', name, remote, name, self)
        return self.git.push(remote, name)

    def checkout(self,
                 ref: Str = defaults.VCS_BRANCH) -> Nothing:
        """
        Switch repository to the version of code defined by ref.

        :param ref: Reference to checkout
        :return: Nothing
        """
        LOG.info('Checking out ref %s for %s', ref, self)
        self.git.checkout(base.safe_ref(ref))


class VersionControl(base.VersionControl):
    """
    Class that represents the `git` version control system.
    """
    def is_repo_path(self, path: FilePath) -> Bool:
        """
        Check to see if the given file path is a valid repository.

        :param path: File path to check
        :return: True if valid repository path, False otherwise
        """
        return os.path.exists(os.path.join(path, '.git'))

    def repo_url(self, path: FilePath) -> Str:
        """
        Retrieve the URL for the remote server where this repository is stored
        for the given repository file path.

        :return: Repository remote URL.
        """
        return sh.git.remote('get-url', 'origin', _cwd=path, _tty_out=False).stdout.decode('utf-8').strip()

    def local(self,
              src: Str,
              dst: Str,
              ref: OptionalStr = defaults.TEMPLATE_REF,
              options: config.VCS = config.VCS()) -> Repository:
        """
        Create a repository from a local file path.

        :param src: Source location where repository was originally retrieved
        :param dst: Output path where repository was originally saved
        :param ref: Version control reference of the source to checkout
        :param options: VCS options to use
        :return: Repository containing code on local file system
        """
        dst = utils.resolve_path(dst)

        repo = Repository(self, src, dst, ref, options)
        repo.update()

        if ref:
            repo.checkout(ref)

        return repo

    def remote(self,
               src: Str,
               dst: Str,
               ref: OptionalStr = defaults.TEMPLATE_REF,
               options: config.VCS = config.VCS()) -> Repository:
        """
        Get a repository from a remote location.

        :param src: Source location of repository to retrieve
        :param dst: Output path where repository should be saved
        :param ref: Version control reference of the source to checkout
        :param options: VCS options to use
        :return: Repository containing code on local file system
        """
        dst = utils.resolve_path(dst)

        sh.git.clone(src, dst, depth=options.depth, _tty_out=False)
        if ref:
            sh.git.checkout(ref, _cwd=dst, _tty_out=False)

        return Repository(self, src, dst, ref, options)
