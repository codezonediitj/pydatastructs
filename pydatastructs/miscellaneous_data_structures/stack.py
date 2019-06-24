
from __future__ import print_function, division
from pydatastructs.linear_data_structures import OneDimensionalArray
from copy import deepcopy as dc

__all__ = [
    'Stack'
]

_check_type = lambda a, t: isinstance(a, t)
NoneType = type(None)

class Stack(object):
    """Respresentation of stack data structure

    Parameters
    ==========

    max_size : int
        Maximum size of stack allowed

    Raises
    ======

    TypeError
        max_size argument should of type 'int'.

    Example
    =======

    >>> from pydatastructs import Stack
    >>> my_stack = Stack()
    >>> my_stack.push(1)
    >>> my_stack.push(2)
    >>> my_stack.pop()
    2
    >>> str(my_stack)
    <Stack length:[1]>
    """

    def __new__(cls, implementation='array', **kwargs):
        if implementation == 'array':
            return ArrayStack(
                kwargs.get('maxsize', None),
                kwargs.get('top', None),
                kwargs.get('items', None),
                kwargs.get('dtype', int))
        raise NotImplementedError(
                "LinkedListStack hasn't been implemented yet.")

    def initialize(self, *args, **kwargs):
        raise NotImplementedError(
                "This is an abstract method.")

    def push(self, *args, **kwargs):
        raise NotImplementedError(
            "This is an abstract method.")

    def pop(self, *args, **kwargs):
        raise NotImplementedError(
              "This is an abstract method.")

class ArrayStack(Stack):

    def __new__(maxsize=None, top=None, items=None, dtype=int):
        if not _check_type(maxsize, int):
            raise ValueError("maxsize is missing.")
        if not _check_type(top, int):
            raise ValueError("top is missing.")
        if items == None:
            items = OneDimensionalArray(dtype, maxsize)
        if not _check_type(items, OneDimensionalArray):
            raise ValueError("items is not of type, OneDimensionalArray")
        if items._size > maxsize:
            raise ValueError("Overflow, size of items %s is greater "
                            "than maxsize, %s"%(items._size, maxsize))
