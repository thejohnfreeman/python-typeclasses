"""The :func:`typeclass` decorator."""

import functools
import inspect


def _empty():
    pass


def _docstring():
    """Just an empty function with a docstring."""


def _code(function):
    """Return the byte code for a function.

    If this Python interpreter does not supply the byte code for functions,
    then this function returns NaN so that all functions compare unequal.
    """
    return (
        function.__code__.co_code
        if hasattr(function, '__code__') else float('nan')
    )


def _is_empty(function):
    """Return whether a function has an empty body."""
    return _code(function) in (_code(_empty), _code(_docstring))


class TypeClassMethod:
    """A method of a type class.

    This docstring will be overwritten by that of the method's default
    implementation.
    """

    __name__: str

    def __init__(self, get_type_argument, default_implementation):
        """Construct a type class method.

        Parameters
        ----------
        get_type_argument :
            A function that, when passed ``*args`` and ``**kwargs`` for the
            method, will return the type argument for this class.
        default_implementation :
            The default implementation for the method, and source of its
            docstring.
        """
        self.get_type_argument = get_type_argument
        self.type_instances = {}
        self.protocol_instances = {}
        self.default_implementation = default_implementation

    def __call__(self, *args, **kwargs):
        type_argument = self.get_type_argument(*args, **kwargs)

        implementation = self.type_instances.get(type_argument, None)
        if implementation is not None:
            return implementation(*args, **kwargs)

        for protocol, implementation in self.protocol_instances.items():
            if issubclass(type_argument, protocol):
                return implementation(*args, **kwargs)

        if _is_empty(self.default_implementation):
            raise NotImplementedError(
                f'missing instance of {self.__name__} for {type_argument}'
            )

        return self.default_implementation(*args, **kwargs)

    def instance(self, type_argument, *, protocol=False):
        """Declare an instance for this type class method."""
        instances = (
            self.protocol_instances if protocol else self.type_instances
        )

        def decorator(implementation):
            instances[type_argument] = implementation
            return implementation

        return decorator


def typeclass(type_variable):
    """Declare a type class of a single method over a single type variable."""

    def decorator(default_implementation):
        sig = inspect.signature(default_implementation)
        names = [
            p.name
            for p in sig.parameters.values()
            if p.annotation == type_variable
        ]
        if not names:
            raise TypeError(
                f'type variable `{type_variable}` missing from '
                f'signature of method `{default_implementation.__name__}`'
            )
        name = names[0]

        def get_type_argument(*args, **kwargs):
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            return type(bound.arguments[name])

        method = TypeClassMethod(get_type_argument, default_implementation)
        method = functools.wraps(default_implementation)(method)
        return method

    return decorator
