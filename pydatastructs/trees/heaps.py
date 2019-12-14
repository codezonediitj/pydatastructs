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

    elements : list, tuple
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
    __slots__ = ['_comp', 'heap', 'heap_property']

    def __new__(cls, elements=None, heap_property="min"):
        obj = object.__new__(cls)
        obj.heap_property = heap_property
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
        for i in range(self.heap.size):
            self.heap[i].left, self.heap[i].right = \
                2*i + 1, 2*i + 2
        for i in range(self.heap.size//2, -1, -1):
            self._heapify(i)

    def _swap(self, idx1, idx2):
        print(self)
        idx1_key, idx1_data = \
            self.heap[idx1].key, self.heap[idx1].data
        self.heap[idx1].key, self.heap[idx1].data = \
            self.heap[idx2].key, self.heap[idx2].data
        self.heap[idx2].key, self.heap[idx2].data = \
            idx1_key, idx1_data

    def _heapify(self, i):
        target = i
        l = 2*i + 1
        r = 2*i + 2

        if l <= self.heap._last_pos_filled:
            target = l if self._comp(self.heap[l].key, self.heap[target].key) \
                        else i
        if r <= self.heap._last_pos_filled:
            target = r if self._comp(self.heap[r].key, self.heap[target].key) \
                        else target

        if target != i:
            self._swap(target, i)
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
        i = self.heap._last_pos_filled
        self.heap[i].left, self.heap[i].right = 2*i + 1, 2*i + 2

        while True:
            parent = (i - 1)//2
            if i == 0 or self._comp(self.heap[parent].key, self.heap[i].key):
                break
            else:
                self._swap(i, parent)
                i = parent

    def extract(self):
        """
        Extract root element of the Heap.

        Returns
        =======

        root_element : TreeNode
            The TreeNode at the root of the heap,
            if the heap is not empty.
        None
            If the heap is empty.
        """
        if self.heap._last_pos_filled == -1:
            return None
        else:
            element_to_be_extracted = self.heap[0]
            self._swap(0, self.heap._last_pos_filled)
            self.heap[self.heap._last_pos_filled] = TreeNode(None,
                                                    float('inf') if self.heap_property == 'min'
                                                    else float('-inf'))
            self._heapify(0)
            self.heap.delete(self.heap._last_pos_filled)
            return element_to_be_extracted

    def __str__(self):
        to_be_printed = ['' for i in range(self.heap._last_pos_filled + 1)]
        for i in range(self.heap._last_pos_filled + 1):
            if self.heap[i] != None:
                node = self.heap[i]
                to_be_printed[i] = (node.left if node.left <= self.heap._last_pos_filled else None,
                                    node.key, node.data,
                                    node.right if node.right <= self.heap._last_pos_filled else None)
        return str(to_be_printed)
