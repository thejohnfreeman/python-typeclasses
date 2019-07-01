from pathlib import Path
import typing

from typeclasses import typeclass

T = typing.TypeVar('T')


@typeclass(T)
def to_json(value: T) -> str:  # pylint: disable=unused-argument
    """Serialize a value to JSON."""


@to_json.instance(type(None))
def _to_json_none(none):
    return 'null'


@to_json.instance(bool)
def _to_json_bool(value):
    return 'true' if value else 'false'


@to_json.instance(str)
@to_json.instance(bytes)
@to_json.instance(Path)
def _to_json_str(s):
    return f'"{str(s)}"'


@to_json.instance(int)
@to_json.instance(float)
def _to_json_number(n):
    return str(n)


@to_json.instance(typing.Mapping, protocol=True)
def _to_json_mapping(m):
    members = ','.join(f'"{k}":{to_json(v)}' for k, v in m.items())
    return f'{{{members}}}'


@to_json.instance(typing.Iterable, protocol=True)
def _to_json_iterable(xs):
    items = ','.join(to_json(x) for x in xs)
    return f'[{items}]'
