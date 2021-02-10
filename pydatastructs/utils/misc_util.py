__all__ = [
    'TreeNode',
    'MAryTreeNode',
    'LinkedListNode',
    'BinomialTreeNode',
    'AdjacencyListGraphNode',
    'AdjacencyMatrixGraphNode',
    'GraphEdge',
    'Set',
    'CartesianTreeNode',
    'RedBlackTreeNode',
    'TrieNode',
    'BNode'
]

_check_type = lambda a, t: isinstance(a, t)
NoneType = type(None)

class Node(object):
    """
    Abstract class representing a node.
    """
    pass

class TreeNode(Node):
    """
    Represents node in trees.

    Parameters
    ==========

    key
        Required for comparison operations.
    data
        Any valid data to be stored in the node.
    left: int
        Optional, index of the left child node.
    right: int
        Optional, index of the right child node.
    """

    __slots__ = ['key', 'data', 'left', 'right', 'is_root',
                 'height', 'parent', 'size']

    @classmethod
    def methods(cls):
        return ['__new__', '__str__']

    def __new__(cls, key, data=None):
        obj = Node.__new__(cls)
        obj.data, obj.key = data, key
        obj.left, obj.right, obj.parent, obj.height, obj.size = \
            None, None, None, 0, 1
        obj.is_root = False
        return obj

    def __str__(self):
        """
        Used for printing.
        """
        return str((self.left, self.key, self.data, self.right))

class CartesianTreeNode(TreeNode):
    """
    Represents node in cartesian trees.

    Parameters
    ==========

    key
        Required for comparison operations.
    data
        Any valid data to be stored in the node.
    priority: int
        An integer value for heap property.

    """
    __slots__ = ['key', 'data', 'priority']

    def __new__(cls, key, priority, data=None):
        obj = TreeNode.__new__(cls, key, data)
        obj.priority = priority
        return obj

    def __str__(self):
        """
        Used for printing.
        """
        return str((self.left, self.key, self.priority, self.data, self.right))

class RedBlackTreeNode(TreeNode):
    """
    Represents node in red-black trees.

    Parameters
    ==========

    key
        Required for comparison operations.
    data
        Any valid data to be stored in the node.
    color
        0 for black and 1 for red.

    """
    __slots__ = ['key', 'data', 'color']

    @classmethod
    def methods(cls):
        return ['__new__']

    def __new__(cls, key, data=None):
        obj = TreeNode.__new__(cls, key, data)
        obj.color = 1
        return obj

class BinomialTreeNode(TreeNode):
    """
    Represents node in binomial trees.

    Parameters
    ==========

    key
        Required for comparison operations.
    data
        Any valid data to be stored in the node.

    Note
    ====

    The following are the data members of the class:

    parent: BinomialTreeNode
        A reference to the BinomialTreeNode object
        which is a prent of this.
    children: DynamicOneDimensionalArray
        An array of references to BinomialTreeNode objects
        which are children this node.
    is_root: bool, by default, False
        If the current node is a root of the tree then
        set it to True otherwise False.
    """
    __slots__ = ['parent', 'key', 'children', 'data', 'is_root']

    @classmethod
    def methods(cls):
        return ['__new__', 'add_children', '__str__']

    def __new__(cls, key, data=None):
        from pydatastructs.linear_data_structures.arrays import DynamicOneDimensionalArray
        obj = Node.__new__(cls)
        obj.data, obj.key = data, key
        obj.children, obj.parent, obj.is_root = (
        DynamicOneDimensionalArray(BinomialTreeNode, 0),
        None,
        False
        )
        return obj

    def add_children(self, *children):
        """
        Adds children of current node.
        """
        for child in children:
            self.children.append(child)
            child.parent = self

    def __str__(self):
        """
        For printing the key and data.
        """
        return str((self.key, self.data))

class MAryTreeNode(TreeNode):
    """
    Represents node in an M-ary trees.

    Parameters
    ==========

    key
        Required for comparison operations.
    data
        Any valid data to be stored in the node.

    Note
    ====

    The following are the data members of the class:

    children: DynamicOneDimensionalArray
        An array of indices which stores the children of
        this node in the M-ary tree array
    is_root: bool, by default, False
        If the current node is a root of the tree then
        set it to True otherwise False.
    """
    __slots__ = ['key', 'children', 'data', 'is_root']

    @classmethod
    def methods(cls):
        return ['__new__', 'add_children', '__str__']

    def __new__(cls, key, data=None):
        from pydatastructs.linear_data_structures.arrays import DynamicOneDimensionalArray
        obj = Node.__new__(cls)
        obj.data = data
        obj.key = key
        obj.is_root = False
        obj.children = DynamicOneDimensionalArray(int, 0)
        return obj

    def add_children(self, *children):
        """
        Adds children of current node.
        """
        for child in children:
            self.children.append(child)

    def __str__(self):
        return str((self.key, self.data))


