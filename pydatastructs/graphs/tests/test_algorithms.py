from pydatastructs import (breadth_first_search, Graph,
breadth_first_search_parallel, minimum_spanning_tree,
minimum_spanning_tree_parallel, strongly_connected_components,
depth_first_search, shortest_paths,all_pair_shortest_paths, topological_sort,
topological_sort_parallel, max_flow, find_bridges)
from pydatastructs.utils.raises_util import raises
from pydatastructs.utils.misc_util import AdjacencyListGraphNode, AdjacencyMatrixGraphNode
from pydatastructs.graphs._backend.cpp import _graph
from pydatastructs.graphs._backend.cpp import _algorithms
from pydatastructs.utils.misc_util import Backend

def test_breadth_first_search():

    def _test_breadth_first_search(ds):
        import pydatastructs.utils.misc_util as utils
        GraphNode = getattr(utils, "Adjacency" + ds + "GraphNode")

        V1 = GraphNode(0)
        V2 = GraphNode(1)
        V3 = GraphNode(2)

        G1 = Graph(V1, V2, V3)

        assert G1.num_vertices() == 3

        edges = [
            (V1.name, V2.name),
            (V2.name, V3.name),
            (V1.name, V3.name)
        ]

        for edge in edges:
            G1.add_edge(*edge)

        assert G1.num_edges() == len(edges)

        parent = {}
        def bfs_tree(curr_node, next_node, parent):
            if next_node != "":
                parent[next_node] = curr_node
            return True

        breadth_first_search(G1, V1.name, bfs_tree, parent)
        assert (parent[V3.name] == V1.name and parent[V2.name] == V1.name) or \
            (parent[V3.name] == V2.name and parent[V2.name] == V1.name)

        if (ds=='List'):
            parent2 = {}
            V9 = AdjacencyListGraphNode("9",0,backend = Backend.CPP)
            V10 = AdjacencyListGraphNode("10",0,backend = Backend.CPP)
            V11 = AdjacencyListGraphNode("11",0,backend = Backend.CPP)
            G2 = Graph(V9, V10, V11,implementation = 'adjacency_list', backend = Backend.CPP)
            assert G2.num_vertices()==3
            G2.add_edge("9", "10")
            G2.add_edge("10", "11")
            breadth_first_search(G2, "9", bfs_tree, parent2, backend = Backend.CPP)
            assert parent2[V10] == V9
            assert parent2[V11] == V10

        if (ds == 'Matrix'):
            parent3 = {}
            V12 = AdjacencyMatrixGraphNode("12", 0, backend = Backend.CPP)
            V13 = AdjacencyMatrixGraphNode("13", 0, backend = Backend.CPP)
            V14 = AdjacencyMatrixGraphNode("14", 0, backend = Backend.CPP)
            G3 = Graph(V12, V13, V14, implementation = 'adjacency_matrix', backend = Backend.CPP)
            assert G3.num_vertices() == 3
            G3.add_edge("12", "13")
            G3.add_edge("13", "14")
            breadth_first_search(G3, "12", bfs_tree, parent3, backend = Backend.CPP)
            assert parent3[V13] == V12
            assert parent3[V14] == V13

        V4 = GraphNode(0)
        V5 = GraphNode(1)
        V6 = GraphNode(2)
        V7 = GraphNode(3)
        V8 = GraphNode(4)

        edges = [
            (V4.name, V5.name),
            (V5.name, V6.name),
            (V6.name, V7.name),
            (V6.name, V4.name),
            (V7.name, V8.name)
        ]

        G2 = Graph(V4, V5, V6, V7, V8)

        for edge in edges:
            G2.add_edge(*edge)

        assert G2.num_edges() == len(edges)

        path = []
        def path_finder(curr_node, next_node, dest_node, parent, path):
            if next_node != "":
                parent[next_node] = curr_node
            if curr_node == dest_node:
                node = curr_node
                path.append(node)
                while node is not None:
                    if parent.get(node, None) is not None:
                        path.append(parent[node])
                    node = parent.get(node, None)
                path.reverse()
                return False
            return True

        parent.clear()
        breadth_first_search(G2, V4.name, path_finder, V7.name, parent, path)
        assert path == [V4.name, V5.name, V6.name, V7.name]

    _test_breadth_first_search("List")
    _test_breadth_first_search("Matrix")

