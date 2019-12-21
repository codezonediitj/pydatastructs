from __future__ import print_function, division

__all__ = [
    'TreeNode',
    'LinkedListNode'
]

_check_type = lambda a, t: isinstance(a, t)
NoneType = type(None)

class TreeNode(object):
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

class LinkedListNode(object):
    """
    Represents node in linked lists.

    Parameters
    ==========

    data
        Any valid data to be stored in the node.
    """

    # __slots__ = ['data']

    def __new__(cls, data=None, links=['next'], addrs=[None]):
        obj = object.__new__(cls)
        obj.data = data
        for link, addr in zip(links, addrs):
            obj.__setattr__(link, addr)
        obj.__slots__ = ['data'] + links
        return obj

    def __str__(self):
        return str(self.data)
