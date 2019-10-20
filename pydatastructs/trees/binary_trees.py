from __future__ import print_function, division
from pydatastructs.utils import Node
from pydatastructs.miscellaneous_data_structures import Stack
from pydatastructs.linear_data_structures import OneDimensionalArray
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

    See Also
    ========

    pydatastructs.trees.binary_tree.BinaryTree
    """
    def insert(self, key, data):
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

    def delete(self, key, **kwargs):
        (walk, parent) = self.search(key, parent=True)
        a = None
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
                a = parent

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
            if self.tree[twalk].right != None:
                self.tree[self.tree[twalk].right].parent = twalk
            a = par

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
                self.tree[child].parent = parent
                a = parent

        if kwargs.get("balancing_info", False) is not False:
            return a
        return True

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
                                        if node.left != None else -1
    right_height = lambda self, node: self.tree[node.right].height \
                                        if node.right != None else -1
    balance_factor = lambda self, node: self.right_height(node) - \
                                        self.left_height(node)

    def _right_rotate(self, j, k):
        y = self.tree[k].right
        if y != None:
            self.tree[y].parent = j
        self.tree[j].left = y
        self.tree[k].parent = self.tree[j].parent
        if self.tree[k].parent != None:
            self.tree[self.tree[k].parent].left = k
        self.tree[j].parent = k
        self.tree[k].right = j
        self.tree[j].height = max(self.left_height(self.tree[j]),
                                  self.right_height(self.tree[j])) + 1
        self.tree[k].height = max(self.left_height(self.tree[k]),
                                    self.right_height(self.tree[k])) + 1
        kp = self.tree[k].parent
        if kp != None:
            self.tree[kp].height = max(self.left_height(self.tree[kp]),
                                        self.right_height(self.tree[kp])) + 1
        else:
            self.root_idx = k

    def _left_right_rotate(self, j, k):
        i = self.tree[k].right
        v, w = self.tree[i].left, self.tree[i].right
        self.tree[k].right, self.tree[j].left = v, w
        if v != None:
            self.tree[v].parent = k
        if w != None:
            self.tree[w].parent = j
        self.tree[i].left, self.tree[i].right, self.tree[i].parent = \
            k, j, self.tree[j].parent
        self.tree[k].parent, self.tree[j].parent = i, i
        self.tree[j].height = max(self.left_height(self.tree[j]),
                                  self.right_height(self.tree[j])) + 1
        self.tree[k].height = max(self.left_height(self.tree[k]),
                                    self.right_height(self.tree[k])) + 1
        ip = self.tree[i].parent
        if ip != None:
            if self.tree[ip].left == j:
                self.tree[ip].left = i
            else:
                self.tree[ip].right = i
            self.tree[ip].height = max(self.left_height(self.tree[ip]),
                                        self.right_height(self.tree[ip])) + 1
        else:
            self.root_idx = i

    def _right_left_rotate(self, j, k):
        i = self.tree[k].left
        v, w = self.tree[i].left, self.tree[i].right
        self.tree[k].left, self.tree[j].right = w, v
        if v != None:
            self.tree[v].parent = j
        if w != None:
            self.tree[w].parent = k
        self.tree[i].right, self.tree[i].left, self.tree[i].parent = \
            k, j, self.tree[j].parent
        self.tree[k].parent, self.tree[j].parent = i, i
        self.tree[j].height = max(self.left_height(self.tree[j]),
                                  self.right_height(self.tree[j])) + 1
        self.tree[k].height = max(self.left_height(self.tree[k]),
                                    self.right_height(self.tree[k])) + 1
        ip = self.tree[i].parent
        if ip != None:
            if self.tree[ip].left == j:
                self.tree[ip].left = i
            else:
                self.tree[ip].right = i
            self.tree[ip].height = max(self.left_height(self.tree[ip]),
                                        self.right_height(self.tree[ip])) + 1
        else:
            self.root_idx = i

    def _left_rotate(self, j, k):
        y = self.tree[k].left
        if y != None:
            self.tree[y].parent = j
        self.tree[j].right = y
        self.tree[k].parent = self.tree[j].parent
        if self.tree[k].parent != None:
            self.tree[self.tree[k].parent].right = k
        self.tree[j].parent = k
        self.tree[k].left = j
        self.tree[j].height = max(self.left_height(self.tree[j]),
                                  self.right_height(self.tree[j])) + 1
        self.tree[k].height = max(self.left_height(self.tree[k]),
                                    self.right_height(self.tree[k])) + 1
        kp = self.tree[k].parent
        if kp != None:
            self.tree[kp].height = max(self.left_height(self.tree[kp]),
                                        self.right_height(self.tree[kp])) + 1
        else:
            self.root_idx = k

    def _balance_insertion(self, curr, last):
        walk = last
        path = Queue()
        path.append(curr), path.append(last)
        while walk != None:
            self.tree[walk].height = max(self.left_height(self.tree[walk]),
                                        self.right_height(self.tree[walk])) + 1
            last = path.popleft()
            last2last = path.popleft()
            if self.balance_factor(self.tree[walk]) not in (1, 0, -1):
                l = self.tree[walk].left
                if l != None and l == last and self.tree[l].left == last2last:
                    self._right_rotate(walk, last)
                r = self.tree[walk].right
                if r != None and r == last and self.tree[r].right == last2last:
                    self._left_rotate(walk, last)
                if l != None and l == last and self.tree[l].right == last2last:
                    self._left_right_rotate(walk, last)
                if r != None and r == last and self.tree[r].left == last2last:
                    self._right_left_rotate(walk, last)
            path.append(walk), path.append(last)
            walk = self.tree[walk].parent

    def insert(self, key, data):
        walk = self.root_idx
        if self.tree[walk].key == None:
            self.tree[walk].key = key
            self.tree[walk].data = data
            return None
        new_node, prev_node, flag = Node(key, data), 0, True
        while flag:
            if self.tree[walk].key == key:
                self.tree[walk].data = data
                flag = False
            else:
                if not self.comparator(key, self.tree[walk].key):
                    if self.tree[walk].right == None:
                        new_node.parent = prev_node
                        self.tree.append(new_node)
                        self.tree[walk].right = self.size
                        self.size += 1
                        flag = False
                    prev_node = walk = self.tree[walk].right
                else:
                    if self.tree[walk].left == None:
                        new_node.parent = prev_node
                        self.tree.append(new_node)
                        self.tree[walk].left = self.size
                        self.size += 1
                        flag = False
                    prev_node = walk = self.tree[walk].left

        self._balance_insertion(self.size - 1, self.tree[self.size-1].parent)

    def _balance_deletion(self, start_idx, key):
        walk = start_idx
        while walk != None:
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
            if tree[node].right != None:
                s.push(tree[node].right)
            if tree[node].left != None:
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
        while not s.is_empty or node != None:
            if node != None:
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
            cl, cr = l == None or last[l], r == None or last[r]
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
            Each element is of type 'Node'.
        """
        if node == None:
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
            Each element of the list is of type `Node`.
        """
        strategies = ('queue',)
        if strategy not in strategies:
            raise NotImplementedError(
                "%s startegy is not implemented yet"%(strategy))
        if node == None:
            node = self.tree.root_idx
        q, visit, tree = Queue(), [], self.tree.tree
        q.append(node)
        while len(q) > 0:
            node = q.popleft()
            visit.append(tree[node])
            if tree[node].left != None:
                q.append(tree[node].left)
            if tree[node].right != None:
                q.append(tree[node].right)
        return visit
