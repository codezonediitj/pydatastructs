from pydatastructs.linear_data_structures import DynamicOneDimensionalArray

__all__ = [
    'Queue'
]

class Queue(object):
    """Representation of queue data structure

    Examples
    ========

    >>> from pydatastructs import Queue
    >>> q = Queue(10)
    >>> q.append(1)
    >>> q.append(2)
    >>> q.append(3)
    >>> q.popleft()
    >>> q.len()
    1

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Queue_(abstract_data_type)
    """

    def __new__(cls, implementation='array', **kwargs):
        if implementation == 'array':
            return ArrayStack(
                kwargs.get('items', None),
                kwargs.get('dtype', int))
        raise NotImplementedError(
                "%s hasn't been implemented yet."%(implementation))

    def append(self, *args, **kwargs):
        raise NotImplementedError(
            "This is an abstract method.")

    def popleft(self, *args, **kwargs):
        raise NotImplementedError(
            "This is an abstract method.")


    @property
    def is_empty(self):
        return self.front == -1

    @property
    def is_full(self):
        return ((self.rear + 1) % self.size == self.front)

class ArrayStack(Stack):

    __slots__ = ['items', 'dtype']

    def __new__(cls, items=None, dtype=int):
        if items is None:
            items = DynamicOneDimensionalArray(dtype, 0)
        else:
            items = DynamicOneDimensionalArray(dtype, items)
        obj = object.__new__(cls)
        obj.items, obj.dtype = \
            items, items._dtype
        return obj

    def __init__(self):
        self.items.size = size
        self.queue = [None for i in range(size)]
        self.items.front = self.items.rear = -1

    def append(self, x):
        if self.is_full:
            raise ValueError("Queue is full")
        elif (self.items.front == -1):
            self.items.front = 0
            self.items.rear = 0
            self.queue[self.items.rear] = x
        else:
            self.items.rear = (self.items.rear + 1) % self.size
            self.queue[self.items.rear] = x

    def popleft(self):
        if self.is_empty:
            raise ValueError("Queue is empty")
        elif (self.items.front == self.items.rear):
            self.items.front = -1
            self.items.rear = -1
            return self.queue[self.items.front]
        else:
            self.items.front = (self.items.front + 1) % self.size
            return self.queue[self.items.front]

    def len(self):
        return abs(abs(self.size - self.items.front) - abs(self.size - self.items.rear))+1

