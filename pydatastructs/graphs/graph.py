
__all__ = [
    'Graph'
]

class Graph(object):

    def __new__(cls, implementation='adjacency_list'):
        if implementation is 'adjacency_list':
            from pydatastructs.graphs.adjacency_list import AdjacencyList
            return AdjacencyList()
        else:
            raise NotImplementedError("%s implementation is not a part "
                                      "of the library currently."%(implementation))

    def is_adjacent(self, node1, node2):
        return hasattr(node1, node2.name)

    def neighbors(self, node):
        raise NotImplementedError(
            "This is an abstract method.")

    def add_vertex(self, node):
        raise NotImplementedError(
            "This is an abstract method.")

    def remove_vertex(self, node):
        raise NotImplementedError(
            "This is an abstract method.")

    def add_edge(self, source, target):
        raise NotImplementedError(
            "This is an abstract method.")

    def remove_edge(self, source, target):
        raise NotImplementedError(
            "This is an abstract method.")

    def get_vertex_value(self, node):
        return node.data

    def set_vertex_value(self, node, value):
        node.data = value

    def get_edge_value(self, edge):
        return edge.value

    def set_edge_value(self, edge, value):
        edge.value = value
