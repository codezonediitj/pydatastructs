from pydatastructs.graphs.graph import Graph
from pydatastructs.linear_data_structures import DynamicOneDimensionalArray

__all__ = [
    'AdjacencyList'
]

class AdjacencyList(Graph):

    def __new__(cls, *vertices):
        obj = object.__new__(cls)
        for vertex in vertices:
            obj.__setattr__(vertex.name, vertex)
        obj.vertices = set([vertex.name for vertex in vertices])
        return obj

    def neighbors(self, node):
        return [node.name for name in node.adjacent]

    def add_vertex(self, node):
        self.__setattr__(node.name, node)

    def remove_vertex(self, name):
        delattr(self, name)
        self.vertices.remove(name)
        for node in self.vertices:
            if hasattr(node, name):
                delattr(node, name)

    def add_edge(self, source, target):
        source.__setattr__(target.name, target)
        source.adjacent.append(target.name)

    def remove_edge(self, source, target):
        delattr(source, target.name)
