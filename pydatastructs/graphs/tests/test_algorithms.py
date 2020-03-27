from pydatastructs import (breadth_first_search, Graph,
breadth_first_search_parallel, minimum_spanning_tree,
minimum_spanning_tree_parallel)


def test_breadth_first_search():

    def _test_breadth_first_search(ds):
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

        parent = dict()
        def bfs_tree(curr_node, next_node, parent):
            if next_node != "":
                parent[next_node] = curr_node
            return True

        breadth_first_search(G1, V1.name, bfs_tree, parent)
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

        parent = dict()
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

    fmst = minimum_spanning_tree
    fmstp = minimum_spanning_tree_parallel
    _test_minimum_spanning_tree(fmst, "List", "kruskal")
    _test_minimum_spanning_tree(fmst, "Matrix", "kruskal")
    _test_minimum_spanning_tree(fmst, "List", "prim")
    _test_minimum_spanning_tree(fmstp, "List", "kruskal", 3)
    _test_minimum_spanning_tree(fmstp, "Matrix", "kruskal", 3)
    _test_minimum_spanning_tree(fmstp, "List", "prim", 3)