class LinkedListNode(Node):
    """
    Represents node in linked lists.

    Parameters
    ==========

    key
        Any valid identifier to uniquely
        identify the node in the linked list.
    data
        Any valid data to be stored in the node.
    links
        List of names of attributes which should be used as links to other nodes.
    addrs
        List of address of nodes to be assigned to each of the attributes in links.
    """
    @classmethod
    def methods(cls):
        return ['__new__', '__str__']

    def __new__(cls, key, data=None, links=None, addrs=None):
        if links is None:
            links = ['next']
        if addrs is None:
            addrs = [None]
        obj = Node.__new__(cls)
        obj.key = key
        obj.data = data
        for link, addr in zip(links, addrs):
            obj.__setattr__(link, addr)
        obj.__slots__ = ['key', 'data'] + links
        return obj

    def __str__(self):
        return str(self.key)

class GraphNode(Node):
    """
    Abastract class for graph nodes/vertices.
    """
    def __str__(self):
        return str((self.name, self.data))

class AdjacencyListGraphNode(GraphNode):
    """
    Represents nodes for adjacency list implementation
    of graphs.

    Parameters
    ==========

    name: str
        The name of the node by which it is identified
        in the graph. Must be unique.
    data
        The data to be stored at each graph node.
    adjacency_list: list
        Any valid iterator to initialize the adjacent
        nodes of the current node.
        Optional, by default, None
    """
    @classmethod
    def methods(cls):
        return ['__new__', 'add_adjacent_node',
                'remove_adjacent_node']

    def __new__(cls, name, data=None, adjacency_list=None):
        obj = GraphNode.__new__(cls)
        obj.name, obj.data = str(name), data
        obj._impl = 'adjacency_list'
        if adjacency_list is not None:
            for node in adjacency_list:
                obj.__setattr__(node.name, node)
        obj.adjacent = adjacency_list if adjacency_list is not None \
                       else []
        return obj

    def add_adjacent_node(self, name, data=None):
        """
        Adds adjacent node to the current node's
        adjacency list with given name and data.
        """
        if hasattr(self, name):
            getattr(self, name).data = data
        else:
            new_node = AdjacencyListGraphNode(name, data)
            self.__setattr__(new_node.name, new_node)
            self.adjacent.append(new_node.name)

    def remove_adjacent_node(self, name):
        """
        Removes node with given name from
        adjacency list.
        """
        if not hasattr(self, name):
            raise ValueError("%s is not adjacent to %s"%(name, self.name))
        self.adjacent.remove(name)
        delattr(self, name)

class AdjacencyMatrixGraphNode(GraphNode):
    """
    Represents nodes for adjacency matrix implementation
    of graphs.

    Parameters
    ==========

    name: str
        The index of the node in the AdjacencyMatrix.
    data
        The data to be stored at each graph node.
    """
    __slots__ = ['name', 'data']

    @classmethod
    def methods(cls):
        return ['__new__']

    def __new__(cls, name, data=None):
        obj = GraphNode.__new__(cls)
        obj.name, obj.data, obj.is_connected = \
            str(name), data, None
        obj._impl = 'adjacency_matrix'
        return obj

class GraphEdge(object):
    """
    Represents the concept of edges in graphs.

    Parameters
    ==========

    node1: GraphNode or it's child classes
        The source node of the edge.
    node2: GraphNode or it's child classes
        The target node of the edge.
    """
    @classmethod
    def methods(cls):
        return ['__new__', '__str__']

    def __new__(cls, node1, node2, value=None):
        obj = object.__new__(cls)
        obj.source, obj.target = node1, node2
        obj.value = value
        return obj

    def __str__(self):
        return str((self.source.name, self.target.name))

class Set(object):
    """
    Represents a set in a forest of disjoint sets.

    Parameters
    ==========

    key: Hashable python object
        The key which uniquely identifies
        the set.
    data: Python object
        The data to be stored in the set.
    """

    __slots__ = ['parent', 'size', 'key', 'data']

    @classmethod
    def methods(cls):
        return ['__new__']

    def __new__(cls, key, data=None):
        obj = object.__new__(cls)
        obj.key = key
        obj.data = data
        obj.parent, obj.size = [None]*2
        return obj

class TrieNode(Node):
    """
    Represents nodes in the trie data structure.

    Parameters
    ==========

    char: The character stored in the current node.
          Optional, by default None.
    """

    __slots__ = ['char', '_children', 'is_terminal']

    @classmethod
    def methods(cls):
        return ['__new__', 'add_child', 'get_child', 'remove_child']

    def __new__(cls, char=None):
        obj = Node.__new__(cls)
        obj.char = char
        obj._children = {}
        obj.is_terminal = False
        return obj

    def add_child(self, trie_node) -> None:
        self._children[trie_node.char] = trie_node

    def get_child(self, char: str):
        return self._children.get(char, None)

    def remove_child(self, char: str) -> None:
        self._children.pop(char)

