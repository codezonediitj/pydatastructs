from pydatastructs.graphs.graph import Graph
from pydatastructs.utils.misc_util import GraphEdge

__all__ = [
    'AdjacencyList'
]


class AdjacencyList(Graph):
    """
    Adjacency list implementation of graphs.

    See also
    ========

    pydatastructs.graphs.graph.Graph
    """

    def __new__(cls, *vertices):
        obj = object.__new__(cls)
        for vertex in vertices:
            obj.__setattr__(vertex.name, vertex)
        obj.vertices = [vertex.name for vertex in vertices]
        obj.edge_weights = {}
        return obj

    @classmethod
    def methods(cls):
        return ['is_adjacent', 'neighbors',
                'add_vertex', 'remove_vertex', 'add_edge',
                'get_edge', 'remove_edge', '__new__']

    def is_adjacent(self, node1, node2):
        node1 = self.__getattribute__(node1)
        return hasattr(node1, node2)

    def neighbors(self, node):
        node = self.__getattribute__(node)
        return [self.__getattribute__(name) for name in node.adjacent]

    def add_vertex(self, node):
        if not hasattr(self, node.name):
            self.vertices.append(node.name)
            self.__setattr__(node.name, node)

    def remove_vertex(self, name):
        delattr(self, name)
        self.vertices.remove(name)
        for node in self.vertices:
            node_obj = self.__getattribute__(node)
            if hasattr(node_obj, name):
                delattr(node_obj, name)
                node_obj.adjacent.remove(name)

    def add_edge(self, source, target, cost=None):
        source, target = self.__getattribute__(source), self.__getattribute__(target)
        source.add_adjacent_node(target.name)
        if cost is not None:
            self.edge_weights[source.name + "_" + target.name] = \
                GraphEdge(source, target, cost)

    def get_edge(self, source, target):
        return self.edge_weights.get(
            source + "_" + target,
            None)

    def remove_edge(self, source, target):
        source, target = self.__getattribute__(source), self.__getattribute__(target)
        source.remove_adjacent_node(target.name)
        self.edge_weights.pop(source.name + "_" + target.name,
                              None)
