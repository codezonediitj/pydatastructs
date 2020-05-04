from pydatastructs.trees.binary_trees import (
    BinarySearchTree, BinaryTreeTraversal, AVLTree,
    ArrayForTrees, BinaryIndexedTree, SelfBalancingBinaryTree, SplayTree, CartesianTree, Treap)
from pydatastructs.utils.raises_util import raises
from pydatastructs.utils.misc_util import TreeNode
from copy import deepcopy
import random

def test_BinarySearchTree():
    BST = BinarySearchTree
    b = BST(8, 8)
    b.delete(8)
    b.insert(8, 8)
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
    assert b.search(-1) is None
    assert b.delete(13) is True
    assert b.search(13) is None
    assert b.delete(10) is True
    assert b.search(10) is None
    assert b.delete(3) is True
    assert b.search(3) is None
    assert b.delete(13) is None
    assert str(b) == \
    ("[(1, 8, 8, 7), (3, 4, 4, 4), '', (None, 1, 1, None), "
    "(None, 6, 6, 6), '', (None, 7, 7, None), (None, 14, 14, None)]")
    b.delete(7)
    b.delete(6)
    b.delete(1)
    b.delete(4)
    assert str(b) == "[(None, 8, 8, 2), '', (None, 14, 14, None)]"
    bc = BST(1, 1)
    assert bc.insert(1, 2) is None
    b = BST(-8, 8)
    b.insert(-3, 3)
    b.insert(-10, 10)
    b.insert(-1, 1)
    b.insert(-6, 6)
    b.insert(-4, 4)
    b.insert(-7, 7)
    b.insert(-14, 14)
    b.insert(-13, 13)
    assert b.delete(-13) is True
    assert b.delete(-10) is True
    assert b.delete(-3) is True
    assert b.delete(-13) is None
    bl = BST()
    nodes = [50, 30, 90, 70, 100, 60, 80, 55, 20, 40, 15, 10, 16, 17, 18]
    for node in nodes:
        bl.insert(node, node)

    assert bl.lowest_common_ancestor(80, 55, 2) == 70
    assert bl.lowest_common_ancestor(60, 70, 2) == 70
    assert bl.lowest_common_ancestor(18, 18, 2) == 18
    assert bl.lowest_common_ancestor(40, 90, 2) == 50

    assert bl.lowest_common_ancestor(18, 10, 2) == 15
    assert bl.lowest_common_ancestor(55, 100, 2) == 90
    assert bl.lowest_common_ancestor(16, 80, 2) == 50
    assert bl.lowest_common_ancestor(30, 55, 2) == 50

    assert raises(ValueError, lambda: bl.lowest_common_ancestor(60, 200, 2))
    assert raises(ValueError, lambda: bl.lowest_common_ancestor(200, 60, 2))
    assert raises(ValueError, lambda: bl.lowest_common_ancestor(-3, 4, 2))

    assert bl.lowest_common_ancestor(80, 55, 1) == 70
    assert bl.lowest_common_ancestor(60, 70, 1) == 70
    assert bl.lowest_common_ancestor(18, 18, 1) == 18
    assert bl.lowest_common_ancestor(40, 90, 1) == 50

    assert bl.lowest_common_ancestor(18, 10, 1) == 15
    assert bl.lowest_common_ancestor(55, 100, 1) == 90
    assert bl.lowest_common_ancestor(16, 80, 1) == 50
    assert bl.lowest_common_ancestor(30, 55, 1) == 50

    assert raises(ValueError, lambda: bl.lowest_common_ancestor(60, 200, 1))
    assert raises(ValueError, lambda: bl.lowest_common_ancestor(200, 60, 1))
    assert raises(ValueError, lambda: bl.lowest_common_ancestor(-3, 4, 1))

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
    assert raises(NotImplementedError, lambda: trav.breadth_first_search(strategy='iddfs'))
    assert raises(NotImplementedError, lambda: trav.depth_first_search(order='in_out_order'))
    assert raises(TypeError, lambda: BTT(1))

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
    assert [a.balance_factor(n) for n in a.tree if n is not None] == \
        [0, -1, 0, 0, 0, 0, 0, -1, 0, 0]
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
    a3 = AVLTree()
    a3.tree = ArrayForTrees(TreeNode, 0)
    for i in range(7):
        a3.tree.append(TreeNode(i, i))
    a3.tree[0].left = 1
    a3.tree[0].right = 6
    a3.tree[1].left = 5
    a3.tree[1].right = 2
    a3.tree[2].left = 3
    a3.tree[2].right = 4
    a3._left_right_rotate(0, 1)
    assert str(a3) == ("[(4, 0, 0, 6), (5, 1, 1, 3), (1, 2, 2, 0), "
                       "(None, 3, 3, None), (None, 4, 4, None), "
                       "(None, 5, 5, None), (None, 6, 6, None)]")
    a4 = AVLTree()
    a4.tree = ArrayForTrees(TreeNode, 0)
    for i in range(7):
        a4.tree.append(TreeNode(i, i))
    a4.tree[0].left = 1
    a4.tree[0].right = 2
    a4.tree[2].left = 3
    a4.tree[2].right = 4
    a4.tree[3].left = 5
    a4.tree[3].right = 6
    a4._right_left_rotate(0, 2)
    assert str(a4) == ("[(1, 0, 0, 5), (None, 1, 1, None), (6, 2, 2, 4), "
                      "(0, 3, 3, 2), (None, 4, 4, None), (None, 5, 5, None), "
                      "(None, 6, 6, None)]")

    a5 = AVLTree(is_order_statistic=True)
    a5.tree = ArrayForTrees(TreeNode, [
        TreeNode(10, 10),
        TreeNode(5, 5),
        TreeNode(17, 17),
        TreeNode(2, 2),
        TreeNode(9, 9),
        TreeNode(12, 12),
        TreeNode(20, 20),
        TreeNode(3, 3),
        TreeNode(11, 11),
        TreeNode(15, 15),
        TreeNode(18, 18),
        TreeNode(30, 30),
        TreeNode(13, 13),
        TreeNode(33, 33)
    ])

    a5.tree[0].left, a5.tree[0].right, a5.tree[0].parent, a5.tree[0].height = \
        1, 2, None, 4
    a5.tree[1].left, a5.tree[1].right, a5.tree[1].parent, a5.tree[1].height = \
        3, 4, 0, 2
    a5.tree[2].left, a5.tree[2].right, a5.tree[2].parent, a5.tree[2].height = \
        5, 6, 0, 3
    a5.tree[3].left, a5.tree[3].right, a5.tree[3].parent, a5.tree[3].height = \
        None, 7, 1, 1
    a5.tree[4].left, a5.tree[4].right, a5.tree[4].parent, a5.tree[4].height = \
        None, None, 1, 0
    a5.tree[5].left, a5.tree[5].right, a5.tree[5].parent, a5.tree[5].height = \
        8, 9, 2, 2
    a5.tree[6].left, a5.tree[6].right, a5.tree[6].parent, a5.tree[6].height = \
        10, 11, 2, 2
    a5.tree[7].left, a5.tree[7].right, a5.tree[7].parent, a5.tree[7].height = \
        None, None, 3, 0
    a5.tree[8].left, a5.tree[8].right, a5.tree[8].parent, a5.tree[8].height = \
        None, None, 5, 0
    a5.tree[9].left, a5.tree[9].right, a5.tree[9].parent, a5.tree[9].height = \
        12, None, 5, 1
    a5.tree[10].left, a5.tree[10].right, a5.tree[10].parent, a5.tree[10].height = \
        None, None, 6, 0
    a5.tree[11].left, a5.tree[11].right, a5.tree[11].parent, a5.tree[11].height = \
        None, 13, 6, 1
    a5.tree[12].left, a5.tree[12].right, a5.tree[12].parent, a5.tree[12].height = \
        None, None, 9, 0
    a5.tree[13].left, a5.tree[13].right, a5.tree[13].parent, a5.tree[13].height = \
        None, None, 11, 0

    # testing order statistics
    a5.tree[0].size = 14
    a5.tree[1].size = 4
    a5.tree[2].size = 9
    a5.tree[3].size = 2
    a5.tree[4].size = 1
    a5.tree[5].size = 4
    a5.tree[6].size = 4
    a5.tree[7].size = 1
    a5.tree[8].size = 1
    a5.tree[9].size = 2
    a5.tree[10].size = 1
    a5.tree[11].size = 2
    a5.tree[12].size = 1
    a5.tree[13].size = 1

    assert raises(ValueError, lambda: a5.select(0))
    assert raises(ValueError, lambda: a5.select(15))
    assert a5.rank(-1) is None
    def test_select_rank(expected_output):
        output = []
        for i in range(len(expected_output)):
            output.append(a5.select(i + 1).key)
        assert output == expected_output

        output = []
        expected_ranks = [i + 1 for i in range(len(expected_output))]
        for i in range(len(expected_output)):
            output.append(a5.rank(expected_output[i]))
        assert output == expected_ranks

    test_select_rank([2, 3, 5, 9, 10, 11, 12, 13, 15, 17, 18, 20, 30, 33])
    a5.delete(9)
    a5.delete(13)
    a5.delete(20)
    assert str(a5) == ("[(7, 10, 10, 5), (None, 5, 5, None), "
                       "(0, 17, 17, 6), (None, 2, 2, None), '', "
                       "(8, 12, 12, 9), (10, 30, 30, 13), (3, 3, 3, 1), "
                       "(None, 11, 11, None), (None, 15, 15, None), "
                       "(None, 18, 18, None), '', '', (None, 33, 33, None)]")
    test_select_rank([2, 3, 5, 10, 11, 12, 15, 17, 18, 30, 33])
    a5.delete(10)
    a5.delete(17)
    test_select_rank([2, 3, 5, 11, 12, 15, 18, 30, 33])
    a5.delete(11)
    a5.delete(30)
    test_select_rank([2, 3, 5, 12, 15, 18, 33])
    a5.delete(12)
    test_select_rank([2, 3, 5, 15, 18, 33])
    a5.delete(15)
    test_select_rank([2, 3, 5, 18, 33])
    a5.delete(18)
    test_select_rank([2, 3, 5, 33])
    a5.delete(33)
    test_select_rank([2, 3, 5])
    a5.delete(5)
    test_select_rank([2, 3])
    a5.delete(3)
    test_select_rank([2])
    a5.delete(2)
    test_select_rank([])

