import random
from collections import deque as Queue
from pydatastructs.utils import TreeNode, CartesianTreeNode, RedBlackTreeNode
from pydatastructs.miscellaneous_data_structures import Stack
from pydatastructs.linear_data_structures import OneDimensionalArray
from pydatastructs.linear_data_structures.arrays import ArrayForTrees
from pydatastructs.utils.misc_util import (
    Backend, raise_if_backend_is_not_python)
from pydatastructs.trees._backend.cpp import _trees

__all__ = [
    'AVLTree',
    'BinaryTree',
    'BinarySearchTree',
    'BinaryTreeTraversal',
    'BinaryIndexedTree',
    'CartesianTree',
    'Treap',
    'SplayTree',
    'RedBlackTree'
]

class BinaryTree(object):
    """
    Abstract binary tree.

    Parameters
    ==========

    key
        Required if tree is to be instantiated with
        root otherwise not needed.
    root_data
        Optional, the root node of the binary tree.
        If not of type TreeNode, it will consider
        root as data and a new root node will
        be created.
    comp: lambda/function
        Optional, A lambda function which will be used
        for comparison of keys. Should return a
        bool value. By default it implements less
        than operator.
    is_order_statistic: bool
        Set it to True, if you want to use the
        order statistic features of the tree.
    backend: pydatastructs.Backend
        The backend to be used. Available backends: Python and C++
        Optional, by default, the Python backend is used. For faster execution, use the C++ backend.

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Binary_tree
    """

    __slots__ = ['root_idx', 'comparator', 'tree', 'size',
                 'is_order_statistic']

    def __new__(cls, key=None, root_data=None, comp=None,
                is_order_statistic=False, **kwargs):
        backend = kwargs.get('backend', Backend.PYTHON)
        if backend == Backend.CPP:
            if comp is None:
                comp = lambda key1, key2: key1 < key2
            return _trees.BinaryTree(key, root_data, comp, is_order_statistic, **kwargs) # If any argument is not given, then it is passed as None, except for comp
        obj = object.__new__(cls)
        if key is None and root_data is not None:
            raise ValueError('Key required.')
        key = None if root_data is None else key
        root = TreeNode(key, root_data)
        root.is_root = True
        obj.root_idx = 0
        obj.tree, obj.size = ArrayForTrees(TreeNode, [root]), 1
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
        balancing_info: bool
            Optional, by default, False
            The information needed for updating
            the tree is returned if this parameter
            is set to True. It is not meant for
            user facing APIs.

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


    def __str__(self):
        to_be_printed = ['' for i in range(self.tree._last_pos_filled + 1)]
        for i in range(self.tree._last_pos_filled + 1):
            if self.tree[i] is not None:
                node = self.tree[i]
                to_be_printed[i] = (node.left, node.key, node.data, node.right)
        return str(to_be_printed)

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
    >>> b.search(-1) is None
    True
    >>> b.delete(1) is True
    True
    >>> b.search(1) is None
    True
    >>> b.delete(2) is True
    True
    >>> b.search(2) is None
    True

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Binary_search_tree

    See Also
    ========

    pydatastructs.trees.binary_tree.BinaryTree
    """

    @classmethod
    def methods(cls):
        return ['insert', 'search', 'delete', 'select',
        'rank', 'lowest_common_ancestor']

    left_size = lambda self, node: self.tree[node.left].size \
                                        if node.left is not None else 0
    right_size = lambda self, node: self.tree[node.right].size \
                                        if node.right is not None else 0
    def __new__(cls, key=None, root_data=None, comp=None,
                is_order_statistic=False, **kwargs):
        backend = kwargs.get('backend', Backend.PYTHON)
        if backend == Backend.CPP:
            if comp is None:
                comp = lambda key1, key2: key1 < key2
            return _trees.BinarySearchTree(key, root_data, comp, is_order_statistic, **kwargs) # If any argument is not given, then it is passed as None, except for comp
        return super().__new__(cls, key, root_data, comp, is_order_statistic, **kwargs)

    def _update_size(self, start_idx):
        if self.is_order_statistic:
            walk = start_idx
            while walk is not None:
                self.tree[walk].size = (
                    self.left_size(self.tree[walk]) +
                    self.right_size(self.tree[walk]) + 1)
                walk = self.tree[walk].parent

    def insert(self, key, data=None):
        res = self.search(key)
        if res is not None:
            self.tree[res].data = data
            return None
        walk = self.root_idx
        if self.tree[walk].key is None:
            self.tree[walk].key = key
            self.tree[walk].data = data
            return None
        new_node, prev_node, flag = TreeNode(key, data), self.root_idx, True
        while flag:
            if not self.comparator(key, self.tree[walk].key):
                if self.tree[walk].right is None:
                    new_node.parent = prev_node
                    self.tree.append(new_node)
                    self.tree[walk].right = self.size
                    self.size += 1
                    flag = False
                prev_node = walk = self.tree[walk].right
            else:
                if self.tree[walk].left is None:
                    new_node.parent = prev_node
                    self.tree.append(new_node)
                    self.tree[walk].left = self.size
                    self.size += 1
                    flag = False
                prev_node = walk = self.tree[walk].left
        self._update_size(walk)

    def search(self, key, **kwargs):
        ret_parent = kwargs.get('parent', False)
        parent = None
        walk = self.root_idx
        if self.tree[walk].key is None:
            return None
        while walk is not None:
            if self.tree[walk].key == key:
                break
            parent = walk
            if self.comparator(key, self.tree[walk].key):
                walk = self.tree[walk].left
            else:
                walk = self.tree[walk].right
        return (walk, parent) if ret_parent else walk

    def _bound_helper(self, node_idx, bound_key, is_upper=False):
        if node_idx is None:
            return None
        if self.tree[node_idx].key is None:
            return None

        if self.tree[node_idx].key == bound_key:
            if not is_upper:
                return self.tree[node_idx].key
            else:
                return self._bound_helper(self.tree[node_idx].right,
                                            bound_key, is_upper)

        if self.comparator(self.tree[node_idx].key, bound_key):
            return self._bound_helper(self.tree[node_idx].right,
                                            bound_key, is_upper)
        else:
            res_bound = self._bound_helper(self.tree[node_idx].left,
                                                   bound_key, is_upper)
            return res_bound if res_bound is not None else self.tree[node_idx].key


    def lower_bound(self, key, **kwargs):
        """
        Finds the lower bound of the given key in the tree

        Parameters
        ==========

        key
            The key for comparison

        Examples
        ========

        >>> from pydatastructs.trees import BinarySearchTree as BST
        >>> b = BST()
        >>> b.insert(10, 10)
        >>> b.insert(18, 18)
        >>> b.insert(7, 7)
        >>> b.lower_bound(9)
        10
        >>> b.lower_bound(7)
        7
        >>> b.lower_bound(20) is None
        True

        Returns
        =======

        value
            The lower bound of the given key.
            Returns None if the value doesn't exist
        """
        return self._bound_helper(self.root_idx, key)


    def upper_bound(self, key, **kwargs):
        """
        Finds the upper bound of the given key in the tree

        Parameters
        ==========

        key
            The key for comparison

        Examples
        ========

        >>> from pydatastructs.trees import BinarySearchTree as BST
        >>> b = BST()
        >>> b.insert(10, 10)
        >>> b.insert(18, 18)
        >>> b.insert(7, 7)
        >>> b.upper_bound(9)
        10
        >>> b.upper_bound(7)
        10
        >>> b.upper_bound(20) is None
        True

        Returns
        =======

        value
            The upper bound of the given key.
            Returns None if the value doesn't exist
        """
        return self._bound_helper(self.root_idx, key, True)


    def delete(self, key, **kwargs):
        (walk, parent) = self.search(key, parent=True)
        a = None
        if walk is None:
            return None
        if self.tree[walk].left is None and \
            self.tree[walk].right is None:
            if parent is None:
                self.tree[self.root_idx].data = None
                self.tree[self.root_idx].key = None
            else:
                if self.tree[parent].left == walk:
                    self.tree[parent].left = None
                else:
                    self.tree[parent].right = None
                a = parent
                par_key, root_key = (self.tree[parent].key,
                                     self.tree[self.root_idx].key)
                new_indices = self.tree.delete(walk)
                if new_indices is not None:
                    a = new_indices[par_key]
                    self.root_idx = new_indices[root_key]
            self._update_size(a)

        elif self.tree[walk].left is not None and \
            self.tree[walk].right is not None:
            twalk = self.tree[walk].right
            par = walk
            flag = False
            while self.tree[twalk].left is not None:
                flag = True
                par = twalk
                twalk = self.tree[twalk].left
            self.tree[walk].data = self.tree[twalk].data
            self.tree[walk].key = self.tree[twalk].key
            if flag:
                self.tree[par].left = self.tree[twalk].right
            else:
                self.tree[par].right = self.tree[twalk].right
            if self.tree[twalk].right is not None:
                self.tree[self.tree[twalk].right].parent = par
            if twalk is not None:
                a = par
                par_key, root_key = (self.tree[par].key,
                                     self.tree[self.root_idx].key)
                new_indices = self.tree.delete(twalk)
                if new_indices is not None:
                    a = new_indices[par_key]
                    self.root_idx = new_indices[root_key]
            self._update_size(a)

        else:
            if self.tree[walk].left is not None:
                child = self.tree[walk].left
            else:
                child = self.tree[walk].right
            if parent is None:
                self.tree[self.root_idx].left = self.tree[child].left
                self.tree[self.root_idx].right = self.tree[child].right
                self.tree[self.root_idx].data = self.tree[child].data
                self.tree[self.root_idx].key = self.tree[child].key
                self.tree[self.root_idx].parent = None
                root_key = self.tree[self.root_idx].key
                new_indices = self.tree.delete(child)
                if new_indices is not None:
                    self.root_idx = new_indices[root_key]
            else:
                if self.tree[parent].left == walk:
                    self.tree[parent].left = child
                else:
                    self.tree[parent].right = child
                self.tree[child].parent = parent
                a = parent
                par_key, root_key = (self.tree[parent].key,
                                     self.tree[self.root_idx].key)
                new_indices = self.tree.delete(walk)
                if new_indices is not None:
                    parent = new_indices[par_key]
                    self.tree[child].parent = new_indices[par_key]
                    a = new_indices[par_key]
                    self.root_idx = new_indices[root_key]
                self._update_size(a)

        if kwargs.get("balancing_info", False) is not False:
            return a
        return True

    def select(self, i):
        """
        Finds the i-th smallest node in the tree.

        Parameters
        ==========

        i: int
            A positive integer

        Returns
        =======

        n: TreeNode
            The node with the i-th smallest key

        References
        ==========

        .. [1] https://en.wikipedia.org/wiki/Order_statistic_tree
        """
        i -= 1 # The algorithm is based on zero indexing
        if i < 0:
            raise ValueError("Expected a positive integer, got %d"%(i + 1))
        if i >= self.tree._num:
            raise ValueError("%d is greater than the size of the "
                "tree which is, %d"%(i + 1, self.tree._num))
        walk = self.root_idx
        while walk is not None:
            l = self.left_size(self.tree[walk])
            if i == l:
                return self.tree[walk]
            left_walk = self.tree[walk].left
            right_walk = self.tree[walk].right
            if left_walk is None and right_walk is None:
                raise IndexError("The traversal is terminated "
                                 "due to no child nodes ahead.")
            if i < l:
                if left_walk is not None and \
                    self.comparator(self.tree[left_walk].key,
                    self.tree[walk].key):
                    walk = left_walk
                else:
                    walk = right_walk
            else:
                if right_walk is not None and \
                    not self.comparator(self.tree[right_walk].key,
                    self.tree[walk].key):
                    walk = right_walk
                else:
                    walk = left_walk
                i -= (l + 1)

    def rank(self, x):
        """
        Finds the rank of the given node, i.e.
        its index in the sorted list of nodes
        of the tree.

        Parameters
        ==========

        x: key
            The key of the node whose rank is to be found out.
        """
        walk = self.search(x)
        if walk is None:
            return None
        r = self.left_size(self.tree[walk]) + 1
        while self.tree[walk].key != self.tree[self.root_idx].key:
            p = self.tree[walk].parent
            if walk == self.tree[p].right:
                r += self.left_size(self.tree[p]) + 1
            walk = p
        return r

    def _simple_path(self, key, root):
        """
        Utility funtion to find the simple path between root and node.

        Parameters
        ==========

        key: Node.key
            Key of the node to be searched

        Returns
        =======

        path: list
        """

        stack = Stack()
        stack.push(root)
        path = []
        node_idx = -1

        while not stack.is_empty:
            node = stack.pop()
            if self.tree[node].key == key:
                node_idx = node
                break
            if self.tree[node].left:
                stack.push(self.tree[node].left)
            if self.tree[node].right:
                stack.push(self.tree[node].right)

        if node_idx == -1:
            return path

        while node_idx != 0:
            path.append(node_idx)
            node_idx = self.tree[node_idx].parent
        path.append(0)
        path.reverse()

        return path

    def _lca_1(self, j, k):
        root = self.root_idx
        path1 = self._simple_path(j, root)
        path2 = self._simple_path(k, root)
        if not path1 or not path2:
            raise ValueError("One of two path doesn't exists. See %s, %s"
                             %(path1, path2))

        n, m = len(path1), len(path2)
        i = j = 0
        while i < n and j < m:
            if path1[i] != path2[j]:
                return self.tree[path1[i - 1]].key
            i += 1
            j += 1
        if path1 < path2:
            return self.tree[path1[-1]].key
        return self.tree[path2[-1]].key

    def _lca_2(self, j, k):
        curr_root = self.root_idx
        u, v = self.search(j), self.search(k)
        if (u is None) or (v is None):
            raise ValueError("One of the nodes with key %s "
                             "or %s doesn't exits"%(j, k))
        u_left = self.comparator(self.tree[u].key, \
            self.tree[curr_root].key)
        v_left = self.comparator(self.tree[v].key, \
            self.tree[curr_root].key)

        while not (u_left ^ v_left):
            if u_left and v_left:
                curr_root = self.tree[curr_root].left
            else:
                curr_root = self.tree[curr_root].right

            if curr_root == u or curr_root == v:
                if curr_root is None:
                    return None
                return self.tree[curr_root].key
            u_left = self.comparator(self.tree[u].key, \
                self.tree[curr_root].key)
            v_left = self.comparator(self.tree[v].key, \
                self.tree[curr_root].key)

        if curr_root is None:
            return curr_root
        return self.tree[curr_root].key

    def lowest_common_ancestor(self, j, k, algorithm=1):

        """
        Computes the lowest common ancestor of two nodes.

        Parameters
        ==========

        j: Node.key
            Key of first node

        k: Node.key
            Key of second node

        algorithm: int
            The algorithm to be used for computing the
            lowest common ancestor.
            Optional, by default uses algorithm 1.

            1 -> Determines the lowest common ancestor by finding
                    the first intersection of the paths from v and w
                    to the root.

            2 -> Modifed version of the algorithm given in the
                    following publication,
                    D. Harel. A linear time algorithm for the
                    lowest common ancestors problem. In 21s
                    Annual Symposium On Foundations of
                    Computer Science, pages 308-319, 1980.

        Returns
        =======

        Node.key
            The key of the lowest common ancestor in the tree.
            if both the nodes are present in the tree.

        References
        ==========

        .. [1] https://en.wikipedia.org/wiki/Lowest_common_ancestor

        .. [2] https://pdfs.semanticscholar.org/e75b/386cc554214aa0ebd6bd6dbdd0e490da3739.pdf

        """
        return getattr(self, "_lca_"+str(algorithm))(j, k)

class SelfBalancingBinaryTree(BinarySearchTree):
    """
    Represents Base class for all rotation based balancing trees like AVL tree, Red Black tree, Splay Tree.
    """
    def __new__(cls, key=None, root_data=None, comp=None,
                is_order_statistic=False, **kwargs):
        backend = kwargs.get('backend', Backend.PYTHON)
        if backend == Backend.CPP:
            if comp is None:
                comp = lambda key1, key2: key1 < key2
            return _trees.SelfBalancingBinaryTree(key, root_data, comp, is_order_statistic, **kwargs) # If any argument is not given, then it is passed as None, except for comp
        return super().__new__(cls, key, root_data, comp, is_order_statistic, **kwargs)

    def _right_rotate(self, j, k):
        y = self.tree[k].right
        if y is not None:
            self.tree[y].parent = j
        self.tree[j].left = y
        self.tree[k].parent = self.tree[j].parent
        if self.tree[k].parent is not None:
            if self.tree[self.tree[k].parent].left == j:
                self.tree[self.tree[k].parent].left = k
            else:
                self.tree[self.tree[k].parent].right = k
        self.tree[j].parent = k
        self.tree[k].right = j
        kp = self.tree[k].parent
        if kp is None:
            self.root_idx = k

    def _left_right_rotate(self, j, k):
        i = self.tree[k].right
        v, w = self.tree[i].left, self.tree[i].right
        self.tree[k].right, self.tree[j].left = v, w
        if v is not None:
            self.tree[v].parent = k
        if w is not None:
            self.tree[w].parent = j
        self.tree[i].left, self.tree[i].right, self.tree[i].parent = \
            k, j, self.tree[j].parent
        self.tree[k].parent, self.tree[j].parent = i, i
        ip = self.tree[i].parent
        if ip is not None:
            if self.tree[ip].left == j:
                self.tree[ip].left = i
            else:
                self.tree[ip].right = i
        else:
            self.root_idx = i

    def _right_left_rotate(self, j, k):
        i = self.tree[k].left
        v, w = self.tree[i].left, self.tree[i].right
        self.tree[k].left, self.tree[j].right = w, v
        if v is not None:
            self.tree[v].parent = j
        if w is not None:
            self.tree[w].parent = k
        self.tree[i].right, self.tree[i].left, self.tree[i].parent = \
            k, j, self.tree[j].parent
        self.tree[k].parent, self.tree[j].parent = i, i
        ip = self.tree[i].parent
        if ip is not None:
            if self.tree[ip].left == j:
                self.tree[ip].left = i
            else:
                self.tree[ip].right = i
        else:
            self.root_idx = i

    def _left_rotate(self, j, k):
        y = self.tree[k].left
        if y is not None:
            self.tree[y].parent = j
        self.tree[j].right = y
        self.tree[k].parent = self.tree[j].parent
        if self.tree[k].parent is not None:
            if self.tree[self.tree[k].parent].left == j:
                self.tree[self.tree[k].parent].left = k
            else:
                self.tree[self.tree[k].parent].right = k
        self.tree[j].parent = k
        self.tree[k].left = j
        kp = self.tree[k].parent
        if kp is None:
            self.root_idx = k

class CartesianTree(SelfBalancingBinaryTree):
    """
    Represents cartesian trees.

    Examples
    ========

    >>> from pydatastructs.trees import CartesianTree as CT
    >>> c = CT()
    >>> c.insert(1, 4, 1)
    >>> c.insert(2, 3, 2)
    >>> child = c.tree[c.root_idx].left
    >>> c.tree[child].data
    1
    >>> c.search(1)
    0
    >>> c.search(-1) is None
    True
    >>> c.delete(1) is True
    True
    >>> c.search(1) is None
    True
    >>> c.delete(2) is True
    True
    >>> c.search(2) is None
    True

    References
    ==========

    .. [1] https://www.cs.princeton.edu/courses/archive/spr09/cos423/Lectures/geo-st.pdf

    See Also
    ========

    pydatastructs.trees.binary_trees.SelfBalancingBinaryTree
    """
    def __new__(cls, key=None, root_data=None, comp=None,
            is_order_statistic=False, **kwargs):
        backend = kwargs.get('backend', Backend.PYTHON)
        if backend == Backend.CPP:
            if comp is None:
                comp = lambda key1, key2: key1 < key2
            return _trees.CartesianTree(key, root_data, comp, is_order_statistic, **kwargs) # If any argument is not given, then it is passed as None, except for comp
        return super().__new__(cls, key, root_data, comp, is_order_statistic, **kwargs)

    @classmethod
    def methods(cls):
        return ['__new__', '__str__', 'insert', 'delete']

    def _bubble_up(self, node_idx):
        node = self.tree[node_idx]
        parent_idx = self.tree[node_idx].parent
        parent = self.tree[parent_idx]
        while (node.parent is not None) and (parent.priority > node.priority):
            if parent.right == node_idx:
                self._left_rotate(parent_idx, node_idx)
            else:
                self._right_rotate(parent_idx, node_idx)
            node = self.tree[node_idx]
            parent_idx = self.tree[node_idx].parent
            if parent_idx is not None:
                parent = self.tree[parent_idx]
        if node.parent is None:
            self.tree[node_idx].is_root = True

    def _trickle_down(self, node_idx):
        node = self.tree[node_idx]
        while node.left is not None or node.right is not None:
            if node.left is None:
                self._left_rotate(node_idx, self.tree[node_idx].right)
            elif node.right is None:
                self._right_rotate(node_idx, self.tree[node_idx].left)
            elif self.tree[node.left].priority < self.tree[node.right].priority:
                self._right_rotate(node_idx, self.tree[node_idx].left)
            else:
                self._left_rotate(node_idx, self.tree[node_idx].right)
            node = self.tree[node_idx]

    def insert(self, key, priority, data=None):
        super(CartesianTree, self).insert(key, data)
        node_idx = super(CartesianTree, self).search(key)
        node = self.tree[node_idx]
        new_node = CartesianTreeNode(key, priority, data)
        new_node.parent = node.parent
        new_node.left = node.left
        new_node.right = node.right
        self.tree[node_idx] = new_node
        if node.is_root:
            self.tree[node_idx].is_root = True
        else:
            self._bubble_up(node_idx)

    def delete(self, key, **kwargs):
        balancing_info = kwargs.get('balancing_info', False)
        node_idx = super(CartesianTree, self).search(key)
        if node_idx is not None:
            self._trickle_down(node_idx)
            return super(CartesianTree, self).delete(key, balancing_info = balancing_info)

    def __str__(self):
        to_be_printed = ['' for i in range(self.tree._last_pos_filled + 1)]
        for i in range(self.tree._last_pos_filled + 1):
            if self.tree[i] is not None:
                node = self.tree[i]
                to_be_printed[i] = (node.left, node.key, node.priority, node.data, node.right)
        return str(to_be_printed)

class Treap(CartesianTree):
    """
    Represents treaps.

    Examples
    ========

    >>> from pydatastructs.trees import Treap as T
    >>> t = T()
    >>> t.insert(1, 1)
    >>> t.insert(2, 2)
    >>> t.search(1)
    0
    >>> t.search(-1) is None
    True
    >>> t.delete(1) is True
    True
    >>> t.search(1) is None
    True
    >>> t.delete(2) is True
    True
    >>> t.search(2) is None
    True

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Treap

    """
    def __new__(cls, key=None, root_data=None, comp=None,
            is_order_statistic=False, **kwargs):
        backend = kwargs.get('backend', Backend.PYTHON)
        if backend == Backend.CPP:
            if comp is None:
                comp = lambda key1, key2: key1 < key2
            return _trees.Treap(key, root_data, comp, is_order_statistic, **kwargs) # If any argument is not given, then it is passed as None, except for comp
        return super().__new__(cls, key, root_data, comp, is_order_statistic, **kwargs)

    @classmethod
    def methods(cls):
        return ['__new__', 'insert']

    def insert(self, key, data=None):
        priority = random.random()
        super(Treap, self).insert(key, priority, data)

class AVLTree(SelfBalancingBinaryTree):
    """
    Represents AVL trees.

    References
    ==========

    .. [1] https://courses.cs.washington.edu/courses/cse373/06sp/handouts/lecture12.pdf
    .. [2] https://en.wikipedia.org/wiki/AVL_tree
    .. [3] http://faculty.cs.niu.edu/~freedman/340/340notes/340avl2.htm

    See Also
    ========

    pydatastructs.trees.binary_trees.BinaryTree
    """

    def __new__(cls, key=None, root_data=None, comp=None,
                is_order_statistic=False, **kwargs):
        backend = kwargs.get('backend', Backend.PYTHON)
        if backend == Backend.CPP:
            if comp is None:
                comp = lambda key1, key2: key1 < key2
            return _trees.AVLTree(key, root_data, comp, is_order_statistic, **kwargs) # If any argument is not given, then it is passed as None, except for comp
        return super().__new__(cls, key, root_data, comp, is_order_statistic, **kwargs)

    @classmethod
    def methods(cls):
        return ['__new__', 'set_tree', 'insert', 'delete']

    left_height = lambda self, node: self.tree[node.left].height \
                                        if node.left is not None else -1
    right_height = lambda self, node: self.tree[node.right].height \
                                        if node.right is not None else -1
    balance_factor = lambda self, node: self.right_height(node) - \
                                        self.left_height(node)

    def set_tree(self, arr):
        self.tree = arr

    def _right_rotate(self, j, k):
        super(AVLTree, self)._right_rotate(j, k)
        self.tree[j].height = max(self.left_height(self.tree[j]),
                                  self.right_height(self.tree[j])) + 1
        if self.is_order_statistic:
            self.tree[j].size = (self.left_size(self.tree[j]) +
                                 self.right_size(self.tree[j]) + 1)

    def _left_right_rotate(self, j, k):
        super(AVLTree, self)._left_right_rotate(j, k)
        self.tree[j].height = max(self.left_height(self.tree[j]),
                                  self.right_height(self.tree[j])) + 1
        self.tree[k].height = max(self.left_height(self.tree[k]),
                                    self.right_height(self.tree[k])) + 1
        if self.is_order_statistic:
            self.tree[j].size = (self.left_size(self.tree[j]) +
                                 self.right_size(self.tree[j]) + 1)
            self.tree[k].size = (self.left_size(self.tree[k]) +
                                 self.right_size(self.tree[k]) + 1)

    def _right_left_rotate(self, j, k):
        super(AVLTree, self)._right_left_rotate(j, k)
        self.tree[j].height = max(self.left_height(self.tree[j]),
                                  self.right_height(self.tree[j])) + 1
        self.tree[k].height = max(self.left_height(self.tree[k]),
                                    self.right_height(self.tree[k])) + 1
        if self.is_order_statistic:
            self.tree[j].size = (self.left_size(self.tree[j]) +
                                 self.right_size(self.tree[j]) + 1)
            self.tree[k].size = (self.left_size(self.tree[k]) +
                                 self.right_size(self.tree[k]) + 1)

    def _left_rotate(self, j, k):
        super(AVLTree, self)._left_rotate(j, k)
        self.tree[j].height = max(self.left_height(self.tree[j]),
                                  self.right_height(self.tree[j])) + 1
        self.tree[k].height = max(self.left_height(self.tree[k]),
                                    self.right_height(self.tree[k])) + 1
        if self.is_order_statistic:
            self.tree[j].size = (self.left_size(self.tree[j]) +
                                 self.right_size(self.tree[j]) + 1)

    def _balance_insertion(self, curr, last):
        walk = last
        path = Queue()
        path.append(curr), path.append(last)
        while walk is not None:
            self.tree[walk].height = max(self.left_height(self.tree[walk]),
                                        self.right_height(self.tree[walk])) + 1
            if self.is_order_statistic:
                self.tree[walk].size = (self.left_size(self.tree[walk]) +
                                        self.right_size(self.tree[walk]) + 1)
            last = path.popleft()
            last2last = path.popleft()
            if self.balance_factor(self.tree[walk]) not in (1, 0, -1):
                l = self.tree[walk].left
                if l is not None and l == last and self.tree[l].left == last2last:
                    self._right_rotate(walk, last)
                r = self.tree[walk].right
                if r is not None and r == last and self.tree[r].right == last2last:
                    self._left_rotate(walk, last)
                if l is not None and l == last and self.tree[l].right == last2last:
                    self._left_right_rotate(walk, last)
                if r is not None and r == last and self.tree[r].left == last2last:
                    self._right_left_rotate(walk, last)
            path.append(walk), path.append(last)
            walk = self.tree[walk].parent

    def insert(self, key, data=None):
        super(AVLTree, self).insert(key, data)
        self._balance_insertion(self.size - 1, self.tree[self.size-1].parent)

    def _balance_deletion(self, start_idx, key):
        walk = start_idx
        while walk is not None:
            self.tree[walk].height = max(self.left_height(self.tree[walk]),
                                        self.right_height(self.tree[walk])) + 1
            if self.is_order_statistic:
                self.tree[walk].size = (self.left_size(self.tree[walk]) +
                                        self.right_size(self.tree[walk]) + 1)
            if self.balance_factor(self.tree[walk]) not in (1, 0, -1):
                if self.balance_factor(self.tree[walk]) < 0:
                    b = self.tree[walk].left
                    if self.balance_factor(self.tree[b]) <= 0:
                        self._right_rotate(walk, b)
                    else:
                        self._left_right_rotate(walk, b)
                else:
                    b = self.tree[walk].right
                    if self.balance_factor(self.tree[b]) >= 0:
                        self._left_rotate(walk, b)
                    else:
                        self._right_left_rotate(walk, b)
            walk = self.tree[walk].parent


    def delete(self, key, **kwargs):
        a = super(AVLTree, self).delete(key, balancing_info=True)
        self._balance_deletion(a, key)
        return True

class SplayTree(SelfBalancingBinaryTree):
    """
    Represents Splay Trees.

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Splay_tree

    """

    def __new__(cls, key=None, root_data=None, comp=None,
                is_order_statistic=False, **kwargs):
        backend = kwargs.get('backend', Backend.PYTHON)
        if backend == Backend.CPP:
            if comp is None:
                comp = lambda key1, key2: key1 < key2
            return _trees.SplayTree(key, root_data, comp, is_order_statistic, **kwargs) # If any argument is not given, then it is passed as None, except for comp
        return super().__new__(cls, key, root_data, comp, is_order_statistic, **kwargs)

    @classmethod
    def methods(cls):
        return ['__new__', 'insert', 'delete', 'join', 'split']

    def _zig(self, x, p):
        if self.tree[p].left == x:
            super(SplayTree, self)._right_rotate(p, x)
        else:
            super(SplayTree, self)._left_rotate(p, x)

    def _zig_zig(self, x, p):
        super(SplayTree, self)._right_rotate(self.tree[p].parent, p)
        super(SplayTree, self)._right_rotate(p, x)

    def _zig_zag(self, p):
        super(SplayTree, self)._left_right_rotate(self.tree[p].parent, p)

    def _zag_zag(self, x, p):
        super(SplayTree, self)._left_rotate(self.tree[p].parent, p)
        super(SplayTree, self)._left_rotate(p, x)

    def _zag_zig(self, p):
        super(SplayTree, self)._right_left_rotate(self.tree[p].parent, p)

    def splay(self, x, p):
        while self.tree[x].parent is not None:
            if self.tree[p].parent is None:
                self._zig(x, p)
            elif self.tree[p].left == x and \
                self.tree[self.tree[p].parent].left == p:
                self._zig_zig(x, p)
            elif self.tree[p].right == x and \
                self.tree[self.tree[p].parent].right == p:
                self._zag_zag(x, p)
            elif self.tree[p].left == x and \
                self.tree[self.tree[p].parent].right == p:
                self._zag_zig(p)
            else:
                self._zig_zag(p)
            p = self.tree[x].parent

    def insert(self, key, x):
        super(SelfBalancingBinaryTree, self).insert(key, x)
        e, p = super(SelfBalancingBinaryTree, self).search(key, parent=True)
        self.tree[self.size-1].parent = p
        self.splay(e, p)

    def delete(self, x):
        e, p = super(SelfBalancingBinaryTree, self).search(x, parent=True)
        if e is None:
            return
        self.splay(e, p)
        status = super(SelfBalancingBinaryTree, self).delete(x)
        return status

    def join(self, other):
        """
        Joins two trees current and other such that all elements of
        the current splay tree are smaller than the elements of the other tree.

        Parameters
        ==========

        other: SplayTree
            SplayTree which needs to be joined with the self tree.

        """
        maxm = self.root_idx
        while self.tree[maxm].right is not None:
            maxm = self.tree[maxm].right
        minm = other.root_idx
        while other.tree[minm].left is not None:
            minm = other.tree[minm].left
        if not self.comparator(self.tree[maxm].key,
                                other.tree[minm].key):
            raise ValueError("Elements of %s aren't less "
                             "than that of %s"%(self, other))
        self.splay(maxm, self.tree[maxm].parent)
        idx_update = self.tree._size
        for node in other.tree:
            if node is not None:
                node_copy = TreeNode(node.key, node.data)
                if node.left is not None:
                    node_copy.left = node.left + idx_update
                if node.right is not None:
                    node_copy.right = node.right + idx_update
                self.tree.append(node_copy)
            else:
                self.tree.append(node)
        self.tree[self.root_idx].right = \
            other.root_idx + idx_update

    def split(self, x):
        """
        Splits current splay tree into two trees such that one tree contains nodes
        with key less than or equal to x and the other tree containing
        nodes with key greater than x.

        Parameters
        ==========

        x: key
            Key of the element on the basis of which split is performed.

        Returns
        =======

        other: SplayTree
            SplayTree containing elements with key greater than x.

        """
        e, p = super(SelfBalancingBinaryTree, self).search(x, parent=True)
        if e is None:
            return
        self.splay(e, p)
        other = SplayTree(None, None)
        if self.tree[self.root_idx].right is not None:
            traverse = BinaryTreeTraversal(self)
            elements = traverse.depth_first_search(order='pre_order', node=self.tree[self.root_idx].right)
            for i in range(len(elements)):
                super(SelfBalancingBinaryTree, other).insert(elements[i].key, elements[i].data)
            for j in range(len(elements) - 1, -1, -1):
                e, p = super(SelfBalancingBinaryTree, self).search(elements[j].key, parent=True)
                self.tree[e] = None
            self.tree[self.root_idx].right = None
        return other

class RedBlackTree(SelfBalancingBinaryTree):
    """
    Represents Red Black trees.

    Examples
    ========

    >>> from pydatastructs.trees import RedBlackTree as RB
    >>> b = RB()
    >>> b.insert(1, 1)
    >>> b.insert(2, 2)
    >>> child = b.tree[b.root_idx].right
    >>> b.tree[child].data
    2
    >>> b.search(1)
    0

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Red%E2%80%93black_tree

    See Also
    ========

    pydatastructs.trees.binary_trees.SelfBalancingBinaryTree
    """

    def __new__(cls, key=None, root_data=None, comp=None,
                is_order_statistic=False, **kwargs):
        backend = kwargs.get('backend', Backend.PYTHON)
        if backend == Backend.CPP:
            if comp is None:
                comp = lambda key1, key2: key1 < key2
            return _trees.RedBlackTree(key, root_data, comp, is_order_statistic, **kwargs) # If any argument is not given, then it is passed as None, except for comp
        return super().__new__(cls, key, root_data, comp, is_order_statistic, **kwargs)

    @classmethod
    def methods(cls):
        return ['__new__', 'insert', 'delete']

    def _get_parent(self, node_idx):
        return self.tree[node_idx].parent

    def _get_grand_parent(self, node_idx):
        parent_idx=self._get_parent(node_idx)
        return self.tree[parent_idx].parent

    def _get_sibling(self, node_idx):
        parent_idx=self._get_parent(node_idx)
        if parent_idx is None:
            return None
        node = self.tree[parent_idx]
        if node_idx==node.left:
            sibling_idx=node.right
            return sibling_idx
        else:
            sibling_idx=node.left
            return sibling_idx

    def _get_uncle(self, node_idx):
        parent_idx=self._get_parent(node_idx)
        return self._get_sibling(parent_idx)

    def _is_onleft(self, node_idx):
        parent = self._get_parent(node_idx)
        if self.tree[parent].left == node_idx:
            return True
        return False

    def _is_onright(self, node_idx):
        if self._is_onleft(node_idx) is False:
            return True
        return False

    def __fix_insert(self, node_idx):
        while self._get_parent(node_idx) is not None and \
        self.tree[self._get_parent(node_idx)].color == 1 and self.tree[node_idx].color==1:
            parent_idx=self._get_parent(node_idx)
            grand_parent_idx=self._get_grand_parent(node_idx)
            uncle_idx = self._get_uncle(node_idx)
            if uncle_idx is not None and self.tree[uncle_idx].color == 1:
                self.tree[uncle_idx].color = 0
                self.tree[parent_idx].color = 0
                self.tree[grand_parent_idx].color = 1
                node_idx= grand_parent_idx
            else:
                self.tree[self.root_idx].is_root=False
                if self._is_onright(parent_idx):
                    if self._is_onleft(node_idx):
                        self._right_rotate(parent_idx, node_idx)
                        node_idx=parent_idx
                        parent_idx=self._get_parent(node_idx)
                    node_idx=parent_idx
                    parent_idx=self._get_parent(node_idx)
                    self._left_rotate(parent_idx, node_idx)
                elif self._is_onleft(parent_idx):
                    if self._is_onright(node_idx):
                        self._left_rotate(parent_idx, node_idx)
                        node_idx=parent_idx
                        parent_idx=self._get_parent(node_idx)
                    node_idx=parent_idx
                    parent_idx=self._get_parent(node_idx)
                    self._right_rotate(parent_idx, node_idx)
                self.tree[node_idx].color = 0
                self.tree[parent_idx].color = 1
                self.tree[self.root_idx].is_root=True
            if self.tree[node_idx].is_root:
                break
        self.tree[self.root_idx].color=0

    def insert(self, key, data=None):
        super(RedBlackTree, self).insert(key, data)
        node_idx = super(RedBlackTree, self).search(key)
        node = self.tree[node_idx]
        new_node = RedBlackTreeNode(key, data)
        new_node.parent = node.parent
        new_node.left = node.left
        new_node.right = node.right
        self.tree[node_idx] = new_node
        if node.is_root:
            self.tree[node_idx].is_root = True
            self.tree[node_idx].color=0
        elif self.tree[self.tree[node_idx].parent].color==1:
            self.__fix_insert(node_idx)

    def _find_predecessor(self, node_idx):
        while self.tree[node_idx].right is not None:
            node_idx = self.tree[node_idx].right
        return node_idx

    def _transplant_values(self, node_idx1, node_idx2):
        parent = self.tree[node_idx1].parent
        if self.tree[node_idx1].is_root and self._has_one_child(node_idx1):
            self.tree[self.root_idx].key = self.tree[node_idx2].key
            self.tree[self.root_idx].data = self.tree[node_idx2].data
            self.tree[self.root_idx].left = self.tree[node_idx2].left
            self.tree[self.root_idx].right = self.tree[node_idx2].right
            self.tree[node_idx1].parent = None
            return self.tree[self.root_idx].key
        else:
            self.tree[node_idx1].key = self.tree[node_idx2].key
            self.tree[node_idx1].data = self.tree[node_idx2].data

    def _has_one_child(self, node_idx):
        if self._is_leaf(node_idx) is False and self._has_two_child(node_idx) is False:
            return True
        return False

    def _is_leaf(self, node_idx):
        if self.tree[node_idx].left is None and self.tree[node_idx].right is None:
            return True
        return False

    def _has_two_child(self, node_idx):
        if self.tree[node_idx].left is not None and self.tree[node_idx].right is not None:
            return True
        return False

    def __has_red_child(self, node_idx):
        left_idx = self.tree[node_idx].left
        right_idx = self.tree[node_idx].right
        if (left_idx is not None and self.tree[left_idx].color == 1) or \
            (right_idx is not None and self.tree[right_idx].color == 1):
            return True
        return False

    def _replace_node(self, node_idx):
        if self._is_leaf(node_idx):
            return None
        elif self._has_one_child(node_idx):
            if self.tree[node_idx].left is not None:
                child = self.tree[node_idx].left
            else:
                child = self.tree[node_idx].right
            return child
        else:
            return self._find_predecessor(self.tree[node_idx].left)

    def __walk1_walk_isblack(self, color, node_idx1):
        if (node_idx1 is None or self.tree[node_idx1].color == 0) and (color == 0):
            return True
        return False

    def __left_left_siblingcase(self, node_idx):
        left_idx = self.tree[node_idx].left
        parent = self._get_parent(node_idx)
        parent_color = self.tree[parent].color
        self.tree[left_idx].color = self.tree[node_idx].color
        self.tree[node_idx].color = parent_color
        self._right_rotate(parent, node_idx)

    def __right_left_siblingcase(self, node_idx):
        left_idx = self.tree[node_idx].left
        parent = self._get_parent(node_idx)
        parent_color = self.tree[parent].color
        self.tree[left_idx].color = parent_color
        self._right_rotate(node_idx, left_idx)
        child = self._get_parent(node_idx)
        self._left_rotate(parent, child)

    def __left_right_siblingcase(self, node_idx):
        right_idx = self.tree[node_idx].right
        parent = self._get_parent(node_idx)
        parent_color = self.tree[parent].color
        self.tree[right_idx].color = parent_color
        self._left_rotate(node_idx, right_idx)
        child = self._get_parent(node_idx)
        self._right_rotate(parent, child)

    def __right_right_siblingcase(self, node_idx):
        right_idx = self.tree[node_idx].right
        parent = self._get_parent(node_idx)
        parent_color = self.tree[parent].color
        self.tree[right_idx].color = self.tree[node_idx].color
        self.tree[node_idx].color = parent_color
        self._left_rotate(parent, node_idx)

    def __fix_deletion(self, node_idx):
        node = self.tree[node_idx]
        color = node.color
        while node_idx!= self.root_idx and color == 0:
            sibling_idx = self._get_sibling(node_idx)
            parent_idx = self._get_parent(node_idx)
            if sibling_idx is None:
                node_idx = parent_idx
                continue
            else:
                if self.tree[sibling_idx].color == 1:
                    self.tree[self.root_idx].is_root = False
                    self.tree[parent_idx].color = 1
                    self.tree[sibling_idx].color = 0
                    if self._is_onleft(sibling_idx):
                        self._right_rotate(parent_idx, sibling_idx)
                    else:
                        self._left_rotate(parent_idx, sibling_idx)
                    self.tree[self.root_idx].is_root = True
                    continue
                else:
                    if self.__has_red_child(sibling_idx):
                        self.tree[self.root_idx].is_root = False
                        left_idx = self.tree[sibling_idx].left
                        if self.tree[sibling_idx].left is not None and \
                            self.tree[left_idx].color == 1:
                            if self._is_onleft(sibling_idx):
                                self.__left_left_siblingcase(sibling_idx)
                            else:
                                self.__right_left_siblingcase(sibling_idx)
                        else:
                            if self._is_onleft(sibling_idx):
                                self.__left_right_siblingcase(sibling_idx)
                            else:
                                self.__right_right_siblingcase(sibling_idx)
                        self.tree[self.root_idx].is_root = True
                        self.tree[parent_idx].color = 0
                    else:
                        self.tree[sibling_idx].color = 1
                        if self.tree[parent_idx].color == 0:
                            node_idx = parent_idx
                            continue
                        else:
                            self.tree[parent_idx].color = 0
            color = 1

    def _remove_node(self, node_idx):
        parent = self._get_parent(node_idx)
        a = parent
        if self._is_leaf(node_idx):
            par_key, root_key = (self.tree[parent].key, self.tree[self.root_idx].key)
            new_indices = self.tree.delete(node_idx)
            if new_indices is not None:
                a = new_indices[par_key]
                self.root_idx = new_indices[root_key]
        elif self._has_one_child(node_idx):
            child = self._replace_node(node_idx)
            parent = self._get_parent(node_idx)
            par_key, root_key = (self.tree[parent].key, self.tree[self.root_idx].key)
            new_indices = self.tree.delete(node_idx)
        self._update_size(a)

    def _delete_root(self, node_idx, node_idx1):
        if self._is_leaf(node_idx):
            self.tree[self.root_idx].data = None
            self.tree[self.root_idx].key = None
        elif self._has_one_child(node_idx):
            root_key = self._transplant_values(node_idx, node_idx1)
            new_indices = self.tree.delete(node_idx1)
            if new_indices is not None:
                self.root_idx = new_indices[root_key]

    def __leaf_case(self, node_idx, node_idx1):
        walk = node_idx
        walk1 = node_idx1
        parent = self._get_parent(node_idx)
        color = self.tree[walk].color
        if parent is None:
            self._delete_root(walk, walk1)
        else:
            if self.__walk1_walk_isblack(color, walk1):
                self.__fix_deletion(walk)
            else:
                sibling_idx = self._get_sibling(walk)
                if sibling_idx is not None:
                    self.tree[sibling_idx].color = 1
            if self._is_onleft(walk):
                self.tree[parent].left = None
            else:
                self.tree[parent].right = None
            self._remove_node(walk)

    def __one_child_case(self, node_idx, node_idx1):
        walk = node_idx
        walk1 = node_idx1
        walk_original_color = self.tree[walk].color
        parent = self._get_parent(node_idx)
        if parent is None:
            self._delete_root(walk, walk1)
        else:
            if self._is_onleft(walk):
                self.tree[parent].left = walk1
            else:
                self.tree[parent].right = walk1
            self.tree[walk1].parent = parent
            a = self._remove_node(walk)
            if self.__walk1_walk_isblack(walk_original_color, walk1):
                self.__fix_deletion(walk1)
            else:
                self.tree[walk1].color = 0

    def __two_child_case(self, node_idx):
        walk = node_idx
        successor = self._replace_node(walk)
        self._transplant_values(walk, successor)
        walk = successor
        walk1 = self._replace_node(walk)
        return walk, walk1

    def delete(self, key, **kwargs):
        walk = super(RedBlackTree, self).search(key)
        if walk is not None:
            walk1 = self._replace_node(walk)
            if self._has_two_child(walk):
                walk, walk1 = self.__two_child_case(walk)
            if self._is_leaf(walk):
                self.__leaf_case(walk, walk1)
            elif self._has_one_child(walk):
                self.__one_child_case(walk, walk1)
            return True
        else:
            return None

class BinaryTreeTraversal(object):
    """
    Represents the traversals possible in
    a binary tree.

    Parameters
    ==========

    tree: BinaryTree
        The binary tree for whose traversal
        is to be done.
    backend: pydatastructs.Backend
        The backend to be used. Available backends: Python and C++
        Optional, by default, the Python backend is used. For faster execution, use the C++ backend.

    Traversals
    ==========

    - Depth First Search
        In Order, Post Order, Pre Order Out Order

    - Breadth First Search

    Examples
    ========

    >>> from pydatastructs import BinarySearchTree as BST
    >>> from pydatastructs import BinaryTreeTraversal as BTT
    >>> b = BST(2, 2)
    >>> b.insert(1, 1)
    >>> b.insert(3, 3)
    >>> trav = BTT(b)
    >>> dfs = trav.depth_first_search()
    >>> [str(n) for n in dfs]
    ['(None, 1, 1, None)', '(1, 2, 2, 2)', '(None, 3, 3, None)']
    >>> bfs = trav.breadth_first_search()
    >>> [str(n) for n in bfs]
    ['(1, 2, 2, 2)', '(None, 1, 1, None)', '(None, 3, 3, None)']

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Tree_traversal
    """

    @classmethod
    def methods(cls):
        return ['__new__', 'depth_first_search',
                'breadth_first_search']

    __slots__ = ['tree']

    def __new__(cls, tree, **kwargs):
        backend = kwargs.get('backend', Backend.PYTHON)
        if backend == Backend.CPP:
            return _trees.BinaryTreeTraversal(tree, **kwargs)
        if not isinstance(tree, BinaryTree):
            raise TypeError("%s is not a binary tree"%(tree))
        obj = object.__new__(cls)
        obj.tree = tree
        return obj

    def _pre_order(self, node):
        """
        Utility method for computing pre-order
        of a binary tree using iterative algorithm.
        """
        visit = []
        tree, size = self.tree.tree, self.tree.size
        s = Stack()
        s.push(node)
        while not s.is_empty:
            node = s.pop()
            visit.append(tree[node])
            if tree[node].right is not None:
                s.push(tree[node].right)
            if tree[node].left is not None:
                s.push(tree[node].left)
        return visit

    def _in_order(self, node):
        """
        Utility method for computing in-order
        of a binary tree using iterative algorithm.
        """
        visit = []
        tree, size = self.tree.tree, self.tree.size
        s = Stack()
        while not s.is_empty or node is not None:
            if node is not None:
                s.push(node)
                node = tree[node].left
            else:
                node = s.pop()
                visit.append(tree[node])
                node = tree[node].right
        return visit

    def _post_order(self, node):
        """
        Utility method for computing post-order
        of a binary tree using iterative algorithm.
        """
        visit = []
        tree, size = self.tree.tree, self.tree.size
        s = Stack()
        s.push(node)
        last = OneDimensionalArray(int, size)
        last.fill(False)
        while not s.is_empty:
            node = s.peek
            l, r = tree[node].left, tree[node].right
            cl, cr = l is None or last[l], r is None or last[r]
            if cl and cr:
                s.pop()
                visit.append(tree[node])
                last[node] = True
                continue
            if not cr:
                s.push(r)
            if not cl:
                s.push(l)
        return visit

    def _out_order(self, node):
        """
        Utility method for computing out-order
        of a binary tree using iterative algorithm.
        """
        return reversed(self._in_order(node))

    def depth_first_search(self, order='in_order', node=None):
        """
        Computes the depth first search traversal of the binary
        trees.

        Parameters
        ==========

        order : str
            One of the strings, 'in_order', 'post_order',
            'pre_order', 'out_order'.
            By default, it is set to, 'in_order'.
        node : int
            The index of the node from where the traversal
            is to be instantiated.

        Returns
        =======

        list
            Each element is of type 'TreeNode'.
        """
        if node is None:
            node = self.tree.root_idx
        if order not in ('in_order', 'post_order', 'pre_order', 'out_order'):
            raise NotImplementedError(
                "%s order is not implemented yet."
                "We only support `in_order`, `post_order`, "
                "`pre_order` and `out_order` traversals.")
        return getattr(self, '_' + order)(node)

    def breadth_first_search(self, node=None, strategy='queue'):
        """
        Computes the breadth first search traversal of a binary tree.

        Parameters
        ==========

        node : int
            The index of the node from where the traversal has to be instantiated.
            By default, set to, root index.

        strategy : str
            The strategy using which the computation has to happen.
            By default, it is set 'queue'.

        Returns
        =======

        list
            Each element of the list is of type `TreeNode`.
        """
        # TODO: IMPLEMENT ITERATIVE DEEPENING-DEPTH FIRST SEARCH STRATEGY
        strategies = ('queue',)
        if strategy not in strategies:
            raise NotImplementedError(
                "%s startegy is not implemented yet"%(strategy))
        if node is None:
            node = self.tree.root_idx
        q, visit, tree = Queue(), [], self.tree.tree
        q.append(node)
        while len(q) > 0:
            node = q.popleft()
            visit.append(tree[node])
            if tree[node].left is not None:
                q.append(tree[node].left)
            if tree[node].right is not None:
                q.append(tree[node].right)
        return visit

class BinaryIndexedTree(object):
    """
    Represents binary indexed trees
    a.k.a fenwick trees.

    Parameters
    ==========

    array: list/tuple
        The array whose elements are to be
        considered for the queries.
    backend: pydatastructs.Backend
        The backend to be used. Available backends: Python and C++
        Optional, by default, the Python backend is used. For faster execution, use the C++ backend.

    Examples
    ========

    >>> from pydatastructs import BinaryIndexedTree
    >>> bit = BinaryIndexedTree([1, 2, 3])
    >>> bit.get_sum(0, 2)
    6
    >>> bit.update(0, 100)
    >>> bit.get_sum(0, 2)
    105

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Fenwick_tree
    """

    __slots__ = ['tree', 'array', 'flag']

    def __new__(cls, array, **kwargs):
        backend = kwargs.get('backend', Backend.PYTHON)
        if backend == Backend.CPP:
            return _trees.BinaryIndexedTree(type(array[0]), array, **kwargs)
        obj = object.__new__(cls)
        obj.array = OneDimensionalArray(type(array[0]), array)
        obj.tree = [0] * (obj.array._size + 2)
        obj.flag = [0] * (obj.array._size)
        for index in range(obj.array._size):
            obj.update(index, array[index])
        return obj

    @classmethod
    def methods(cls):
        return ['update', 'get_prefix_sum',
        'get_sum']

    def update(self, index, value):
        """
        Updates value at the given index.

        Parameters
        ==========

        index: int
            Index of element to be updated.

        value
            The value to be inserted.
        """
        _index, _value = index, value
        if self.flag[index] == 0:
            self.flag[index] = 1
            index += 1
            while index < self.array._size + 1:
                self.tree[index] += value
                index = index + (index & (-index))
        else:
            value = value - self.array[index]
            index += 1
            while index < self.array._size + 1:
                self.tree[index] += value
                index = index + (index & (-index))
        self.array[_index] = _value

    def get_prefix_sum(self, index):
        """
        Computes sum of elements from index 0 to given index.

        Parameters
        ==========

        index: int
            Index till which sum has to be calculated.

        Returns
        =======

        sum: int
            The required sum.
        """
        index += 1
        sum = 0
        while index > 0:
            sum += self.tree[index]
            index = index - (index & (-index))
        return sum

    def get_sum(self, left_index, right_index):
        """
        Get sum of elements from left index to right index.

        Parameters
        ==========

        left_index: int
            Starting index from where sum has to be computed.

        right_index: int
            Ending index till where sum has to be computed.

        Returns
        =======

        sum: int
            The required sum
        """
        if left_index >= 1:
            return self.get_prefix_sum(right_index) - \
                   self.get_prefix_sum(left_index - 1)
        else:
            return self.get_prefix_sum(right_index)
