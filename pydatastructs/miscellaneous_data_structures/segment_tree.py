class SegmentTree:
    """
    Represents the Segment Tree

    Parameters
    ==========

    inp_list: Initial list of values to build the tree.

    Examples
    ========

    >>> from segment_tree import SegmentTree
    
    >>> t = SegmentTree([3, 4, 8, 10, 1])
    >>> t.tree
    [0, 26, 25, 1, 7, 18, 1, 0, 3, 4, 8, 10, 1, 0, 0, 0]
    >>> t.lazy
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    >>> n = t.get_list_len()
    
    >>> t.query(1, 0, n - 1, 2, 4)
    19
    >>> t.point_update(3, 29)
    >>> t.tree
    [0, 45, 44, 1, 7, 37, 1, 0, 3, 4, 8, 29, 1, 0, 0, 0]
    >>> t.range_update(1, 0, n - 1, 0, 3, -4)
    >>> t.tree
    [0, 29, 28, 1, 7, 37, 1, 0, 3, 4, 8, 29, 1, 0, 0, 0]
    >>> t.lazy
    [0, 0, 0, 0, -4, -4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    >>> t.query(1, 0, n - 1, 1, 3)
    29

    Note
    ====

    The tree can be modified accordingly to get the [sum, max, min, gcd, etc.]
    or any other compatible function or query type.

    References
    ==========

    https://cp-algorithms.com/data_structures/segment_tree.html

    """

    def __init__(self, inp_list):

        def get_len(size):
            """
            Returns the new list size (the closest power of 2).

            Parameters
            ==========

            size: Size of the initial list.

            """

            if size and size & (size - 1) == 0:

                return size
            else:

                bit_len = len(bin(size)) - 2
                return 1 << bit_len

        self.tree_size = 2 * get_len(len(inp_list))

        self.tree = [0 for _ in range(self.tree_size)]
        self.lazy = [0 for _ in range(self.tree_size)]

        def build(init_list):
            """
            Builds the tree using the initial list.

            Parameters
            ==========

            init_list: Initial list passed in the object declaration.

            """

            list_size = len(init_list)

            for i in range(list_size):

                self.tree[self.tree_size // 2 + i] = init_list[i]

            for i in range(list_size, self.tree_size // 2):

                self.tree[self.tree_size // 2 + i] = 0

            for i in range(self.tree_size // 2 - 1, 0, -1):

                self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

            self.root = self.tree[1]

        build(inp_list)

    def query(self, node, tree_left, tree_right, left, right):
        """
        Returns the query value for the range [L, R].

        Parameters
        ==========

        node: Root Node (Initial call : 1).
        tree_left: Left index of the node (Initial call : 0).
        tree_right: Right index of the node (Initial call : [object].get_list_len() - 1).
        left: Query index left.
        right: Query index right.

        """

        if self.lazy[node]:

            self.tree[node] += self.lazy[node] * (tree_right - tree_left + 1)

            if tree_left != tree_right:

                self.lazy[2 * node] += self.lazy[node]
                self.lazy[2 * node + 1] += self.lazy[node]

            self.lazy[node] = 0

        if tree_left >= left and tree_right <= right:

            return self.tree[node]

        elif tree_left > right or tree_right < left:

            return 0

        else:

            mid = (tree_left + tree_right) // 2

            return \
                self.query(2 * node, tree_left, mid, left, right) + \
                self.query(2 * node + 1, mid + 1, tree_right, left, right)

    def range_update(self, node, tree_left, tree_right, left, right, new_val):
        """
        Adds the new value to the range [L, R].

        Parameters
        ==========

        node: Node (Initial call : 1 {Root Node}).
        tree_left: Left index of the node (Initial call : 0).
        tree_right: Right index of the node (Initial call : [object].get_list_len() - 1).
        left: Query index left.
        right: Query Range right.
        new_val: New Value to be added.

        """

        if self.lazy[node]:

            self.tree[node] += self.lazy[node] * (tree_right - tree_left + 1)

            if tree_left != tree_right:

                self.lazy[2 * node] += self.lazy[node]
                self.lazy[2 * node + 1] += self.lazy[node]

            self.lazy[node] = 0

        if tree_left >= left and tree_right <= right:

            self.tree[node] += new_val * (tree_right - tree_left + 1)

            if tree_left != tree_right:

                self.lazy[2 * node] += new_val
                self.lazy[2 * node + 1] += new_val

        elif tree_left > right or tree_right < left:

            return
        else:

            mid = (tree_left + tree_right) // 2

            self.range_update(2 * node, tree_left, mid, left, right, new_val)
            self.range_update(2 * node + 1, mid + 1, tree_right, left, right, new_val)

            self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def point_update(self, pos, new_val):
        """
        Updates the specified position in the tree with the new value.

        Parameters
        ==========

        pos: Position to be updated.
        new_val: The new value.

        """

        self.tree[self.tree_size // 2 + pos] = new_val

        node = (self.tree_size // 2 + pos) // 2

        while node >= 1:

            self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
            node //= 2

    def get_list_len(self):
        """
        Returns the new list size as modified in the get_len(size) function.

        """
        
        return self.tree_size // 2
