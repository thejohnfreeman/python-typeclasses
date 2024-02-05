"""The (synchronous) functor type class."""

import itertools
import typing as t

from typeclasses.decorator import typeclass

F = t.TypeVar('F')  # pylint: disable=invalid-name

_NO_ARGUMENT: t.Any = object()


@typeclass(F)
def fmap(function: t.Callable, functor: F = _NO_ARGUMENT):
    """Recursively apply a function within a functor.

    By "recursive", we mean if a functor is nested, even with different types,
    e.g. a list of dicts, then :func:`fmap` will recurse into each level and
    apply :param:`function` at the "leaf" values.

    Parameters
    ----------
    function :
        A function to apply to the values within :param:`functor`. It must be
        able to handle any type found within :param:`functor`.
    functor :
        A functor. Known functors include lists, dicts, and other collections.

    Returns
    -------
    Functor
        A copy of :param:`functor` with the results of applying
        :param:`function` to all of its leaf values.
    """
    # Curry if no functor given.
    if functor is _NO_ARGUMENT:
        return lambda functor: fmap(function, functor)
    # Assume it is the identity functor.
    return function(functor)


@fmap.instance(t.Mapping, protocol=True)
@fmap.instance(dict)
def _fmap_mapping(function, mapping):
    values = _fmap_generator(function, mapping.values())
    kvs = itertools.zip_longest(mapping.keys(), values)
    return type(mapping)(kvs)


@fmap.instance(t.Iterator, protocol=True)
@fmap.instance(range)
def _fmap_generator(function, generator):
    for x in generator:
        yield fmap(function, x)


@fmap.instance(t.Iterable, protocol=True)
@fmap.instance(bytes)
@fmap.instance(frozenset)
@fmap.instance(list)
@fmap.instance(set)
@fmap.instance(tuple)
def _fmap_iterable(function, iterable):
    return type(iterable)(fmap(function, x) for x in iterable)


@fmap.instance(str)
def _fmap_str(function, string):
    return ''.join(map(function, string))
