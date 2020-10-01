"""
    microsync/hints
    ~~~~~~~~~~~~~~~

    Contains common type hint definitions.
"""
import os
import typing
from pathlib import Path

Any = typing.Any
AnyStr = typing.AnyStr
AnyDict = typing.Dict[typing.Any, typing.Any]
Args = typing.Any
Kwargs = typing.Any
Bool = bool
Bytes = bytes
Dict = dict
Error = Exception
FilePath = typing.Union[os.PathLike, str, Path]
IgnoreNamesFunction = typing.Callable[[str, typing.List[str]], typing.List[str]]
Int = int
IO = typing.IO
Nothing = None
OptionalBool = typing.Optional[bool]
OptionalError = typing.Optional[Exception]
OptionalStr = typing.Optional[str]
Str = str
StrAnyDict = typing.Dict[str, typing.Any]
StrDict = typing.Dict[str, str]
StrIterator = typing.Iterator[str]
StrList = typing.List[str]
StrTuple = typing.Tuple[str]
Type = typing.Type
TypeVar = typing.TypeVar
