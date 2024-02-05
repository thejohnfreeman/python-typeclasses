.. start-include

===========
typeclasses
===========

Extensible methods for Python mimicking typeclasses in Haskell.

.. .. image:: https://readthedocs.org/projects/python-typeclasses/badge/?version=latest
..    :target: https://python-typeclasses.readthedocs.io/
..    :alt: Documentation status

.. image:: https://img.shields.io/pypi/v/typeclasses.svg
   :target: https://pypi.org/project/typeclasses/
   :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/pyversions/typeclasses.svg
   :target: https://pypi.org/project/typeclasses/
   :alt: Python versions supported


Motivation
==========

Some statically typed languages have `ad hoc polymorphism`_ where a function
can have multiple implementations depending on the types of its arguments. In
languages like C++ and Java, it is called function overloading. In Haskell, it
is accomplished with type classes.

.. _`ad hoc polymorphism`: https://en.wikipedia.org/wiki/Ad_hoc_polymorphism

Consider an example of writing a ``toJson`` function in C++. The function
takes a single value and returns a string, but it must be implemented
differently for each different type of value:

.. code-block:: cpp

   std::string toJson(int i);
   std::string toJson(double d);
   std::string toJson(std::string s);

Some implementations may be "recursive", and call the implementation for
another type:

.. code-block:: cpp

   template <typename T>
   std::string toJson(std::vector<T> const& xs) {
       ...
       for (T const& x : xs) {
           ... toJson(x) ...
       }
       ...
   }

Many dynamically typed languages, like Python and JavaScript, lack ad hoc
polymorphism in the language, but developers can implement it by hand by
inspecting the argument types and dispatching to implementations accordingly:

.. code-block:: python

   def to_json(value):
       if isinstance(value, int):
           return ...
       if isinstance(value, float):
           return ...
       if isinstance(value, str):
           return ...
       if isinstance(value, list):
           return '[' + ','.join(to_json(x) for x in value) + ']'

In addition to being a little uglier, this technique suffers from
a limitation: once we've defined the function, we can't add any more
overloads. Imagine we want to define a JSON serialization for our
user-defined type:

.. code-block:: python

   from ... import to_json

   @dataclass
   class Person:
       name: str

   def to_json_person(person):
       return f'{{"name":{to_json(person.name)}}}'


While this example works for serializing ``Person``, we won't be able to
serialize a ``list`` of ``Person`` because the implementation of ``to_json``
for ``list`` won't call ``to_json_person``.


Type Classes
============

In many languages, e.g. C++ and Java, two functions with the same name but
different types are called **overloads** of the name.
In Haskell, these overloads are not permitted: no two functions (or any other
values for that matter) can have the same name in the same scope.
However, type classes offer a way around this limitation.

A **type class** in Haskell is a group of polymorphic functions, called
**methods**, parameterized by a single **type variable**.
The type class only needs to *declare* the method signatures;
it does not need to provide any definitions.

An **instance** for a type class *defines* all the methods of the type class
for a specific **type argument** in the place of the type variable.
In other words, a type class has exactly one *polymorphic* declaration, but
many *monomorphic* instances, one for every possible type argument.
Thus, a method can have many definitions (i.e. implementations), one from each
instance, which means it can be overloaded.

At a method call site, how does Haskell know which overload, from which
instance, to use?
Haskell requires that the signature of the method in the type class
declaration mentions the type variable in one of its parameters or its return
type.
It tries to unify that polymorphic declaration signature with the call site to
fill in the type variable; if it succeeds, then it selects the monomorphic
instance for that type argument.


Tutorial
=========

How can we replicate type classes in Python?

Decorate a method signature with a call to ``typeclass``, giving it the
name of a type variable. The decorator will check the signature to make sure
that the type variable appears at least once in the type annotations of the
parameters. Unlike Haskell, Python cannot infer the *return type* at a call
site, so that path to instance discovery is impossible; the type variable
*must* be used as the type of at least one *parameter*.

.. code-block:: python

   T = typing.TypeVar('T')
   @typeclass(T)
   def to_json(value: T) -> str:
       """Serialize a value to JSON."""

We may optionally provide a default implementation. If we do not, the
default behavior is to raise a ``NotImplementedError`` diagnosing
a missing instance for the specific type variable.

The ``typeclass`` decorator will add an ``instance`` attribute to the method.
Use that to decorate monomorphic implementations, giving it the type argument:

.. code-block:: python

   @to_json.instance(str)
   def _to_json_str(s):
       return f'"{s}"'

We can decorate an implementation multiple times if it can serve multiple
instances:

.. code-block:: python

   @to_json.instance(int)
   @to_json.instance(float)
   def _to_json_number(n):
       return str(n)

We can define an implementation for all types structurally matching
a protocol_. Because it is presently impossible to infer the difference
between a protocol and a type, we must differentiate it for the decorator:

.. _protocol: https://mypy.readthedocs.io/en/latest/protocols.html

.. code-block:: python

   @to_json.instance(typing.Iterable, protocol=True)
   def _to_json_iterable(xs):
      return '[' + ','.join(to_json(x) for x in xs) + ']'

If a type argument matches multiple protocols, the instance that was first
defined will be chosen.

Now we can define instances for types whether we defined the type or imported
it.

.. code-block:: python

   @to_json.instance(Person)
   def _to_json_person(person):
       return f'{{"name":{to_json(person.name)}}}'

.. code-block:: python

   >>> to_json([Person(name='John')])
   [{"name":"John"}]


.. end-include
