"""A method for content hashing values."""

import hashlib
import operator
import pickle
import typing as t

from typeclasses import typeclass

T = t.TypeVar('T')  # pylint: disable=invalid-name


@typeclass(T)
def add_bytes(stream, value: T):
    """Serialize a value to a byte stream."""
    stream.update(pickle.dumps(value))


@add_bytes.instance(t.Mapping, protocol=True)
def _add_bytes_mapping(stream, mapping):
    # We have to canonicalize the order of keys.
    items = sorted(mapping.items(), key=operator.itemgetter(0))
    for k, v in items:
        add_bytes(stream, k)
        add_bytes(stream, v)


def fhash(value, algorithm=hashlib.sha256):
    stream = algorithm()
    add_bytes(stream, value)
    return stream
