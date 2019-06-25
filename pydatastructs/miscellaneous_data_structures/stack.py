
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

    implementation : str
        Implementation to be used for stack.
        By default, 'array'
        Currently only supports 'array'
        implementation.
    maxsize : int
        The maximum size of the stack.
        For array implementation.
    top : int
        The top element of the stack.
        For array implementation.
    items : OneDimensionalArray
        Optional, by default, None
        The inital items in the stack.
        For array implementation.
    dtype : A valid python type
        Optional, by default int if item
        is None, otherwise takes the data
        type of OneDimensionalArray
        For array implementation.

    Example
    =======

    >>> from pydatastructs import Stack
    >>> s = Stack(maxsize=5, top=0)
    >>> s.push(1)
    >>> s.push(2)
    >>> s.push(3)
    >>> str(s)
    '[1, 2, 3, None, None]'
    >>> s.pop()
    3
    """

    def __new__(cls, implementation='array', **kwargs):
        if implementation == 'array':
            return ArrayStack(
                kwargs.get('maxsize', None),
                kwargs.get('top', None),
                kwargs.get('items', None),
                kwargs.get('dtype', int))
        raise NotImplementedError(
                "%s hasn't been implemented yet."%(implementation))

    def push(self, *args, **kwargs):
        raise NotImplementedError(
            "This is an abstract method.")

    def pop(self, *args, **kwargs):
        raise NotImplementedError(
              "This is an abstract method.")

class ArrayStack(Stack):

    def __new__(cls, maxsize=None, top=0, items=None, dtype=int):
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
        obj = object.__new__(cls)
        obj.maxsize, obj.top, obj.items, obj.dtype = \
            maxsize, top, items, items._dtype
        return obj

    def push(self, x):
        if self.top == self.maxsize:
            raise ValueError("Stack is full.")
        self.items[self.top] = self.dtype(x)
        self.top += 1

    def pop(self):
        if self.top == 0:
            raise ValueError("Stack is already empty.")
        self.top -= 1
        r = self.items[self.top]
        self.items[self.top] = None
        return r

    def __str__(self):
        """
        Used for printing.
        """
        return str(self.items._data)
