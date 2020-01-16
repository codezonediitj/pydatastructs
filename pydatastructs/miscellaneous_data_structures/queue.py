
__all__ = [
    'Queue'
]

class Queue(object):
    """Respresentation of queue data structure

    Examples
    ========

    >>> from pydatastructs import Queue
    >>> q = Queue()
    >>> q.append(1)
    >>> q.append(2)
    >>> q.append(3)
    >>> q.len()
    3
    >>> q.popleft()
    >>> q.len()
    2

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Queue_(abstract_data_type)
    """

    def __init__(self, size):
        self.size = size
        self.queue = [None for i in range(size)]
        self.front = self.rear = -1

    def append(self, data):
        if self.is_full:
            raise ValueError("Queue is full")
        elif (self.front == -1):
            self.front = 0
            self.rear = 0
            self.queue[self.rear] = data
        else:
            self.rear = (self.rear + 1) % self.size
            self.queue[self.rear] = data

    def popleft(self):
        if self.is_empty:
            raise ValueError("Queue is empty")
        elif (self.front == self.rear):
            self.front = -1
            self.rear = -1
            return self.queue[self.front]
        else:
            self.front = (self.front + 1) % self.size
            return self.queue[self.front]

    def len(self):
        return abs(abs(self.size - self.front) - abs(self.size - self.rear))+1

    @property
    def is_empty(self):
        return self.front == -1

    @property
    def is_full(self):
        return ((self.rear + 1) % self.size == self.front)
