"""
    microsync/vcs/base
    ~~~~~~~~~~~~~~~~~~

    Contains base classes for all version control system implementations.
"""
import abc

from .. import defaults, models, results
from ..hints import Bool, FilePath, Nothing, OptionalStr, Str, Type, TypeVar


class Repository(metaclass=abc.ABCMeta):
    """
    Abstract class that represents a code repository in a version control system.
    """
    def __init__(self: 'RT',
                 vc: 'VT',
                 src: Str,
                 path: FilePath,
                 ref: OptionalStr,
                 options: models.VCS) -> Nothing:
        self.vc = vc
        self.src = src
        self.path = path
        self.ref = ref
        self.options = options

    def __repr__(self):
        return '<{}({!r})>'.format(self.__class__.__name__, str(self))

    def __str__(self):
        return f'{self.src} at {self.path}'

    @abc.abstractmethod
    def is_valid(self) -> Bool:
        """
         Check to see if the repository is valid.

         :return: True if valid, False otherwise.
         """
        raise NotImplementedError('Derived classes must implement this method')

    @abc.abstractmethod
    def is_clean(self) -> results.Result:
        """
        Check to see if the repository is clean.

        :return: Result indicating repository status
        """
        raise NotImplementedError('Derived classes must implement this method')

    @abc.abstractmethod
    def is_dirty(self) -> results.Result:
        """
        Check to see if the repository is dirty.

        :return: Result indicating repository status
        """
        raise NotImplementedError('Derived classes must implement this method')

    @abc.abstractmethod
    def check_patch(self, patch: Str) -> results.Result:
        """
        Check to see if the given patch can be applied without conflicts.

        :param patch: Patch to check
        :return: Result indicating check status
        """
        raise NotImplementedError('Derived classes must implement this method')

    @abc.abstractmethod
    def apply_patch(self, patch: Str, commit_message: Str) -> results.Result:
        """
        Apply the given patch and commit with the given message.

        :param patch: Patch to apply
        :param commit_message: Message of commit for patch
        :return: Result indicating apply status
        """
        raise NotImplementedError('Derived classes must implement this method')

    @abc.abstractmethod
    def commit_id(self: 'RT') -> Str:
        """
        Retrieve identifier for the current commit on the local.

        :return: Commit identifier
        """
        raise NotImplementedError('Derived classes must implement this method')

    @abc.abstractmethod
    def commit_subject(self: 'RT', ref: Str) -> Str:
        """
        Retrieve commit message "subject" (short version) for the given ref.

        :param ref: Commit identifier to get subject for
        :return: Commit message subject line
        """
        raise NotImplementedError('Derived classes must implement this method')

    @abc.abstractmethod
    def remote_commit_id(self: 'RT') -> Str:
        """
        Retrieve identifier for the latest commit on the remote.

        :return: Commit identifier
        """
        raise NotImplementedError('Derived classes must implement this method')

    @abc.abstractmethod
    def reset(self: 'RT') -> Nothing:
        """
        Undo any local modifications/commits and reset to previous state.

        :return: Nothing
        """
        raise NotImplementedError('Derived classes must implement this method')

    @abc.abstractmethod
    def update(self: 'RT') -> Nothing:
        """
        Pull down and merge any remote modifications.

        :return: Nothing
        """
        raise NotImplementedError('Derived classes must implement this method')


RT = TypeVar('RT', bound=Repository)


class VersionControl(metaclass=abc.ABCMeta):
    """
    Abstract class that represents a version control system.
    """
    @abc.abstractmethod
    def local(self: Type['VT'],
              src: Str,
              dst: Str,
              ref: OptionalStr = defaults.TEMPLATE_REF,
              options: models.VCS = models.VCS()) -> Type[RT]:
        """
        Create a repository from a local file path.

        :param src: Source location where repository was originally retrieved
        :param dst: Output path where repository was originally saved
        :param ref: Version control reference of the source to checkout
        :param options: VCS options to use
        :return: Repository containing code on local file system
        """
        raise NotImplementedError('Derived classes must implement this method')

    @abc.abstractmethod
    def get(self: Type['VT'],
            src: Str,
            dst: Str,
            ref: OptionalStr = defaults.TEMPLATE_REF,
            options: models.VCS = models.VCS()) -> Type[RT]:
        """
        Retrieve a repository based on the given configuration.

        :param src: Source location of repository to retrieve
        :param dst: Output path where repository should be saved
        :param ref: Version control reference of the source to checkout
        :param options: VCS options to use
        :return: Repository containing code on local file system
        """
        raise NotImplementedError('Derived classes must implement this method')


VT = TypeVar('VT', bound=VersionControl)
