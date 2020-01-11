from pydatastructs.graphs.graph import Graph
from pydatastructs.linear_data_structures import OneDimensionalArray
from pydatastructs.utils.misc_util import AdjacencyMatrixGraphNode

__all__ = [
    'AdjacencyMatrix'
]

class AdjacencyMatrix(Graph):

    def __new__(cls, *vertices):
        obj = object.__new__(cls)
        num_vertices = len(vertices)
        obj.vertices = OneDimensionalArray(
                        AdjacencyMatrixGraphNode,
                        num_vertices)
        for vertex in vertices:
            obj.vertices[vertex.name] = vertex
        obj.matrix = OneDimensionalArray(
                        OneDimensionalArray,
                        num_vertices)
        for i in range(num_vertices):
            obj.matrix[i] = OneDimensionalArray(
                            bool,
                            num_vertices)
            obj.matrix[i].fill(False)
        return obj

    def is_adjacent(self, node1, node2):
        return self.matrix[node1][node2]

    def neighbors(self, node):
        neighbors = []
        for i in range(self.matrix[node]._size):
            if self.matrix[node][i]:
                neighbors.append(self.vertices[i])
        return neighbors

    def add_vertex(self, node):
        raise NotImplementedError("Currently we allow "
                "adjacency matrix for static graphs only")

    def remove_vertex(self, node):
        raise NotImplementedError("Currently we allow "
                "adjacency matrix for static graphs only.")

    def add_edge(self, source, target):
        self.matrix[source][target] = True

    def remove_edge(self, source, target):
        self.matrix[source][target] = False
