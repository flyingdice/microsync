"""
    microsync/vcs/git
    ~~~~~~~~~~~~~~~~~

    Contains version control system implementation for `git`.
"""
import logging
import os

import sh

from .. import defaults, models, results, utils
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
                 options: models.VCS) -> Nothing:
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
        self.git.reset('--hard', 'origin/master')

    def update(self) -> Nothing:
        """
        Pull down and merge any remote modifications.

        :return: Nothing
        """
        LOG.info('Checkout and pull master for %s', self)
        self.git.checkout('master')
        self.git.pull()


class VersionControl(base.VersionControl):
    """
    Class that represents the `git` version control system.
    """
    def local(self,
              src: Str,
              dst: Str,
              ref: OptionalStr = defaults.TEMPLATE_REF,
              options: models.VCS = models.VCS()) -> Repository:
        """
        Create a repository from a local file path.

        :param src: Source location where repository was originally retrieved
        :param dst: Output path where repository was originally saved
        :param ref: Version control reference of the source to checkout
        :param options: VCS options to use
        :return: Repository containing code on local file system
        """
        dst = utils.resolve_path(dst)
        return Repository(self, src, dst, ref=ref, options=options)

    def get(self,
            src: Str,
            dst: Str,
            ref: OptionalStr = defaults.TEMPLATE_REF,
            options: models.VCS = models.VCS()) -> Repository:
        """
        Retrieve a repository based on the given configuration.

        :param src: Source location of repository to retrieve
        :param dst: Output path where repository should be saved
        :param ref: Version control reference of the source to checkout
        :param options: VCS options to use
        :return: Repository containing code on local file system
        """
        dst = os.path.join(dst, repo_name(src))

        LOG.info('Cloning %s to %s with depth=%s', src, dst, options.depth)
        sh.git.clone(src, dst, depth=options.depth)

        if ref:
            LOG.info('Checking out ref %s', ref)
            sh.git.checkout(ref, _cwd=dst)

        return Repository(self, src, dst, ref, options)


def repo_name(src: Str) -> Str:
    """
    Get name of repository from template source.

    :param src:
    :return:
    """
    return os.path.splitext(os.path.basename(src))[0]
