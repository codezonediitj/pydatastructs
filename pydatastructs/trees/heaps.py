from pydatastructs.utils.misc_util import (
    _check_type, TreeNode, BinomialTreeNode,
    Backend, raise_if_backend_is_not_python)
from pydatastructs.linear_data_structures.arrays import (
     DynamicOneDimensionalArray, Array)
from pydatastructs.miscellaneous_data_structures.binomial_trees import BinomialTree

__all__ = [
    'BinaryHeap',
    'TernaryHeap',
    'DHeap',
    'BinomialHeap'
]

class Heap(object):
    """
    Abstract class for representing heaps.
    """
    pass


class DHeap(Heap):
    """
    Represents D-ary Heap.

    Parameters
    ==========

    elements: list, tuple, Array
        Optional, by default 'None'.
        list/tuple/Array of initial TreeNode in Heap.
    heap_property: str
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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Examples
    ========

    >>> from pydatastructs.trees.heaps import DHeap
    >>> min_heap = DHeap(heap_property="min", d=3)
    >>> min_heap.insert(1, 1)
    >>> min_heap.insert(5, 5)
    >>> min_heap.insert(7, 7)
    >>> min_heap.extract().key
    1
    >>> min_heap.insert(4, 4)
    >>> min_heap.extract().key
    4

    >>> max_heap = DHeap(heap_property='max', d=2)
    >>> max_heap.insert(1, 1)
    >>> max_heap.insert(5, 5)
    >>> max_heap.insert(7, 7)
    >>> max_heap.extract().key
    7
    >>> max_heap.insert(6, 6)
    >>> max_heap.extract().key
    6

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/D-ary_heap
    """
    __slots__ = ['_comp', 'heap', 'd', 'heap_property', '_last_pos_filled']

    def __new__(cls, elements=None, heap_property="min", d=4,
                **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
        obj = Heap.__new__(cls)
        obj.heap_property = heap_property
        obj.d = d
        if heap_property == "min":
            obj._comp = lambda key_parent, key_child: key_parent <= key_child
        elif heap_property == "max":
            obj._comp = lambda key_parent, key_child: key_parent >= key_child
        else:
            raise ValueError("%s is invalid heap property"%(heap_property))
        if elements is None:
            elements = DynamicOneDimensionalArray(TreeNode, 0)
        elif _check_type(elements, (list,tuple)):
            elements = DynamicOneDimensionalArray(TreeNode, len(elements), elements)
        elif _check_type(elements, Array):
            elements = DynamicOneDimensionalArray(TreeNode, len(elements), elements._data)
        else:
            raise ValueError(f'Expected a list/tuple/Array of TreeNode got {type(elements)}')
        obj.heap = elements
        obj._last_pos_filled = obj.heap._last_pos_filled
        obj._build()
        return obj

    @classmethod
    def methods(cls):
        return ['__new__', 'insert', 'extract', '__str__', 'is_empty']

    def _build(self):
        for i in range(self._last_pos_filled + 1):
            self.heap[i]._leftmost, self.heap[i]._rightmost = \
                self.d*i + 1, self.d*i + self.d
        for i in range((self._last_pos_filled + 1)//self.d, -1, -1):
            self._heapify(i)

    def _swap(self, idx1, idx2):
        idx1_key, idx1_data = \
            self.heap[idx1].key, self.heap[idx1].data
        self.heap[idx1].key, self.heap[idx1].data = \
            self.heap[idx2].key, self.heap[idx2].data
        self.heap[idx2].key, self.heap[idx2].data = \
            idx1_key, idx1_data

    def _heapify(self, i):
        while True:
            target = i
            l = self.d*i + 1
            r = self.d*i + self.d

            for j in range(l, r+1):
                if j <= self._last_pos_filled:
                    target = j if self._comp(self.heap[j].key, self.heap[target].key) \
                            else target
                else:
                    break

            if target != i:
                self._swap(target, i)
                i = target
            else:
                break

    def insert(self, key, data=None):
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
        self.heap[i]._leftmost, self.heap[i]._rightmost = self.d*i + 1, self.d*i + self.d

        while True:
            parent = (i - 1)//self.d
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

        root_element: TreeNode
            The TreeNode at the root of the heap,
            if the heap is not empty.

        None
            If the heap is empty.
        """
        if self._last_pos_filled == -1:
            raise IndexError("Heap is empty.")
        else:
            element_to_be_extracted = TreeNode(self.heap[0].key, self.heap[0].data)
            self._swap(0, self._last_pos_filled)
            self.heap.delete(self._last_pos_filled)
            self._last_pos_filled -= 1
            self._heapify(0)
            return element_to_be_extracted

    def __str__(self):
        to_be_printed = ['' for i in range(self._last_pos_filled + 1)]
        for i in range(self._last_pos_filled + 1):
            node = self.heap[i]
            if node._leftmost <= self._last_pos_filled:
                if node._rightmost <= self._last_pos_filled:
                    children = list(range(node._leftmost, node._rightmost + 1))
                else:
                    children = list(range(node._leftmost, self._last_pos_filled + 1))
            else:
                children = []
            to_be_printed[i] = (node.key, node.data, children)
        return str(to_be_printed)

    @property
    def is_empty(self):
        """
        Checks if the heap is empty.
        """
        return self.heap._last_pos_filled == -1


class BinaryHeap(DHeap):
    """
    Represents Binary Heap.

    Parameters
    ==========

    elements: list, tuple
        Optional, by default 'None'.
        List/tuple of initial elements in Heap.
    heap_property: str
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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Examples
    ========

    >>> from pydatastructs.trees.heaps import BinaryHeap
    >>> min_heap = BinaryHeap(heap_property="min")
    >>> min_heap.insert(1, 1)
    >>> min_heap.insert(5, 5)
    >>> min_heap.insert(7, 7)
    >>> min_heap.extract().key
    1
    >>> min_heap.insert(4, 4)
    >>> min_heap.extract().key
    4

    >>> max_heap = BinaryHeap(heap_property='max')
    >>> max_heap.insert(1, 1)
    >>> max_heap.insert(5, 5)
    >>> max_heap.insert(7, 7)
    >>> max_heap.extract().key
    7
    >>> max_heap.insert(6, 6)
    >>> max_heap.extract().key
    6

    References
    ==========

    .. [1] https://en.m.wikipedia.org/wiki/Binary_heap
    """
    def __new__(cls, elements=None, heap_property="min",
                **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
        obj = DHeap.__new__(cls, elements, heap_property, 2)
        return obj

    @classmethod
    def methods(cls):
        return ['__new__']


class TernaryHeap(DHeap):
    """
    Represents Ternary Heap.

    Parameters
    ==========

    elements: list, tuple
        Optional, by default 'None'.
        List/tuple of initial elements in Heap.
    heap_property: str
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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Examples
    ========

    >>> from pydatastructs.trees.heaps import TernaryHeap
    >>> min_heap = TernaryHeap(heap_property="min")
    >>> min_heap.insert(1, 1)
    >>> min_heap.insert(5, 5)
    >>> min_heap.insert(7, 7)
    >>> min_heap.insert(3, 3)
    >>> min_heap.extract().key
    1
    >>> min_heap.insert(4, 4)
    >>> min_heap.extract().key
    3

    >>> max_heap = TernaryHeap(heap_property='max')
    >>> max_heap.insert(1, 1)
    >>> max_heap.insert(5, 5)
    >>> max_heap.insert(7, 7)
    >>> min_heap.insert(3, 3)
    >>> max_heap.extract().key
    7
    >>> max_heap.insert(6, 6)
    >>> max_heap.extract().key
    6

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/D-ary_heap
    .. [2] https://ece.uwaterloo.ca/~dwharder/aads/Algorithms/d-ary_heaps/Ternary_heaps/
    """
    def __new__(cls, elements=None, heap_property="min",
                **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
        obj = DHeap.__new__(cls, elements, heap_property, 3)
        return obj

    @classmethod
    def methods(cls):
        return ['__new__']


class BinomialHeap(Heap):
    """
    Represents binomial heap.

    Parameters
    ==========

    root_list: list/tuple/Array
        By default, []
        The list of BinomialTree object references
        in sorted order.
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Examples
    ========

    >>> from pydatastructs import BinomialHeap
    >>> b = BinomialHeap()
    >>> b.insert(1, 1)
    >>> b.insert(2, 2)
    >>> b.find_minimum().key
    1
    >>> b.find_minimum().children[0].key
    2

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Binomial_heap
    """
    __slots__ = ['root_list']

    def __new__(cls, root_list=None, **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
        if root_list is None:
            root_list = []
        if not all((_check_type(root, BinomialTree))
                for root in root_list):
                    raise TypeError("The root_list should contain "
                                    "references to objects of BinomialTree.")
        obj = Heap.__new__(cls)
        obj.root_list = root_list
        return obj

    @classmethod
    def methods(cls):
        return ['__new__', 'merge_tree', 'merge', 'insert',
        'find_minimum', 'is_emtpy', 'decrease_key', 'delete',
        'delete_minimum']

    def merge_tree(self, tree1, tree2):
        """
        Merges two BinomialTree objects.

        Parameters
        ==========

        tree1: BinomialTree

        tree2: BinomialTree
        """
        if (not _check_type(tree1, BinomialTree)) or \
            (not _check_type(tree2, BinomialTree)):
            raise TypeError("Both the trees should be of type "
                            "BinomalTree.")
        ret_value = None
        if tree1.root.key <= tree2.root.key:
            tree1.add_sub_tree(tree2)
            ret_value = tree1
        else:
            tree2.add_sub_tree(tree1)
            ret_value = tree2
        return ret_value

    def _merge_heap_last_new_tree(self, new_root_list, new_tree):
        """
        Merges last tree node in root list with the incoming tree.
        """
        pos = -1
        if len(new_root_list) > 0 and new_root_list[pos].order == new_tree.order:
            new_root_list[pos] = self.merge_tree(new_root_list[pos], new_tree)
        else:
            new_root_list.append(new_tree)

    def merge(self, other_heap):
        """
        Merges current binomial heap with the given binomial heap.

        Parameters
        ==========

        other_heap: BinomialHeap
        """
        if not _check_type(other_heap, BinomialHeap):
            raise TypeError("Other heap is not of type BinomialHeap.")
        new_root_list = []
        i, j = 0, 0
        while (i < len(self.root_list)) and \
              (j < len(other_heap.root_list)):
            new_tree = None
            while self.root_list[i] is None:
                i += 1
            while other_heap.root_list[j] is None:
                j += 1
            if self.root_list[i].order == other_heap.root_list[j].order:
                new_tree = self.merge_tree(self.root_list[i],
                                           other_heap.root_list[j])
                i += 1
                j += 1
            else:
                if self.root_list[i].order < other_heap.root_list[j].order:
                    new_tree = self.root_list[i]
                    i += 1
                else:
                    new_tree = other_heap.root_list[j]
                    j += 1
            self._merge_heap_last_new_tree(new_root_list, new_tree)

        while i < len(self.root_list):
            new_tree = self.root_list[i]
            self._merge_heap_last_new_tree(new_root_list, new_tree)
            i += 1
        while j < len(other_heap.root_list):
            new_tree = other_heap.root_list[j]
            self._merge_heap_last_new_tree(new_root_list, new_tree)
            j += 1
        self.root_list = new_root_list

    def insert(self, key, data=None):
        """
        Inserts new node with the given key and data.

        key
            The key of the node which can be operated
            upon by relational operators.

        data
            The data to be stored in the new node.
        """
        new_node = BinomialTreeNode(key, data)
        new_tree = BinomialTree(root=new_node, order=0)
        new_heap = BinomialHeap(root_list=[new_tree])
        self.merge(new_heap)

    def find_minimum(self, **kwargs):
        """
        Finds the node with the minimum key.

        Returns
        =======

        min_node: BinomialTreeNode
        """
        if self.is_empty:
            raise IndexError("Binomial heap is empty.")
        min_node = None
        idx, min_idx = 0, None
        for tree in self.root_list:
            if ((min_node is None) or
                (tree is not None and tree.root is not None and
                 min_node.key > tree.root.key)):
                min_node = tree.root
                min_idx = idx
            idx += 1
        if kwargs.get('get_index', None) is not None:
            return min_node, min_idx
        return min_node

    def delete_minimum(self):
        """
        Deletes the node with minimum key.
        """
        min_node, min_idx = self.find_minimum(get_index=True)
        child_root_list = []
        for k, child in enumerate(min_node.children):
            if child is not None:
                child_root_list.append(BinomialTree(root=child, order=k))
        self.root_list.remove(self.root_list[min_idx])
        child_heap = BinomialHeap(root_list=child_root_list)
        self.merge(child_heap)

    @property
    def is_empty(self):
        return not self.root_list

    def decrease_key(self, node, new_key):
        """
        Decreases the key of the given node.

        Parameters
        ==========

        node: BinomialTreeNode
            The node whose key is to be reduced.
        new_key
            The new key of the given node,
            should be less than the current key.
        """
        if node.key <= new_key:
            raise ValueError("The new key "
            "should be less than current node's key.")
        node.key = new_key
        while ((not node.is_root) and
               (node.parent.key > node.key)):
            node.parent.key, node.key = \
                node.key, node.parent.key
            node.parent.data, node.data = \
                node.data, node.parent.data
            node = node.parent

    def delete(self, node):
        """
        Deletes the given node.

        Parameters
        ==========

        node: BinomialTreeNode
            The node which is to be deleted.
        """
        self.decrease_key(node, self.find_minimum().key - 1)
        self.delete_minimum()
