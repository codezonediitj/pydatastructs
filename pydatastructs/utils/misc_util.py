import math, pydatastructs
from enum import Enum
from pydatastructs.utils._backend.cpp import _nodes

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
    'SkipNode',
    'minimum',
    'summation',
    'greatest_common_divisor',
    'Backend'
]


class Backend(Enum):

    PYTHON = 'Python'
    CPP = 'Cpp'

    def __str__(self):
        return self.value

def raise_if_backend_is_not_python(api, backend):
    if backend != Backend.PYTHON:
        raise ValueError("As of {} version, only {} backend is supported for {} API".format(
                            pydatastructs.__version__, str(Backend.PYTHON), api))

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
    backend: pydatastructs.Backend
        The backend to be used. Available backends: Python and C++
        Optional, by default, the Python backend is used. For faster execution, use the C++ backend.
    """

    __slots__ = ['key', 'data', 'left', 'right', 'is_root',
                 'height', 'parent', 'size']

    @classmethod
    def methods(cls):
        return ['__new__', '__str__']

    def __new__(cls, key, data=None, **kwargs):
        backend = kwargs.get('backend', Backend.PYTHON)
        if backend == Backend.CPP:
            return _nodes.TreeNode(key, data, **kwargs)
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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.
    """
    __slots__ = ['key', 'data', 'priority']

    def __new__(cls, key, priority, data=None, **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.
    """
    __slots__ = ['key', 'data', 'color']

    @classmethod
    def methods(cls):
        return ['__new__']

    def __new__(cls, key, data=None, **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.
    """
    __slots__ = ['parent', 'key', 'children', 'data', 'is_root']

    @classmethod
    def methods(cls):
        return ['__new__', 'add_children', '__str__']

    def __new__(cls, key, data=None, **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

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

    def __new__(cls, key, data=None, **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
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
        List of names of attributes which should
        be used as links to other nodes.
    addrs
        List of address of nodes to be assigned to
        each of the attributes in links.
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.
    """
    @classmethod
    def methods(cls):
        return ['__new__', '__str__']

    def __new__(cls, key, data=None, links=None, addrs=None,
                **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
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
        return str((self.key, self.data))

class SkipNode(Node):
    """
    Represents node in linked lists.

    Parameters
    ==========

    key
        Any valid identifier to uniquely
        identify the node in the skip list.
    data
        Any valid data to be stored in the node.
    next
        Reference to the node lying just forward
        to the current node.
        Optional, by default, None.
    down
        Reference to the node lying just below the
        current node.
        Optional, by default, None.
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.
    """

    __slots__ = ['key', 'data', 'next', 'down']

    def __new__(cls, key, data=None, next=None, down=None,
                **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
        obj = Node.__new__(cls)
        obj.key, obj.data = key, data
        obj.next, obj.down = next, down
        return obj

    def __str__(self):
        return str((self.key, self.data))

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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.
    """
    @classmethod
    def methods(cls):
        return ['__new__', 'add_adjacent_node',
                'remove_adjacent_node']

    def __new__(cls, name, data=None, adjacency_list=None,
                **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.
    """
    __slots__ = ['name', 'data']

    @classmethod
    def methods(cls):
        return ['__new__']

    def __new__(cls, name, data=None,
                **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.
    """
    @classmethod
    def methods(cls):
        return ['__new__', '__str__']

    def __new__(cls, node1, node2, value=None,
                **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.
    """

    __slots__ = ['parent', 'size', 'key', 'data']

    @classmethod
    def methods(cls):
        return ['__new__']

    def __new__(cls, key, data=None,
                **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.
    """

    __slots__ = ['char', '_children', 'is_terminal']

    @classmethod
    def methods(cls):
        return ['__new__', 'add_child', 'get_child', 'remove_child']

    def __new__(cls, char=None, **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
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

def _check_range_query_inputs(input, bounds):
    start, end = input
    if start >= end:
        raise ValueError("Input (%d, %d) range is empty."%(start, end))
    if start < bounds[0] or end > bounds[1]:
        raise IndexError("Input (%d, %d) range is out of "
                         "bounds of array indices (%d, %d)."
                         %(start, end, bounds[0], bounds[1]))

def minimum(x_y):
    if len(x_y) == 1:
        return x_y[0]

    x, y = x_y
    if x is None or y is None:
        return x if y is None else y

    return min(x, y)

def greatest_common_divisor(x_y):
    if len(x_y) == 1:
        return x_y[0]

    x, y = x_y
    if x is None or y is None:
        return x if y is None else y

    return math.gcd(x, y)

def summation(x_y):
    if len(x_y) == 1:
        return x_y[0]

    x, y = x_y
    if x is None or y is None:
        return x if y is None else y

    return x + y
