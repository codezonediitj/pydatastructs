from pydatastructs.linear_data_structures import DynamicOneDimensionalArray, SinglyLinkedList
from pydatastructs.miscellaneous_data_structures._backend.cpp import _stack
from pydatastructs.utils.misc_util import (
    _check_type, NoneType, Backend,
    raise_if_backend_is_not_python)
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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

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
        backend = kwargs.get('backend', Backend.PYTHON)
        if implementation == 'array':
            items = kwargs.get('items', None)
            dtype = kwargs.get('dtype', int)
            if backend == Backend.CPP:
                return _stack.ArrayStack(items, dtype)

            return ArrayStack(items, dtype)
        if implementation == 'linked_list':
            raise_if_backend_is_not_python(cls, backend)

            return LinkedListStack(
                kwargs.get('items', None)
            )
        raise NotImplementedError(
            "%s hasn't been implemented yet."%(implementation))

    @classmethod
    def methods(cls):
        return ['__new__']

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

    def __new__(cls, items=None, dtype=NoneType,
                **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
        if items is None:
            items = DynamicOneDimensionalArray(dtype, 0)
        else:
            items = DynamicOneDimensionalArray(dtype, items)
        obj = object.__new__(cls)
        obj.items = items
        return obj

    @classmethod
    def methods(cls):
        return ['__new__', 'push', 'pop', 'is_emtpy',
        'peek', '__len__', '__str__']

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
        return self.items._num

    def __str__(self):
        """
        Used for printing.
        """
        return str(self.items._data)


class LinkedListStack(Stack):

    __slots__ = ['stack']

    def __new__(cls, items=None, **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
        obj = object.__new__(cls)
        obj.stack = SinglyLinkedList()
        if items is None:
            pass
        elif type(items) in (list, tuple):
            for x in items:
                obj.push(x)
        else:
            raise TypeError("Expected type: list/tuple")
        return obj

    @classmethod
    def methods(cls):
        return ['__new__', 'push', 'pop', 'is_emtpy',
        'peek', '__len__', '__str__']

    def push(self, x):
        self.stack.appendleft(x)

    def pop(self):
        if self.is_empty:
            raise IndexError("Stack is empty")
        return self.stack.popleft()

    @property
    def is_empty(self):
        return self.__len__() == 0

    @property
    def peek(self):
        return self.stack.head

    @property
    def size(self):
        return self.stack.size

    def __len__(self):
        return self.stack.size

    def __str__(self):
        elements = []
        current_node = self.peek
        while current_node is not None:
            elements.append(str(current_node))
            current_node = current_node.next
        return str(elements[::-1])
