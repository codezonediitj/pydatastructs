from pydatastructs.linear_data_structures import DynamicOneDimensionalArray

__all__ = [
    'Queue'
]

class Queue(object):
    """Representation of queue data structure

    Examples
    ========

    >>> from pydatastructs import Queue
    >>> q = Queue()
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
            return ArrayQueue(
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

class ArrayQueue(Queue):

    __slots__ = ['front', 'rear', 'dtype']

    def __new__(cls, front=None, dtype=int):
        if front is None:
            front = DynamicOneDimensionalArray(dtype, 0)
        else if:
            front = DynamicOneDimensionalArray(dtype, front)
        obj = object.__new__(cls)
        obj.front, obj.dtype = \
            front, front._dtype
        return obj

    def __new__(cls, rear=None, dtype=int):
        if rear is None:
            rear = DynamicOneDimensionalArray(dtype, 0)
        else if:
            rear = DynamicOneDimensionalArray(dtype, rear)
        obj = object.__new__(cls)
        obj.rear, obj.dtype = \
            rear, rear._dtype
        return obj

    def append(self, x):
        if self.is_full:
            raise ValueError("Queue is full")
        elif (self.front == -1):
            self.front = 0
            self.rear = 0
            self.rear = x
        else:
            self.rear = (self.rear + 1) % self.size
            self.rear = x

    def popleft(self):
        if self.is_empty:
            raise ValueError("Queue is empty")
        elif (self.front == self.rear):
            self.front = -1
            self.rear = -1
            return self.front
        else:
            self.front = (self.front + 1) % self.size
            return self.front

    def len(self):
        return abs(abs(self.size - self.front) - abs(self.size - self.rear)) + 1