def test_breadth_first_search_parallel():

    def _test_breadth_first_search_parallel(ds):
        import pydatastructs.utils.misc_util as utils
        GraphNode = getattr(utils, "Adjacency" + ds + "GraphNode")

        V1 = GraphNode(0)
        V2 = GraphNode(1)
        V3 = GraphNode(2)
        V4 = GraphNode(3)
        V5 = GraphNode(4)
        V6 = GraphNode(5)
        V7 = GraphNode(6)
        V8 = GraphNode(7)


        G1 = Graph(V1, V2, V3, V4, V5, V6, V7, V8)

        edges = [
            (V1.name, V2.name),
            (V1.name, V3.name),
            (V1.name, V4.name),
            (V2.name, V5.name),
            (V2.name, V6.name),
            (V3.name, V6.name),
            (V3.name, V7.name),
            (V4.name, V7.name),
            (V4.name, V8.name)
        ]

        for edge in edges:
            G1.add_edge(*edge)

        parent = {}
        def bfs_tree(curr_node, next_node, parent):
            if next_node != "":
                parent[next_node] = curr_node
            return True

        breadth_first_search_parallel(G1, V1.name, 5, bfs_tree, parent)
        assert (parent[V2.name] == V1.name and parent[V3.name] == V1.name and
                parent[V4.name] == V1.name and parent[V5.name] == V2.name and
                (parent[V6.name] in (V2.name, V3.name)) and
                (parent[V7.name] in (V3.name, V4.name)) and (parent[V8.name] == V4.name))

    _test_breadth_first_search_parallel("List")
    _test_breadth_first_search_parallel("Matrix")

