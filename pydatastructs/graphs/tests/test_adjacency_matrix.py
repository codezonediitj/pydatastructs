from pydatastructs.graphs import Graph
from pydatastructs.utils import AdjacencyMatrixGraphNode

def test_AdjacencyMatrix():
    v_0 = AdjacencyMatrixGraphNode(0, 0)
    v_1 = AdjacencyMatrixGraphNode(1, 1)
    v_2 = AdjacencyMatrixGraphNode(2, 2)
    g = Graph(v_0, v_1, v_2, implementation='adjacency_matrix')
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    assert g.is_adjacent(0, 1) is True
    assert g.is_adjacent(1, 2) is True
    assert g.is_adjacent(2, 0) is True
    assert g.is_adjacent(1, 0) is False
    assert g.is_adjacent(2, 1) is False
    assert g.is_adjacent(0, 2) is False
    neighbors = g.neighbors(0)
    assert neighbors == [v_1]
    g.remove_edge(0, 1)
    assert g.is_adjacent(0, 1) is False
