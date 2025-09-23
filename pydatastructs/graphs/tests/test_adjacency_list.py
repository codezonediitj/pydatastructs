from pydatastructs.graphs import Graph
from pydatastructs.utils import AdjacencyListGraphNode
from pydatastructs.utils.raises_util import raises
from pydatastructs.utils.misc_util import Backend

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
    g.add_edge('v_1', 'v', 0)
    g.add_edge('v_2', 'v', 0)
    g.add_edge('v_3', 'v', 0)
    assert g.is_adjacent('v_1', 'v') is True
    assert g.is_adjacent('v_2', 'v') is True
    assert g.is_adjacent('v_3', 'v') is True
    e1 = g.get_edge('v_1', 'v')
    e2 = g.get_edge('v_2', 'v')
    e3 = g.get_edge('v_3', 'v')
    assert (e1.source.name, e1.target.name) == ('v_1', 'v')
    assert (e2.source.name, e2.target.name) == ('v_2', 'v')
    assert (e3.source.name, e3.target.name) == ('v_3', 'v')
    g.remove_edge('v_1', 'v')
    assert g.is_adjacent('v_1', 'v') is False
    g.remove_vertex('v')
    assert g.is_adjacent('v_2', 'v') is False
    assert g.is_adjacent('v_3', 'v') is False

    assert raises(ValueError, lambda: g.add_edge('u', 'v'))
    assert raises(ValueError, lambda: g.add_edge('v', 'x'))

    v_4 = AdjacencyListGraphNode('v_4', 4, backend = Backend.CPP)
    v_5 = AdjacencyListGraphNode('v_5', 5, backend = Backend.CPP)
    g2 = Graph(v_4,v_5,implementation = 'adjacency_list', backend = Backend.CPP)
    v_6 = AdjacencyListGraphNode('v_6', 6, backend = Backend.CPP)
    assert raises(ValueError, lambda: g2.add_vertex(v_5))
    g2.add_vertex(v_6)
    g2.add_edge('v_4', 'v_5')
    g2.add_edge('v_5', 'v_6')
    g2.add_edge('v_4', 'v_6')
    assert g2.is_adjacent('v_4', 'v_5') is True
    assert g2.is_adjacent('v_5', 'v_6') is True
    assert g2.is_adjacent('v_4', 'v_6') is True
    assert g2.is_adjacent('v_5', 'v_4') is False
    assert g2.is_adjacent('v_6', 'v_5') is False
    assert g2.is_adjacent('v_6', 'v_4') is False
    assert g2.num_edges() == 3
    assert g2.num_vertices() == 3
    neighbors = g2.neighbors('v_4')
    assert neighbors == [v_6, v_5]
    v = AdjacencyListGraphNode('v', 4, backend = Backend.CPP)
    g2.add_vertex(v)
    g2.add_edge('v_4', 'v', 0)
    g2.add_edge('v_5', 'v', 0)
    g2.add_edge('v_6', 'v', "h")
    assert g2.is_adjacent('v_4', 'v') is True
    assert g2.is_adjacent('v_5', 'v') is True
    assert g2.is_adjacent('v_6', 'v') is True
    e1 = g2.get_edge('v_4', 'v')
    e2 = g2.get_edge('v_5', 'v')
    e3 = g2.get_edge('v_6', 'v')
    assert (str(e1)) == "('v_4', 'v', 0)"
    assert (str(e2)) == "('v_5', 'v', 0)"
    assert (str(e3)) == "('v_6', 'v', h)"
    g2.remove_edge('v_4', 'v')
    assert g2.is_adjacent('v_4', 'v') is False
    g2.remove_vertex('v')
    assert raises(ValueError, lambda: g2.add_edge('v_4', 'v'))

    g3 = Graph('a','b',implementation = 'adjacency_list', backend = Backend.LLVM)
    g3.add_edge('a', 'b',10)
    assert g3.is_adjacent('a','b') is True
    g3.add_vertex('c')
    g3.add_edge('a','c')
    assert g3.is_adjacent('a','c') is True
    assert g3.is_adjacent('b','c') is False
    g3.remove_edge('a','b')
    assert g3.is_adjacent('a','b') is False
    g3.remove_vertex('a')
    assert g3.is_adjacent('a','c') is False
