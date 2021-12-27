.. PyDataStructs documentation master file, created by
   sphinx-quickstart on Sun Oct 17 19:57:08 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyDataStructs's documentation!
=========================================

This project aims to be a Python package for various data
structures in computer science. We are also working on the
development of algorithms including their parallel implementations.
To the best of our knowledge, a well-designed library/package which
has covered most of the data structures and algorithms doesn't exist yet.

Once the software design becomes more stable after a few releases of
this package in the near future, we also aim to provide APIs for the
code in C++ and Java as well.

.. note::

   This project is under active development and contributions are welcome.

Installation
============

After changing your directory to project root, you can
install the package by running the following command,

``python scripts/build/install.py``

For development purposes, i.e., if you intend to be a contributor,

``python scripts/build/develop.py``

For building documentation execute the following commands one after
the other,

1. ``pip install -r docs/requirements.txt``
2. ``sphinx-build -b html docs/source/ docs/build/html``

Make sure that your python version is at least ``3.8``.

Why PyDataStructs?
==================

1. **Single package for all your data structures and algorithms** - We have and are
   implementing many popular and useful data structures and algorithms.

2. **Consistent and Clean Interface** - The APIs we have provided are **consistent** with each other,
   **clean** and **easy to use**. We make sure of that before adding any new data structure or algorithm.

3. **Well Tested** - We thoroughly test our code before making any new addition to PyDataStructs.
   **99 percent** lines of our code have already been tested by us.

So, **you can easily rely on PyDataStructs** for any data structure or algorithm you want to use
**without worrying about implementing** it **from scratch**. Everything is just a few calls away.

Why do we use Python?
=====================

As we know Python is an interpreted language and hence is
slow compared to C++, the most popular language for competitive programming.
We still decided to use Python because the software development can happen
at a much faster pace and it is much easier to test various software designs
and APIs as coding them out takes no time. However, keeping the need of the
users in mind, we will shift to C++ backend,  which will happen quickly as
we would be required to just translate the tested code rather than writing it
from scratch, after a few releases with APIs available for all the languages.

Contents
========

.. toctree::
   :maxdepth: 1

   tutorials.rst
   pydatastructs_sphinx_graphs
   contributing.rst
   authors.rst
   pydatastructs/pydatastructs.rst
