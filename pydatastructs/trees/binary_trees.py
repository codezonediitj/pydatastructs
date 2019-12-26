from pydatastructs.utils import TreeNode
from pydatastructs.miscellaneous_data_structures import Stack
from pydatastructs.linear_data_structures import (
    OneDimensionalArray, DynamicOneDimensionalArray)
from pydatastructs.linear_data_structures.arrays import ArrayForTrees
# TODO: REPLACE COLLECTIONS QUEUE WITH PYDATASTRUCTS QUEUE
from collections import deque as Queue

__all__ = [
    'AVLTree',
    'BinaryTree',
    'BinarySearchTree',
    'BinaryTreeTraversal'
]

class BinaryTree(object):
    """
    Abstract binary tree.

    Parameters
    ==========

    root_data
        Optional, the root node of the binary tree.
        If not of type TreeNode, it will consider
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
    is_order_statistic: bool
        Set it to True, if you want to use the
        order statistic features of the tree.

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Binary_tree
    """

    __slots__ = ['root_idx', 'comparator', 'tree', 'size',
                 'is_order_statistic']

    def __new__(cls, key=None, root_data=None, comp=None,
                is_order_statistic=False):
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
    left_size = lambda self, node: self.tree[node.left].size \
                                        if node.left is not None else 0
    right_size = lambda self, node: self.tree[node.right].size \
                                        if node.right is not None else 0

    def _update_size(self, start_idx):
        if self.is_order_statistic:
            walk = start_idx
            while walk is not None:
                self.tree[walk].size = (
                    self.left_size(self.tree[walk]) +
                    self.right_size(self.tree[walk]) + 1)
                walk = self.tree[walk].parent

    def insert(self, key, data):
        res = self.search(key)
        if res is not None:
            self.tree[res].data = data
            return None
        walk = self.root_idx
        if self.tree[walk].key is None:
            self.tree[walk].key = key
            self.tree[walk].data = data
            return None
        new_node, prev_node, flag = TreeNode(key, data), 0, True
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

        Parameter
        =========

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

class AVLTree(BinarySearchTree):
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
    left_height = lambda self, node: self.tree[node.left].height \
                                        if node.left is not None else -1
    right_height = lambda self, node: self.tree[node.right].height \
                                        if node.right is not None else -1
    balance_factor = lambda self, node: self.right_height(node) - \
                                        self.left_height(node)

    def _right_rotate(self, j, k):
        y = self.tree[k].right
        if y is not None:
            self.tree[y].parent = j
        self.tree[j].left = y
        self.tree[k].parent = self.tree[j].parent
        if self.tree[k].parent is not None:
            self.tree[self.tree[k].parent].left = k
        self.tree[j].parent = k
        self.tree[k].right = j
        self.tree[j].height = max(self.left_height(self.tree[j]),
                                  self.right_height(self.tree[j])) + 1
        kp = self.tree[k].parent
        if kp is None:
            self.root_idx = k
        if self.is_order_statistic:
            self.tree[j].size = (self.left_size(self.tree[j]) +
                                 self.right_size(self.tree[j]) + 1)

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
        self.tree[j].height = max(self.left_height(self.tree[j]),
                                  self.right_height(self.tree[j])) + 1
        self.tree[k].height = max(self.left_height(self.tree[k]),
                                    self.right_height(self.tree[k])) + 1
        ip = self.tree[i].parent
        if ip is not None:
            if self.tree[ip].left == j:
                self.tree[ip].left = i
            else:
                self.tree[ip].right = i
        else:
            self.root_idx = i
        if self.is_order_statistic:
            self.tree[j].size = (self.left_size(self.tree[j]) +
                                 self.right_size(self.tree[j]) + 1)
            self.tree[k].size = (self.left_size(self.tree[k]) +
                                 self.right_size(self.tree[k]) + 1)

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
        self.tree[j].height = max(self.left_height(self.tree[j]),
                                  self.right_height(self.tree[j])) + 1
        self.tree[k].height = max(self.left_height(self.tree[k]),
                                    self.right_height(self.tree[k])) + 1
        ip = self.tree[i].parent
        if ip is not None:
            if self.tree[ip].left == j:
                self.tree[ip].left = i
            else:
                self.tree[ip].right = i
        else:
            self.root_idx = i
        if self.is_order_statistic:
            self.tree[j].size = (self.left_size(self.tree[j]) +
                                 self.right_size(self.tree[j]) + 1)
            self.tree[k].size = (self.left_size(self.tree[k]) +
                                 self.right_size(self.tree[k]) + 1)

    def _left_rotate(self, j, k):
        y = self.tree[k].left
        if y is not None:
            self.tree[y].parent = j
        self.tree[j].right = y
        self.tree[k].parent = self.tree[j].parent
        if self.tree[k].parent is not None:
            self.tree[self.tree[k].parent].right = k
        self.tree[j].parent = k
        self.tree[k].left = j
        self.tree[j].height = max(self.left_height(self.tree[j]),
                                  self.right_height(self.tree[j])) + 1
        self.tree[k].height = max(self.left_height(self.tree[k]),
                                    self.right_height(self.tree[k])) + 1
        kp = self.tree[k].parent
        if kp is None:
            self.root_idx = k
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

    def insert(self, key, data):
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

class BinaryTreeTraversal(object):
    """
    Represents the traversals possible in
    a binary tree.

    Parameters
    ==========

    tree: BinaryTree
        The binary tree for whose traversal
        is to be done.

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

    __slots__ = ['tree']

    def __new__(cls, tree):
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
        s = Stack(maxsize=size)
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
        s = Stack(maxsize=size)
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
        s = Stack(maxsize=size)
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
        # TODO: IMPLEMENT ITERATIVE DEEPENING-DEPTH FIRST SEARCH STRATEGY
        """
        Computes the breadth first search traversal of a binary tree.

        Parameters
        ==========

        strategy : str
            The strategy using which the computation has to happen.
            By default, it is set 'queue'.
        node : int
            The index of the node from where the traversal has to be instantiated.
            By default, set to, root index.

        Returns
        =======

        list
            Each element of the list is of type `TreeNode`.
        """
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
