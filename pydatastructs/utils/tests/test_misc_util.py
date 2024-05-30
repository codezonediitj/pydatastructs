from pydatastructs.utils import (TreeNode, AdjacencyListGraphNode, AdjacencyMatrixGraphNode,
                                GraphEdge, BinomialTreeNode, MAryTreeNode, CartesianTreeNode, RedBlackTreeNode, SkipNode)
from pydatastructs.utils.raises_util import raises
from pydatastructs.utils.misc_util import Backend

def test_cpp_TreeNode():
    n = TreeNode(1,100,backend=Backend.CPP)
    assert str(n) == "(None, 1, 100, None)"

def test_AdjacencyListGraphNode():
    g_1 = AdjacencyListGraphNode('g_1', 1)
    g_2 = AdjacencyListGraphNode('g_2', 2)
    g = AdjacencyListGraphNode('g', 0, adjacency_list=[g_1, g_2])
    g.add_adjacent_node('g_3', 3)
    assert g.g_1.name == 'g_1'
    assert g.g_2.name == 'g_2'
    assert g.g_3.name == 'g_3'
    g.remove_adjacent_node('g_3')
    assert hasattr(g, 'g_3') is False
    assert raises(ValueError, lambda: g.remove_adjacent_node('g_3'))
    g.add_adjacent_node('g_1', 4)
    assert g.g_1.data == 4
    assert str(g) == "('g', 0)"

def test_AdjacencyMatrixGraphNode():
    g = AdjacencyMatrixGraphNode("1", 3)
    assert str(g) == "('1', 3)"

def test_GraphEdge():
    g_1 = AdjacencyListGraphNode('g_1', 1)
    g_2 = AdjacencyListGraphNode('g_2', 2)
    e = GraphEdge(g_1, g_2, value=2)
    assert str(e) == "('g_1', 'g_2')"

def test_BinomialTreeNode():
    b = BinomialTreeNode(1,1)
    b.add_children(*[BinomialTreeNode(i,i) for i in range(2,10)])
    assert str(b) == '(1, 1)'
    assert str(b.children) == "['(2, 2)', '(3, 3)', '(4, 4)', '(5, 5)', '(6, 6)', '(7, 7)', '(8, 8)', '(9, 9)']"

def test_MAryTreeNode():
    m = MAryTreeNode(1, 1)
    m.add_children(*list(range(2, 10)))
    assert str(m) == "(1, 1)"
    assert str(m.children) == "['2', '3', '4', '5', '6', '7', '8', '9']"

def test_CartesianTreeNode():
    c = CartesianTreeNode(1, 1, 1)
    assert str(c) == "(None, 1, 1, 1, None)"

def test_RedBlackTreeNode():
    c = RedBlackTreeNode(1, 1)
    assert str(c) == "(None, 1, 1, None)"

def test_SkipNode():
    c = SkipNode(1)
    assert str(c) == '(1, None)'
