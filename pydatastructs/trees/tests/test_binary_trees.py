from pydatastructs.trees.binary_trees import (
    BinarySearchTree, BinaryTreeTraversal)
from pydatastructs.utils.raises_util import raises

def test_BinarySearchTree():
    BST = BinarySearchTree
    b = BST(8, 8)
    b.insert(3, 3)
    b.insert(10, 10)
    b.insert(1, 1)
    b.insert(6, 6)
    b.insert(4, 4)
    b.insert(7, 7)
    b.insert(14, 14)
    b.insert(13, 13)
    assert str(b) == \
    ("[(1, 8, 8, 2), (3, 3, 3, 4), (None, 10, 10, 7), (None, 1, 1, None), "
    "(5, 6, 6, 6), (None, 4, 4, None), (None, 7, 7, None), (8, 14, 14, None), "
    "(None, 13, 13, None)]")
    assert b.search(10) == 2
    assert b.search(-1) == None
    assert b.delete(13) == True
    assert b.search(13) == None
    assert b.delete(10) == True
    assert b.search(10) == None
    assert b.delete(3) == True
    assert b.search(3) == None
    assert b.delete(13) == None
    assert str(b) == \
    ("[(1, 8, 8, 7), (3, 4, 4, 4), (None, 10, 10, 7), (None, 1, 1, None), "
    "(None, 6, 6, 6), (None, 4, 4, None), (None, 7, 7, None), (None, 14, 14, None), "
    "(None, 13, 13, None)]")
    bc = BST(1, 1)
    assert bc.insert(1, 2) == None
    raises(ValueError, lambda: BST(root_data=6))

def test_BinaryTreeTraversal():
    BST = BinarySearchTree
    BTT = BinaryTreeTraversal
    b = BST('F', 'F')
    b.insert('B', 'B')
    b.insert('A', 'A')
    b.insert('G', 'G')
    b.insert('D', 'D')
    b.insert('C', 'C')
    b.insert('E', 'E')
    b.insert('I', 'I')
    b.insert('H', 'H')
    trav = BTT(b)
    pre = trav.depth_first_search(order='pre_order')
    assert [str(n) for n in pre] == \
    ["(1, 'F', 'F', 3)", "(2, 'B', 'B', 4)", "(None, 'A', 'A', None)",
     "(5, 'D', 'D', 6)", "(None, 'C', 'C', None)", "(None, 'E', 'E', None)",
     "(None, 'G', 'G', 7)", "(8, 'I', 'I', None)", "(None, 'H', 'H', None)"]
    post = trav.depth_first_search()
    assert [str(n) for n in post] == \
    ["(None, 'A', 'A', None)", "(2, 'B', 'B', 4)", "(None, 'C', 'C', None)",
     "(5, 'D', 'D', 6)", "(None, 'E', 'E', None)", "(1, 'F', 'F', 3)",
     "(None, 'G', 'G', 7)", "(None, 'H', 'H', None)", "(8, 'I', 'I', None)"]
