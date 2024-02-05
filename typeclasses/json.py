"""A method for serializing values to JSON."""

from pathlib import Path
import typing

from typeclasses import typeclass

T = typing.TypeVar('T')  # pylint: disable=invalid-name


@typeclass(T)
def to_json(value: T) -> str:  # type: ignore[empty-body] # pylint: disable=unused-argument
    """Serialize a value to JSON."""


@to_json.instance(type(None))
def _to_json_none(_):
    return 'null'


@to_json.instance(bool)
def _to_json_bool(value):
    return 'true' if value else 'false'


@to_json.instance(str)
@to_json.instance(bytes)
@to_json.instance(Path)
def _to_json_string(string):
    return f'"{str(string)}"'


@to_json.instance(int)
@to_json.instance(float)
def _to_json_number(number):
    return str(number)


@to_json.instance(typing.Mapping, protocol=True)
def _to_json_mapping(mapping):
    members = ','.join(f'"{k}":{to_json(v)}' for k, v in mapping.items())
    return f'{{{members}}}'


@to_json.instance(typing.Iterable, protocol=True)
def _to_json_iterable(iterable):
    items = ','.join(to_json(x) for x in iterable)
    return f'[{items}]'
