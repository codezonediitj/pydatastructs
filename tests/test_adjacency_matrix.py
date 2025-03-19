from pydatastructs.graphs import Graph
from pydatastructs.utils import AdjacencyMatrixGraphNode
from pydatastructs.utils.raises_util import raises

def test_AdjacencyMatrix():
    v_0 = AdjacencyMatrixGraphNode(0, 0)
    v_1 = AdjacencyMatrixGraphNode(1, 1)
    v_2 = AdjacencyMatrixGraphNode(2, 2)
    g = Graph(v_0, v_1, v_2)
    g.add_edge(0, 1, 0)
    g.add_edge(1, 2, 0)
    g.add_edge(2, 0, 0)
    e1 = g.get_edge(0, 1)
    e2 = g.get_edge(1, 2)
    e3 = g.get_edge(2, 0)
    assert (e1.source.name, e1.target.name) == ('0', '1')
    assert (e2.source.name, e2.target.name) == ('1', '2')
    assert (e3.source.name, e3.target.name) == ('2', '0')
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
    assert raises(ValueError, lambda: g.add_edge('u', 'v'))
    assert raises(ValueError, lambda: g.add_edge('v', 'x'))
    assert raises(ValueError, lambda: g.add_edge(2, 3))
    assert raises(ValueError, lambda: g.add_edge(3, 2))
