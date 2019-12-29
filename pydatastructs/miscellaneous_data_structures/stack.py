from pydatastructs.linear_data_structures import DynamicOneDimensionalArray
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
	0
    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Stack_(abstract_data_type)
    """

    def __new__(cls, implementation='array', **kwargs):
        if implementation == 'array':
            return ArrayStack(
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

    @property
    def is_empty(self):
        return None

    @property
    def peek(self):
        return None

class ArrayStack(Stack):

    __slots__ = ['items', 'dtype']

    def __new__(cls, items=None, dtype=int):
        if items is None:
            items = DynamicOneDimensionalArray(dtype, 0)
        if not _check_type(items, DynamicOneDimensionalArray):
            raise ValueError("items is not of type, DynamicOneDimensionalArray")
        obj = object.__new__(cls)
        obj.items, obj.dtype = \
            items, items._dtype
        return obj

    def push(self, x):
        self.items.append(x)

    def pop(self):
        if(self.items._last_pos_filled==-1):
         raise ValueError("stack is empty")
        else:
         top_element = dc(self.items[self.items._last_pos_filled])
         self.items.delete(self.items._last_pos_filled)
         return top_element

    @property
    def is_empty(self):
        return self.items._last_pos_filled == -1

    @property
    def peek(self):
        return self.items[self.items._last_pos_filled]

    def __str__(self):
        """
        Used for printing.
        """
        return str(self.items._data)
