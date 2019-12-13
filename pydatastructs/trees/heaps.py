from pydatastructs.utils.misc_util import _check_type, NoneType, TreeNode
from pydatastructs.linear_data_structures.arrays import ArrayForTrees

__all__ = [
    'BinaryHeap'
]

class Heap:
    """
    Abstract class for representing heaps.
    """
    pass

class BinaryHeap:
    """
    Represents Binary Heap.

    Parameters
    ==========

    array : list, tuple
        Optional, by default 'None'.
        List/tuple of initial elements in Heap.

    heap_property : str
        The property of binary heap.
        If the key stored in each node is
        either greater than or equal to
        the keys in the node's children
        then pass 'max'.
        If the key stored in each node is
        either less than or equal to
        the keys in the node's children
        then pass 'min'.
        By default, the heap property is
        set to 'min'.

    Examples
    ========

    >>> from pydatastructs.trees.heaps import BinaryHeap
    >>> min_heap = BinaryHeap(heap_property="min")
    >>> min_heap.insert(1, 1)
    >>> min_heap.insert(5, 5)
    >>> min_heap.insert(7, 7)
    >>> min_heap.extract()
    1
    >>> min_heap.insert(4, 4)
    >>> min_heap.extract()
    4

    >>> max_heap = BinaryHeap(heap_property='max')
    >>> max_heap.insert(1, 1)
    >>> max_heap.insert(5, 5)
    >>> max_heap.insert(7, 7)
    >>> max_heap.extract()
    7
    >>> max_heap.insert(6, 6)
    >>> max_heap.extract()
    6

    References
    ==========

    .. [1] https://en.m.wikipedia.org/wiki/Binary_heap
    """
    __slots__ = ['_comp', 'heap']

    def __new__(cls, elements=None, heap_property="min"):
        obj = object.__new__(cls)
        if heap_property == "min":
            obj._comp = lambda key_parent, key_child: key_parent <= key_child
        elif heap_property == "max":
            obj._comp = lambda key_parent, key_child: key_parent >= key_child
        else:
            raise ValueError("%s is invalid heap property"%(heap_property))
        if elements is None:
            elements = []
        obj.heap = ArrayForTrees(TreeNode, elements)
        obj._build()
        return obj

    def _build(self):
        for i in range(self.heap.size//2, -1, -1):
            self._heapify(i)

    def _heapify(self, i):
        target = i
        l = 2*i + 1
        r = 2*i + 2

        if l <= self.heap._last_pos_filled:
            target = l if (not self._comp(self.heap[l].key, self.heap[target].key)) \
                        else i
        if r <= self.heap._last_pos_filled:
            target = r if (not self._comp(self.heap[r].key, self.heap[target].key)) \
                        else target

        if target != i:
            target_key, target_data = \
                self.heap[target].key, self.heap[target].data
            self.heap[target].key, self.heap[target].data = \
                self.heap[i].key, self.heap[i].data
            self.heap[i].key, self.heap[i].data = \
                target_key, target_data
            i = target
            self._heapify(i)

    def insert(self, key, data):
        """
        Insert a new element to the heap according to heap property.

        Parameters
        ==========

        key
            The key for comparison.
        data
            The data to be inserted.

        Returns
        =======

        None
        """
        new_node = TreeNode(key, data)
        self.heap.append(new_node)
        self._last_pos_filled += 1
        i = self._last_pos_filled

        while True:
            parent = (i-1)//2
            if i == 0 or self.array[parent] < self.array[i]:
                break
            else:
                self.array[parent], self.array[i] = self.array[i], self.array[parent]
                i = parent

    def extract(self):
        """
        Extract root element of the Heap.

        Returns
        =======

        root_element : TreeNode
            The TreeNode at the root of the heap.
        """
        if self._last_pos_filled == -1:
            return "Nothing to extract!"
        else:
            element_to_be_extracted = self.array[0]
            self.array[0] = self.array[self._last_pos_filled]
            self.array[self._last_pos_filled] = float('inf')
            self._heapify(0)
            self.array.pop(self._last_pos_filled)
            self._last_pos_filled-=1
            return element_to_be_extracted
