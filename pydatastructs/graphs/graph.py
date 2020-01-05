
__all__ = [
    'Graph'
]

class Graph(object):

    def __new__(cls, *args, **kwargs):
        implementation = kwargs.get('implementation', 'adjacency_list')
        if implementation is 'adjacency_list':
            from pydatastructs.graphs.adjacency_list import AdjacencyList
            return AdjacencyList(*args)
        else:
            raise NotImplementedError("%s implementation is not a part "
                                      "of the library currently."%(implementation))

    def is_adjacent(self, node1, node2):
        node1 = self.__getattribute__(node1)
        return hasattr(node1, node2)

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