def test_BinaryIndexedTree():

    FT = BinaryIndexedTree

    t = FT([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    assert t.get_sum(0, 2) == 6
    assert t.get_sum(0, 4) == 15
    assert t.get_sum(0, 9) == 55
    t.update(0, 100)
    assert t.get_sum(0, 2) == 105
    assert t.get_sum(0, 4) == 114
    assert t.get_sum(1, 9) == 54

def test_CartesianTree():
    tree = CartesianTree()
    tree.insert(3, 1, 3)
    tree.insert(1, 6, 1)
    tree.insert(0, 9, 0)
    tree.insert(5, 11, 5)
    tree.insert(4, 14, 4)
    tree.insert(9, 17, 9)
    tree.insert(7, 22, 7)
    tree.insert(6, 42, 6)
    tree.insert(8, 49, 8)
    tree.insert(2, 99, 2)
    assert str(tree) == \
           ("[(1, 3, 1, 3, 3), (2, 1, 6, 1, 9), "
            "(None, 0, 9, 0, None), (4, 5, 11, 5, 5), "
            "(None, 4, 14, 4, None), (6, 9, 17, 9, None), "
            "(7, 7, 22, 7, 8), (None, 6, 42, 6, None), "
            "(None, 8, 49, 8, None), (None, 2, 99, 2, None)]")
    tree.insert(1.5, 4, 1.5)
    assert str(tree) == \
           ("[(10, 3, 1, 3, 3), (2, 1, 6, 1, None), "
            "(None, 0, 9, 0, None), (4, 5, 11, 5, 5), "
            "(None, 4, 14, 4, None), (6, 9, 17, 9, None), "
            "(7, 7, 22, 7, 8), (None, 6, 42, 6, None), "
            "(None, 8, 49, 8, None), (None, 2, 99, 2, None), "
            "(1, 1.5, 4, 1.5, 9)]")
    k = tree.search(1.5)
    assert tree.tree[tree.tree[k].parent].key == 3
    tree.delete(1.5)
    tree.tree[tree.tree[tree.root_idx].left].key == 1
    tree.delete(8)
    assert tree.search(8) is None
    tree.delete(7)
    assert tree.search(7) is None
    tree.delete(3)
    assert tree.search(3) is None
    assert tree.delete(18) is None

def test_Treap():

    random.seed(0)
    tree = Treap()
    tree.insert(7, 7)
    tree.insert(2, 2)
    tree.insert(3, 3)
    tree.insert(4, 4)
    tree.insert(5, 5)
    assert isinstance(tree.tree[0].priority, float)
    tree.delete(1)
    assert tree.search(1) is None
    assert tree.search(2) == 1
    assert tree.delete(1) is None

def test_issue_234():
    """
    https://github.com/codezonediitj/pydatastructs/issues/234
    """
    tree = SelfBalancingBinaryTree()
    tree.insert(5, 5)
    tree.insert(5.5, 5.5)
    tree.insert(4.5, 4.5)
    tree.insert(4.6, 4.6)
    tree.insert(4.4, 4.4)
    tree.insert(4.55, 4.55)
    tree.insert(4.65, 4.65)
    original_tree = str(tree)
    tree._right_rotate(3, 5)
    assert tree.tree[3].parent == 5
    assert tree.tree[2].right != 3
    assert tree.tree[tree.tree[5].parent].right == 5
    assert str(tree) == ("[(2, 5, 5, 1), (None, 5.5, 5.5, None), "
                         "(4, 4.5, 4.5, 5), (None, 4.6, 4.6, 6), "
                         "(None, 4.4, 4.4, None), (None, 4.55, 4.55, 3), "
                         "(None, 4.65, 4.65, None)]")
    assert tree.tree[tree.tree[3].parent].right == 3
    tree._left_rotate(5, 3)
    assert str(tree) == original_tree
    tree.insert(4.54, 4.54)
    tree.insert(4.56, 4.56)
    tree._left_rotate(5, 8)
    assert tree.tree[tree.tree[8].parent].left == 8

def test_SplayTree():
    t = SplayTree(100, 100)
    t.insert(50, 50)
    t.insert(200, 200)
    t.insert(40, 40)
    t.insert(30, 30)
    t.insert(20, 20)
    t.insert(55, 55)

    assert str(t) == ("[(None, 100, 100, None), (None, 50, 50, None), "
                      "(0, 200, 200, None), (None, 40, 40, 1), (5, 30, 30, 3), "
                      "(None, 20, 20, None), (4, 55, 55, 2)]")
    t.delete(40)
    assert str(t) == ("[(None, 100, 100, None), '', (0, 200, 200, None), "
                      "(4, 50, 50, 6), (5, 30, 30, None), (None, 20, 20, None), "
                      "(None, 55, 55, 2)]")
    t.delete(150)
    assert str(t) == ("[(None, 100, 100, None), '', (0, 200, 200, None), (4, 50, 50, 6), "
                      "(5, 30, 30, None), (None, 20, 20, None), (None, 55, 55, 2)]")

    t1 = SplayTree(1000, 1000)
    t1.insert(2000, 2000)
    assert str(t1) == ("[(None, 1000, 1000, None), (0, 2000, 2000, None)]")

    t.join(t1)
    assert str(t) == ("[(None, 100, 100, None), '', (6, 200, 200, 8), (4, 50, 50, None), "
                      "(5, 30, 30, None), (None, 20, 20, None), (3, 55, 55, 0), (None, 1000, 1000, None), "
                      "(7, 2000, 2000, None), '']")

    s = t.split(200)
    assert str(s) == ("[(1, 2000, 2000, None), (None, 1000, 1000, None)]")
    assert str(t) == ("[(None, 100, 100, None), '', (6, 200, 200, None), (4, 50, 50, None), "
                      "(5, 30, 30, None), (None, 20, 20, None), (3, 55, 55, 0), '', '', '']")
