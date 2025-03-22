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
        if node.name in self.matrix:
            raise ValueError("Vertex %s already exists in the graph." % node.name)
        self.vertices.append(node.name)
        setattr(self, node.name, node)
        self.matrix[node.name] = {}

    def remove_vertex(self, node):
        node = str(node)
        if node not in self.matrix:
            raise ValueError("Vertex '%s' is not present in the graph." % node)

        # first we need to remove the edges involving the `node`

        # removing records from dict while iterating over them is tricky
        # so we'll first identify which edges to remove first

        edges_to_remove = []

        for target in self.matrix[node]:
            if self.matrix[node].get(target, False):
                edges_to_remove.append((node, target))

        for source in self.vertices:
            if self.matrix[source].get(node):
                edges_to_remove.append((source, node))

        # remove the identified edge weights
        for source, target in edges_to_remove:
            edge_key = str(source) + "_" + str(target)
            self.edge_weights.pop(edge_key)

        self.vertices.remove(node)
        # eliminate all outgoing edges
        self.matrix.pop(node, None)

        # eliminate all incoming edges
        for source in self.vertices:
            self.matrix[source].pop(node, None)

        if hasattr(self, node):
            delattr(self, node)

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
