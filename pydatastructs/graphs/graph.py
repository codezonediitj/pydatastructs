__all__ = [
    'Graph'
]


class Graph(object):
    """
    Represents generic concept of graphs.

    Parameters
    ==========

    implementation: str
        The implementation to be used for storing
        graph in memory. It can be figured out
        from type of the vertices(if passed at construction).
        By default, 'adjacency_list'.
    vertices: AdjacencyListGraphNode(s)
        For AdjacencyList implementation vertices
        can be passed for initializing the graph.

    Examples
    ========

    >>> from pydatastructs.graphs import Graph
    >>> from pydatastructs.utils import AdjacencyListGraphNode
    >>> v_1 = AdjacencyListGraphNode('v_1', 1)
    >>> v_2 = AdjacencyListGraphNode('v_2', 2)
    >>> g = Graph(v_1, v_2)
    >>> g.add_edge('v_1', 'v_2')
    >>> g.add_edge('v_2', 'v_1')
    >>> g.is_adjacent('v_1', 'v_2')
    True
    >>> g.is_adjacent('v_2', 'v_1')
    True
    >>> g.remove_edge('v_1', 'v_2')
    >>> g.is_adjacent('v_1', 'v_2')
    False
    >>> g.is_adjacent('v_2', 'v_1')
    True

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Graph_(abstract_data_type)
    """

    __slots__ = ['_impl']

    def __new__(cls, *args, **kwargs):
        default_impl = args[0]._impl if args else 'adjacency_list'
        implementation = kwargs.get('implementation', default_impl)
        if implementation == 'adjacency_list':
            from pydatastructs.graphs.adjacency_list import AdjacencyList
            obj = AdjacencyList(*args)
            obj._impl = implementation
            return obj
        elif implementation == 'adjacency_matrix':
            from pydatastructs.graphs.adjacency_matrix import AdjacencyMatrix
            obj = AdjacencyMatrix(*args)
            obj._impl = implementation
            return obj
        else:
            raise NotImplementedError("%s implementation is not a part "
                                      "of the library currently." % implementation)

    def is_adjacent(self, node1, node2):
        """
        Checks if the nodes with the given
        with the given names are adjacent
        to each other.
        """
        raise NotImplementedError(
            "This is an abstract method.")

    def neighbors(self, node):
        """
        Lists the neighbors of the node
        with given name.
        """
        raise NotImplementedError(
            "This is an abstract method.")

    def add_vertex(self, node):
        """
        Adds the input vertex to the node.
        """
        raise NotImplementedError(
            "This is an abstract method.")

    def remove_vertex(self, node):
        """
        Removes the input vertex along with all the edges
        pointing towards to it.
        """
        raise NotImplementedError(
            "This is an abstract method.")

    def add_edge(self, source, target, cost=None):
        """
        Adds the edge starting at first parameter
        i.e., source and ending at the second
        parameter i.e., target.
        """
        raise NotImplementedError(
            "This is an abstract method.")

    def get_edge(self, source, target):
        """
        Returns GraphEdge object if there
        is an edge between source and target
        otherwise None.
        """
        raise NotImplementedError(
            "This is an abstract method.")

    def remove_edge(self, source, target):
        """
        Removes the edge starting at first parameter
        i.e., source and ending at the second
        parameter i.e., target.
        """
        raise NotImplementedError(
            "This is an abstract method.")

    @property
    def impl(self):
        return self._impl
