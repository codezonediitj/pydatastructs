from pydatastructs.linear_data_structures.arrays import DynamicOneDimensionalArray

__all__ = [
    'TreeNode',
    'LinkedListNode',
    'BinomialTreeNode'
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

    data
        Any valid data to be stored in the node.
    key
        Required for comparison operations.
    left: int
        Optional, index of the left child node.
    right: int
        Optional, index of the right child node.
    """

    __slots__ = ['key', 'data', 'left', 'right', 'is_root',
                 'height', 'parent', 'size']

    def __new__(cls, key, data):
        obj = object.__new__(cls)
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

class BinomialTreeNode(TreeNode):
    """
    Represents node in binomial trees.

    Parameters
    ==========

    data
        Any valid data to be stored in the node.
    key
        Required for comparison operations.

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

    def __new__(cls, key, data):
        obj = object.__new__(cls)
        obj.data, obj.key = data, key
        obj.children, obj.parent, obj.is_root = (
        DynamicOneDimensionalArray(BinomialTreeNode, 0),
        None,
        False
        )
        return obj

    def add_children(self, *children):
        for child in children:
            self.children.append(child)

    def __str__(self):
        """
        For printing the key and data.
        """
        return str((self.key, self.data))

class LinkedListNode(Node):
    """
    Represents node in linked lists.

    Parameters
    ==========

    data
        Any valid data to be stored in the node.
    """
    def __new__(cls, data=None, links=['next'], addrs=[None]):
        obj = object.__new__(cls)
        obj.data = data
        for link, addr in zip(links, addrs):
            obj.__setattr__(link, addr)
        obj.__slots__ = ['data'] + links
        return obj

    def __str__(self):
        return str(self.data)
