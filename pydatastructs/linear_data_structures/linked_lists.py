from pydatastructs.utils.misc_util import _check_type, LinkedListNode, SkipListNode
from random import random

__all__ = [
    'SinglyLinkedList',
    'DoublyLinkedList',
    'SinglyCircularLinkedList',
    'DoublyCircularLinkedList',
    'SkipList'
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
            if current_node == self.head:
                break
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
    >>> str(dll)
    '[2, 6, 5]'
    >>> dll[0].data = 7.2
    >>> dll.extract(1).data
    6
    >>> str(dll)
    '[7.2, 5]'

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
        if new_node.next is not None:
            new_node.next.prev = new_node
        prev_node.next = new_node
        new_node.prev = prev_node

        if new_node.next is None:
            self.tail = new_node

    def insert_before(self, next_node, data):
        """
        Inserts a new node before the next_node.

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
        if new_node.prev is not None:
            new_node.prev.next = new_node
        else:
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
        return self.extract(0)

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
        return self.extract(-1)

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

class SinglyLinkedList(LinkedList):
    """
    Represents Singly Linked List

    Examples
    ========

    >>> from pydatastructs import SinglyLinkedList
    >>> sll = SinglyLinkedList()
    >>> sll.append(6)
    >>> sll[0].data
    6
    >>> sll.head.data
    6
    >>> sll.append(5)
    >>> sll.append_left(2)
    >>> str(sll)
    '[2, 6, 5]'
    >>> sll[0].data = 7.2
    >>> sll.extract(1).data
    6
    >>> str(sll)
    '[7.2, 5]'

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
                                 links=['next'],
                                 addrs=[None])
        new_node.next = prev_node.next
        prev_node.next = new_node

        if new_node.next is None:
            self.tail = new_node

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
        return self.extract(0)

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
        return self.extract(-1)

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
        if index == 0:
            self.head = current_node.next
        if index == self.size:
            self.tail = prev_node
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

