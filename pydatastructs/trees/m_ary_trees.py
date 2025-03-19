import math
from pydatastructs.utils import MAryTreeNode
from pydatastructs.linear_data_structures.arrays import ArrayForTrees
from pydatastructs.utils.misc_util import (
    Backend, raise_if_backend_is_not_python)

__all__ = [
    'MAryTree',
    'FusionTree'
]

class MAryTree(object):
    """
    Abstract m-ary tree.

    Parameters
    ==========

    key
        Required if tree is to be instantiated with
        root otherwise not needed.
    root_data
        Optional, the root node of the binary tree.
        If not of type MAryTreeNode, it will consider
        root as data and a new root node will
        be created.
    comp: lambda
        Optional, A lambda function which will be used
        for comparison of keys. Should return a
        bool value. By default it implements less
        than operator.
    is_order_statistic: bool
        Set it to True, if you want to use the
        order statistic features of the tree.
    max_children
        Optional, specifies the maximum number of children
        a node can have. Defaults to 2 in case nothing is
        specified.

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/M-ary_tree
    """

    __slots__ = ['root_idx', 'max_children', 'comparator', 'tree', 'size',
                 'is_order_statistic']


    def __new__(cls, key=None, root_data=None, comp=None,
                is_order_statistic=False, max_children=2,
                **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
        obj = object.__new__(cls)
        if key is None and root_data is not None:
            raise ValueError('Key required.')
        key = None if root_data is None else key
        root = MAryTreeNode(key, root_data)
        root.is_root = True
        obj.root_idx = 0
        obj.max_children = max_children
        obj.tree, obj.size = ArrayForTrees(MAryTreeNode, [root]), 1
        obj.comparator = lambda key1, key2: key1 < key2 \
                        if comp is None else comp
        obj.is_order_statistic = is_order_statistic
        return obj

    @classmethod
    def methods(cls):
        return ['__new__', '__str__']

    def insert(self, key, data=None):
        """
        Inserts data by the passed key using iterative
        algorithm.

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
        raise NotImplementedError("This is an abstract method.")

    def delete(self, key, **kwargs):
        """
        Deletes the data with the passed key
        using iterative algorithm.

        Parameters
        ==========

        key
            The key of the node which is
            to be deleted.

        Returns
        =======

        True
            If the node is deleted successfully.

        None
            If the node to be deleted doesn't exists.

        Note
        ====

        The node is deleted means that the connection to that
        node are removed but the it is still in tree.
        """
        raise NotImplementedError("This is an abstract method.")

    def search(self, key, **kwargs):
        """
        Searches for the data in the binary search tree
        using iterative algorithm.

        Parameters
        ==========

        key
            The key for searching.
        parent: bool
            If true then returns index of the
            parent of the node with the passed
            key.
            By default, False

        Returns
        =======

        int
            If the node with the passed key is
            in the tree.
        tuple
            The index of the searched node and
            the index of the parent of that node.
        None
            In all other cases.
        """
        raise NotImplementedError("This is an abstract method.")

    def to_binary_tree(self):
        """
        Converts an m-ary tree to a binary tree.

        Returns
        =======

        TreeNode
            The root of the newly created binary tree.
        """
        raise NotImplementedError("This is an abstract method.")


    def __str__(self):
        to_be_printed = ['' for i in range(self.tree._last_pos_filled + 1)]
        for i in range(self.tree._last_pos_filled + 1):
            if self.tree[i] is not None:
                node = self.tree[i]
                to_be_printed[i] = (node.key, node.data)
                for j in node.children:
                    if j is not None:
                        to_be_printed[i].append(j)
        return str(to_be_printed)


class FusionTree(MAryTree):
    """
    Implements a Fusion Tree, a multi-way search tree optimized for integer keys.

    Parameters
    ==========

    key: int
        The integer key to insert.
    root_data: Any
        Optional data to store with the key.
    backend: pydatastructs.Backend
        The backend to be used. Available backends: Python and C++
        Optional, by default, the Python backend is used. For faster execution, use the C++ backend.
    word_size: int
        The size of the integer keys in bits.
        Optional, by default, set to 64.

    Examples
    ========

    >>> from pydatastructs import FusionTree
    >>> ft = FusionTree()
    >>> ft.insert(1, 1)
    >>> ft.insert(2, 2)
    >>> ft.search(1)
    0
    >>> ft.delete(1)
    True
    >>> ft.search(1)


    References:
    - https://en.wikipedia.org/wiki/Fusion_tree
    - Fredman & Willard (1990): "Fusion Trees"
    """

    __slots__ = ['root_idx', 'tree', 'size', 'B',
                 'sketch_mask', 'fingerprint_multiplier']

    def __new__(cls, key=None, root_data=None, **kwargs):
        backend = kwargs.get('backend', Backend.PYTHON)
        raise_if_backend_is_not_python(cls, backend)

        obj = object.__new__(cls)
        key = None if root_data is None else key
        root = MAryTreeNode(key, root_data)
        root.is_root = True
        obj.root_idx = 0
        obj.tree, obj.size = ArrayForTrees(MAryTreeNode, [root]), 1
        obj.B = int(math.log2(kwargs.get('word_size', 64))
                    ** (1/5))  # Multi-way branching factor
        obj.sketch_mask = 0  # Computed dynamically
        obj.fingerprint_multiplier = 2654435761  # Prime multiplier for fingerprinting
        return obj

    def _compute_sketch_mask(self):
        """
        Computes a sketch mask for efficient parallel comparisons.
        """
        keys = [node.key for node in self.tree if node is not None]
        if len(keys) > 1:
            significant_bits = [max(k.bit_length() for k in keys)]
            self.sketch_mask = sum(1 << b for b in significant_bits)

    def insert(self, key, data=None):
        """
        Inserts a key into the Fusion Tree.

        Parameters
        ==========

        key: int
            The integer key to insert.
        data: Any
            Optional data to store with the key.
        """
        # Edge case for root node if not intially inserted
        if self.size == 1 and self.tree[0].key is None:
            self.tree[0] = MAryTreeNode(key, data)
            self.tree[0].is_root = True
            return

        node = MAryTreeNode(key, data)
        self.tree.append(node)
        self.size += 1
        if self.size > 1:
            self._compute_sketch_mask()

    def _sketch_key(self, key):
        """
        Applies the sketch mask to compress the key for fast comparison.
        """
        return key & self.sketch_mask

    def _fingerprint(self, key):
        """
        Uses multiplication-based fingerprinting to create a unique identifier
        for the key, allowing fast parallel searches.
        """
        return (key * self.fingerprint_multiplier) & ((1 << 64) - 1)

    def search(self, key):
        """
        Searches for a key in the Fusion Tree using bitwise sketching and fingerprinting.

        Parameters
        ==========

        key: int
            The integer key to search.

        Returns
        =======

        int: The index of the key in the tree, or None if not found.
        """
        sketch = self._sketch_key(key)
        fingerprint = self._fingerprint(key)
        for i in range(self.size):
            if self._sketch_key(self.tree[i].key) == sketch and self._fingerprint(self.tree[i].key) == fingerprint:
                return i
        return None

    def delete(self, key):
        """
        Deletes a key from the Fusion Tree.

        Parameters
        ==========

        key: int
            The integer key to delete.

        Returns
        =======

        bool: True if the key was successfully deleted, False otherwise.

        """
        index = self.search(key)
        if index is not None:
            self.tree[index] = None  # Soft delete
            # Compact tree
            self.tree = [node for node in self.tree if node is not None]
            self.size -= 1
            if self.size > 1:
                self._compute_sketch_mask()
            return True
        return False

    def __str__(self):
        """
        Returns a string representation of the Fusion Tree.
        """
        return str([(node.key, node.data) for node in self.tree if node is not None])
