"""
    microsync/results
    ~~~~~~~~~~~~~~~~~

    Contains functionality for encapsulating the result of a call.
"""
import dataclasses

import sh

from . import defaults, errors, loggers
from .hints import Bool, Error, Int, OptionalError, Str

LOG = loggers.get_logger()


@dataclasses.dataclass
class Result:
    """
    Simple type that contains execution results.
    """
    success: Bool
    stdout: Str = defaults.RESULT_STDOUT
    stderr: Str = defaults.RESULT_STDERR
    error: OptionalError = defaults.RESULT_ERROR

    @property
    def exit_code(self) -> Int:
        return int(not self.success)

    def __bool__(self) -> Bool:
        return self.success


def success(stdout: Str = defaults.RESULT_STDOUT,
            stderr: Str = defaults.RESULT_STDERR) -> Result:
    """
    Create a successful result with the given stdout/stderr.

    :param stdout: Stdout of the call
    :param stderr: Stderr of the call
    :return: Successful result
    """
    return Result(True, stdout, stderr)


def failure(stdout: Str = defaults.RESULT_STDOUT,
            stderr: Str = defaults.RESULT_STDERR) -> Result:
    """
    Create a failed result with the given stdout/stderr.

    :param stdout: Stdout of the call
    :param stderr: Stderr of the call
    :return: Failed result
    """
    return Result(False, stdout, stderr)


def error(exc: Error,
          stdout: Str = defaults.RESULT_STDOUT,
          stderr: Str = defaults.RESULT_STDERR) -> Result:
    """
    Create an error result with the given stdout/stderr/exception.

    :param exc: Exception raised
    :param stdout: Stdout of the call
    :param stderr: Stderr of the call
    :return: Errored result
    """
    return Result(False, stdout, stderr, exc)


def command(cmd: sh.RunningCommand) -> Result:
    """
    Create a result from a completed shell command.

    :param cmd: Shell command that ran
    :return: Result determined by success of shell command
    """
    return Result(success=cmd.exit_code == 0,
                  stdout=cmd.stdout.decode('utf-8'),
                  stderr=cmd.stderr.decode('utf-8'))


def inverse(result: Result) -> Result:
    """
    Create a result that is an inverse of the given result, e.g.
    if the given result is successful, the returned result will be a failure.

    :param result: Result to invert
    :return: Inverse success of the result
    """
    return Result(success=not result.success,
                  stdout=result.stdout,
                  stderr=result.stderr,
                  error=result.error)


def wrapper(func):
    """
    Wrap the retval of the function in a :class:`~microsync.results.Result`.
    """
    def decorator(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if isinstance(result, sh.RunningCommand):
                return command(result)
            return result
        except errors.StateFileNotFound as ex:
            return error(ex, stderr=f'Not a microsync repository; state file not found "{ex.path}"')
        except Exception as ex:
            raise ex
            return error(ex, stderr=str(ex))
    return decorator


def logger(func):
    """
    Log the retval of the function that returns a :class:`~microsync.result.Result`.
    """
    def decorator(*args, **kwargs):
        result = func(*args, **kwargs)
        if result.stdout:
            LOG.info(result.stdout)
        if result.stderr:
            LOG.error(result.stderr)
        if result.error and not result.stderr:
            LOG.error(str(result.error))
        return result
    return decorator
