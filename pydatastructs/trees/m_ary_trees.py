from pydatastructs.utils import MAryTreeNode, ParentPointerTreeNode
from pydatastructs.linear_data_structures.arrays import ArrayForTrees
from pydatastructs.utils.misc_util import (
    Backend, raise_if_backend_is_not_python)

__all__ = [
    'MAryTree'
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

class ParentPointerTree(MAryTree):
    """
    Implements a tree with parent pointers.

    Parameters
    ==========

    key
        Required if tree is to be instantiated with
        root otherwise not needed.
    root_data
        Optional, the root node of the tree.
        If not of type TreeNode, it will consider
        root as data and a new root node will
        be created.
    comp: lambda
        Optional, A lambda function which will be used
        for comparison of keys. Should return a
        bool value. By default it implements less
        than operator.

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Tree_(data_structure)#Parent_pointer_tree
    """

    __slots__ = ['root_idx', 'comparator', 'tree', 'size']

    def __new__(cls, key=None, root_data=None, comp=None, **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
        obj = object.__new__(cls)

        # Empty tree
        if key is None:
            obj.root_idx = None
            obj.tree, obj.size = ArrayForTrees(ParentPointerTreeNode, []), 0
            obj.comparator = lambda key1, key2: key1 < key2 \
                if comp is None else comp
            return obj

        root = ParentPointerTreeNode(key, root_data)
        root.is_root = True
        obj.root_idx = 0
        obj.tree, obj.size = ArrayForTrees(ParentPointerTreeNode, [root]), 1
        obj.comparator = lambda key1, key2: key1 < key2 \
            if comp is None else comp

        return obj

    @classmethod
    def methods(cls):
        return ['__new__', '__str__']

    def insert(self, parent_key, key, data=None):
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
        if key is None:
            raise ValueError("Key is required.")

        # Empty tree
        if self.size == 0:
            if parent_key is not None:
                raise ValueError("Parent key should be None.")

            root = ParentPointerTreeNode(key, data)
            root.is_root = True
            self.tree.append(root)
            self.size += 1
            return

        if parent_key is None:
            raise ValueError("Parent key is required.")

        if self.search(key) is not None:
            raise ValueError("Key already exists.")

        parent_node = self.search(parent_key)
        new_node = ParentPointerTreeNode(key, data, parent_node)

        self.tree.append(new_node)
        self.size += 1

    def delete(self, key):
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
        for idx in range(self.tree._last_pos_filled + 1):
            if self.tree[idx] and self.tree[idx].key == key:
                self.tree.delete(idx)
                self.size -= 1
                return True

        return None

    def search(self, key, **kwargs):
        """
        Searches for the data in the tree
        using iterative algorithm.

        Parameters
        ==========

        key
            The key for searching.
        get_parent: bool
            If true then returns node of the
            parent of the node with the passed
            key.
            By default, False

        Returns
        =======

        ParentPointerTreeNode
            The tree node if it was found
            in the tree.
        None
            In all other cases.
        """
        parent = kwargs.get('parent', False)

        for idx in range(self.tree._last_pos_filled + 1):
            node = self.tree[idx]
            if node is not None and node.key == key:
                if parent:
                    return node.parent
                return node

        return None


    def least_common_ancestor(self, first_child_key, second_child_key):
        """
        Finds the least common ancestor of two nodes in
        the tree.

        Parameters
        ==========

        first_child_key
            The key of the first child node.
        second_child_key
            The key of the second child node.

        Returns
        =======

        ParentPointerTreeNode
            The least common ancestor node.
        None
            If either of the nodes doesn't exist in the tree.
        """
        first_node = self.search(first_child_key)
        second_node = self.search(second_child_key)

        # One or both nodes do not exist
        if first_node is None or second_node is None:
            return None

        first_ancestors = set()

        while first_node is not None:
            first_ancestors.add(first_node)
            first_node = first_node.parent

        while second_node is not None:
            if second_node in first_ancestors:
                return second_node  # Found the least common ancestor
            second_node = second_node.parent

        return None  # No common ancestor found

    def __str__(self):
        to_be_printed = []
        for i in range(self.tree._last_pos_filled + 1):
            if self.tree[i] is not None:
                node = self.tree[i]
                to_be_printed.append((node.key, node.data, str(node.parent)))
        return str(to_be_printed)
