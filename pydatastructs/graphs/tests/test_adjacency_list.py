from pydatastructs.graphs import Graph
from pydatastructs.utils import AdjacencyListGraphNode
from pydatastructs.utils.raises_util import raises

def test_adjacency_list():
    v_1 = AdjacencyListGraphNode('v_1', 1)
    v_2 = AdjacencyListGraphNode('v_2', 2)
    g = Graph(v_1, v_2, implementation='adjacency_list')
    v_3 = AdjacencyListGraphNode('v_3', 3)
    g.add_vertex(v_2)
    g.add_vertex(v_3)
    g.add_edge('v_1', 'v_2')
    g.add_edge('v_2', 'v_3')
    g.add_edge('v_3', 'v_1')
    assert g.is_adjacent('v_1', 'v_2') is True
    assert g.is_adjacent('v_2', 'v_3') is True
    assert g.is_adjacent('v_3', 'v_1') is True
    assert g.is_adjacent('v_2', 'v_1') is False
    assert g.is_adjacent('v_3', 'v_2') is False
    assert g.is_adjacent('v_1', 'v_3') is False
    neighbors = g.neighbors('v_1')
    assert neighbors == [v_2]
    v = AdjacencyListGraphNode('v', 4)
    g.add_vertex(v)
    g.add_edge('v_1', 'v')
    g.add_edge('v_2', 'v')
    g.add_edge('v_3', 'v')
    assert g.is_adjacent('v_1', 'v') is True
    assert g.is_adjacent('v_2', 'v') is True
    assert g.is_adjacent('v_3', 'v') is True
    g.remove_edge('v_1', 'v')
    assert g.is_adjacent('v_1', 'v') is False
    g.remove_vertex('v')
    assert g.is_adjacent('v_2', 'v') is False
    assert g.is_adjacent('v_3', 'v') is False
    assert raises(NotImplementedError, lambda: Graph(implementation=''))
