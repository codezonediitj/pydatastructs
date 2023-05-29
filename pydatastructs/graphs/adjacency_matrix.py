from pydatastructs.graphs.graph import Graph
from pydatastructs.utils.misc_util import (
    GraphEdge, raise_if_backend_is_not_python,
    Backend)

__all__ = [
    'AdjacencyMatrix'
]

class AdjacencyMatrix(Graph):
    """
    Adjacency matrix implementation of graphs.

    See also
    ========

    pydatastructs.graphs.graph.Graph
    """
    def __new__(cls, *vertices, **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
        obj = object.__new__(cls)
        obj.vertices = [vertex.name for vertex in vertices]
        for vertex in vertices:
            obj.__setattr__(vertex.name, vertex)
        obj.matrix = {}
        for vertex in vertices:
            obj.matrix[vertex.name] = {}
        obj.edge_weights = {}
        return obj

    @classmethod
    def methods(self):
        return ['is_adjacent', 'neighbors',
        'add_edge', 'get_edge', 'remove_edge',
        '__new__']

    def is_adjacent(self, node1, node2):
        node1, node2 = str(node1), str(node2)
        row = self.matrix.get(node1, {})
        return row.get(node2, False) is not False

    def num_vertices(self):
        return len(self.vertices)

    def num_edges(self):
        return sum(len(v) for v in self.matrix.values())

    def neighbors(self, node):
        node = str(node)
        neighbors = []
        row = self.matrix.get(node, {})
        for node, presence in row.items():
            if presence:
                neighbors.append(self.__getattribute__(
                                 str(node)))
        return neighbors

    def add_vertex(self, node):
        raise NotImplementedError("Currently we allow "
                "adjacency matrix for static graphs only")

    def remove_vertex(self, node):
        raise NotImplementedError("Currently we allow "
                "adjacency matrix for static graphs only.")

    def add_edge(self, source, target, cost=None):
        source, target = str(source), str(target)
        error_msg = ("Vertex %s is not present in the graph."
                     "Call Graph.add_vertex to add a new"
                     "vertex. Graph.add_edge is only responsible"
                     "for adding edges and it will not add new"
                     "vertices on its own. This is done to maintain"
                     "clear separation between the functionality of"
                     "these two methods.")
        if source not in self.matrix:
            raise ValueError(error_msg % (source))
        if target not in self.matrix:
            raise ValueError(error_msg % (target))

        self.matrix[source][target] = True
        if cost is not None:
            self.edge_weights[source + "_" + target] = \
                GraphEdge(self.__getattribute__(source),
                          self.__getattribute__(target),
                          cost)

    def get_edge(self, source, target):
        return self.edge_weights.get(
            str(source) + "_" + str(target),
            None)

    def remove_edge(self, source, target):
        source, target = str(source), str(target)
        self.matrix[source][target] = False
        self.edge_weights.pop(str(source) + "_" + str(target), None)
