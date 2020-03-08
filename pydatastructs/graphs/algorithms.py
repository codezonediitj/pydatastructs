"""
Contains all the algorithms associated with graph
data structure.
"""
# TODO: REPLACE COLLECTIONS QUEUE WITH PYDATASTRUCTS QUEUE
from collections import deque as Queue
from pydatastructs.utils.misc_util import AdjacencyListGraphNode
from concurrent.futures import ThreadPoolExecutor

__all__ = [
    'breadth_first_search',
    'breadth_first_search_parallel'
]

def breadth_first_search(
    graph, source_node, operation, *args, **kwargs):
    """
    Implementation of serial breadth first search(BFS)
    algorithm.

    Parameters
    ==========

    graph: Graph
        The graph on which BFS is to be performed.
    source_node: str
        The name of the source node from where the BFS is
        to be initiated.
    operation: function
        The function which is to be applied
        on every node when it is visited.
        The prototype which is to be followed is,
        `function_name(curr_node, next_node,
                       arg_1, arg_2, . . ., arg_n)`.
        Here, the first two arguments denote, the
        current node and the node next to current node.
        The rest of the arguments are optional and you can
        provide your own stuff there.

    Note
    ====

    You should pass all the arguments which you are going
    to use in the prototype of your `operation` after
    passing the operation function.

    Examples
    ========

    >>> from pydatastructs import Graph, AdjacencyListGraphNode
    >>> V1 = AdjacencyListGraphNode("V1")
    >>> V2 = AdjacencyListGraphNode("V2")
    >>> V3 = AdjacencyListGraphNode("V3")
    >>> G = Graph(V1, V2, V3)
    >>> from pydatastructs import breadth_first_search
    >>> def f(curr_node, next_node, dest_node):
    ...     return curr_node != dest_node
    ...
    >>> G.add_edge(V1.name, V2.name)
    >>> G.add_edge(V2.name, V3.name)
    >>> breadth_first_search(G, V1.name, f, V3.name)
    """
    import pydatastructs.graphs.algorithms as algorithms
    func = "_breadth_first_search_" + graph._impl
    if not hasattr(algorithms, func):
        raise NotImplementedError(
        "Currently breadth first search isn't implemented for "
        "%s graphs."%(graph._impl))
    return getattr(algorithms, func)(
           graph, source_node, operation, *args, **kwargs)

def _breadth_first_search_adjacency_list(
    graph, source_node, operation, *args, **kwargs):
    bfs_queue = Queue()
    visited = dict()
    bfs_queue.append(source_node)
    visited[source_node] = True
    while len(bfs_queue) != 0:
        curr_node = bfs_queue.popleft()
        next_nodes = graph.neighbors(curr_node)
        if len(next_nodes) != 0:
            for next_node in next_nodes:
                if visited.get(next_node.name, False) is False:
                    status = operation(curr_node, next_node.name, *args, **kwargs)
                    if not status:
                        return None
                    bfs_queue.append(next_node.name)
                    visited[next_node.name] = True
        else:
            status = operation(curr_node, "", *args, **kwargs)
            if not status:
                return None

_breadth_first_search_adjacency_matrix = _breadth_first_search_adjacency_list

def breadth_first_search_parallel(
    graph, source_node, num_threads, operation, *args, **kwargs):
    if num_threads <= 0:
        raise ValueError("Number threads should be positive, "
                         "found %s"%(num_threads))
    import pydatastructs.graphs.algorithms as algorithms
    func = "_breadth_first_search_parallel_" + graph._impl
    if not hasattr(algorithms, func):
        raise NotImplementedError(
        "Currently breadth first search isn't implemented for "
        "%s graphs."%(graph._impl))
    return getattr(algorithms, func)(
           graph, source_node, num_threads, operation, *args, **kwargs)

def generate_layer(graph, curr_node, next_layer, visited,
                   status, operation, args, kwargs):
    print(curr_node)
    next_nodes = graph.neighbors(curr_node)
    if len(next_nodes) != 0:
        for next_node in next_nodes:
            if visited.get(next_node, False) is False:
                status = status and operation(curr_node, next_node.name, *args, **kwargs)
                next_layer.add(next_node.name)
                visited[next_node] = True
    else:
        status = status and operation(curr_node, "", *args, **kwargs)

def _breadth_first_search_parallel_adjacency_list(
    graph, source_node, num_threads, operation, *args, **kwargs):
    visited, layers = dict(), dict()
    layers[0] = set()
    layers[0].add(source_node)
    visited[source_node] = True
    layer = 0
    while len(layers[layer]) != 0:
        status = True
        layers[layer+1] = set()
        with ThreadPoolExecutor(max_workers=num_threads) as Threads:
            Threads.map(generate_layer,
                        [(graph, node, layers[layer+1], visited,
                         status, operation, args, kwargs)
                         for node in layers[layer]])
        layer += 1
        if not status:
            return None
