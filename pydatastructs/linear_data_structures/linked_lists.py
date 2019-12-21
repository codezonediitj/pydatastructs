from __future__ import print_function, division
from pydatastructs.utils.misc_util import _check_type, LinkedListNode

__all__ = [
    'DoublyLinkedList'
]

class LinkedList(object):
    """
    Abstract class for Linked List.
    """
    __slots__ = ['head', 'size']

    def __len__(self):
        return self.size

    @property
    def is_empty(self):
        return self.size == 0

    def __str__(self):
        """
        For printing the linked list.
        """
        elements = []
        current_node = self.head
        while current_node is not None:
            elements.append(current_node.data)
            current_node = current_node.next
        return str(elements)

class DoublyLinkedList(LinkedList):
    """
    Represents Doubly Linked List

    Examples
    ========

    >>> from pydatastructs import DoublyLinkedList
    >>> dll = DoublyLinkedList()
    >>> dll.append(6)
    >>> dll[0].data
    6
    >>> dll.head.data
    6
    >>> dll.append(5)
    >>> dll.append_left(2)
    >>> print(dll)
    [2, 6, 5]
    >>> dll[0].data = 7.2
    >>> dll.extract(1).data
    6
    >>> print(dll)
    [7.2, 5]

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Doubly_linked_list

    """
    __slots__ = ['head', 'tail', 'size']

    def __new__(cls):
        obj = object.__new__(cls)
        obj.head = None
        obj.tail = None
        obj.size = 0
        return obj

    def append_left(self, data):
        """
        Pushes a new node at the start i.e.,
        the left of the list.

        Parameters
        ==========

        data
            Any valid data to be stored in the node.
        """
        self.insert_at(0, data)

    def append(self, data):
        """
        Appends a new node at the end of the list.

        Parameters
        ==========

        data
            Any valid data to be stored in the node.
        """
        self.insert_at(self.size, data)

    def insert_after(self, prev_node, data):
        """
        Inserts a new node after the prev_node.

        Parameters
        ==========

        prev_node: LinkedListNode
            The node after which the
            new node is to be inserted.

        data
            Any valid data to be stored in the node.
        """
        self.size += 1
        new_node = LinkedListNode(data,
                                 links=['next', 'prev'],
                                 addrs=[None, None])
        new_node.next = prev_node.next
        prev_node.next = new_node
        new_node.prev = prev_node

        if new_node.next is None:
            self.tail = new_node

    def insert_before(self, next_node, data):
        """
        Inserts a new node before the new_node.

        Parameters
        ==========

        next_node: LinkedListNode
            The node before which the
            new node is to be inserted.

        data
            Any valid data to be stored in the node.
        """
        self.size += 1
        new_node = LinkedListNode(data,
                                 links=['next', 'prev'],
                                 addrs=[None, None])
        new_node.prev = next_node.prev
        next_node.prev = new_node
        new_node.next = next_node

        if new_node.prev is None:
            self.head = new_node

    def insert_at(self, index, data):
        """
        Inserts a new node at the input index.

        Parameters
        ==========

        index: int
            An integer satisfying python indexing properties.

        data
            Any valid data to be stored in the node.
        """
        if self.size == 0 and (index in (0, -1)):
            index = 0

        if index < 0:
            index = self.size + index

        if index > self.size:
            raise IndexError('%d index is out of range.'%(index))

        self.size += 1
        new_node = LinkedListNode(data,
                                    links=['next', 'prev'],
                                    addrs=[None, None])
        if self.size == 1:
            self.head, self.tail = \
                new_node, new_node
        else:
            counter = 0
            current_node = self.head
            prev_node = None
            while counter != index:
                prev_node = current_node
                current_node = current_node.next
                counter += 1
            new_node.prev = prev_node
            new_node.next = current_node
            if prev_node is not None:
                prev_node.next = new_node
            if current_node is not None:
                current_node.prev = new_node
            if new_node.next is None:
                self.tail = new_node
            if new_node.prev is None:
                self.head = new_node

    def pop_left(self):
        """
        Extracts the Node from the left
        i.e. start of the list.

        Returns
        =======

        old_head: LinkedListNode
            The leftmost element of linked
            list.
        """
        self.extract(0)

    def pop_right(self):
        """
        Extracts the node from the right
        of the linked list.

        Returns
        =======

        old_tail: LinkedListNode
            The leftmost element of linked
            list.
        """
        self.extract(-1)

    def extract(self, index):
        """
        Extracts the node at the index of the list.

        Parameters
        ==========

        index: int
            An integer satisfying python indexing properties.

        Returns
        =======

        current_node: LinkedListNode
            The node at index i.
        """
        if self.is_empty:
            raise ValueError("The list is empty.")

        if index < 0:
            index = self.size + index

        if index >= self.size:
            raise IndexError('%d is out of range.'%(index))

        self.size -= 1
        counter = 0
        current_node = self.head
        prev_node = None
        while counter != index:
            prev_node = current_node
            current_node = current_node.next
            counter += 1
        if prev_node is not None:
            prev_node.next = current_node.next
        if current_node.next is not None:
            current_node.next.prev = prev_node
        if index == 0:
            self.head = current_node.next
        if index == self.size:
            self.tail = current_node.prev
        return current_node

    def __getitem__(self, index):
        """
        Returns
        =======

        current_node: LinkedListNode
            The node at given index.
        """
        if index < 0:
            index = self.size + index

        if index >= self.size:
            raise IndexError('%d index is out of range.'%(index))

        counter = 0
        current_node = self.head
        while counter != index:
            current_node = current_node.next
            counter += 1
        return current_node
