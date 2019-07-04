from __future__ import print_function, division

__all__ = [
    'Node',
    'NodeV2'
]

_check_type = lambda a, t: isinstance(a, t)
NoneType = type(None)

class Node(object):
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

    __slots__ = ['key', 'data', 'left', 'right', 'is_root']

    def __new__(cls, key, data):
        obj = object.__new__(cls)
        obj.data, obj.key = data, key
        obj.left, obj.right = None, None
        obj.is_root = False
        return obj

    def __str__(self):
        """
        Used for printing.
        """
        return str((self.left, self.key, self.data, self.right))

class NodeV2(Node):
    """
    Extends `Node` by storing, height and parent.

    Parameters
    ==========

    height: int
        Height of the node,
        given as max(height of left child, height of right child) + 1.
    parent: int
        The index of the parent node.
    """

    def __new__(cls, key, data):
        obj = super(cls, NodeV2).__new__(cls, key, data)
        obj.parent, obj.height = None, 0
        return obj
