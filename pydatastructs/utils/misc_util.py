from __future__ import print_function, division

__all__ = [
    'TreeNode'
    'Node'
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


# A linked list node 
class Node: 

    '''
    Node class for Linked List and Doubly Linked List [ Intended for internal use and not to be imported]

    Parameters
    ==========
    
    For Doubly Linked List use Default constructor(__init__):

        data: type
            A valid object type.
            Should be convertible to string using str() method to use print() method on instance

    For Single Linked List use Alternative constructor(singleLink):
        data: type
            A valid object type
            Should be convertible to string using str() method to use print() method on instance
    
    Note
    ====

    classmethod singleLink has been used for Node class for Single linked list due to non existence of a 
    previous link between the nodes.
    '''

    __slots__ = ['data', 'next', 'prev']
    
    # Constructor to create a new node 
    def __new__(self, data): 
        self.data = data 
        self.next = NoneType
        self.prev = NoneType
    #Alternative constructor for Single Linked List
    @classmethod
    def singleLink(obj, data):
        obj.data = data
        obj.next = NoneType
        return obj
    
    def __str__(self):
        return str(self.data)