def test_minimum_spanning_tree():

    def _test_minimum_spanning_tree(func, ds, algorithm, *args):
        import pydatastructs.utils.misc_util as utils
        GraphNode = getattr(utils, "Adjacency" + ds + "GraphNode")
        a, b, c, d, e = [GraphNode(x) for x in [0, 1, 2, 3, 4]]
        graph = Graph(a, b, c, d, e)
        graph.add_edge(a.name, c.name, 10)
        graph.add_edge(c.name, a.name, 10)
        graph.add_edge(a.name, d.name, 7)
        graph.add_edge(d.name, a.name, 7)
        graph.add_edge(c.name, d.name, 9)
        graph.add_edge(d.name, c.name, 9)
        graph.add_edge(d.name, b.name, 32)
        graph.add_edge(b.name, d.name, 32)
        graph.add_edge(d.name, e.name, 23)
        graph.add_edge(e.name, d.name, 23)
        mst = func(graph, algorithm, *args)
        expected_mst = [('0_3', 7), ('2_3', 9), ('3_4', 23), ('3_1', 32),
                        ('3_0', 7), ('3_2', 9), ('4_3', 23), ('1_3', 32)]
        assert len(expected_mst) == len(mst.edge_weights.items())
        for k, v in mst.edge_weights.items():
            assert (k, v.value) in expected_mst

    def _test_minimum_spanning_tree_cpp(ds, algorithm, *args):
        if (ds == 'List' and algorithm == "prim"):
            a1 = AdjacencyListGraphNode('a', 0, backend = Backend.CPP)
            b1 = AdjacencyListGraphNode('b', 0, backend = Backend.CPP)
            c1 = AdjacencyListGraphNode('c', 0, backend = Backend.CPP)
            d1 = AdjacencyListGraphNode('d', 0, backend = Backend.CPP)
            e1 = AdjacencyListGraphNode('e', 0, backend = Backend.CPP)
            g = Graph(a1, b1, c1, d1, e1, backend = Backend.CPP)
            g.add_edge(a1.name, c1.name, 10)
            g.add_edge(c1.name, a1.name, 10)
            g.add_edge(a1.name, d1.name, 7)
            g.add_edge(d1.name, a1.name, 7)
            g.add_edge(c1.name, d1.name, 9)
            g.add_edge(d1.name, c1.name, 9)
            g.add_edge(d1.name, b1.name, 32)
            g.add_edge(b1.name, d1.name, 32)
            g.add_edge(d1.name, e1.name, 23)
            g.add_edge(e1.name, d1.name, 23)
            mst = minimum_spanning_tree(g, "prim", backend = Backend.CPP)
            expected_mst = ["('a', 'd', 7)", "('d', 'c', 9)", "('e', 'd', 23)", "('b', 'd', 32)",
                        "('d', 'a', 7)", "('c', 'd', 9)", "('d', 'e', 23)", "('d', 'b', 32)"]
            assert str(mst.get_edge('a', 'd')) in expected_mst
            assert str(mst.get_edge('e', 'd')) in expected_mst
            assert str(mst.get_edge('d', 'c')) in expected_mst
            assert str(mst.get_edge('b', 'd')) in expected_mst
            assert mst.num_edges() == 8
            a=AdjacencyListGraphNode('0', 0, backend = Backend.CPP)
            b=AdjacencyListGraphNode('1', 0, backend = Backend.CPP)
            c=AdjacencyListGraphNode('2', 0, backend = Backend.CPP)
            d=AdjacencyListGraphNode('3', 0, backend = Backend.CPP)
            g2 = Graph(a,b,c,d,backend = Backend.CPP)
            g2.add_edge('0', '1', 74)
            g2.add_edge('1', '0', 74)
            g2.add_edge('0', '3', 55)
            g2.add_edge('3', '0', 55)
            g2.add_edge('1', '2', 74)
            g2.add_edge('2', '1', 74)
            mst2=minimum_spanning_tree(g2, "prim", backend = Backend.CPP)
            assert mst2.num_edges() == 6

    fmst = minimum_spanning_tree
    fmstp = minimum_spanning_tree_parallel
    _test_minimum_spanning_tree(fmst, "List", "kruskal")
    _test_minimum_spanning_tree(fmst, "Matrix", "kruskal")
    _test_minimum_spanning_tree(fmst, "List", "prim")
    _test_minimum_spanning_tree(fmstp, "List", "kruskal", 3)
    _test_minimum_spanning_tree(fmstp, "Matrix", "kruskal", 3)
    _test_minimum_spanning_tree(fmstp, "List", "prim", 3)
    _test_minimum_spanning_tree_cpp("List", "prim")

def test_strongly_connected_components():

    def _test_strongly_connected_components(func, ds, algorithm, *args):
        import pydatastructs.utils.misc_util as utils
        GraphNode = getattr(utils, "Adjacency" + ds + "GraphNode")
        a, b, c, d, e, f, g, h = \
        [GraphNode(chr(x)) for x in range(ord('a'), ord('h') + 1)]
        graph = Graph(a, b, c, d, e, f, g, h)
        graph.add_edge(a.name, b.name)
        graph.add_edge(b.name, c.name)
        graph.add_edge(b.name, f.name)
        graph.add_edge(b.name, e.name)
        graph.add_edge(c.name, d.name)
        graph.add_edge(c.name, g.name)
        graph.add_edge(d.name, h.name)
        graph.add_edge(d.name, c.name)
        graph.add_edge(e.name, f.name)
        graph.add_edge(e.name, a.name)
        graph.add_edge(f.name, g.name)
        graph.add_edge(g.name, f.name)
        graph.add_edge(h.name, d.name)
        graph.add_edge(h.name, g.name)
        comps = func(graph, algorithm)
        expected_comps = [{'e', 'a', 'b'}, {'d', 'c', 'h'}, {'g', 'f'}]
        assert comps.sort() == expected_comps.sort()

    scc = strongly_connected_components
    _test_strongly_connected_components(scc, "List", "kosaraju")
    _test_strongly_connected_components(scc, "Matrix", "kosaraju")
    _test_strongly_connected_components(scc, "List", "tarjan")
    _test_strongly_connected_components(scc, "Matrix", "tarjan")

