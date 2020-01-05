from pydatastructs.utils import AdjacencyListGraphNode, AdjacencyMatrixGraphNode, GraphEdge
from pydatastructs.utils.raises_util import raises

def test_AdjacencyListGraphNode():
    g_1 = AdjacencyListGraphNode('g_1', 1)
    g_2 = AdjacencyListGraphNode('g_2', 2)
    g = AdjacencyListGraphNode('g', 0, adjacency_list=[g_1, g_2])
    g.add_adjacent_node('g_3', 3)
    assert g.g_1.name is 'g_1'
    assert g.g_2.name is 'g_2'
    assert g.g_3.name is 'g_3'
    g.remove_adjacent_node('g_3')
    assert hasattr(g, 'g_3') is False
    assert raises(ValueError, lambda: g.remove_adjacent_node('g_3'))
    g.add_adjacent_node('g_1', 4)
    assert g.g_1.data is 4
    assert str(g) == "('g', 0)"

def test_AdjacencyMatrixGraphNode():
    g = AdjacencyMatrixGraphNode('g', 3)
    assert str(g) == "('g', 3)"

def test_GraphEdge():
    g_1 = AdjacencyListGraphNode('g_1', 1)
    g_2 = AdjacencyListGraphNode('g_2', 2)
    e = GraphEdge(g_1, g_2, value=2)
    assert str(e) == "('g_1', 'g_2')"
