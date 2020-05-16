from pydatastructs.utils.misc_util import _check_type, LinkedListNode

__all__ = [
    'SinglyLinkedList',
    'DoublyLinkedList',
    'SinglyCircularLinkedList',
    'DoublyCircularLinkedList'
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

    def search(self, key):
        curr_node = self.head
        while curr_node is not None:
            if curr_node.key == key:
                return curr_node
            curr_node = curr_node.next
            if curr_node is self.head:
                return None
        return None

    def __str__(self):
        """
        For printing the linked list.
        """
        elements = []
        current_node = self.head
        while current_node is not None:
            elements.append(str(current_node))
            current_node = current_node.next
            if current_node == self.head:
                break
        return str(elements)

    def insert_after(self, prev_node, key, data=None):
        """
        Inserts a new node after the prev_node.

        Parameters
        ==========

        prev_node: LinkedListNode
            The node after which the
            new node is to be inserted.

        key
            Any valid identifier to uniquely
            identify the node in the linked list.

        data
            Any valid data to be stored in the node.
        """
        raise NotImplementedError('This is an abstract method')

    def insert_at(self, index, key, data=None):
        """
        Inserts a new node at the input index.

        Parameters
        ==========

        index: int
            An integer satisfying python indexing properties.

        key
            Any valid identifier to uniquely
            identify the node in the linked list.

        data
            Any valid data to be stored in the node.
        """
        raise NotImplementedError('This is an abstract method')

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
        raise NotImplementedError('This is an abstract method')

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

    def appendleft(self, key, data=None):
        """
        Pushes a new node at the start i.e.,
        the left of the list.

        Parameters
        ==========

        key
            Any valid identifier to uniquely
            identify the node in the linked list.

        data
            Any valid data to be stored in the node.
        """
        self.insert_at(0, key, data)

    def append(self, key, data=None):
        """
        Appends a new node at the end of the list.

        Parameters
        ==========

        key
            Any valid identifier to uniquely
            identify the node in the linked list.

        data
            Any valid data to be stored in the node.
        """
        self.insert_at(self.size, key, data)

    def insert_before(self, next_node, key, data=None):
        """
        Inserts a new node before the next_node.

        Parameters
        ==========

        next_node: LinkedListNode
            The node before which the
            new node is to be inserted.

        key
            Any valid identifier to uniquely
            identify the node in the linked list.

        data
            Any valid data to be stored in the node.
        """
        raise NotImplementedError('This is an abstract method')

    def popleft(self):
        """
        Extracts the Node from the left
        i.e. start of the list.

        Returns
        =======

        old_head: LinkedListNode
            The leftmost element of linked
            list.
        """
        return self.extract(0)

    def popright(self):
        """
        Extracts the node from the right
        of the linked list.

        Returns
        =======

        old_tail: LinkedListNode
            The leftmost element of linked
            list.
        """
        return self.extract(-1)

class DoublyLinkedList(LinkedList):
    """
    Represents Doubly Linked List

    Examples
    ========

    >>> from pydatastructs import DoublyLinkedList
    >>> dll = DoublyLinkedList()
    >>> dll.append(6)
    >>> dll[0].key
    6
    >>> dll.head.key
    6
    >>> dll.append(5)
    >>> dll.appendleft(2)
    >>> str(dll)
    "['2', '6', '5']"
    >>> dll[0].key = 7.2
    >>> dll.extract(1).key
    6
    >>> str(dll)
    "['7.2', '5']"

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Doubly_linked_list

    """
    __slots__ = ['head', 'tail', 'size']

    def __new__(cls):
        obj = LinkedList.__new__(cls)
        obj.head = None
        obj.tail = None
        obj.size = 0
        return obj

    @classmethod
    def methods(cls):
        return ['__new__', 'insert_after',
        'insert_before', 'insert_at', 'extract']

    def insert_after(self, prev_node, key, data=None):
        self.size += 1
        new_node = LinkedListNode(key, data,
                                 links=['next', 'prev'],
                                 addrs=[None, None])
        new_node.next = prev_node.next
        if new_node.next is not None:
            new_node.next.prev = new_node
        prev_node.next = new_node
        new_node.prev = prev_node

        if new_node.next is None:
            self.tail = new_node

    def insert_before(self, next_node, key, data=None):
        self.size += 1
        new_node = LinkedListNode(key, data,
                                 links=['next', 'prev'],
                                 addrs=[None, None])
        new_node.prev = next_node.prev
        next_node.prev = new_node
        new_node.next = next_node
        if new_node.prev is not None:
            new_node.prev.next = new_node
        else:
            self.head = new_node

    def insert_at(self, index, key, data=None):
        if self.size == 0 and (index in (0, -1)):
            index = 0

        if index < 0:
            index = self.size + index

        if index > self.size:
            raise IndexError('%d index is out of range.'%(index))

        self.size += 1
        new_node = LinkedListNode(key, data,
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

    def extract(self, index):
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

class SinglyLinkedList(LinkedList):
    """
    Represents Singly Linked List

    Examples
    ========

    >>> from pydatastructs import SinglyLinkedList
    >>> sll = SinglyLinkedList()
    >>> sll.append(6)
    >>> sll[0].key
    6
    >>> sll.head.key
    6
    >>> sll.append(5)
    >>> sll.appendleft(2)
    >>> str(sll)
    "['2', '6', '5']"
    >>> sll[0].key = 7.2
    >>> sll.extract(1).key
    6
    >>> str(sll)
    "['7.2', '5']"

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Singly_linked_list

    """
    __slots__ = ['head', 'tail', 'size']

    def __new__(cls):
        obj = LinkedList.__new__(cls)
        obj.head = None
        obj.tail = None
        obj.size = 0
        return obj

    @classmethod
    def methods(cls):
        return ['insert_after', 'insert_at',
        'extract']

    def insert_after(self, prev_node, key, data=None):
        self.size += 1
        new_node = LinkedListNode(key, data,
                                 links=['next'],
                                 addrs=[None])
        new_node.next = prev_node.next
        prev_node.next = new_node

        if new_node.next is None:
            self.tail = new_node

    def insert_at(self, index, key, data=None):
        if self.size == 0 and (index in (0, -1)):
            index = 0

        if index < 0:
            index = self.size + index

        if index > self.size:
            raise IndexError('%d index is out of range.'%(index))

        self.size += 1
        new_node = LinkedListNode(key, data,
                                    links=['next'],
                                    addrs=[None])
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
            new_node.next = current_node
            if prev_node is not None:
                prev_node.next = new_node
            if new_node.next is None:
                self.tail = new_node
            if index == 0:
                self.head = new_node

    def extract(self, index):
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
        if index == 0:
            self.head = current_node.next
        if index == self.size:
            self.tail = prev_node
        return current_node

class SinglyCircularLinkedList(SinglyLinkedList):
    """
    Represents Singly Circular Linked List.


    Examples
    ========

    >>> from pydatastructs import SinglyCircularLinkedList
    >>> scll = SinglyCircularLinkedList()
    >>> scll.append(6)
    >>> scll[0].key
    6
    >>> scll.head.key
    6
    >>> scll.append(5)
    >>> scll.appendleft(2)
    >>> str(scll)
    "['2', '6', '5']"
    >>> scll[0].key = 7.2
    >>> scll.extract(1).key
    6
    >>> str(scll)
    "['7.2', '5']"

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Linked_list#Circular_linked_list

    """

    @classmethod
    def methods(cls):
        return ['insert_after', 'insert_at', 'extract']

    def insert_after(self, prev_node, key, data=None):
        super(SinglyCircularLinkedList, self).\
            insert_after(prev_node, key, data)
        if prev_node.next.next == self.head:
            self.tail = prev_node.next

    def insert_at(self, index, key, data=None):
        super(SinglyCircularLinkedList, self).insert_at(index, key, data)
        if self.size == 1:
            self.head.next = self.head
        new_node = self.__getitem__(index)
        if index == 0:
            self.tail.next = new_node
        if new_node.next == self.head:
            self.tail = new_node

    def extract(self, index):
        node = super(SinglyCircularLinkedList, self).extract(index)
        if self.tail is None:
            self.head = None
        elif index == 0:
            self.tail.next = self.head
        return node

class DoublyCircularLinkedList(DoublyLinkedList):
    """
    Represents Doubly Circular Linked List

    Examples
    ========

    >>> from pydatastructs import DoublyCircularLinkedList
    >>> dcll = DoublyCircularLinkedList()
    >>> dcll.append(6)
    >>> dcll[0].key
    6
    >>> dcll.head.key
    6
    >>> dcll.append(5)
    >>> dcll.appendleft(2)
    >>> str(dcll)
    "['2', '6', '5']"
    >>> dcll[0].key = 7.2
    >>> dcll.extract(1).key
    6
    >>> str(dcll)
    "['7.2', '5']"

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Doubly_linked_list#Circular_doubly_linked_lists

    """

    @classmethod
    def methods(cls):
        return ['insert_after', 'insert_before',
        'insert_at', 'extract']

    def insert_after(self, prev_node, key, data=None):
        super(DoublyCircularLinkedList, self)\
            .insert_after(prev_node, key, data)
        if prev_node.next.next == self.head:
            self.tail = prev_node.next

    def insert_before(self, next_node, key, data=None):
        super(DoublyCircularLinkedList, self).\
            insert_before(next_node, key, data)
        if next_node == self.head:
            self.head = next_node.prev

    def insert_at(self, index, key, data=None):
        super(DoublyCircularLinkedList, self).\
            insert_at(index, key, data)
        if self.size == 1:
            self.head.next = self.head
            self.head.prev = self.head
        new_node = self.__getitem__(index)
        if index == 0:
            self.tail.next = new_node
            new_node.prev = self.tail
        if new_node.next == self.head:
            self.tail = new_node
            new_node.next = self.head
            self.head.prev = new_node

    def extract(self, index):
        node = super(DoublyCircularLinkedList, self).extract(index)
        if self.tail is None:
            self.head = None
        elif index == 0:
            self.tail.next = self.head
        return node