def _comp(u, v, tcomp):
    """
    Overloaded comparator for comparing
    two values where any one of them can be
    `None`.
    """
    if u is None and v is not None:
        return False
    elif u is not None and v is None:
        return True
    elif u is None and v is None:
        return False
    else:
        return tcomp(u, v)

class BNode(object):
    __slots__ = ["tree", "contents", "children"]

    def __new__(cls, tree, contents=None, children=None):
        obj = Node.__new__(cls)
        obj.tree = tree
        obj.contents = contents or []
        obj.children = children or []
        if obj.children:
            assert len(obj.contents) + 1 == len(obj.children), \
                    "one more child than data item required"
        return obj

    def __repr__(self):
        name = getattr(self, "children", 0) and "Branch" or "Leaf"
        return "<%s %s>" % (name, ", ".join(map(str, self.contents)))

    def lateral(self, parent, parent_index, dest, dest_index):
        if parent_index > dest_index:
            dest.contents.append(parent.contents[dest_index])
            parent.contents[dest_index] = self.contents.pop(0)
            if self.children:
                dest.children.append(self.children.pop(0))
        else:
            dest.contents.insert(0, parent.contents[parent_index])
            parent.contents[parent_index] = self.contents.pop()
            if self.children:
                dest.children.insert(0, self.children.pop())

    def shrink(self, ancestors):
        parent = None

        if ancestors:
            parent, parent_index = ancestors.pop()
            if parent_index:
                left_sib = parent.children[parent_index - 1]
                if len(left_sib.contents) < self.tree.order:
                    self.lateral(
                            parent, parent_index, left_sib, parent_index - 1)
                    return

            if parent_index + 1 < len(parent.children):
                right_sib = parent.children[parent_index + 1]
                if len(right_sib.contents) < self.tree.order:
                    self.lateral(
                            parent, parent_index, right_sib, parent_index + 1)
                    return

        center = len(self.contents) // 2
        sibling, push = self.split()

        if not parent:
            parent, parent_index = self.tree.BRANCH(
                    self.tree, children=[self]), 0
            self.tree._root = parent

        parent.contents.insert(parent_index, push)
        parent.children.insert(parent_index + 1, sibling)
        if len(parent.contents) > parent.tree.order:
            parent.shrink(ancestors)

    def grow(self, ancestors):
        parent, parent_index = ancestors.pop()

        minimum = self.tree.order // 2
        left_sib = right_sib = None

        if parent_index + 1 < len(parent.children):
            right_sib = parent.children[parent_index + 1]
            if len(right_sib.contents) > minimum:
                right_sib.lateral(parent, parent_index + 1, self, parent_index)
                return

        if parent_index:
            left_sib = parent.children[parent_index - 1]
            if len(left_sib.contents) > minimum:
                left_sib.lateral(parent, parent_index - 1, self, parent_index)
                return

        if left_sib:
            left_sib.contents.append(parent.contents[parent_index - 1])
            left_sib.contents.extend(self.contents)
            if self.children:
                left_sib.children.extend(self.children)
            parent.contents.pop(parent_index - 1)
            parent.children.pop(parent_index)
        else:
            self.contents.append(parent.contents[parent_index])
            self.contents.extend(right_sib.contents)
            if self.children:
                self.children.extend(right_sib.children)
            parent.contents.pop(parent_index)
            parent.children.pop(parent_index + 1)

        if len(parent.contents) < minimum:
            if ancestors:
                parent.grow(ancestors)
            elif not parent.contents:
                self.tree._root = left_sib or self

    def split(self):
        center = len(self.contents) // 2
        median = self.contents[center]
        sibling = type(self)(
                self.tree,
                self.contents[center + 1:],
                self.children[center + 1:])
        self.contents = self.contents[:center]
        self.children = self.children[:center + 1]
        return sibling, median

    def insert(self, index, item, ancestors):
        self.contents.insert(index, item)
        if len(self.contents) > self.tree.order:
            self.shrink(ancestors)

    def remove(self, index, ancestors):
        minimum = self.tree.order // 2

        if self.children:
            additional_ancestors = [(self, index + 1)]
            descendent = self.children[index + 1]
            while descendent.children:
                additional_ancestors.append((descendent, 0))
                descendent = descendent.children[0]
            if len(descendent.contents) > minimum:
                ancestors.extend(additional_ancestors)
                self.contents[index] = descendent.contents[0]
                descendent.remove(0, ancestors)
                return

            additional_ancestors = [(self, index)]
            descendent = self.children[index]
            while descendent.children:
                additional_ancestors.append(
                        (descendent, len(descendent.children) - 1))
                descendent = descendent.children[-1]
            ancestors.extend(additional_ancestors)
            self.contents[index] = descendent.contents[-1]
            descendent.remove(len(descendent.children) - 1, ancestors)
        else:
            self.contents.pop(index)
            if len(self.contents) < minimum and ancestors:
                self.grow(ancestors)
