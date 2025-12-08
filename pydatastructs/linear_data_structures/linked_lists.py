import math, random
from pydatastructs.utils.misc_util import _check_type, LinkedListNode, SkipNode
from pydatastructs.utils.misc_util import (
    Backend, raise_if_backend_is_not_python)

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

    Parameters
    ==========

    mode: str
        The mode of the linked list.
        'standard' (default) - Uses separate next and prev pointers
        'xor' - Uses XOR of adjacent node addresses for memory efficiency

    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

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
    "['(2, None)', '(6, None)', '(5, None)']"
    >>> dll[0].key = 7.2
    >>> dll.extract(1).key
    6
    >>> str(dll)
    "['(7.2, None)', '(5, None)']"

    XOR Mode Example:

    >>> dll_xor = DoublyLinkedList(mode='xor')
    >>> dll_xor.append(1)
    >>> dll_xor.append(2)
    >>> dll_xor.append(3)
    >>> str(dll_xor)
    "['(1, None)', '(2, None)', '(3, None)']"

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Doubly_linked_list
    .. [2] https://en.wikipedia.org/wiki/XOR_linked_list

    """
    __slots__ = ['head', 'tail', 'size', 'mode', '_id_to_node']

    def __new__(cls, **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
        obj = LinkedList.__new__(cls)
        obj.head = None
        obj.tail = None
        obj.size = 0
        obj.mode = kwargs.get('mode', 'standard')
        if obj.mode not in ('standard', 'xor'):
            raise ValueError("mode must be 'standard' or 'xor'")
        if obj.mode == 'xor':
            obj._id_to_node = {}
        return obj

    @classmethod
    def methods(cls):
        return ['__new__', 'insert_after',
        'insert_before', 'insert_at', 'extract']

    def _get_node_id(self, node):
        """
        Helper method to get node ID for XOR operations.
        Returns 0 for None nodes.
        """
        return id(node) if node is not None else 0

    def _xor(self, a_id, b_id):
        """
        XOR two node IDs.
        """
        return a_id ^ b_id

    def _get_node_from_id(self, node_id):
        """
        Retrieve node from ID in XOR mode.
        Returns None if node_id is 0.
        """
        if node_id == 0:
            return None
        return self._id_to_node.get(node_id)

    def _register_node(self, node):
        """
        Register a node in the id_to_node dictionary for XOR mode.
        """
        if self.mode == 'xor':
            self._id_to_node[id(node)] = node

    def _unregister_node(self, node):
        """
        Unregister a node from the id_to_node dictionary for XOR mode.
        """
        if self.mode == 'xor' and node is not None:
            node_id = id(node)
            if node_id in self._id_to_node:
                del self._id_to_node[node_id]

    def _get_next(self, current_node, prev_node):
        """
        Get the next node in XOR mode.
        In XOR mode: next = prev XOR both
        """
        if self.mode == 'standard':
            return current_node.next
        else:
            prev_id = self._get_node_id(prev_node)
            next_id = self._xor(prev_id, current_node.both)
            return self._get_node_from_id(next_id)

    def _get_prev(self, current_node, next_node):
        """
        Get the previous node in XOR mode.
        In XOR mode: prev = next XOR both
        """
        if self.mode == 'standard':
            return current_node.prev
        else:
            next_id = self._get_node_id(next_node)
            prev_id = self._xor(next_id, current_node.both)
            return self._get_node_from_id(prev_id)

    def insert_after(self, prev_node, key, data=None):
        self.size += 1

        if self.mode == 'standard':
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
        else:  # XOR mode
            new_node = LinkedListNode(key, data,
                                     links=['both'],
                                     addrs=[0])
            self._register_node(new_node)

            # Find prev_node in the list to get its neighbors
            current = self.head
            prev_prev = None
            found_prev_prev = None

            while current is not None and current != prev_node:
                prev_prev = current
                current = self._get_next(current, found_prev_prev)
                found_prev_prev = prev_prev

            if current != prev_node:
                raise ValueError("prev_node not found in list")

            # Now current == prev_node, found_prev_prev is the node before prev_node
            next_node = self._get_next(prev_node, found_prev_prev)

            # Update new_node's both pointer
            new_node.both = self._xor(id(prev_node), self._get_node_id(next_node))

            # Update prev_node's both pointer
            prev_node.both = self._xor(self._get_node_id(found_prev_prev), id(new_node))

            # Update next_node's both pointer if it exists
            if next_node is not None:
                next_next = self._get_next(next_node, prev_node)
                next_node.both = self._xor(id(new_node), self._get_node_id(next_next))
            else:
                self.tail = new_node

    def insert_before(self, next_node, key, data=None):
        self.size += 1

        if self.mode == 'standard':
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
        else:  # XOR mode
            new_node = LinkedListNode(key, data,
                                     links=['both'],
                                     addrs=[0])
            self._register_node(new_node)

            # Find next_node in the list to get its neighbors
            current = self.head
            prev_of_current = None
            found_prev = None

            while current is not None and current != next_node:
                prev_of_current = current
                current = self._get_next(current, found_prev)
                found_prev = prev_of_current

            if current != next_node:
                raise ValueError("next_node not found in list")

            # Now current == next_node, found_prev is the node before next_node
            prev_node = found_prev
            next_next = self._get_next(next_node, prev_node)

            # Update new_node's both pointer
            new_node.both = self._xor(self._get_node_id(prev_node),
                                      id(next_node))

            # Update next_node's both pointer
            next_node.both = self._xor(id(new_node), self._get_node_id(next_next))

            # Update prev_node's both pointer if it exists
            if prev_node is not None:
                prev_prev = self._get_prev(prev_node, next_node)
                prev_node.both = self._xor(self._get_node_id(prev_prev),
                                          id(new_node))
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

        if self.mode == 'standard':
            new_node = LinkedListNode(key, data,
                                        links=['next', 'prev'],
                                        addrs=[None, None])
            if self.size == 1:
                self.head, self.tail = \
                    new_node, new_node
            elif index == self.size - 1:
                new_node.prev = self.tail
                new_node.next = self.tail.next
                self.tail.next = new_node
                self.tail = new_node
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
        else:  # XOR mode
            new_node = LinkedListNode(key, data,
                                        links=['both'],
                                        addrs=[0])
            self._register_node(new_node)

            if self.size == 1:
                # First node
                new_node.both = 0
                self.head, self.tail = new_node, new_node
            elif index == self.size - 1:
                # Append at end
                # tail's both currently = XOR(prev_of_tail, 0)
                # After insertion: tail's both = XOR(prev_of_tail, new_node)
                # new_node's both = XOR(tail, 0)
                prev_of_tail_id = self.tail.both  # Since tail.next is None (0)
                self.tail.both = self._xor(prev_of_tail_id, id(new_node))
                new_node.both = self._xor(id(self.tail), 0)
                self.tail = new_node
            elif index == 0:
                # Insert at beginning
                # head's both currently = XOR(0, next_of_head)
                # After insertion: head's both = XOR(new_node, next_of_head)
                # new_node's both = XOR(0, head)
                next_of_head_id = self.head.both  # Since head.prev is None (0)
                self.head.both = self._xor(id(new_node), next_of_head_id)
                new_node.both = self._xor(0, id(self.head))
                self.head = new_node
            else:
                # Insert in the middle
                counter = 0
                current_node = self.head
                prev_node = None
                prev_prev_node = None
                while counter != index:
                    prev_prev_node = prev_node
                    prev_node = current_node
                    if current_node is not None:
                        current_node = self._get_next(current_node, prev_prev_node)
                    counter += 1

                # Insert new_node between prev_node and current_node
                new_node.both = self._xor(self._get_node_id(prev_node),
                                         self._get_node_id(current_node))

                if prev_node is not None:
                    prev_node.both = self._xor(self._get_node_id(prev_prev_node),
                                              id(new_node))
                else:
                    self.head = new_node

                if current_node is not None:
                    next_node = self._get_next(current_node, prev_node)
                    current_node.both = self._xor(id(new_node),
                                                  self._get_node_id(next_node))
                else:
                    self.tail = new_node

    def extract(self, index):
        if self.is_empty:
            raise ValueError("The list is empty.")

        if index < 0:
            index = self.size + index

        if index >= self.size:
            raise IndexError('%d is out of range.'%(index))

        self.size -= 1

        if self.mode == 'standard':
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
        else:  # XOR mode
            counter = 0
            current_node = self.head
            prev_node = None
            prev_prev_node = None

            while counter != index:
                prev_prev_node = prev_node
                prev_node = current_node
                if current_node is not None:
                    current_node = self._get_next(current_node, prev_prev_node)
                counter += 1

            # Get the next node
            next_node = self._get_next(current_node, prev_node)

            # Update prev_node's both pointer
            if prev_node is not None:
                prev_node.both = self._xor(self._get_node_id(prev_prev_node),
                                          self._get_node_id(next_node))
            else:
                # Removing head
                self.head = next_node
                if next_node is not None:
                    # Update new head's both to remove reference to removed node
                    next_next = self._get_next(next_node, current_node)
                    next_node.both = self._xor(0, self._get_node_id(next_next))

            # Update next_node's both pointer
            if next_node is not None and prev_node is not None:
                next_next = self._get_next(next_node, current_node)
                next_node.both = self._xor(self._get_node_id(prev_node),
                                          self._get_node_id(next_next))
            elif next_node is None:
                # Removing tail
                self.tail = prev_node
                if prev_node is not None:
                    prev_node.both = self._xor(self._get_node_id(prev_prev_node), 0)

            # Unregister the removed node
            self._unregister_node(current_node)

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

        if self.mode == 'standard':
            counter = 0
            current_node = self.head
            while counter != index:
                current_node = current_node.next
                counter += 1
            return current_node
        else:  # XOR mode
            counter = 0
            current_node = self.head
            prev_node = None
            while counter != index:
                if current_node is None:
                    raise IndexError('Traversal reached None before index')
                next_node = self._get_next(current_node, prev_node)
                prev_node = current_node
                current_node = next_node
                counter += 1
            return current_node

    def __str__(self):
        """
        For printing the linked list.
        """
        elements = []
        if self.mode == 'standard':
            current_node = self.head
            while current_node is not None:
                elements.append(str(current_node))
                current_node = current_node.next
                if current_node == self.head:
                    break
        else:  # XOR mode
            current_node = self.head
            prev_node = None
            while current_node is not None:
                elements.append(str(current_node))
                next_node = self._get_next(current_node, prev_node)
                prev_node = current_node
                current_node = next_node
                if current_node == self.head:
                    break
        return str(elements)

    def search(self, key):
        """
        Searches for a node by key.

        Parameters
        ==========

        key
            The key to search for.

        Returns
        =======

        node: LinkedListNode or None
            The node with the given key, or None if not found.
        """
        if self.mode == 'standard':
            curr_node = self.head
            while curr_node is not None:
                if curr_node.key == key:
                    return curr_node
                curr_node = curr_node.next
                if curr_node == self.head:
                    return None
            return None
        else:  # XOR mode
            curr_node = self.head
            prev_node = None
            while curr_node is not None:
                if curr_node.key == key:
                    return curr_node
                next_node = self._get_next(curr_node, prev_node)
                prev_node = curr_node
                curr_node = next_node
                if curr_node == self.head:
                    return None
            return None

class SinglyLinkedList(LinkedList):
    """
    Represents Singly Linked List

    Parameters
    ==========

    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

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
    "['(2, None)', '(6, None)', '(5, None)']"
    >>> sll[0].key = 7.2
    >>> sll.extract(1).key
    6
    >>> str(sll)
    "['(7.2, None)', '(5, None)']"

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Singly_linked_list

    """
    __slots__ = ['head', 'tail', 'size']

    def __new__(cls, **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
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
        elif index == self.size - 1:
            new_node.next = self.tail.next
            self.tail.next = new_node
            self.tail = new_node
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

    Parameters
    ==========

    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.


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
    "['(2, None)', '(6, None)', '(5, None)']"
    >>> scll[0].key = 7.2
    >>> scll.extract(1).key
    6
    >>> str(scll)
    "['(7.2, None)', '(5, None)']"

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

    Parameters
    ==========

    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

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
    "['(2, None)', '(6, None)', '(5, None)']"
    >>> dcll[0].key = 7.2
    >>> dcll.extract(1).key
    6
    >>> str(dcll)
    "['(7.2, None)', '(5, None)']"

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

class SkipList(object):
    """
    Represents Skip List

    Parameters
    ==========

    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Examples
    ========

    >>> from pydatastructs import SkipList
    >>> sl = SkipList()
    >>> sl.insert(6)
    >>> sl.insert(1)
    >>> sl.insert(3)
    >>> node = sl.extract(1)
    >>> str(node)
    '(1, None)'
    >>> sl.insert(4)
    >>> sl.insert(2)
    >>> sl.search(4)
    True
    >>> sl.search(10)
    False

    """

    __slots__ = ['head', 'tail', '_levels', '_num_nodes', 'seed']

    def __new__(cls, **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
        obj = object.__new__(cls)
        obj.head, obj.tail = None, None
        obj._num_nodes = 0
        obj._levels = 0
        obj._add_level()
        return obj

    @classmethod
    def methods(cls):
        return ['__new__', 'levels', 'search',
                'extract', '__str__', 'size']

    def _add_level(self):
        self.tail = SkipNode(math.inf, next=None, down=self.tail)
        self.head = SkipNode(-math.inf, next=self.tail, down=self.head)
        self._levels += 1

    @property
    def levels(self):
        """
        Returns the number of levels in the
        current skip list.
        """
        return self._levels

    def _search(self, key) -> list:
        path = []
        node = self.head
        while node:
            if node.next.key >= key:
                path.append(node)
                node = node.down
            else:
                node = node.next
        return path

    def search(self, key) -> bool:
        return self._search(key)[-1].next.key == key

    def insert(self, key, data=None):
        """
        Inserts a new node to the skip list.

        Parameters
        ==========

        key
            Any valid identifier to uniquely
            identify the node in the linked list.

        data
            Any valid data to be stored in the node.
        """
        path = self._search(key)
        tip = path[-1]
        below = SkipNode(key=key, data=data, next=tip.next)
        tip.next = below
        total_level = self._levels
        level = 1
        while random.getrandbits(1) % 2 == 0 and level <= total_level:
            if level == total_level:
                self._add_level()
                prev = self.head
            else:
                prev = path[total_level - 1 - level]
            below = SkipNode(key=key, data=None, next=prev.next, down=below)
            prev.next = below
            level += 1
        self._num_nodes += 1

    @property
    def size(self):
        return self._num_nodes

    def extract(self, key):
        """
        Extracts the node with the given key in the skip list.

        Parameters
        ==========

        key
            The key of the node under consideration.

        Returns
        =======

        return_node: SkipNode
            The node with given key.
        """
        path = self._search(key)
        tip = path[-1]
        if tip.next.key != key:
            raise KeyError('Node with key %s is not there in %s'%(key, self))
        return_node = SkipNode(tip.next.key, tip.next.data)
        total_level = self._levels
        level = total_level - 1
        while level >= 0 and path[level].next.key == key:
            path[level].next = path[level].next.next
            level -= 1
        walk = self.head
        while walk is not None:
            if walk.next is self.tail:
                self._levels -= 1
                self.head = walk.down
                self.tail = self.tail.down
                walk = walk.down
            else:
                break
        self._num_nodes -= 1
        if self._levels == 0:
            self._add_level()
        return return_node

    def __str__(self):
        node2row = {}
        node2col = {}
        walk = self.head
        curr_level = self._levels - 1
        while walk is not None:
            curr_node = walk
            col = 0
            while curr_node is not None:
                if curr_node.key != math.inf and curr_node.key != -math.inf:
                    node2row[curr_node] = curr_level
                    if walk.down is None:
                        node2col[curr_node.key] = col
                    col += 1
                curr_node = curr_node.next
            walk = walk.down
            curr_level -= 1
        sl_mat = [[str(None) for _ in range(self._num_nodes)] for _ in range(self._levels)]
        walk = self.head
        while walk is not None:
            curr_node = walk
            while curr_node is not None:
                if curr_node in node2row:
                    row = node2row[curr_node]
                    col = node2col[curr_node.key]
                    sl_mat[row][col] = str(curr_node)
                curr_node = curr_node.next
            walk = walk.down
        sl_str = ""
        for level_list in sl_mat[::-1]:
            for node_str in level_list:
                sl_str += node_str + " "
            if len(sl_str) > 0:
                sl_str += "\n"
        return sl_str
