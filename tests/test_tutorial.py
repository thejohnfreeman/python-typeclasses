"""Test the tutorial from the documentation."""

# pylint: disable=invalid-name

from dataclasses import dataclass

import pytest  # type: ignore

from typeclasses.json import to_json


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
        to_json(object())


def test_name():
    assert to_json.__name__ == 'to_json'


def test_docstring():
    assert to_json.__doc__ == 'Serialize a value to JSON.'
