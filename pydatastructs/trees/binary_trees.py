from __future__ import print_function, division
from pydatastructs.utils.misc_util import Node

__all__ = [
    'Node',
    'BinaryTree',
    'BinarySearchTree'
]

class BinaryTree(object):
    """
    Abstract binary tree.

    Parameters
    ==========

    root_data
        Optional, the root node of the binary tree.
        If not of type Node, it will consider
        root as data and a new root node will
        be created.
    key
        Required if tree is to be instantiated with
        root otherwise not needed.
    comp: lambda
        Optional, A lambda function which will be used
        for comparison of keys. Should return a
        bool value. By default it implements less
        than operator.

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Binary_tree
    """

    __slots__ = ['root_idx', 'comparator', 'tree', 'size']

    def __new__(cls, key=None, root_data=None, comp=None):
        obj = object.__new__(cls)
        if key == None and root_data != None:
            raise ValueError('Key required.')
        key = None if root_data == None else key
        root = Node(key, root_data)
        root.is_root = True
        obj.root_idx = 0
        obj.tree, obj.size = [root], 1
        obj.comparator = lambda key1, key2: key1 < key2 \
                        if comp == None else comp
        return obj

    def __str__(self):
        return str([(node.left, node.key, node.data, node.right)
                    for node in self.tree])


class BinarySearchTree(BinaryTree):
    """
    Represents binary search trees.

    Examples
    ========

    >>> from pydatastructs.trees import BinarySearchTree as BST
    >>> b = BST()
    >>> b.insert(1, 1)
    >>> b.insert(2, 2)
    >>> child = b.tree[b.root_idx].right
    >>> b.tree[child].data
    2
    >>> b.search(1)
    0
    >>> b.search(-1) == None
    True
    >>> b.delete(1) == True
    True
    >>> b.search(1) == None
    True
    >>> b.delete(2) == True
    True
    >>> b.search(2) == None
    True

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Binary_search_tree
    """
    def insert(self, key, data):
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
        walk = self.root_idx
        if self.tree[walk].key == None:
            self.tree[walk].key = key
            self.tree[walk].data = data
            return None
        new_node = Node(key, data)
        while True:
            if self.tree[walk].key == key:
                self.tree[walk].data = data
                return None
            if not self.comparator(key, self.tree[walk].key):
                if self.tree[walk].right == None:
                    self.tree.append(new_node)
                    self.tree[walk].right = self.size
                    self.size += 1
                    return None
                walk = self.tree[walk].right
            else:
                if self.tree[walk].left == None:
                    self.tree.append(new_node)
                    self.tree[walk].left = self.size
                    self.size += 1
                    return None
                walk = self.tree[walk].left

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
        ret_parent = kwargs.get('parent', False)
        parent = None
        walk = self.root_idx
        if self.tree[walk].key == None:
            return None
        while walk != None:
            if self.tree[walk].key == key:
                break
            parent = walk
            if self.comparator(key, self.tree[walk].key):
                walk = self.tree[walk].left
            else:
                walk = self.tree[walk].right
        return (walk, parent) if ret_parent else walk

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
        node are removed but the it is still in three. This
        is being done to keep the complexity of deletion, O(logn).
        """
        (walk, parent) = self.search(key, parent=True)
        if walk == None:
            return None
        if self.tree[walk].left == None and \
            self.tree[walk].right == None:
            if parent == None:
                self.tree[self.root_idx].data = None
                self.tree[self.root_idx].key = None
            else:
                if self.tree[parent].left == walk:
                    self.tree[parent].left = None
                else:
                    self.tree[parent].right = None

        elif self.tree[walk].left != None and \
            self.tree[walk].right != None:
            twalk = self.tree[walk].right
            par = walk
            while self.tree[twalk].left != None:
                par = twalk
                twalk = self.tree[twalk].left
            self.tree[walk].data = self.tree[twalk].data
            self.tree[walk].key = self.tree[twalk].key
            self.tree[par].left = self.tree[twalk].right

        else:
            if self.tree[walk].left != None:
                child = self.tree[walk].left
            else:
                child = self.tree[walk].right
            if parent == None:
                self.tree[self.root_idx].left = self.tree[child].left
                self.tree[self.root_idx].right = self.tree[child].right
                self.tree[self.root_idx].data = self.tree[child].data
                self.tree[self.root_idx].key = self.tree[child].key
                self.tree[child].left = None
                self.tree[child].right = None
            else:
                if self.tree[parent].left == walk:
                    self.tree[parent].left = child
                else:
                    self.tree[parent].right = child

        return True
