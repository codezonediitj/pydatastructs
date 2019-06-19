from pydatastructs.trees.binary_trees import BinarySearchTree
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
    assert str(b) == \
    ("[(1, 8, 8, 7), (3, 4, 4, 4), (None, 10, 10, 7), (None, 1, 1, None), "
    "(None, 6, 6, 6), (None, 4, 4, None), (None, 7, 7, None), (None, 14, 14, None), "
    "(None, 13, 13, None)]")
    raises(ValueError, lambda: BST(root_data=6))
