from pydatastructs.trees.binary_trees import (
    BinarySearchTree, BinaryTreeTraversal, AVLTree)
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
    b = BST(-8, 8)
    b.insert(-3, 3)
    b.insert(-10, 10)
    b.insert(-1, 1)
    b.insert(-6, 6)
    b.insert(-4, 4)
    b.insert(-7, 7)
    b.insert(-14, 14)
    b.insert(-13, 13)
    assert b.delete(-13) == True
    assert b.delete(-10) == True
    assert b.delete(-3) == True
    assert b.delete(-13) == None
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
    ino = trav.depth_first_search()
    assert [str(n) for n in ino] == \
    ["(None, 'A', 'A', None)", "(2, 'B', 'B', 4)", "(None, 'C', 'C', None)",
     "(5, 'D', 'D', 6)", "(None, 'E', 'E', None)", "(1, 'F', 'F', 3)",
     "(None, 'G', 'G', 7)", "(None, 'H', 'H', None)", "(8, 'I', 'I', None)"]
    out = trav.depth_first_search(order='out_order')
    assert [str(n) for n in out] == \
    ["(8, 'I', 'I', None)", "(None, 'H', 'H', None)", "(None, 'G', 'G', 7)",
     "(1, 'F', 'F', 3)", "(None, 'E', 'E', None)", "(5, 'D', 'D', 6)",
     "(None, 'C', 'C', None)", "(2, 'B', 'B', 4)", "(None, 'A', 'A', None)"]
    post = trav.depth_first_search(order='post_order')
    assert [str(n) for n in post] == \
    ["(None, 'A', 'A', None)", "(None, 'C', 'C', None)",
     "(None, 'E', 'E', None)", "(5, 'D', 'D', 6)", "(2, 'B', 'B', 4)",
     "(None, 'H', 'H', None)", "(8, 'I', 'I', None)", "(None, 'G', 'G', 7)",
     "(1, 'F', 'F', 3)"]
    bfs = trav.breadth_first_search()
    assert [str(n) for n in bfs] == \
        ["(1, 'F', 'F', 3)", "(2, 'B', 'B', 4)", "(None, 'G', 'G', 7)",
         "(None, 'A', 'A', None)", "(5, 'D', 'D', 6)", "(8, 'I', 'I', None)",
         "(None, 'C', 'C', None)", "(None, 'E', 'E', None)",
         "(None, 'H', 'H', None)"]
    raises(NotImplementedError, lambda: trav.breadth_first_search(strategy='iddfs'))
    raises(NotImplementedError, lambda: trav.depth_first_search(order='in_out_order'))
    raises(TypeError, lambda: BTT(1))

def test_AVLTree():
    a = AVLTree('M', 'M')
    a.insert('N', 'N')
    a.insert('O', 'O')
    a.insert('L', 'L')
    a.insert('K', 'K')
    a.insert('Q', 'Q')
    a.insert('P', 'P')
    a.insert('H', 'H')
    a.insert('I', 'I')
    a.insert('A', 'A')
    assert str(a) == ("[(None, 'M', 'M', None), (8, 'N', 'N', 6), "
                      "(None, 'O', 'O', None), (4, 'L', 'L', 0), "
                      "(None, 'K', 'K', None), (None, 'Q', 'Q', None), "
                      "(2, 'P', 'P', 5), (9, 'H', 'H', None), "
                      "(7, 'I', 'I', 3), (None, 'A', 'A', None)]")
    assert [a.balance_factor(n) for n in a.tree] == [0, 1, 0, 0, 0, 0, 0, 1, 0, 0]
    a1 = AVLTree(1, 1)
    a1.insert(2, 2)
    a1.insert(3, 3)
    a1.insert(4, 4)
    a1.insert(5, 5)
    assert str(a1) == ("[(None, 1, 1, None), (0, 2, 2, 3), (None, 3, 3, None), "
                      "(2, 4, 4, 4), (None, 5, 5, None)]")
    a3 = AVLTree(-1, 1)
    a3.insert(-2, 2)
    a3.insert(-3, 3)
    a3.insert(-4, 4)
    a3.insert(-5, 5)
    assert str(a3) == ("[(None, -1, 1, None), (3, -2, 2, 0), "
                       "(None, -3, 3, None), (4, -4, 4, 2), "
                       "(None, -5, 5, None)]")
    a2 = AVLTree()
    a2.insert(1, 1)
    a2.insert(1, 1)
    assert str(a2) == "[(None, 1, 1, None)]"
