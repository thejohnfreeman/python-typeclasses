"""Test recursive synchronous fmap."""

import typing as t

from typeclasses.functor import fmap


def times2(x):
    return x * 2


def test_fmap_str():
    assert fmap(times2, 'test') == 'tteesstt'


def test_fmap_btes():
    assert fmap(times2, bytes([1, 2, 3])) == bytes([2, 4, 6])


def test_fmap_dict():
    assert fmap(times2, {'a': 1, 'b': 2}) == {'a': 2, 'b': 4}


def test_fmap_frozenset():
    assert fmap(times2, frozenset({1, 2, 3})) == frozenset({2, 4, 6})


def test_fmap_list():
    assert fmap(times2, [1, 2, 3]) == [2, 4, 6]


def test_fmap_range():
    assert isinstance(fmap(times2, range(3)), t.Generator)


def test_fmap_set():
    assert fmap(times2, {1, 2, 3}) == {2, 4, 6}


def test_fmap_tuple():
    assert fmap(times2, (1, 2, 3)) == (2, 4, 6)


def test_dict_of_list():
    assert fmap(times2, {'xs': [1, 2, 3]}) == {'xs': [2, 4, 6]}


def test_args_and_kwargs():
    assert fmap(times2, ((1, 2), {'xs': [3, 4]})) == ((2, 4), {'xs': [6, 8]})
