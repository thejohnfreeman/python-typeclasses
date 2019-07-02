# pylint: disable=missing-docstring

from string import printable

from hypothesis import assume, given, HealthCheck, settings
from hypothesis.strategies import (
    none,
    booleans,
    floats,
    text,
    lists,
    dictionaries,
    recursive,
)

from typeclasses.hash import hexhash

json = recursive( # pylint: disable=invalid-name
    none() | booleans() | floats() | text(printable),
    lambda children: lists(children, 1) |
    dictionaries(text(printable), children, min_size=1),
)


@given(json)
def test_reflexive(value):
    assert hexhash(value) == hexhash(value)


@given(json, json)
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_injective(a, b):
    assume(a != b)
    assert hexhash(a) != hexhash(b)


def test_dict_literal_order():
    a = {'a': 1, 'b': 2}
    b = {'b': 2, 'a': 1}
    assert hexhash(a) == hexhash(b)


def test_dict_insert_order():
    a = {}
    a['a'] = 1
    a['b'] = 2

    b = {}
    b['b'] = 2
    b['a'] = 1

    assert hexhash(a) == hexhash(b)
