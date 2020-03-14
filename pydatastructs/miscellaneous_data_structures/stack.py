from pydatastructs.linear_data_structures import DynamicOneDimensionalArray
from pydatastructs.utils.misc_util import _check_type, NoneType
from copy import deepcopy as dc

__all__ = [
    'Stack'
]

class Stack(object):
    """Representation of stack data structure

    Parameters
    ==========

    implementation : str
        Implementation to be used for stack.
        By default, 'array'
        Currently only supports 'array'
        implementation.
    items : list/tuple
        Optional, by default, None
        The inital items in the stack.
        For array implementation.
    dtype : A valid python type
        Optional, by default NoneType if item
        is None, otherwise takes the data
        type of DynamicOneDimensionalArray
        For array implementation.

    Examples
    ========

    >>> from pydatastructs import Stack
    >>> s = Stack()
    >>> s.push(1)
    >>> s.push(2)
    >>> s.push(3)
    >>> str(s)
    '[1, 2, 3]'
    >>> s.pop()
    3

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
        raise NotImplementedError(
              "This is an abstract method.")

    @property
    def peek(self):
        raise NotImplementedError(
              "This is an abstract method.")

class ArrayStack(Stack):
    
    __slots__ = ['items']

    def __new__(cls, items=None, dtype=NoneType):
        if items is None:
            items = DynamicOneDimensionalArray(dtype, 0)
        else:
            items = DynamicOneDimensionalArray(dtype, items)
        obj = object.__new__(cls)
        obj.items = items
        return obj

    def push(self, x):
        if self.is_empty:
            self.items._dtype = type(x)
        self.items.append(x)

    def pop(self):
        if self.is_empty:
            raise IndexError("Stack is empty")

        top_element = dc(self.items[self.items._last_pos_filled])
        self.items.delete(self.items._last_pos_filled)
        return top_element

    @property
    def is_empty(self):
        return self.items._last_pos_filled == -1

    @property
    def peek(self):
        return self.items[self.items._last_pos_filled]

    def __len__(self):
        return self.items.size

    def __str__(self):
        """
        Used for printing.
        """
        return str(self.items._data)
