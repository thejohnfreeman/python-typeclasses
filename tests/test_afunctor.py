"""Test asynchronous functor."""

import typing as t

import pytest  # type: ignore

from typeclasses.afunctor import afmap


async def times2(x):  # pylint: disable=invalid-name
    return x * 2


@pytest.mark.asyncio
async def test_afmap_str():
    assert await afmap(times2, 'test') == 'tteesstt'


@pytest.mark.asyncio
async def test_afmap_btes():
    assert await afmap(times2, bytes([1, 2, 3])) == bytes([2, 4, 6])


@pytest.mark.asyncio
async def test_afmap_dict():
    assert await afmap(times2, {'a': 1, 'b': 2}) == {'a': 2, 'b': 4}


@pytest.mark.asyncio
async def test_afmap_frozenset():
    assert await afmap(times2, frozenset({1, 2, 3})) == frozenset({2, 4, 6})


@pytest.mark.asyncio
async def test_afmap_list():
    assert await afmap(times2, [1, 2, 3]) == [2, 4, 6]


@pytest.mark.asyncio
async def test_afmap_range():
    assert isinstance(await afmap(times2, range(3)), t.AsyncGenerator)


@pytest.mark.asyncio
async def test_afmap_set():
    assert await afmap(times2, {1, 2, 3}) == {2, 4, 6}


@pytest.mark.asyncio
async def test_afmap_tuple():
    assert await afmap(times2, (1, 2, 3)) == (2, 4, 6)


@pytest.mark.asyncio
async def test_dict_of_list():
    assert await afmap(times2, {'xs': [1, 2, 3]}) == {'xs': [2, 4, 6]}


@pytest.mark.asyncio
async def test_args_and_kwargs():
    actual = await afmap(times2, ((1, 2), {'xs': [3, 4]}))
    assert actual == ((2, 4), {'xs': [6, 8]})