def test_depth_first_search():

    def _test_depth_first_search(ds):
        import pydatastructs.utils.misc_util as utils
        GraphNode = getattr(utils, "Adjacency" + ds + "GraphNode")

        V1 = GraphNode(0)
        V2 = GraphNode(1)
        V3 = GraphNode(2)

        G1 = Graph(V1, V2, V3)

        edges = [
            (V1.name, V2.name),
            (V2.name, V3.name),
            (V1.name, V3.name)
        ]

        for edge in edges:
            G1.add_edge(*edge)

        parent = {}
        def dfs_tree(curr_node, next_node, parent):
            if next_node != "":
                parent[next_node] = curr_node
            return True

        depth_first_search(G1, V1.name, dfs_tree, parent)
        assert (parent[V3.name] == V1.name and parent[V2.name] == V1.name) or \
            (parent[V3.name] == V2.name and parent[V2.name] == V1.name)

        V4 = GraphNode(0)
        V5 = GraphNode(1)
        V6 = GraphNode(2)
        V7 = GraphNode(3)
        V8 = GraphNode(4)

        edges = [
            (V4.name, V5.name),
            (V5.name, V6.name),
            (V6.name, V7.name),
            (V6.name, V4.name),
            (V7.name, V8.name)
        ]

        G2 = Graph(V4, V5, V6, V7, V8)

        for edge in edges:
            G2.add_edge(*edge)

        path = []
        def path_finder(curr_node, next_node, dest_node, parent, path):
            if next_node != "":
                parent[next_node] = curr_node
            if curr_node == dest_node:
                node = curr_node
                path.append(node)
                while node is not None:
                    if parent.get(node, None) is not None:
                        path.append(parent[node])
                    node = parent.get(node, None)
                path.reverse()
                return False
            return True

        parent.clear()
        depth_first_search(G2, V4.name, path_finder, V7.name, parent, path)
        assert path == [V4.name, V5.name, V6.name, V7.name]

    _test_depth_first_search("List")
    _test_depth_first_search("Matrix")

def test_shortest_paths():

    def _test_shortest_paths_positive_edges(ds, algorithm):
        import pydatastructs.utils.misc_util as utils
        GraphNode = getattr(utils, "Adjacency" + ds + "GraphNode")
        vertices = [GraphNode('S'), GraphNode('C'),
                    GraphNode('SLC'), GraphNode('SF'),
                    GraphNode('D')]

        graph = Graph(*vertices)
        graph.add_edge('S', 'SLC', 2)
        graph.add_edge('C', 'S', 4)
        graph.add_edge('C', 'D', 2)
        graph.add_edge('SLC', 'C', 2)
        graph.add_edge('SLC', 'D', 3)
        graph.add_edge('SF', 'SLC', 2)
        graph.add_edge('SF', 'S', 2)
        graph.add_edge('D', 'SF', 3)
        dist, pred = shortest_paths(graph, algorithm, 'SLC')
        assert dist == {'S': 6, 'C': 2, 'SLC': 0, 'SF': 6, 'D': 3}
        assert pred == {'S': 'C', 'C': 'SLC', 'SLC': None, 'SF': 'D', 'D': 'SLC'}
        dist, pred = shortest_paths(graph, algorithm, 'SLC', 'SF')
        assert dist == 6
        assert pred == {'S': 'C', 'C': 'SLC', 'SLC': None, 'SF': 'D', 'D': 'SLC'}
        graph.remove_edge('SLC', 'D')
        graph.add_edge('D', 'SLC', -10)
        assert raises(ValueError, lambda: shortest_paths(graph, 'bellman_ford', 'SLC'))

    def _test_shortest_paths_negative_edges(ds, algorithm):
        import pydatastructs.utils.misc_util as utils
        GraphNode = getattr(utils, "Adjacency" + ds + "GraphNode")
        vertices = [GraphNode('s'), GraphNode('a'),
                    GraphNode('b'), GraphNode('c'),
                    GraphNode('d')]

        graph = Graph(*vertices)
        graph.add_edge('s', 'a', 3)
        graph.add_edge('s', 'b', 2)
        graph.add_edge('a', 'c', 1)
        graph.add_edge('b', 'd', 1)
        graph.add_edge('b', 'a', -2)
        graph.add_edge('c', 'd', 1)
        dist, pred = shortest_paths(graph, algorithm, 's')
        assert dist == {'s': 0, 'a': 0, 'b': 2, 'c': 1, 'd': 2}
        assert pred == {'s': None, 'a': 'b', 'b': 's', 'c': 'a', 'd': 'c'}
        dist, pred = shortest_paths(graph, algorithm, 's', 'd')
        assert dist == 2
        assert pred == {'s': None, 'a': 'b', 'b': 's', 'c': 'a', 'd': 'c'}

    _test_shortest_paths_positive_edges("List", 'bellman_ford')
    _test_shortest_paths_positive_edges("Matrix", 'bellman_ford')
    _test_shortest_paths_negative_edges("List", 'bellman_ford')
    _test_shortest_paths_negative_edges("Matrix", 'bellman_ford')
    _test_shortest_paths_positive_edges("List", 'dijkstra')
    _test_shortest_paths_positive_edges("Matrix", 'dijkstra')

