"""The asynchronous functor type class."""

import asyncio
import itertools
import typing as t

from typeclasses.decorator import typeclass

F = t.TypeVar('F')  # pylint: disable=invalid-name

_NO_ARGUMENT: t.Any = object()


@typeclass(F)
async def afmap(function: t.Callable, functor: F = _NO_ARGUMENT):
    """Recursively apply an asynchronous function within a functor.

    By "recursive", we mean if a functor is nested, even with different types,
    e.g. a list of dicts, then :func:`afmap` will recurse into each level and
    apply :param:`function` at the "leaf" values.

    Calls of the function will be evaluated concurrently, thus there is no
    guaranteed order of execution (you want a monad for that).

    Parameters
    ----------
    function :
        A function to apply to the values within :param:`functor`. It must be
        able to handle any type found within :param:`functor`.
    functor :
        A functor. Known functors include lists, dicts, and other collections.

    Returns
    -------
    AsyncFunctor
        A copy of :param:`functor` with the results of applying
        :param:`function` to all of its leaf values.
    """
    # Curry if no functor given.
    if functor is _NO_ARGUMENT:
        return lambda functor: afmap(function, functor)
    # Assume it is the identity functor.
    return await function(functor)


@afmap.instance(t.Mapping, protocol=True)
@afmap.instance(dict)
async def _afmap_mapping(function, mapping):
    coros = (afmap(function, v) for v in mapping.values())
    values = await asyncio.gather(*coros)
    kvs = itertools.zip_longest(mapping.keys(), values)
    return type(mapping)(kvs)


@afmap.instance(t.Iterator, protocol=True)
@afmap.instance(range)
async def _afmap_generator(function, generator):
    # These type specializations are awaited unconditionally in :func:`afmap`.
    # If this function itself were a generator, it could not be awaited.
    # Instead, it must return an awaitable that returns an async generator.
    # Gross.
    async def generate():
        for x in generator:
            yield await afmap(function, x)

    return generate()


@afmap.instance(t.Iterable, protocol=True)
@afmap.instance(bytes)
@afmap.instance(frozenset)
@afmap.instance(list)
@afmap.instance(set)
@afmap.instance(tuple)
async def _afmap_iterable(function, iterable):
    ys = await asyncio.gather(*(afmap(function, x) for x in iterable))
    return type(iterable)(ys)


@afmap.instance(str)
async def _afmap_str(function, string):
    ys = await asyncio.gather(*map(function, string))
    return ''.join(ys)
