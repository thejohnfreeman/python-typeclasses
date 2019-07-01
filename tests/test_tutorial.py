"""Test the tutorial from the documentation."""

# pylint: disable=invalid-name

from dataclasses import dataclass
import typing

import pytest  # type: ignore

from typeclasses import typeclass

T = typing.TypeVar('T')


@typeclass(T)
def to_json(value: T) -> str:  # pylint: disable=unused-argument
    """Serialize a value to JSON."""


@to_json.instance(str)
def _to_json_str(s):
    return f'"{s}"'


@to_json.instance(int)
@to_json.instance(float)
def _to_json_number(n):
    return str(n)


@to_json.instance(typing.Mapping, protocol=True)
def _to_json_mapping(m):
    return '{' + ','.join(f'"{k}":{to_json(v)}' for k, v in m.items()) + '}'


@to_json.instance(typing.Iterable, protocol=True)
def _to_json_iterable(xs):
    return '[' + ','.join(to_json(x) for x in xs) + ']'


@dataclass
class Person:
    name: str


@to_json.instance(Person)
def _to_json_person(person):
    return f'{{"name":{to_json(person.name)}}}'


def test_str():
    assert to_json('hello') == '"hello"'


def test_int():
    assert to_json(100) == '100'


def test_float():
    assert to_json(3.14) == '3.14'


def test_ints():
    assert to_json([1, 2, 3]) == '[1,2,3]'


def test_protocol_order():
    assert to_json({'x': 1, 'y': 2}) == '{"x":1,"y":2}'


def test_persons():
    assert to_json([Person(name='John')]) == '[{"name":"John"}]'


def test_missing_instance():
    with pytest.raises(NotImplementedError):
        to_json(True)


def test_name():
    assert to_json.__name__ == 'to_json'


def test_docstring():
    assert to_json.__doc__ == 'Serialize a value to JSON.'
