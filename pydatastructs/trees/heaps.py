from pydatastructs.utils.misc_util import _check_type, NoneType, TreeNode, BinomialTreeNode
from pydatastructs.linear_data_structures.arrays import (ArrayForTrees,
     DynamicOneDimensionalArray)
from pydatastructs.miscellaneous_data_structures.binomial_trees import BinomialTree

__all__ = [
    'BinaryHeap',
    'BinomialHeap'
]

class Heap(object):
    """
    Abstract class for representing heaps.
    """
    pass

class BinaryHeap(Heap):
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
    __slots__ = ['_comp', 'heap', 'heap_property', '_last_pos_filled']

    def __new__(cls, elements=None, heap_property="min"):
        obj = Heap.__new__(cls)
        obj.heap_property = heap_property
        if heap_property == "min":
            obj._comp = lambda key_parent, key_child: key_parent <= key_child
        elif heap_property == "max":
            obj._comp = lambda key_parent, key_child: key_parent >= key_child
        else:
            raise ValueError("%s is invalid heap property"%(heap_property))
        if elements is None:
            elements = []
        obj.heap = elements
        obj._last_pos_filled = len(elements) - 1
        obj._build()
        return obj

    def _build(self):
        for i in range(self._last_pos_filled + 1):
            self.heap[i].left, self.heap[i].right = \
                2*i + 1, 2*i + 2
        for i in range((self._last_pos_filled + 1)//2, -1, -1):
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
            l = 2*i + 1
            r = 2*i + 2

            if l <= self._last_pos_filled:
                target = l if self._comp(self.heap[l].key, self.heap[target].key) \
                        else i
            if r <= self._last_pos_filled:
                target = r if self._comp(self.heap[r].key, self.heap[target].key) \
                        else target

            if target != i:
                self._swap(target, i)
                i = target
            else:
                break


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
        if self._last_pos_filled == -1:
            return None
        else:
            element_to_be_extracted = TreeNode(self.heap[0].key, self.heap[0].data)
            self._swap(0, self._last_pos_filled)
            self.heap[self._last_pos_filled] = TreeNode(float('inf') if self.heap_property == 'min'
                                                                else float('-inf'), None)
            self._heapify(0)
            self.heap.pop()
            self._last_pos_filled -= 1
            return element_to_be_extracted

    def __str__(self):
        to_be_printed = ['' for i in range(self._last_pos_filled + 1)]
        for i in range(self._last_pos_filled + 1):
            node = self.heap[i]
            to_be_printed[i] = (node.left if node.left <= self._last_pos_filled else None,
                                node.key, node.data,
                                node.right if node.right <= self._last_pos_filled else None)
        return str(to_be_printed)


class BinomialHeap(Heap):
    """
    Represents binomial heap.

    Parameters
    ==========

    root_list: list/tuple
        By default, []
        The list of BinomialTree object references
        in sorted order.

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

    def __new__(cls, root_list=[]):
        if not all((_check_type(root, BinomialTree))
                for root in root_list):
                    raise TypeError("The root_list should contain "
                                    "references to objects of BinomialTree.")
        obj = Heap.__new__(cls)
        obj.root_list = DynamicOneDimensionalArray(BinomialTree, root_list)
        return obj

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
        pos = new_root_list._last_pos_filled
        if (new_root_list.size != 0) and new_root_list[pos].order == new_tree.order:
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
        new_root_list = DynamicOneDimensionalArray(BinomialTree, 0)
        i, j = 0, 0
        while ((i <= self.root_list._last_pos_filled) and
               (j <= other_heap.root_list._last_pos_filled)):
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

        while i <= self.root_list._last_pos_filled:
            new_tree = self.root_list[i]
            self._merge_heap_last_new_tree(new_root_list, new_tree)
            i += 1
        while j <= other_heap.root_list._last_pos_filled:
            new_tree = other_heap.root_list[j]
            self._merge_heap_last_new_tree(new_root_list, new_tree)
            j += 1
        self.root_list = new_root_list

    def insert(self, key, data):
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
            raise ValueError("Binomial heap is empty.")
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
        self.root_list.delete(min_idx)
        child_heap = BinomialHeap(root_list=child_root_list)
        self.merge(child_heap)

    @property
    def is_empty(self):
        return self.root_list._last_pos_filled == -1

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
          
     class FibonacciHeap:
          def iterate(self, head):
        node = stop = head
        flag = False
        while True:
            if node == stop and flag is True:
                break
            elif node == stop:
                flag = True
            yield node
            node = node.right

    # pointer to the head and minimum node in the root list
    root_list, min_node = None, None

    # maintain total node count in full fibonacci heap
    total_nodes = 0

    # return min node in O(1) time
    def find_min(self):
        return self.min_node

    # extract (delete) the min node from the heap in O(log n) time
    # amortized cost analysis can be found here (http://bit.ly/1ow1Clm)
    def extract_min(self):
        z = self.min_node
        if z is not None:
            if z.child is not None:
                # attach child nodes to root list
                children = [x for x in self.iterate(z.child)]
                for i in range(0, len(children)):
                    self.merge_with_root_list(children[i])
                    children[i].parent = None
            self.remove_from_root_list(z)
            # set new min node in heap
            if z == z.right:
                self.min_node = self.root_list = None
            else:
                self.min_node = z.right
                self.consolidate()
            self.total_nodes -= 1
        return z

    # insert new node into the unordered root list in O(1) time
    # returns the node so that it can be used for decrease_key later
    def insert(self, key, value=None):
        n = self.Node(key, value)
        n.left = n.right = n
        self.merge_with_root_list(n)
        if self.min_node is None or n.key < self.min_node.key:
            self.min_node = n
        self.total_nodes += 1
        return n

    # modify the key of some node in the heap in O(1) time
    def decrease_key(self, x, k):
        if k > x.key:
            return None
        x.key = k
        y = x.parent
        if y is not None and x.key < y.key:
            self.cut(x, y)
            self.cascading_cut(y)
        if x.key < self.min_node.key:
            self.min_node = x

    # merge two fibonacci heaps in O(1) time by concatenating the root lists
    # the root of the new root list becomes equal to the first list and the second
    # list is simply appended to the end (then the proper min node is determined)
    def merge(self, h2):
        H = FibonacciHeap()
        H.root_list, H.min_node = self.root_list, self.min_node
        # fix pointers when merging the two heaps
        last = h2.root_list.left
        h2.root_list.left = H.root_list.left
        H.root_list.left.right = h2.root_list
        H.root_list.left = last
        H.root_list.left.right = H.root_list
        # update min node if needed
        if h2.min_node.key < H.min_node.key:
            H.min_node = h2.min_node
        # update total nodes
        H.total_nodes = self.total_nodes + h2.total_nodes
        return H

    # if a child node becomes smaller than its parent node we
    # cut this child node off and bring it up to the root list
    def cut(self, x, y):
        self.remove_from_child_list(y, x)
        y.degree -= 1
        self.merge_with_root_list(x)
        x.parent = None
        x.mark = False

    # cascading cut of parent node to obtain good time bounds
    def cascading_cut(self, y):
        z = y.parent
        if z is not None:
            if y.mark is False:
                y.mark = True
            else:
                self.cut(y, z)
                self.cascading_cut(z)

    # combine root nodes of equal degree to consolidate the heap
    # by creating a list of unordered binomial trees
    def consolidate(self):
        A = [None] * int(math.log(self.total_nodes) * 2)
        nodes = [w for w in self.iterate(self.root_list)]
        for w in range(0, len(nodes)):
            x = nodes[w]
            d = x.degree
            while A[d] != None:
                y = A[d]
                if x.key > y.key:
                    temp = x
                    x, y = y, temp
                self.heap_link(y, x)
                A[d] = None
                d += 1
            A[d] = x
        # find new min node - no need to reconstruct new root list below
        # because root list was iteratively changing as we were moving
        # nodes around in the above loop
        for i in range(0, len(A)):
            if A[i] is not None:
                if A[i].key < self.min_node.key:
                    self.min_node = A[i]

    # actual linking of one node to another in the root list
    # while also updating the child linked list
    def heap_link(self, y, x):
        self.remove_from_root_list(y)
        y.left = y.right = y
        self.merge_with_child_list(x, y)
        x.degree += 1
        y.parent = x
        y.mark = False

    # merge a node with the doubly linked root list
    def merge_with_root_list(self, node):
        if self.root_list is None:
            self.root_list = node
        else:
            node.right = self.root_list.right
            node.left = self.root_list
            self.root_list.right.left = node
            self.root_list.right = node

    # merge a node with the doubly linked child list of a root node
    def merge_with_child_list(self, parent, node):
        if parent.child is None:
            parent.child = node
        else:
            node.right = parent.child.right
            node.left = parent.child
            parent.child.right.left = node
            parent.child.right = node

    # remove a node from the doubly linked root list
    def remove_from_root_list(self, node):
        if node == self.root_list:
            self.root_list = node.right
        node.left.right = node.right
        node.right.left = node.left

    # remove a node from the doubly linked child list
    def remove_from_child_list(self, parent, node):
        if parent.child == parent.child.right:
            parent.child = None
        elif parent.child == node:
            parent.child = node.right
            node.right.parent = parent
        node.left.right = node.right
        node.right.left = node.left
