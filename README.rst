.. start-include

===========
typeclasses
===========

Extensible methods for Python mimicking typeclasses in Haskell.

.. image:: https://travis-ci.org/thejohnfreeman/python-typeclasses.svg?branch=master
   :target: https://travis-ci.org/thejohnfreeman/python-typeclasses
   :alt: Build status

.. image:: https://readthedocs.org/projects/python-typeclasses/badge/?version=latest
   :target: https://python-typeclasses.readthedocs.io/
   :alt: Documentation status

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

Many dynamically typed languages, like Python and JavaScript, lack ad hoc
polymorphism in the language, but developers can hand-implement it by
inspecting the argument types and dispatching to implementations accordingly.

I want a framework for implementing this pattern easily and correctly.


Technique
=========

In Haskell, no two functions can have the same name in the same scope.
However, a function from a type class can have a different implementation from
every instance of the class. At a function call site, how does Haskell know
which instance to use? It knows from the signature of the function that one of
the arguments or the return type mentions the type variable of the class. It
tries to unify that signature with the call site to fill in the type variable;
if it succeeds, then it selects the instance for that type.

(to be continued)

.. end-include
