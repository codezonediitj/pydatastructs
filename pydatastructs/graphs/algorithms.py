# TODO: REPLACE COLLECTIONS QUEUE WITH PYDATASTRUCTS QUEUE
from collections import deque as Queue
from pydatastructs.utils.misc_util import AdjacencyListGraphNode

__all__ = [
    'breadth_first_search',
]

def breadth_first_search(
    graph, source_node, operation, *args, **kwargs):
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
    bfs_queue.append(source_node)
    visited = dict()
    while len(bfs_queue) != 0:
        curr_node = bfs_queue.popleft()
        status = operation(curr_node, *args, **kwargs)
        visited[curr_node.name] = True
        if not status:
            break
        for next_node in graph.neighbors(curr_node):
            if visited.get(next_node.name, False) is False:
                bfs_queue.append(next_node)
