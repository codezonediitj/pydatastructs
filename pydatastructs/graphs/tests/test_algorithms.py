from pydatastructs import breadth_first_search, Graph, AdjacencyListGraphNode

def test_breadth_first_search():

    V1 = AdjacencyListGraphNode("V1")
    V2 = AdjacencyListGraphNode("V2")
    V3 = AdjacencyListGraphNode("V3")

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
    print(parent)
    assert (parent['V3'] == 'V1' and parent['V2'] == 'V1') or \
           (parent['V3'] == 'V2' and parent['V2'] == 'V1')

    V4 = AdjacencyListGraphNode("V4")
    V5 = AdjacencyListGraphNode("V5")
    V6 = AdjacencyListGraphNode("V6")
    V7 = AdjacencyListGraphNode("V7")
    V8 = AdjacencyListGraphNode("V8")

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
    assert path == ['V4', 'V5', 'V6', 'V7']
