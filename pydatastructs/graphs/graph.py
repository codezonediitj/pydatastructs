
from pydatastructs.utils.misc_util import Backend, raise_if_backend_is_not_python

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
        Currently the following implementations are supported,

        'adjacency_list' -> Adjacency list implementation.

        'adjacency_matrix' -> Adjacency matrix implementation.

        By default, 'adjacency_list'.
    vertices: GraphNode(s)
        For AdjacencyList implementation vertices
        can be passed for initializing the graph.
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

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

    Note
    ====

    Make sure to create nodes (AdjacencyListGraphNode or AdjacencyMatrixGraphNode)
    and them in your graph using Graph.add_vertex before adding edges whose
    end points require either of the nodes that you added. In other words,
    Graph.add_edge doesn't add new nodes on its own if the input
    nodes are not already present in the Graph.

    """

    __slots__ = ['_impl']

    def __new__(cls, *args, **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
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
                                      "of the library currently."%(implementation))

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
        Adds the input vertex to the node, or does nothing
        if the input vertex is already in the graph.
        """
        raise NotImplementedError(
            "This is an abstract method.")

    def remove_vertex(self, node):
        """
        Removes the input vertex along with all the edges
        pointing towards it.
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

    def num_vertices(self):
        """
        Number of vertices
        """
        raise NotImplementedError(
            "This is an abstract method.")

    def num_edges(self):
        """
        Number of edges
        """
        raise NotImplementedError(
            "This is an abstract method.")