class SinglyCircularLinkedList(SinglyLinkedList):
    """
    Represents Singly Circular Linked List.


    Examples
    ========

    >>> from pydatastructs import SinglyCircularLinkedList
    >>> scll = SinglyCircularLinkedList()
    >>> scll.append(6)
    >>> scll[0].data
    6
    >>> scll.head.data
    6
    >>> scll.append(5)
    >>> scll.append_left(2)
    >>> str(scll)
    '[2, 6, 5]'
    >>> scll[0].data = 7.2
    >>> scll.extract(1).data
    6
    >>> str(scll)
    '[7.2, 5]'

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Linked_list#Circular_linked_list

    """

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
        super(SinglyCircularLinkedList, self).insert_after(prev_node, data)
        if prev_node.next.next == self.head:
            self.tail = prev_node.next

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
        super(SinglyCircularLinkedList, self).insert_at(index, data)
        if self.size == 1:
            self.head.next = self.head
        new_node = self.__getitem__(index)
        if index == 0:
            self.tail.next = new_node
        if new_node.next == self.head:
            self.tail = new_node

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
    >>> dcll[0].data
    6
    >>> dcll.head.data
    6
    >>> dcll.append(5)
    >>> dcll.append_left(2)
    >>> str(dcll)
    '[2, 6, 5]'
    >>> dcll[0].data = 7.2
    >>> dcll.extract(1).data
    6
    >>> str(dcll)
    '[7.2, 5]'

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Doubly_linked_list#Circular_doubly_linked_lists

    """
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
        super(DoublyCircularLinkedList, self).insert_after(prev_node, data)
        if prev_node.next.next == self.head:
            self.tail = prev_node.next

    def insert_before(self, next_node, data):
        """
        Inserts a new node before the next_node.

        Parameters
        ==========

        next_node: LinkedListNode
            The node before which the
            new node is to be inserted.

        data
            Any valid data to be stored in the node.
        """
        super(DoublyCircularLinkedList, self).insert_before(next_node,data)
        if next_node == self.head:
            self.head = next_node.prev

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
        super(DoublyCircularLinkedList, self).insert_at(index, data)
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
        node = super(DoublyCircularLinkedList, self).extract(index)
        if self.tail is None:
            self.head = None
        elif index == 0:
            self.tail.next = self.head
        return node

class SkipList(LinkedList):
    """
    Represents Skip List

    Examples
    ========

    >>> from pydatastructs import SkipList
    >>> skip_list = SkipList()
    >>> skip_list.insert(2, "2")
    >>> skip_list.insert(4, "4")
    >>> skip_list.insert(6, "4")
    >>> skip_list.insert(4, "5")
    >>> skip_list.insert(8, "4")
    >>> skip_list.insert(9, "4")
    >>> skip_list.delete(4)

    References
    ==========

    .. [1] https://epaperpress.com/sortsearch/download/skiplist.pdf
    .. [2] https://github.com/TheAlgorithms/Python/blob/a9f73e318cddf43769083614a3e1f9dab1ec50fc/data_structures/linked_list/skip_list.py

    Parameters
    ==========

    p
        Fraction of nodes of level i which are present at level i+1 also.

    max_level
        Maximum level that can be attained by any node.

    """

    __slots__ = ['size', 'level', 'p', 'max_level']

    def __new__(cls, p=0.5, max_level=16):
        obj = LinkedList.__new__(cls)
        obj.head = SkipListNode("root", None)
        obj.level = 0
        obj.p = p
        obj.max_level = max_level
        obj.size = 0
        return obj

    def __str__(self):
        """
        :return: Visual representation of SkipList
        >>> skip_list = SkipList()
        >>> print(skip_list)
        SkipList(level=0)
        >>> skip_list.insert("Key1", "Value")
        >>> print(skip_list) # doctest: +ELLIPSIS
        SkipList(level=...
        [root]--...
        [Key1]--Key1...
        None    *...
        >>> skip_list.insert("Key2", "OtherValue")
        >>> print(skip_list) # doctest: +ELLIPSIS
        SkipList(level=...
        [root]--...
        [Key1]--Key1...
        [Key2]--Key2...
        None    *...
        """

        items = list(self)

        if len(items) == 0:
            return f"SkipList(level={self.level})"

        label_size = max((len(str(item)) for item in items), default=4)
        label_size = max(label_size, 4) + 4

        node = self.head
        lines = []

        forwards = node.forward.copy()
        lines.append(f"[{node.key}]".ljust(label_size, "-") + "* " * len(forwards))
        lines.append(" " * label_size + "| " * len(forwards))

        while len(node.forward) != 0:
            node = node.forward[0]

            lines.append(
                f"[{node.key}]".ljust(label_size, "-")
                + " ".join(str(n.key) if n.key == node.key else "|" for n in forwards)
            )
            lines.append(" " * label_size + "| " * len(forwards))
            forwards[: node.level] = node.forward

        lines.append("None".ljust(label_size) + "* " * len(forwards))
        return f"SkipList(level={self.level})\n" + "\n".join(lines)

    def __iter__(self):
        node = self.head

        while len(node.forward) != 0:
            yield node.forward[0].key
            node = node.forward[0]

    def random_level(self):
        level = 1
        while random() < self.p and level < self.max_level:
            level += 1

        return level

    def _locate_node(self, key):
        """
        :param key: Searched key,
        :return: Tuple with searched node (or None if given key is not present)
                 and list of nodes that refer (if key is present) of should refer to given node.
        """
        update_vector = []

        node = self.head

        for i in reversed(range(self.level)):
            while i < node.level and node.forward[i].key < key:
                node = node.forward[i]
            update_vector.append(node)

        update_vector.reverse()
        if len(node.forward) != 0 and node.forward[0].key == key:
            return node.forward[0], update_vector
        else:
            return None, update_vector

    def delete(self, key):
        """
        :param key: Key to remove from list.
        >>> skip_list = SkipList()
        >>> skip_list.insert(2, "Two")
        >>> skip_list.insert(1, "One")
        >>> skip_list.insert(3, "Three")
        >>> list(skip_list)
        [1, 2, 3]
        >>> skip_list.delete(2)
        >>> list(skip_list)
        [1, 3]
        """

        node, update_vector = self._locate_node(key)

        if node is not None:
            for i, update_node in enumerate(update_vector):
                if update_node.level > i and update_node.forward[i].key == key:
                    if node.level > i:
                        update_node.forward[i] = node.forward[i]
                    else:
                        update_node.forward = update_node.forward[:i]
            self.size -= 1

    def insert(self, key, value):
        """
        :param key: Key to insert.
        :param value: Value associated with given key.
        >>> skip_list = SkipList()
        >>> skip_list.insert(2, "Two")
        >>> skip_list.find(2)
        'Two'
        >>> list(skip_list)
        [2]
        """

        node, update_vector = self._locate_node(key)
        if node is not None:
            node.value = value
        else:
            level = self.random_level()

            if level > self.level:
                for i in range(self.level - 1, level):
                    update_vector.append(self.head)
                self.level = level

            new_node = SkipListNode(key, value)

            for i, update_node in enumerate(update_vector[:level]):
                if update_node.level > i:
                    new_node.forward.append(update_node.forward[i])

                if update_node.level < i + 1:
                    update_node.forward.append(new_node)
                else:
                    update_node.forward[i] = new_node
            self.size += 1

    def find(self, key):
        """
        :param key: Search key.
        :return: Value associated with given key or None if given key is not present.
        >>> skip_list = SkipList()
        >>> skip_list.find(2)
        >>> skip_list.insert(2, "Two")
        >>> skip_list.find(2)
        'Two'
        >>> skip_list.insert(2, "Three")
        >>> skip_list.find(2)
        'Three'
        """

        node, _ = self._locate_node(key)

        if node is not None:
            return node.value

        return None
