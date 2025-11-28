from pydatastructs.trees.binary_trees import (
    BinaryTree, BinarySearchTree, BinaryTreeTraversal, AVLTree,
    ArrayForTrees, BinaryIndexedTree, SelfBalancingBinaryTree, SplayTree, CartesianTree, Treap, RedBlackTree)
from pydatastructs.utils.raises_util import raises
from pydatastructs.utils.misc_util import TreeNode
from copy import deepcopy
from pydatastructs.utils.misc_util import Backend
import random
from pydatastructs.utils._backend.cpp import _nodes

def _test_BinarySearchTree(backend):
    BST = BinarySearchTree
    b = BST(8, 8, backend=backend)
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
    # Explicit check for the __str__ method of Binary Trees Class
    assert str(b) == \
    ("[(1, 8, 8, 2), (3, 3, 3, 4), (None, 10, 10, 7), (None, 1, 1, None), "
    "(5, 6, 6, 6), (None, 4, 4, None), (None, 7, 7, None), (8, 14, 14, None), "
    "(None, 13, 13, None)]")
    assert b.root_idx == 0

    assert b.tree[0].left == 1
    assert b.tree[0].key == 8
    assert b.tree[0].data == 8
    assert b.tree[0].right == 2

    trav = BinaryTreeTraversal(b, backend=backend)
    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [1, 3, 4, 6, 7, 8, 10, 13, 14]
    assert [node.key for node in pre_order] == [8, 3, 1, 6, 4, 7, 10, 14, 13]

    assert b.search(10) == 2
    assert b.search(-1) is None
    assert b.delete(13) is True
    assert b.search(13) is None
    assert b.delete(10) is True
    assert b.search(10) is None
    assert b.delete(3) is True
    assert b.search(3) is None
    assert b.delete(13) is None

    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [1, 4, 6, 7, 8, 14]
    assert [node.key for node in pre_order] == [8, 4, 1, 6, 7, 14]

    b.delete(7)
    b.delete(6)
    b.delete(1)
    b.delete(4)

    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [8, 14]
    assert [node.key for node in pre_order] == [8, 14]

    bc = BST(1, 1, backend=backend)
    assert bc.insert(1, 2) is None

    b = BST(-8, 8, backend=backend)
    b.insert(-3, 3)
    b.insert(-10, 10)
    b.insert(-1, 1)
    b.insert(-6, 6)
    b.insert(-4, 4)
    b.insert(-7, 7)
    b.insert(-14, 14)
    b.insert(-13, 13)

    b.delete(-13)
    b.delete(-10)
    b.delete(-3)
    b.delete(-13)
    assert str(b) == "[(7, -8, 8, 1), (4, -1, 1, None), '', '', (6, -6, 6, 5), (None, -4, 4, None), (None, -7, 7, None), (None, -14, 14, None)]"

    bl = BST(backend=backend)
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

def test_BinarySearchTree():
    _test_BinarySearchTree(Backend.PYTHON)

def test_cpp_BinarySearchTree():
    _test_BinarySearchTree(Backend.CPP)

