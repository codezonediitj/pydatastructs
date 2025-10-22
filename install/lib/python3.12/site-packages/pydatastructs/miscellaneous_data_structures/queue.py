from pydatastructs.linear_data_structures import DynamicOneDimensionalArray, SinglyLinkedList
from pydatastructs.utils.misc_util import (
    NoneType, Backend, raise_if_backend_is_not_python)
from pydatastructs.trees.heaps import BinaryHeap, BinomialHeap
from copy import deepcopy as dc

__all__ = [
    'Queue',
    'PriorityQueue'
]

class Queue(object):
    """Representation of queue data structure.

    Parameters
    ==========

    implementation : str
        Implementation to be used for queue.
        By default, 'array'
    items : list/tuple
        Optional, by default, None
        The inital items in the queue.
    dtype : A valid python type
        Optional, by default NoneType if item
        is None.
        Required only for 'array' implementation.
    double_ended : bool
        Optional, by default, False.
        Set to True if the queue should support
        additional, appendleft and pop operations
        from left and right sides respectively.
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Examples
    ========

    >>> from pydatastructs import Queue
    >>> q = Queue()
    >>> q.append(1)
    >>> q.append(2)
    >>> q.append(3)
    >>> q.popleft()
    1
    >>> len(q)
    2

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Queue_(abstract_data_type)
    """

    def __new__(cls, implementation='array', **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
        if implementation == 'array':
            return ArrayQueue(
                kwargs.get('items', None),
                kwargs.get('dtype', int),
                kwargs.get('double_ended', False))
        elif implementation == 'linked_list':
            return LinkedListQueue(
                kwargs.get('items', None),
                kwargs.get('double_ended', False)
            )
        else:
            raise NotImplementedError(
                    "%s hasn't been implemented yet."%(implementation))

    @classmethod
    def methods(cls):
        return ['__new__']

    def _double_ended_check(self):
        if not self._double_ended:
            raise NotImplementedError(
                    "This method is only supported for "
                    "double ended queues.")

    def append(self, *args, **kwargs):
        raise NotImplementedError(
            "This is an abstract method.")

    def appendleft(self, *args, **kwargs):
        raise NotImplementedError(
            "This is an abstract method.")

    def pop(self, *args, **kwargs):
        raise NotImplementedError(
            "This is an abstract method.")

    def popleft(self, *args, **kwargs):
        raise NotImplementedError(
            "This is an abstract method.")

    @property
    def is_empty(self):
        raise NotImplementedError(
            "This is an abstract method.")


class ArrayQueue(Queue):

    __slots__ = ['_front', '_rear', '_double_ended']

    def __new__(cls, items=None, dtype=NoneType, double_ended=False,
                **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
        if items is None:
            items = DynamicOneDimensionalArray(dtype, 0)
        else:
            dtype = type(items[0])
            items = DynamicOneDimensionalArray(dtype, items)
        obj = object.__new__(cls)
        obj.items, obj._front = items, -1
        if items.size == 0:
            obj._front = -1
            obj._rear = -1
        else:
            obj._front = 0
            obj._rear = items._num - 1
        obj._double_ended = double_ended
        return obj

    @classmethod
    def methods(cls):
        return ['__new__', 'append', 'appendleft', 'popleft',
                'pop', 'is_empty', '__len__', '__str__', 'front',
                'rear']

    def append(self, x):
        if self.is_empty:
            self._front = 0
            self.items._dtype = type(x)
        self.items.append(x)
        self._rear += 1

    def appendleft(self, x):
        self._double_ended_check()
        temp = []
        if self.is_empty:
            self._front = 0
            self._rear = -1
        self.items._dtype = type(x)
        temp.append(x)
        for i in range(self._front, self._rear + 1):
            temp.append(self.items._data[i])
        self.items = DynamicOneDimensionalArray(type(temp[0]), temp)
        self._rear += 1

    def popleft(self):
        if self.is_empty:
            raise IndexError("Queue is empty.")
        return_value = dc(self.items[self._front])
        front_temp = self._front
        if self._front == self._rear:
            self._front = -1
            self._rear = -1
        else:
            if (self.items._num - 1)/self.items._size < \
                self.items._load_factor:
                self._front = 0
            else:
                self._front += 1
        self.items.delete(front_temp)
        return return_value

    def pop(self):
        self._double_ended_check()
        if self.is_empty:
            raise IndexError("Queue is empty.")

        return_value = dc(self.items[self._rear])
        rear_temp = self._rear
        if self._front == self._rear:
            self._front = -1
            self._rear = -1
        else:
            if (self.items._num - 1)/self.items._size < \
                self.items._load_factor:
                self._front = 0
            else:
                self._rear -= 1
        self.items.delete(rear_temp)
        return return_value

    @property
    def front(self):
        return self._front

    @property
    def rear(self):
        return self._rear

    @property
    def is_empty(self):
        return self.__len__() == 0

    def __len__(self):
        return self.items._num

    def __str__(self):
        _data = []
        for i in range(self._front, self._rear + 1):
            _data.append(self.items._data[i])
        return str(_data)

class LinkedListQueue(Queue):

    __slots__ = ['queue', '_double_ended']

    def __new__(cls, items=None, double_ended=False,
                **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
        obj = object.__new__(cls)
        obj.queue = SinglyLinkedList()
        if items is None:
            pass
        elif type(items) in (list, tuple):
            for x in items:
                obj.append(x)
        else:
            raise TypeError("Expected type: list/tuple")
        obj._double_ended = double_ended
        return obj

    @classmethod
    def methods(cls):
        return ['__new__', 'append', 'appendleft', 'pop', 'popleft',
                'is_empty', '__len__', '__str__', 'front', 'rear']

    def append(self, x):
        self.queue.append(x)

    def appendleft(self, x):
        self._double_ended_check()
        if self._double_ended:
            self.queue.appendleft(x)

    def pop(self):
        self._double_ended_check()
        if self.is_empty:
            raise IndexError("Queue is empty.")
        return_value = self.queue.popright()
        return return_value

    def popleft(self):
        if self.is_empty:
            raise IndexError("Queue is empty.")
        return_value = self.queue.popleft()
        return return_value

    @property
    def is_empty(self):
        return self.__len__() == 0

    @property
    def front(self):
        return self.queue.head

    @property
    def rear(self):
        return self.queue.tail

    def __len__(self):
        return self.queue.size

    def __str__(self):
        return str(self.queue)

class PriorityQueue(object):
    """
    Represents the concept of priority queue.

    Parameters
    ==========

    implementation: str
        The implementation which is to be
        used for supporting operations
        of priority queue.
        The following implementations are supported,

        'linked_list' -> Linked list implementation.

        'binary_heap' -> Binary heap implementation.

        'binomial_heap' -> Binomial heap implementation.
            Doesn't support custom comparators, minimum
            key data is extracted in every pop.

        Optional, by default, 'binary_heap' implementation
        is used.
    comp: function
        The comparator to be used while comparing priorities.
        Must return a bool object.
        By default, `lambda u, v: u < v` is used to compare
        priorities i.e., minimum priority elements are extracted
        by pop operation.
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Examples
    ========

    >>> from pydatastructs import PriorityQueue
    >>> pq = PriorityQueue()
    >>> pq.push(1, 2)
    >>> pq.push(2, 3)
    >>> pq.pop()
    1
    >>> pq2 = PriorityQueue(comp=lambda u, v: u > v)
    >>> pq2.push(1, 2)
    >>> pq2.push(2, 3)
    >>> pq2.pop()
    2

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Priority_queue
    """

    def __new__(cls, implementation='binary_heap', **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
        comp = kwargs.get("comp", lambda u, v: u < v)
        if implementation == 'linked_list':
            return LinkedListPriorityQueue(comp)
        elif implementation == 'binary_heap':
            return BinaryHeapPriorityQueue(comp)
        elif implementation == 'binomial_heap':
            return BinomialHeapPriorityQueue()
        else:
            raise NotImplementedError(
                "%s implementation is not currently supported "
                "by priority queue.")

    @classmethod
    def methods(cls):
        return ['__new__']

    def push(self, value, priority):
        """
        Pushes the value to the priority queue
        according to the given priority.

        value
            Value to be pushed.
        priority
            Priority to be given to the value.
        """
        raise NotImplementedError(
                "This is an abstract method.")

    def pop(self):
        """
        Pops out the value from the priority queue.
        """
        raise NotImplementedError(
            "This is an abstract method.")

    @property
    def peek(self):
        """
        Returns the pointer to the value which will be
        popped out by `pop` method.
        """
        raise NotImplementedError(
            "This is an abstract method.")

    @property
    def is_empty(self):
        """
        Checks if the priority queue is empty.
        """
        raise NotImplementedError(
            "This is an abstract method.")

class LinkedListPriorityQueue(PriorityQueue):

    __slots__ = ['items', 'comp']

    @classmethod
    def methods(cls):
        return ['__new__', 'push', 'pop', 'peek', 'is_empty']

    def __new__(cls, comp, **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
        obj = object.__new__(cls)
        obj.items = SinglyLinkedList()
        obj.comp = comp
        return obj

    def push(self, value, priority):
        self.items.append(priority, value)

    def pop(self):
        _, max_i = self._find_peek(return_index=True)
        pop_val = self.items.extract(max_i)
        return pop_val.data

    def _find_peek(self, return_index=False):
        if self.is_empty:
            raise IndexError("Priority queue is empty.")

        walk = self.items.head
        i, max_i, max_p = 0, 0, walk
        while walk is not None:
            if self.comp(walk.key, max_p.key):
                max_i = i
                max_p = walk
            i += 1
            walk = walk.next
        if return_index:
            return max_p, max_i
        return max_p

    @property
    def peek(self):
        return self._find_peek()

    @property
    def is_empty(self):
        return self.items.size == 0

class BinaryHeapPriorityQueue(PriorityQueue):

    __slots__ = ['items']

    @classmethod
    def methods(cls):
        return ['__new__', 'push', 'pop', 'peek', 'is_empty']

    def __new__(cls, comp, **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
        obj = object.__new__(cls)
        obj.items = BinaryHeap()
        obj.items._comp = comp
        return obj

    def push(self, value, priority):
        self.items.insert(priority, value)

    def pop(self):
        node = self.items.extract()
        return node.data

    @property
    def peek(self):
        if self.items.is_empty:
            raise IndexError("Priority queue is empty.")
        return self.items.heap[0]

    @property
    def is_empty(self):
        return self.items.is_empty

class BinomialHeapPriorityQueue(PriorityQueue):

    __slots__ = ['items']

    @classmethod
    def methods(cls):
        return ['__new__', 'push', 'pop', 'peek', 'is_empty']

    def __new__(cls, **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
        obj = object.__new__(cls)
        obj.items = BinomialHeap()
        return obj

    def push(self, value, priority):
        self.items.insert(priority, value)

    def pop(self):
        node = self.items.find_minimum()
        self.items.delete_minimum()
        return node.data

    @property
    def peek(self):
        return self.items.find_minimum()

    @property
    def is_empty(self):
        return self.items.is_empty