def test_all_pair_shortest_paths():

    def _test_shortest_paths_negative_edges(ds, algorithm):
        import pydatastructs.utils.misc_util as utils
        GraphNode = getattr(utils, "Adjacency" + ds + "GraphNode")
        vertices = [GraphNode('1'), GraphNode('2'),
                    GraphNode('3'), GraphNode('4')]

        graph = Graph(*vertices)
        graph.add_edge('1', '3', -2)
        graph.add_edge('2', '1', 4)
        graph.add_edge('2', '3', 3)
        graph.add_edge('3', '4', 2)
        graph.add_edge('4', '2', -1)
        dist, next_v = all_pair_shortest_paths(graph, algorithm)
        assert dist == {'1': {'3': -2, '1': 0, '4': 0, '2': -1},
                        '2': {'1': 4, '3': 2, '2': 0, '4': 4},
                        '3': {'4': 2, '3': 0, '1': 5, '2': 1},
                        '4': {'2': -1, '4': 0, '1': 3, '3': 1}}
        assert next_v == {'1': {'3': '1', '1': '1', '4': None, '2': None},
                          '2': {'1': '2', '3': None, '2': '2', '4': None},
                          '3': {'4': '3', '3': '3', '1': None, '2': None},
                          '4': {'2': '4', '4': '4', '1': None, '3': None}}

    _test_shortest_paths_negative_edges("List", 'floyd_warshall')
    _test_shortest_paths_negative_edges("Matrix", 'floyd_warshall')
    _test_shortest_paths_negative_edges("List", 'johnson')

def test_topological_sort():

    def _test_topological_sort(func, ds, algorithm, threads=None):
        import pydatastructs.utils.misc_util as utils
        GraphNode = getattr(utils, "Adjacency" + ds + "GraphNode")
        vertices = [GraphNode('2'), GraphNode('3'), GraphNode('5'),
                    GraphNode('7'), GraphNode('8'), GraphNode('10'),
                    GraphNode('11'), GraphNode('9')]

        graph = Graph(*vertices)
        graph.add_edge('5', '11')
        graph.add_edge('7', '11')
        graph.add_edge('7', '8')
        graph.add_edge('3', '8')
        graph.add_edge('3', '10')
        graph.add_edge('11', '2')
        graph.add_edge('11', '9')
        graph.add_edge('11', '10')
        graph.add_edge('8', '9')
        if threads is not None:
            l = func(graph, algorithm, threads)
        else:
            l = func(graph, algorithm)
        assert all([(l1 in l[0:3]) for l1 in ('3', '5', '7')] +
                   [(l2 in l[3:5]) for l2 in ('8', '11')] +
                   [(l3 in l[5:]) for l3 in ('10', '9', '2')])

    _test_topological_sort(topological_sort, "List", "kahn")
    _test_topological_sort(topological_sort_parallel, "List", "kahn", 3)


