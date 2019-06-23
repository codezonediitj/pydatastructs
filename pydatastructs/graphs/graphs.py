from __future__ import print_function, division
from pydatastructs.utils.misc_util import Node

__all__ = [
    'Graph'
]

class Graph(object):
    """
    Abstract representation of graphs.
    """
    def __new__(cls, data_structure='adjacency_list'):
        if data_structure == 'adjacency_list':
            return AdjacencyList()
        if data_structure == 'adjacency_matrix':
            return AdjacencyMatrix()
        return IncidenceMatrix()

    def adjacent(self, x, y):
        """
        Tests whether there is an edge from the vertex x to the vertex y.
        """
        raise NotImplementedError()

    def neighbors(self, x):
        """
        lists all vertices y such that there is an edge from the vertex x to
        the vertex y.
        """
        raise NotImplementedError()

    def add_vertex(self, x):
        """
        Adds the vertex with key x.
        """
        raise NotImplementedError()

    def remove_vertex(self, x):
        """
        Removes the vertex with key x, if it is there.
        """
        raise NotImplementedError()

    def add_edge(self, x, y):
        """
        Adds the edge from the vertex with key x to the
        vertex with key y, if it is not there.
        """
        raise NotImplementedError()

    def remove_edge(self, x, y):
        """
        Removes the edge from the vertex with key x to
        the vertex with key y, if it is there.
        """
        raise NotImplementedError()

    def get_vertex_value(self, x):
        """
        To obtain the value associated with the vertex with key x.
        """
        raise NotImplementedError()

    def set_vertex_value(self, x, v):
        """
        Sets the value associated with the vertex with key x to v.
        """
        raise NotImplementedError()

    def get_edge_value(self, x, y):
        """
        To obtain the value associated with the edge (x<key>, y<key>).
        """
        raise NotImplementedError()

    def set_edge_value(self, x, y, v):
        """
        Sets the value associated with the edge (x<key>, y<key>) to v.
        """
        raise NotImplementedError()

class AdjacencyList(Graph):

    def __new__(cls):
        obj = object.__new__(cls)
        obj._map = dict()
        obj._edges = dict()
        obj._vertices = []
        return obj

    def adjacent(self, x, y):
        """
        Tests whether there is an edge from the vertex with key
        x to the vertex with key y.

        Parameters
        ==========

        x: A valid python type
            key of the starting node.
        y: A valid python type
            key of the destination node.

        Returns
        =======

        bool
            True if there is an edge, False if there is not an
            edge and None if vertex with key x is not in the graph.
        """
        nx, ny = x, Node(y, None)
        if self._map.get(nx, None) is not None:
            return ny in self._map[nx]

    def neighbors(self, x):
        """
        Lists all vertices y such that there is an edge
        from the vertex with key x to the vertex with key y.

        Parameters
        ==========

        x: A valid python type
            key of the starting node.

        Returns
        =======

        list
            If vertex with key x is in the graph
        None
            In all other cases.
        """
        nx = x
        if self._map.get(nx, None) is not None:
            return self._map[nx]

    def add_vertex(self, x):
        """
        Adds the vertex with key x, if it is not there.

        Parameters
        ==========

        x: A valid python
            The key of the new vertex.
        """
        nx, node = x, Node(x, None)
        if self._map.get(nx, None) is None:
            self._map[nx] = []
            self._vertices.append(node)

    def remove_vertex(self, x):
        """
        Removes the vertex x, if it is there.

        Parameters
        ==========

        x: A valid python data type
            key of the vertex which is to be removed.

        """
        nx = x
        if self._map.get(nx, None) is not None:
            del self._map[nx]
        for key in self._map:
            for node in self._map[key]:
                if node.key == nx:
                    self._map[key].remove(node)
                    break

    def add_edge(self, x, y):
        """
        Adds the edge from the vertex key x to the vertex key y,
        if it is not there.

        Parameters
        ==========

        x: A valid python type
            key of the starting node.
        y: A valid python type
            key of the destination node.

        """
        nx, ny = x, Node(y, None)
        self.add_vertex(nx)
        _is_node_present = False
        for node in self._map[nx]:
            if node.key == y:
                _is_node_present = True
                break
        if not _is_node_present:
            self._map[nx].append(ny)

    def remove_edge(self, x, y):
        """
        Removes the edge from the vertex key x to the vertex key y,
        if it is there.

        Parameters
        ==========

        x: A valid python type
            key of the starting node.
        y: A valid python type
            key of the destination node.
        """
        nx, ny = x, y
        for node in self._map[nx]:
            if node.key == ny:
                self._map[nx].remove(node)
                break

    def get_vertex_value(self, x):
        """
        To obtain the value associated with the vertex with key x.

        Parameters
        ==========

        x: A valid python data type
            key of the vertex which is to be removed.
        """
        nx = x
        if self._map.get(nx, None) is not None:
            for node in self._vertices:
                if node.key == nx:
                    return node.data

    def set_vertex_value(self, x, v):
        """
        Sets the value associated with the vertex x to v.

        Parameters
        ==========

        x: A valid python data type
            key of the vertex which is to be removed.
        v: A valid python type
            value to be associated with the node.
        """
        nx = x
        if self._map.get(nx, None) is not None:
            for i, node in enumerate(self._vertices):
                if node.key == nx:
                    self._vertices[i].data = v


class AdjacencyMatrix(Graph):
    pass

class IncidenceMatrix(Graph):
    pass