def _test_BinaryTreeTraversal(backend):
    BST = BinarySearchTree
    BTT = BinaryTreeTraversal
    b = BST('F', 'F', backend=backend)
    b.insert('B', 'B')
    b.insert('A', 'A')
    b.insert('G', 'G')
    b.insert('D', 'D')
    b.insert('C', 'C')
    b.insert('E', 'E')
    b.insert('I', 'I')
    b.insert('H', 'H')

    trav = BTT(b, backend=backend)
    pre = trav.depth_first_search(order='pre_order')
    assert [node.key for node in pre] == ['F', 'B', 'A', 'D', 'C', 'E', 'G', 'I', 'H']

    ino = trav.depth_first_search()
    assert [node.key for node in ino] == ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

    out = trav.depth_first_search(order='out_order')
    assert [node.key for node in out] == ['I', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']

    post = trav.depth_first_search(order='post_order')
    assert [node.key for node in post] == ['A', 'C', 'E', 'D', 'B', 'H', 'I', 'G', 'F']

    bfs = trav.breadth_first_search()
    assert [node.key for node in bfs] == ['F', 'B', 'G', 'A', 'D', 'I', 'C', 'E', 'H']

    assert raises(NotImplementedError, lambda: trav.breadth_first_search(strategy='iddfs'))
    assert raises(NotImplementedError, lambda: trav.depth_first_search(order='in_out_order'))
    assert raises(TypeError, lambda: BTT(1))

def test_BinaryTreeTraversal():
    _test_BinaryTreeTraversal(Backend.PYTHON)

def test_cpp_BinaryTreeTraversal():
    _test_BinaryTreeTraversal(Backend.CPP)

def _test_AVLTree(backend):
    a = AVLTree('M', 'M', backend=backend)
    a.insert('N', 'N')
    a.insert('O', 'O')
    a.insert('L', 'L')
    a.insert('K', 'K')
    a.insert('Q', 'Q')
    a.insert('P', 'P')
    a.insert('H', 'H')
    a.insert('I', 'I')
    a.insert('A', 'A')
    assert a.root_idx == 1

    trav = BinaryTreeTraversal(a, backend=backend)
    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == ['A', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q']
    assert [node.key for node in pre_order] == ['N', 'I', 'H', 'A', 'L', 'K', 'M', 'P', 'O', 'Q']

    assert [a.balance_factor(a.tree[i]) for i in range(a.tree.size) if a.tree[i] is not None] == \
        [0, -1, 0, 0, 0, 0, 0, -1, 0, 0]
    a1 = AVLTree(1, 1, backend=backend)
    a1.insert(2, 2)
    a1.insert(3, 3)
    a1.insert(4, 4)
    a1.insert(5, 5)

    trav = BinaryTreeTraversal(a1, backend=backend)
    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [1, 2, 3, 4, 5]
    assert [node.key for node in pre_order] == [2, 1, 4, 3, 5]

    a3 = AVLTree(-1, 1, backend=backend)
    a3.insert(-2, 2)
    a3.insert(-3, 3)
    a3.insert(-4, 4)
    a3.insert(-5, 5)

    trav = BinaryTreeTraversal(a3, backend=backend)
    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [-5, -4, -3, -2, -1]
    assert [node.key for node in pre_order] == [-2, -4, -5, -3, -1]

    a2 = AVLTree(backend=backend)
    a2.insert(1, 1)
    a2.insert(1, 1)

    trav = BinaryTreeTraversal(a2, backend=backend)
    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [1]
    assert [node.key for node in pre_order] == [1]

    a3 = AVLTree(backend=backend)
    a3.set_tree( ArrayForTrees(TreeNode, 0, backend=backend) )
    for i in range(0,7):
        a3.tree.append(TreeNode(i, i, backend=backend))
    a3.tree[0].left = 1
    a3.tree[0].right = 6
    a3.tree[1].left = 5
    a3.tree[1].right = 2
    a3.tree[2].left = 3
    a3.tree[2].right = 4
    a3._left_right_rotate(0, 1)
    assert str(a3) == "[(4, 0, 0, 6), (5, 1, 1, 3), (1, 2, 2, 0), (None, 3, 3, None), (None, 4, 4, None), (None, 5, 5, None), (None, 6, 6, None)]"

    trav = BinaryTreeTraversal(a3, backend=backend)
    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [5, 1, 3, 2, 4, 0, 6]
    assert [node.key for node in pre_order] == [2, 1, 5, 3, 0, 4, 6]

    a4 = AVLTree(backend=backend)
    a4.set_tree( ArrayForTrees(TreeNode, 0, backend=backend) )
    for i in range(0,7):
        a4.tree.append(TreeNode(i, i,backend=backend))
    a4.tree[0].left = 1
    a4.tree[0].right = 2
    a4.tree[2].left = 3
    a4.tree[2].right = 4
    a4.tree[3].left = 5
    a4.tree[3].right = 6
    a4._right_left_rotate(0, 2)

    trav = BinaryTreeTraversal(a4, backend=backend)
    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [1, 0, 5, 3, 6, 2, 4]
    assert [node.key for node in pre_order] == [3,0,1,5,2,6,4]

    a5 = AVLTree(is_order_statistic=True,backend=backend)
    if backend==Backend.PYTHON:
        a5.set_tree( ArrayForTrees(TreeNode, [
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
    ]) )
    else:
        a5.set_tree( ArrayForTrees(_nodes.TreeNode, [
            TreeNode(10, 10,backend=backend),
            TreeNode(5, 5,backend=backend),
            TreeNode(17, 17,backend=backend),
            TreeNode(2, 2,backend=backend),
            TreeNode(9, 9,backend=backend),
            TreeNode(12, 12,backend=backend),
            TreeNode(20, 20,backend=backend),
            TreeNode(3, 3,backend=backend),
            TreeNode(11, 11,backend=backend),
            TreeNode(15, 15,backend=backend),
            TreeNode(18, 18,backend=backend),
            TreeNode(30, 30,backend=backend),
            TreeNode(13, 13,backend=backend),
            TreeNode(33, 33,backend=backend)
        ],backend=backend) )

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
    assert str(a5) == "[(1, 10, 10, 2), (3, 5, 5, 4), (5, 17, 17, 6), (None, 2, 2, 7), (None, 9, 9, None), (8, 12, 12, 9), (10, 20, 20, 11), (None, 3, 3, None), (None, 11, 11, None), (12, 15, 15, None), (None, 18, 18, None), (None, 30, 30, 13), (None, 13, 13, None), (None, 33, 33, None)]"

    assert raises(ValueError, lambda: a5.select(0))
    assert raises(ValueError, lambda: a5.select(15))

    assert a5.rank(-1) is None
    def test_select_rank(expected_output):
        if backend==Backend.PYTHON:
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
    assert str(a5) == "[(7, 10, 10, 5), (None, 5, 5, None), (0, 17, 17, 6), (None, 2, 2, None), '', (8, 12, 12, 9), (10, 30, 30, 13), (3, 3, 3, 1), (None, 11, 11, None), (None, 15, 15, None), (None, 18, 18, None), '', '', (None, 33, 33, None)]"

    trav = BinaryTreeTraversal(a5, backend=backend)
    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [2, 3, 5, 10, 11, 12, 15, 17, 18, 30, 33]
    assert [node.key for node in pre_order] == [17, 10, 3, 2, 5, 12, 11, 15, 30, 18, 33]

    test_select_rank([2, 3, 5, 10, 11, 12, 15, 17, 18, 30, 33])
    a5.delete(10)
    a5.delete(17)
    assert str(a5) == "[(7, 11, 11, 5), (None, 5, 5, None), (0, 18, 18, 6), (None, 2, 2, None), '', (None, 12, 12, 9), (None, 30, 30, 13), (3, 3, 3, 1), '', (None, 15, 15, None), '', '', '', (None, 33, 33, None)]"
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
    assert str(a5) == "[(None, None, None, None)]"

def test_AVLTree():
    _test_AVLTree(backend=Backend.PYTHON)
def test_cpp_AVLTree():
    _test_AVLTree(backend=Backend.CPP)

def _test_BinaryIndexedTree(backend):

    FT = BinaryIndexedTree

    t = FT([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], backend=backend)

    assert t.get_sum(0, 2) == 6
    assert t.get_sum(0, 4) == 15
    assert t.get_sum(0, 9) == 55
    t.update(0, 100)
    assert t.get_sum(0, 2) == 105
    assert t.get_sum(0, 4) == 114
    assert t.get_sum(1, 9) == 54

def test_BinaryIndexedTree():
    _test_BinaryIndexedTree(Backend.PYTHON)

def test_cpp_BinaryIndexedTree():
    _test_BinaryIndexedTree(Backend.CPP)

def _test_CartesianTree(backend):
    tree = CartesianTree(backend=backend)
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
    # Explicit check for the redefined __str__ method of Cartesian Trees Class

    trav = BinaryTreeTraversal(tree, backend=backend)
    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert [node.key for node in pre_order] == [3, 1, 0, 2, 5, 4, 9, 7, 6, 8]

    tree.insert(1.5, 4, 1.5)

    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [0, 1, 1.5, 2, 3, 4, 5, 6, 7, 8, 9]
    assert [node.key for node in pre_order] == [3, 1.5, 1, 0, 2, 5, 4, 9, 7, 6, 8]

    k = tree.search(1.5)
    assert tree.tree[tree.tree[k].parent].key == 3
    tree.delete(1.5)
    assert tree.root_idx == 0
    tree.tree[tree.tree[tree.root_idx].left].key == 1
    tree.delete(8)
    assert tree.search(8) is None
    tree.delete(7)
    assert tree.search(7) is None
    tree.delete(3)
    assert tree.search(3) is None
    assert tree.delete(18) is None

def test_CartesianTree():
    _test_CartesianTree(backend=Backend.PYTHON)

def test_cpp_CartesianTree():
    _test_CartesianTree(backend=Backend.CPP)

def _test_Treap(backend):

    random.seed(0)
    tree = Treap(backend=backend)
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

def test_Treap():
    _test_Treap(Backend.PYTHON)

def test_cpp_Treap():
    _test_Treap(Backend.CPP)

def _test_SelfBalancingBinaryTree(backend):
    """
    https://github.com/codezonediitj/pydatastructs/issues/234
    """
    tree = SelfBalancingBinaryTree(backend=backend)
    tree.insert(5, 5)
    tree.insert(5.5, 5.5)
    tree.insert(4.5, 4.5)
    tree.insert(4.6, 4.6)
    tree.insert(4.4, 4.4)
    tree.insert(4.55, 4.55)
    tree.insert(4.65, 4.65)
    original_tree = str(tree)
    tree._right_rotate(3, 5)

    assert str(tree) == "[(2, 5, 5, 1), (None, 5.5, 5.5, None), (4, 4.5, 4.5, 5), (None, 4.6, 4.6, 6), (None, 4.4, 4.4, None), (None, 4.55, 4.55, 3), (None, 4.65, 4.65, None)]"
    assert tree.tree[3].parent == 5
    assert tree.tree[2].right != 3
    assert tree.tree[tree.tree[5].parent].right == 5
    assert tree.root_idx == 0

    trav = BinaryTreeTraversal(tree, backend=backend)
    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [4.4, 4.5, 4.55, 4.6, 4.65, 5, 5.5]
    assert [node.key for node in pre_order] == [5, 4.5, 4.4, 4.55, 4.6, 4.65, 5.5]

    assert tree.tree[tree.tree[3].parent].right == 3
    tree._left_rotate(5, 3)
    assert str(tree) == original_tree
    tree.insert(4.54, 4.54)
    tree.insert(4.56, 4.56)
    tree._left_rotate(5, 8)
    assert tree.tree[tree.tree[8].parent].left == 8
    assert str(tree) == "[(2, 5, 5, 1), (None, 5.5, 5.5, None), (4, 4.5, 4.5, 3), (8, 4.6, 4.6, 6), (None, 4.4, 4.4, None), (7, 4.55, 4.55, None), (None, 4.65, 4.65, None), (None, 4.54, 4.54, None), (5, 4.56, 4.56, None)]"

    tree._left_right_rotate(0, 2)
    assert str(tree) == "[(6, 5, 5, 1), (None, 5.5, 5.5, None), (4, 4.5, 4.5, 8), (2, 4.6, 4.6, 0), (None, 4.4, 4.4, None), (7, 4.55, 4.55, None), (None, 4.65, 4.65, None), (None, 4.54, 4.54, None), (5, 4.56, 4.56, None)]"

    tree._right_left_rotate(0, 2)
    assert str(tree) == "[(6, 5, 5, None), (None, 5.5, 5.5, None), (None, 4.5, 4.5, 8), (2, 4.6, 4.6, 4), (0, 4.4, 4.4, 2), (7, 4.55, 4.55, None), (None, 4.65, 4.65, None), (None, 4.54, 4.54, None), (5, 4.56, 4.56, None)]"

def test_SelfBalancingBinaryTree():
    _test_SelfBalancingBinaryTree(Backend.PYTHON)
def test_cpp_SelfBalancingBinaryTree():
    _test_SelfBalancingBinaryTree(Backend.CPP)

def _test_SplayTree(backend):
    t = SplayTree(100, 100, backend=backend)
    t.insert(50, 50)
    t.insert(200, 200)
    t.insert(40, 40)
    t.insert(30, 30)
    t.insert(20, 20)
    t.insert(55, 55)
    assert str(t) == "[(None, 100, 100, None), (None, 50, 50, None), (0, 200, 200, None), (None, 40, 40, 1), (5, 30, 30, 3), (None, 20, 20, None), (4, 55, 55, 2)]"
    assert t.root_idx == 6

    trav = BinaryTreeTraversal(t, backend=backend)
    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [20, 30, 40, 50, 55, 100, 200]
    assert [node.key for node in pre_order] == [55, 30, 20, 40, 50, 200, 100]

    t.delete(40)

    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [20, 30, 50, 55, 100, 200]
    assert [node.key for node in pre_order] == [50, 30, 20, 55, 200, 100]

    t.delete(150)

    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [20, 30, 50, 55, 100, 200]
    assert [node.key for node in pre_order] == [50, 30, 20, 55, 200, 100]

    t1 = SplayTree(1000, 1000, backend=backend)
    t1.insert(2000, 2000)

    trav2 = BinaryTreeTraversal(t1, backend=backend)
    in_order = trav2.depth_first_search(order='in_order')
    pre_order = trav2.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [1000, 2000]
    assert [node.key for node in pre_order] == [2000, 1000]

    t.join(t1)
    assert str(t) == "[(None, 100, 100, None), '', (6, 200, 200, 8), (4, 50, 50, None), (5, 30, 30, None), (None, 20, 20, None), (3, 55, 55, 0), (None, 1000, 1000, None), (7, 2000, 2000, None), '']"

    if backend == Backend.PYTHON:
        trav3 = BinaryTreeTraversal(t, backend=backend)
        in_order = trav3.depth_first_search(order='in_order')
        pre_order = trav3.depth_first_search(order='pre_order')
        assert [node.key for node in in_order] == [20, 30, 50, 55, 100, 200, 1000, 2000]
        assert [node.key for node in pre_order] == [200, 55, 50, 30, 20, 100, 2000, 1000]

    s = t.split(200)
    assert str(s) == "[(1, 2000, 2000, None), (None, 1000, 1000, None)]"

    trav4 = BinaryTreeTraversal(s, backend=backend)
    in_order = trav4.depth_first_search(order='in_order')
    pre_order = trav4.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [1000, 2000]
    assert [node.key for node in pre_order] == [2000, 1000]

    if backend == Backend.PYTHON:
        trav5 = BinaryTreeTraversal(t, backend=backend)
        in_order = trav5.depth_first_search(order='in_order')
        pre_order = trav5.depth_first_search(order='pre_order')
        assert [node.key for node in in_order] == [20, 30, 50, 55, 100, 200]
        assert [node.key for node in pre_order] == [200, 55, 50, 30, 20, 100]

def test_SplayTree():
    _test_SplayTree(Backend.PYTHON)

def test_cpp_SplayTree():
    _test_SplayTree(Backend.CPP)

def _test_RedBlackTree(backend):
    tree = RedBlackTree(backend=backend)
    tree.insert(10, 10)
    tree.insert(18, 18)
    tree.insert(7, 7)
    tree.insert(15, 15)
    tree.insert(16, 16)
    tree.insert(30, 30)
    tree.insert(25, 25)
    tree.insert(40, 40)
    tree.insert(60, 60)
    tree.insert(2, 2)
    tree.insert(17, 17)
    tree.insert(6, 6)
    assert str(tree) == "[(11, 10, 10, 3), (10, 18, 18, None), (None, 7, 7, None), (None, 15, 15, None), (0, 16, 16, 6), (None, 30, 30, None), (1, 25, 25, 7), (5, 40, 40, 8), (None, 60, 60, None), (None, 2, 2, None), (None, 17, 17, None), (9, 6, 6, 2)]"
    assert tree.root_idx == 4

    trav = BinaryTreeTraversal(tree, backend=backend)
    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [2, 6, 7, 10, 15, 16, 17, 18, 25, 30, 40, 60]
    assert [node.key for node in pre_order] == [16, 10, 6, 2, 7, 15, 25, 18, 17, 40, 30, 60]

    assert tree.lower_bound(0) == 2
    assert tree.lower_bound(2) == 2
    assert tree.lower_bound(3) == 6
    assert tree.lower_bound(7) == 7
    assert tree.lower_bound(25) == 25
    assert tree.lower_bound(32) == 40
    assert tree.lower_bound(41) == 60
    assert tree.lower_bound(60) == 60
    assert tree.lower_bound(61) is None

    assert tree.upper_bound(0) == 2
    assert tree.upper_bound(2) == 6
    assert tree.upper_bound(3) == 6
    assert tree.upper_bound(7) == 10
    assert tree.upper_bound(25) == 30
    assert tree.upper_bound(32) == 40
    assert tree.upper_bound(41) == 60
    assert tree.upper_bound(60) is None
    assert tree.upper_bound(61) is None

    tree = RedBlackTree(backend=backend)

    assert tree.lower_bound(1) is None
    assert tree.upper_bound(0) is None

    tree.insert(10)
    tree.insert(20)
    tree.insert(30)
    tree.insert(40)
    tree.insert(50)
    tree.insert(60)
    tree.insert(70)
    tree.insert(80)
    tree.insert(90)
    tree.insert(100)
    tree.insert(110)
    tree.insert(120)
    tree.insert(130)
    tree.insert(140)
    tree.insert(150)
    tree.insert(160)
    tree.insert(170)
    tree.insert(180)
    assert str(tree) == "[(None, 10, None, None), (0, 20, None, 2), (None, 30, None, None), (1, 40, None, 5), (None, 50, None, None), (4, 60, None, 6), (None, 70, None, None), (3, 80, None, 11), (None, 90, None, None), (8, 100, None, 10), (None, 110, None, None), (9, 120, None, 13), (None, 130, None, None), (12, 140, None, 15), (None, 150, None, None), (14, 160, None, 16), (None, 170, None, 17), (None, 180, None, None)]"

    assert tree._get_sibling(7) is None

    trav = BinaryTreeTraversal(tree, backend=backend)
    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [10, 20, 30, 40, 50, 60, 70, 80, 90,
                                               100, 110, 120, 130, 140, 150, 160, 170, 180]
    assert [node.key for node in pre_order] == [80, 40, 20, 10, 30, 60, 50, 70, 120, 100,
                                                90, 110, 140, 130, 160, 150, 170, 180]

    tree.delete(180)
    tree.delete(130)
    tree.delete(110)
    tree.delete(190)
    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
                                               120, 140, 150, 160, 170]
    assert [node.key for node in pre_order] == [80, 40, 20, 10, 30, 60, 50, 70, 120, 100,
                                                90, 160, 140, 150, 170]

    tree.delete(170)
    tree.delete(100)
    tree.delete(60)
    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [10, 20, 30, 40, 50, 70, 80, 90, 120, 140, 150, 160]
    assert [node.key for node in pre_order] == [80, 40, 20, 10, 30, 50, 70, 120, 90, 150, 140, 160]

    tree.delete(70)
    tree.delete(140)

    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [10, 20, 30, 40, 50, 80, 90, 120, 150, 160]
    assert [node.key for node in pre_order] == [80, 40, 20, 10, 30, 50, 120, 90, 150, 160]

    tree.delete(150)
    tree.delete(120)
    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [10, 20, 30, 40, 50, 80, 90, 160]
    assert [node.key for node in pre_order] == [40, 20, 10, 30, 80, 50, 90, 160]

    tree.delete(50)
    tree.delete(80)
    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [10, 20, 30, 40, 90, 160]
    assert [node.key for node in pre_order] == [40, 20, 10, 30, 90, 160]

    tree.delete(30)
    tree.delete(20)
    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [10, 40, 90, 160]
    assert [node.key for node in pre_order] == [40, 10, 90, 160]

    tree.delete(10)
    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [40, 90, 160]
    assert [node.key for node in pre_order] == [90, 40, 160]

    tree.delete(40)
    tree.delete(90)
    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [160]
    assert [node.key for node in pre_order] == [160]

    tree.delete(160)
    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order if node.key is not None] == []
    assert [node.key for node in pre_order if node.key is not None] == []

    tree = RedBlackTree(backend=backend)
    tree.insert(50)
    tree.insert(40)
    tree.insert(30)
    tree.insert(20)
    tree.insert(10)
    tree.insert(5)

    trav = BinaryTreeTraversal(tree, backend=backend)
    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [5, 10, 20, 30, 40, 50]
    assert [node.key for node in pre_order] == [40, 20, 10, 5, 30, 50]

    assert tree.search(50) == 0
    assert tree.search(20) == 3
    assert tree.search(30) == 2
    tree.delete(50)
    tree.delete(20)
    tree.delete(30)
    assert tree.search(50) is None
    assert tree.search(20) is None
    assert tree.search(30) is None

    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [5, 10, 40]
    assert [node.key for node in pre_order] == [10, 5, 40]

    tree = RedBlackTree(backend=backend)
    tree.insert(10)
    tree.insert(5)
    tree.insert(20)
    tree.insert(15)

    trav = BinaryTreeTraversal(tree, backend=backend)
    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [5, 10, 15, 20]
    assert [node.key for node in pre_order] == [10, 5, 20, 15]

    tree.delete(5)

    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [10, 15, 20]
    assert [node.key for node in pre_order] == [15, 10, 20]

    tree = RedBlackTree(backend=backend)
    tree.insert(10)
    tree.insert(5)
    tree.insert(20)
    tree.insert(15)
    tree.insert(2)
    tree.insert(6)

    trav = BinaryTreeTraversal(tree,backend=backend)
    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [2, 5, 6, 10, 15, 20]
    assert [node.key for node in pre_order] == [10, 5, 2, 6, 20, 15]

    tree.delete(10)

    in_order = trav.depth_first_search(order='in_order')
    pre_order = trav.depth_first_search(order='pre_order')
    assert [node.key for node in in_order] == [2, 5, 6, 15, 20]
    assert [node.key for node in pre_order] == [6, 5, 2, 20, 15]

def test_RedBlackTree():
    _test_RedBlackTree(Backend.PYTHON)

def test_cpp_RedBlackTree():
    _test_RedBlackTree(Backend.CPP)
