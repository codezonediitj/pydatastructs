from pydatastructs.graphs.graph import Graph
from pydatastructs.linear_data_structures import DynamicOneDimensionalArray, OneDimensionalArray
from pydatastructs.utils.misc_util import AdjacencyMatrixGraphNode

__all__ = [
    'AdjacencyMatrix'
]

class AdjacencyMatrix(Graph):

    def __new__(cls, num_vertices=0, *vertices):
        obj = object.__new__(cls)
        obj.vertices = DynamicOneDimensionalArray(
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
        return obj

    def is_adjacent(self, node1, node2):
        return self.matrix[node1][node2]

    def neighbors(self, node):
        neighbors = []
        for i in range(self.matrix[node]._last_pos_filled + 1):
            if self.matrix[node][i]:
                neighbors.append(self.vertices[i])
        return neighbors
