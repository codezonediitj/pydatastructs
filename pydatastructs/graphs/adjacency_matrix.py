from pydatastructs.graphs.graph import Graph
from pydatastructs.linear_data_structures import OneDimensionalArray
from pydatastructs.utils.misc_util import AdjacencyMatrixGraphNode, GraphEdge

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
    def __new__(cls, *vertices):
        obj = object.__new__(cls)
        num_vertices = len(vertices)
        obj.vertices = [vertex.name for vertex in vertices]
        for vertex in vertices:
            obj.__setattr__(str(vertex.name), vertex)
        obj.matrix = OneDimensionalArray(
                        OneDimensionalArray,
                        num_vertices)
        for i in range(num_vertices):
            obj.matrix[i] = OneDimensionalArray(
                            bool,
                            num_vertices)
            obj.matrix[i].fill(False)
        obj.edge_weights = dict()
        return obj

    def is_adjacent(self, node1, node2):
        return self.matrix[node1][node2]

    def neighbors(self, node):
        neighbors = []
        for i in range(self.matrix[node]._size):
            if self.matrix[node][i]:
                neighbors.append(self.__getattribute__(
                                 str(self.vertices[i])))
        return neighbors

    def add_vertex(self, node):
        raise NotImplementedError("Currently we allow "
                "adjacency matrix for static graphs only")

    def remove_vertex(self, node):
        raise NotImplementedError("Currently we allow "
                "adjacency matrix for static graphs only.")

    def add_edge(self, source, target, cost=None):
        self.matrix[source][target] = True
        source, target = str(source), str(target)
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
        self.matrix[source][target] = False
        self.edge_weights.pop(str(source) + "_" + str(target), None)
