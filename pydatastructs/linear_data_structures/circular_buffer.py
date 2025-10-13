"""
Module implements Circular buffer.
"""

__all__ = ['CircularBuffer']

from pydatastructs.utils.misc_util import _check_type

class CircularBuffer(object):

    __slots__ = ['size', 'buffer', 'rear', 'front', 'dtype', 'count']

    def __new__(cls, size, dtype):
        obj = object.__new__(cls)
        obj.size = size
        obj.buffer = [None] * size
        obj.rear = obj.front = -1
        obj.dtype = dtype
        obj.count = 0
        return obj

    def __str__(self):
        return ' -> '.join([str(i) for i in self.buffer])

    def __repr__(self):
        return self.__str__()

    def enqueue(self, data):
        """
        Adds data to the buffer.

        Parameters
        ==========

        data
            Data to be added to the buffer.
        """
        _check_type(data, self.dtype)
        if self.is_full():
            raise OverflowError("Circular buffer is full")
        if self.front == -1:
            self.front = 0
        self.rear = (self.rear + 1) % self.size
        self.buffer[self.rear] = self.dtype(data)
        self.count += 1

    def dequeue(self):
        """
        Removes and returns the data from the buffer.
        """
        if self.is_empty():
            raise ValueError("Circular buffer is empty")
        data = self.buffer[self.front]
        self.buffer[self.front] = None
        if self.front == self.rear:
            self.front = self.rear = -1
        else:
            self.front = (self.front + 1) % self.size
        self.count -= 1
        return data

    def peek(self):
        """
        Returns the data at the front of the buffer without removing it.
        """
        if self.is_empty():
            raise ValueError("Circular buffer is empty")
        return self.buffer[self.front]

    def get(self, index):
        """
        Get the data at the index.

        Parameters
        ==========

        index: int
            The index of the data to be fetched.
        """
        if self.is_empty():
            raise IndexError("The buffer is empty.")
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds.")
        return self.buffer[index]

    def is_empty(self):
        """
        Checks if the buffer is empty.
        """
        return self.count == 0

    def is_full(self):
        """
        Checks if the buffer is full.
        """
        return self.count == self.size