def test_max_flow():
    def _test_max_flow(ds, algorithm):
        import pydatastructs.utils.misc_util as utils
        GraphNode = getattr(utils, "Adjacency" + ds + "GraphNode")

        a = GraphNode('a')
        b = GraphNode('b')
        c = GraphNode('c')
        d = GraphNode('d')
        e = GraphNode('e')

        G = Graph(a, b, c, d, e)

        G.add_edge('a', 'b', 3)
        G.add_edge('a', 'c', 4)
        G.add_edge('b', 'c', 2)
        G.add_edge('b', 'd', 3)
        G.add_edge('c', 'd', 1)
        G.add_edge('d', 'e', 6)

        assert max_flow(G, 'a', 'e', algorithm) == 4
        assert max_flow(G, 'a', 'c', algorithm) == 6

        a = GraphNode('a')
        b = GraphNode('b')
        c = GraphNode('c')
        d = GraphNode('d')
        e = GraphNode('e')
        f = GraphNode('f')

        G2 = Graph(a, b, c, d, e, f)

        G2.add_edge('a', 'b', 16)
        G2.add_edge('a', 'c', 13)
        G2.add_edge('b', 'c', 10)
        G2.add_edge('b', 'd', 12)
        G2.add_edge('c', 'b', 4)
        G2.add_edge('c', 'e', 14)
        G2.add_edge('d', 'c', 9)
        G2.add_edge('d', 'f', 20)
        G2.add_edge('e', 'd', 7)
        G2.add_edge('e', 'f', 4)

        assert max_flow(G2, 'a', 'f', algorithm) == 23
        assert max_flow(G2, 'a', 'd', algorithm) == 19

        a = GraphNode('a')
        b = GraphNode('b')
        c = GraphNode('c')
        d = GraphNode('d')

        G3 = Graph(a, b, c, d)

        G3.add_edge('a', 'b', 3)
        G3.add_edge('a', 'c', 2)
        G3.add_edge('b', 'c', 2)
        G3.add_edge('b', 'd', 3)
        G3.add_edge('c', 'd', 2)

        assert max_flow(G3, 'a', 'd', algorithm) == 5
        assert max_flow(G3, 'a', 'b', algorithm) == 3


    _test_max_flow("List", "edmonds_karp")
    _test_max_flow("Matrix", "edmonds_karp")
    _test_max_flow("List", "dinic")
    _test_max_flow("Matrix", "dinic")


def test_find_bridges():
    def _test_find_bridges(ds):
        import pydatastructs.utils.misc_util as utils
        GraphNode = getattr(utils, "Adjacency" + ds + "GraphNode")

        impl = 'adjacency_list' if ds == "List" else 'adjacency_matrix'

        v0 = GraphNode(0)
        v1 = GraphNode(1)
        v2 = GraphNode(2)
        v3 = GraphNode(3)
        v4 = GraphNode(4)

        G1 = Graph(v0, v1, v2, v3, v4, implementation=impl)
        G1.add_edge(v0.name, v1.name)
        G1.add_edge(v1.name, v2.name)
        G1.add_edge(v2.name, v3.name)
        G1.add_edge(v3.name, v4.name)

        bridges = find_bridges(G1)
        expected_bridges = [('0', '1'), ('1', '2'), ('2', '3'), ('3', '4')]
        assert sorted(bridges) == sorted(expected_bridges)

        u0 = GraphNode(0)
        u1 = GraphNode(1)
        u2 = GraphNode(2)

        G2 = Graph(u0, u1, u2, implementation=impl)
        G2.add_edge(u0.name, u1.name)
        G2.add_edge(u1.name, u2.name)
        G2.add_edge(u2.name, u0.name)

        bridges = find_bridges(G2)
        assert bridges == []

        w0 = GraphNode(0)
        w1 = GraphNode(1)
        w2 = GraphNode(2)
        w3 = GraphNode(3)
        w4 = GraphNode(4)

        G3 = Graph(w0, w1, w2, w3, w4, implementation=impl)
        G3.add_edge(w0.name, w1.name)
        G3.add_edge(w1.name, w2.name)
        G3.add_edge(w3.name, w4.name)

        bridges = find_bridges(G3)
        expected_bridges = [('0', '1'), ('1', '2'), ('3', '4')]
        assert sorted(bridges) == sorted(expected_bridges)

    _test_find_bridges("List")
    _test_find_bridges("Matrix")
