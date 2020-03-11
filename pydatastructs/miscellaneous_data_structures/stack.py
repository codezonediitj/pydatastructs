from pydatastructs.linear_data_structures import DynamicOneDimensionalArray, SinglyLinkedList
from pydatastructs.utils.misc_util import _check_type, NoneType, LinkedListNode
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
        elif implementation == 'linkedlist':
            return LinkedListStack(
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
            raise ValueError("Stack is empty")

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


class LinkedListStack(Stack):

    def __new__(cls, items=None, dtype=NoneType):
        obj = object.__new__(cls)
        obj.stack = SinglyLinkedList()
        obj._dtype = dtype
        obj.front = obj.stack.head
        obj.tail = obj.stack.tail
        obj.size = 0
        if items is None:
            pass
        elif type(items) in (list, tuple):
            if len(items) != 0 and dtype is NoneType:
                obj._dtype = type(items[0])
            for x in items:
                if type(x) == obj._dtype:
                    obj.push(x)
                else:
                    raise TypeError("Expected %s but got %s"%(obj._dtype, type(x)))
        else:
            raise TypeError("Expected type: list/tuple")
        return obj

    def push(self, x):
        if self._dtype is NoneType:
            self._dtype = type(x)
        elif type(x) is not self._dtype:
            raise TypeError("Expected %s but got %s"%(self._dtype, type(x)))
        self.size += 1
        self.stack.append_left(x)
        if self.front is None:
            self.front = self.stack.head
        self.rear = self.stack.tail

    def pop(self):
        if self.is_empty:
            raise ValueError("Stack is empty")
        self.size -= 1
        return_value = self.stack.pop_left()
        self.front = self.stack.head
        self.rear = self.stack.tail
        return return_value

    @property
    def is_empty(self):
        return self.size == 0

    @property
    def peek(self):
        return self.front

    def __len__(self):
        return self.size

    def __str__(self):
        return str(self.stack)
