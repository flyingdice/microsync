"""
    microsync/porcelain/status
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Contains functionality for `status`.
"""
import dataclasses

from .. import vcs
from ..hints import Str

HEADER_FORMAT = """
Local:
{status.local_ref} - {status.local_ref_subject}
 
Remote:
{status.remote_ref} - {status.remote_ref_subject}
"""

EQUAL_BODY_FORMAT = """
Your local repository is up-to-date.
"""

DIFF_BODY_FORMAT = """
Your local repository is out-of-date!
"""


@dataclasses.dataclass
class Status:
    """
    Represents the status of a repository.
    """
    local_ref: Str
    local_ref_subject: Str
    remote_ref: Str
    remote_ref_subject: Str

    @property
    def same(self):
        return self.local_ref == self.remote_ref

    def message_header(self):
        return HEADER_FORMAT.format(status=self)

    def message_body(self):
        if self.same:
            return EQUAL_BODY_FORMAT.format(status=self)
        else:
            return DIFF_BODY_FORMAT.format(status=self)

    def message(self):
        header = self.message_header()
        body = self.message_body()
        return header + body


def status(repo: vcs.Repository) -> Status:
    """
    Porcelain function for `status`.

    This is responsible for comparing the state a local repository to
    the origin template repository that created it.

    :param repo: Repository to get status of
    :return: Status of repository
    """
    local_ref = repo.commit_id()
    local_ref_subject = repo.commit_subject(local_ref)
    remote_ref = repo.remote_commit_id()
    remote_ref_subject = repo.commit_subject(remote_ref)

    return Status(local_ref, local_ref_subject, remote_ref, remote_ref_subject)
