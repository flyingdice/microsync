"""
    microsync/serde
    ~~~~~~~~~~~~~~~

    Contains functionality for serialization/deserialization.
"""
import dataclasses
import io
import json

from .hints import Any, AnyStr, FilePath, Int, Str, Type, TypeVar


class Encoder(json.JSONEncoder):
    """
    JSON encoder that supports additional types.
    """
    def default(self, o: Any) -> Any:
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


class Decoder(json.JSONDecoder):
    """
    JSON decoder that supports additional types.
    """


def loads(s: AnyStr) -> Any:
    """
    Deserialize the given JSON string.

    :param s: String to deserialize
    :return: Object deserialized from string
    """
    return json.loads(s, cls=Decoder)


def dumps(obj: Any) -> Str:
    """
    Serialize the given object to a JSON string.

    :param obj: Object to serialize
    :return: Object serialized as string
    """
    return json.dumps(obj, cls=Encoder, ensure_ascii=False, indent=2, sort_keys=True)


class SupportsJSONSerde:
    """
    Mixin that adds support for JSON based serde.
    """
    @classmethod
    def decode(cls: Type['T'], s: AnyStr) -> 'T':
        """
        Decode string to instance.

        :param s: JSON string to decode
        :return: Instance created from decoded JSON string
        """
        return cls(**loads(s))

    def encode(self: 'T') -> Str:
        """
        Encode instance to JSON string.

        :return: Instance encoded as JSON string.
        """
        return dumps(self)


T = TypeVar('T', bound=SupportsJSONSerde)


class SupportsFileSerde(SupportsJSONSerde):
    """
    Mixin that adds support for file based serde.
    """
    @classmethod
    def read(cls: Type[T], path: FilePath) -> T:
        """
        Create a new instance from a serialized copy stored in the given file.

        :param path: File path to read.
        :return: Instance deserialized from file
        """
        # TODO - Find all dataclass attrs and recurse?
        with io.open(path, mode='r') as f:
            return cls.decode(f.read())

    def write(self: T, path: FilePath) -> Int:
        """
        Write a serialized copy of the instance to the given file.

        :param path: File path to write.
        :return: Number of bytes written to file.
        """
        with io.open(path, mode='w') as f:
            return f.write(self.encode())
