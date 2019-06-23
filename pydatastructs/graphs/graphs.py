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
