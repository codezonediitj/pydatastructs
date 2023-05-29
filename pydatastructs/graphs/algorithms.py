"""
Contains algorithms associated with graph
data structure.
"""
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from pydatastructs.utils.misc_util import (
    _comp, raise_if_backend_is_not_python, Backend)
from pydatastructs.miscellaneous_data_structures import (
    DisjointSetForest, PriorityQueue)
from pydatastructs.graphs.graph import Graph
from pydatastructs.linear_data_structures.algorithms import merge_sort_parallel
from pydatastructs import PriorityQueue

__all__ = [
    'breadth_first_search',
    'breadth_first_search_parallel',
    'minimum_spanning_tree',
    'minimum_spanning_tree_parallel',
    'strongly_connected_components',
    'depth_first_search',
    'shortest_paths',
    'all_pair_shortest_paths',
    'topological_sort',
    'topological_sort_parallel',
    'max_flow'
]

Stack = Queue = deque

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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

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
    raise_if_backend_is_not_python(
        breadth_first_search, kwargs.get('backend', Backend.PYTHON))
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
    visited = {}
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
    """
    Parallel implementation of breadth first search on graphs.

    Parameters
    ==========

    graph: Graph
        The graph on which BFS is to be performed.
    source_node: str
        The name of the source node from where the BFS is
        to be initiated.
    num_threads: int
        Number of threads to be used for computation.
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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

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
    >>> from pydatastructs import breadth_first_search_parallel
    >>> def f(curr_node, next_node, dest_node):
    ...     return curr_node != dest_node
    ...
    >>> G.add_edge(V1.name, V2.name)
    >>> G.add_edge(V2.name, V3.name)
    >>> breadth_first_search_parallel(G, V1.name, 3, f, V3.name)
    """
    raise_if_backend_is_not_python(
        breadth_first_search_parallel, kwargs.get('backend', Backend.PYTHON))
    import pydatastructs.graphs.algorithms as algorithms
    func = "_breadth_first_search_parallel_" + graph._impl
    if not hasattr(algorithms, func):
        raise NotImplementedError(
        "Currently breadth first search isn't implemented for "
        "%s graphs."%(graph._impl))
    return getattr(algorithms, func)(
           graph, source_node, num_threads, operation, *args, **kwargs)

def _generate_layer(**kwargs):
    _args, _kwargs = kwargs.get('args'), kwargs.get('kwargs')
    (graph, curr_node, next_layer, visited, operation) = _args[0:5]
    op_args, op_kwargs = _args[5:], _kwargs
    next_nodes = graph.neighbors(curr_node)
    status = True
    if len(next_nodes) != 0:
        for next_node in next_nodes:
            if visited.get(next_node, False) is False:
                status = status and operation(curr_node, next_node.name, *op_args, **op_kwargs)
                next_layer.add(next_node.name)
                visited[next_node.name] = True
    else:
        status = status and operation(curr_node, "", *op_args, **op_kwargs)
    return status

def _breadth_first_search_parallel_adjacency_list(
    graph, source_node, num_threads, operation, *args, **kwargs):
    visited, layers = {}, {}
    layers[0] = set()
    layers[0].add(source_node)
    visited[source_node] = True
    layer = 0
    while len(layers[layer]) != 0:
        layers[layer+1] = set()
        with ThreadPoolExecutor(max_workers=num_threads) as Executor:
            for node in layers[layer]:
                status = Executor.submit(
                         _generate_layer, args=
                         (graph, node, layers[layer+1], visited,
                          operation, *args), kwargs=kwargs).result()
        layer += 1
        if not status:
            return None

_breadth_first_search_parallel_adjacency_matrix = _breadth_first_search_parallel_adjacency_list

def _generate_mst_object(graph):
    mst = Graph(*[getattr(graph, str(v)) for v in graph.vertices])
    return mst

def _sort_edges(graph, num_threads=None):
    edges = list(graph.edge_weights.items())
    if num_threads is None:
        sort_key = lambda item: item[1].value
        return sorted(edges, key=sort_key)

    merge_sort_parallel(edges, num_threads,
                        comp=lambda u,v: u[1].value <= v[1].value)
    return edges

def _minimum_spanning_tree_kruskal_adjacency_list(graph):
    mst = _generate_mst_object(graph)
    dsf = DisjointSetForest()
    for v in graph.vertices:
        dsf.make_set(v)
    for _, edge in _sort_edges(graph):
        u, v = edge.source.name, edge.target.name
        if dsf.find_root(u) is not dsf.find_root(v):
            mst.add_edge(u, v, edge.value)
            mst.add_edge(v, u, edge.value)
            dsf.union(u, v)
    return mst

_minimum_spanning_tree_kruskal_adjacency_matrix = \
    _minimum_spanning_tree_kruskal_adjacency_list

def _minimum_spanning_tree_prim_adjacency_list(graph):
    q = PriorityQueue(implementation='binomial_heap')
    e = {}
    mst = Graph(implementation='adjacency_list')
    q.push(next(iter(graph.vertices)), 0)
    while not q.is_empty:
        v = q.pop()
        if not hasattr(mst, v):
            mst.add_vertex(graph.__getattribute__(v))
            if e.get(v, None) is not None:
                edge = e[v]
                mst.add_vertex(edge.target)
                mst.add_edge(edge.source.name, edge.target.name, edge.value)
                mst.add_edge(edge.target.name, edge.source.name, edge.value)
            for w_node in graph.neighbors(v):
                w = w_node.name
                vw = graph.edge_weights[v + '_' + w]
                q.push(w, vw.value)
                if e.get(w, None) is None or \
                    e[w].value > vw.value:
                    e[w] = vw
    return mst

def minimum_spanning_tree(graph, algorithm, **kwargs):
    """
    Computes a minimum spanning tree for the given
    graph and algorithm.

    Parameters
    ==========

    graph: Graph
        The graph whose minimum spanning tree
        has to be computed.
    algorithm: str
        The algorithm which should be used for
        computing a minimum spanning tree.
        Currently the following algorithms are
        supported,

        'kruskal' -> Kruskal's algorithm as given in [1].

        'prim' -> Prim's algorithm as given in [2].
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Returns
    =======

    mst: Graph
        A minimum spanning tree using the implementation
        same as the graph provided in the input.

    Examples
    ========

    >>> from pydatastructs import Graph, AdjacencyListGraphNode
    >>> from pydatastructs import minimum_spanning_tree
    >>> u = AdjacencyListGraphNode('u')
    >>> v = AdjacencyListGraphNode('v')
    >>> G = Graph(u, v)
    >>> G.add_edge(u.name, v.name, 3)
    >>> mst = minimum_spanning_tree(G, 'kruskal')
    >>> u_n = mst.neighbors(u.name)
    >>> mst.get_edge(u.name, u_n[0].name).value
    3

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Kruskal%27s_algorithm
    .. [2] https://en.wikipedia.org/wiki/Prim%27s_algorithm

    Note
    ====

    The concept of minimum spanning tree is valid only for
    connected and undirected graphs. So, this function
    should be used only for such graphs. Using with other
    types of graphs may lead to unwanted results.
    """
    raise_if_backend_is_not_python(
        minimum_spanning_tree, kwargs.get('backend', Backend.PYTHON))
    import pydatastructs.graphs.algorithms as algorithms
    func = "_minimum_spanning_tree_" + algorithm + "_" + graph._impl
    if not hasattr(algorithms, func):
        raise NotImplementedError(
        "Currently %s algoithm for %s implementation of graphs "
        "isn't implemented for finding minimum spanning trees."
        %(algorithm, graph._impl))
    return getattr(algorithms, func)(graph)

def _minimum_spanning_tree_parallel_kruskal_adjacency_list(graph, num_threads):
    mst = _generate_mst_object(graph)
    dsf = DisjointSetForest()
    for v in graph.vertices:
        dsf.make_set(v)
    edges = _sort_edges(graph, num_threads)
    for _, edge in edges:
        u, v = edge.source.name, edge.target.name
        if dsf.find_root(u) is not dsf.find_root(v):
            mst.add_edge(u, v, edge.value)
            mst.add_edge(v, u, edge.value)
            dsf.union(u, v)
    return mst

_minimum_spanning_tree_parallel_kruskal_adjacency_matrix = \
    _minimum_spanning_tree_parallel_kruskal_adjacency_list

def _find_min(q, v, i):
    if not q.is_empty:
        v[i] = q.peek
    else:
        v[i] = None

def _minimum_spanning_tree_parallel_prim_adjacency_list(graph, num_threads):
    q = [PriorityQueue(implementation='binomial_heap') for _ in range(num_threads)]
    e = [{} for _ in range(num_threads)]
    v2q = {}
    mst = Graph(implementation='adjacency_list')

    itr = iter(graph.vertices)
    for i in range(len(graph.vertices)):
        v2q[next(itr)] = i%len(q)
    q[0].push(next(iter(graph.vertices)), 0)

    while True:

        _vs = [None for _ in range(num_threads)]
        with ThreadPoolExecutor(max_workers=num_threads) as Executor:
            for i in range(num_threads):
                Executor.submit(_find_min, q[i], _vs, i).result()
        v = None

        for i in range(num_threads):
            if _comp(_vs[i], v, lambda u, v: u.key < v.key):
                v = _vs[i]
        if v is None:
            break
        v = v.data
        idx = v2q[v]
        q[idx].pop()

        if not hasattr(mst, v):
            mst.add_vertex(graph.__getattribute__(v))
            if e[idx].get(v, None) is not None:
                edge = e[idx][v]
                mst.add_vertex(edge.target)
                mst.add_edge(edge.source.name, edge.target.name, edge.value)
                mst.add_edge(edge.target.name, edge.source.name, edge.value)
            for w_node in graph.neighbors(v):
                w = w_node.name
                vw = graph.edge_weights[v + '_' + w]
                j = v2q[w]
                q[j].push(w, vw.value)
                if e[j].get(w, None) is None or \
                    e[j][w].value > vw.value:
                    e[j][w] = vw

    return mst

def minimum_spanning_tree_parallel(graph, algorithm, num_threads, **kwargs):
    """
    Computes a minimum spanning tree for the given
    graph and algorithm using the given number of threads.

    Parameters
    ==========

    graph: Graph
        The graph whose minimum spanning tree
        has to be computed.
    algorithm: str
        The algorithm which should be used for
        computing a minimum spanning tree.
        Currently the following algorithms are
        supported,

        'kruskal' -> Kruskal's algorithm as given in [1].

        'prim' -> Prim's algorithm as given in [2].
    num_threads: int
        The number of threads to be used.
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Returns
    =======

    mst: Graph
        A minimum spanning tree using the implementation
        same as the graph provided in the input.

    Examples
    ========

    >>> from pydatastructs import Graph, AdjacencyListGraphNode
    >>> from pydatastructs import minimum_spanning_tree_parallel
    >>> u = AdjacencyListGraphNode('u')
    >>> v = AdjacencyListGraphNode('v')
    >>> G = Graph(u, v)
    >>> G.add_edge(u.name, v.name, 3)
    >>> mst = minimum_spanning_tree_parallel(G, 'kruskal', 3)
    >>> u_n = mst.neighbors(u.name)
    >>> mst.get_edge(u.name, u_n[0].name).value
    3

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Kruskal%27s_algorithm#Parallel_algorithm
    .. [2] https://en.wikipedia.org/wiki/Prim%27s_algorithm#Parallel_algorithm

    Note
    ====

    The concept of minimum spanning tree is valid only for
    connected and undirected graphs. So, this function
    should be used only for such graphs. Using with other
    types of graphs will lead to unwanted results.
    """
    raise_if_backend_is_not_python(
        minimum_spanning_tree_parallel, kwargs.get('backend', Backend.PYTHON))
    import pydatastructs.graphs.algorithms as algorithms
    func = "_minimum_spanning_tree_parallel_" + algorithm + "_" + graph._impl
    if not hasattr(algorithms, func):
        raise NotImplementedError(
        "Currently %s algoithm for %s implementation of graphs "
        "isn't implemented for finding minimum spanning trees."
        %(algorithm, graph._impl))
    return getattr(algorithms, func)(graph, num_threads)

def _visit(graph, vertex, visited, incoming, L):
    stack = [vertex]
    while stack:
        top = stack[-1]
        if not visited.get(top, False):
            visited[top] = True
            for node in graph.neighbors(top):
                if incoming.get(node.name, None) is None:
                    incoming[node.name] = []
                incoming[node.name].append(top)
                if not visited.get(node.name, False):
                    stack.append(node.name)
        if top is stack[-1]:
            L.append(stack.pop())

def _assign(graph, u, incoming, assigned, component):
    stack = [u]
    while stack:
        top = stack[-1]
        if not assigned.get(top, False):
            assigned[top] = True
            component.add(top)
            for u in incoming[top]:
                if not assigned.get(u, False):
                    stack.append(u)
        if top is stack[-1]:
            stack.pop()

def _strongly_connected_components_kosaraju_adjacency_list(graph):
    visited, incoming, L = {}, {}, []
    for u in graph.vertices:
        if not visited.get(u, False):
            _visit(graph, u, visited, incoming, L)

    assigned = {}
    components = []
    for i in range(-1, -len(L) - 1, -1):
        comp = set()
        if not assigned.get(L[i], False):
            _assign(graph, L[i], incoming, assigned, comp)
        if comp:
            components.append(comp)

    return components

_strongly_connected_components_kosaraju_adjacency_matrix = \
    _strongly_connected_components_kosaraju_adjacency_list

def strongly_connected_components(graph, algorithm, **kwargs):
    """
    Computes strongly connected components for the given
    graph and algorithm.

    Parameters
    ==========

    graph: Graph
        The graph whose minimum spanning tree
        has to be computed.
    algorithm: str
        The algorithm which should be used for
        computing strongly connected components.
        Currently the following algorithms are
        supported,

        'kosaraju' -> Kosaraju's algorithm as given in [1].
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Returns
    =======

    components: list
        Python list with each element as set of vertices.

    Examples
    ========

    >>> from pydatastructs import Graph, AdjacencyListGraphNode
    >>> from pydatastructs import strongly_connected_components
    >>> v1, v2, v3 = [AdjacencyListGraphNode(i) for i in range(3)]
    >>> g = Graph(v1, v2, v3)
    >>> g.add_edge(v1.name, v2.name)
    >>> g.add_edge(v2.name, v3.name)
    >>> g.add_edge(v3.name, v1.name)
    >>> scc = strongly_connected_components(g, 'kosaraju')
    >>> scc == [{'2', '0', '1'}]
    True

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Kosaraju%27s_algorithm

    """
    raise_if_backend_is_not_python(
        strongly_connected_components, kwargs.get('backend', Backend.PYTHON))
    import pydatastructs.graphs.algorithms as algorithms
    func = "_strongly_connected_components_" + algorithm + "_" + graph._impl
    if not hasattr(algorithms, func):
        raise NotImplementedError(
        "Currently %s algoithm for %s implementation of graphs "
        "isn't implemented for finding strongly connected components."
        %(algorithm, graph._impl))
    return getattr(algorithms, func)(graph)

def depth_first_search(
    graph, source_node, operation, *args, **kwargs):
    """
    Implementation of depth first search (DFS)
    algorithm.

    Parameters
    ==========

    graph: Graph
        The graph on which DFS is to be performed.
    source_node: str
        The name of the source node from where the DFS is
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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

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
    >>> from pydatastructs import depth_first_search
    >>> def f(curr_node, next_node, dest_node):
    ...     return curr_node != dest_node
    ...
    >>> G.add_edge(V1.name, V2.name)
    >>> G.add_edge(V2.name, V3.name)
    >>> depth_first_search(G, V1.name, f, V3.name)

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Depth-first_search
    """
    raise_if_backend_is_not_python(
        depth_first_search, kwargs.get('backend', Backend.PYTHON))
    import pydatastructs.graphs.algorithms as algorithms
    func = "_depth_first_search_" + graph._impl
    if not hasattr(algorithms, func):
        raise NotImplementedError(
        "Currently depth first search isn't implemented for "
        "%s graphs."%(graph._impl))
    return getattr(algorithms, func)(
           graph, source_node, operation, *args, **kwargs)

def _depth_first_search_adjacency_list(
    graph, source_node, operation, *args, **kwargs):
    dfs_stack = Stack()
    visited = {}
    dfs_stack.append(source_node)
    visited[source_node] = True
    while len(dfs_stack) != 0:
        curr_node = dfs_stack.pop()
        next_nodes = graph.neighbors(curr_node)
        if len(next_nodes) != 0:
            for next_node in next_nodes:
                if next_node.name not in visited:
                    status = operation(curr_node, next_node.name, *args, **kwargs)
                    if not status:
                        return None
                    dfs_stack.append(next_node.name)
                    visited[next_node.name] = True
        else:
            status = operation(curr_node, "", *args, **kwargs)
            if not status:
                return None

_depth_first_search_adjacency_matrix = _depth_first_search_adjacency_list

def shortest_paths(graph: Graph, algorithm: str,
                   source: str, target: str="",
                   **kwargs) -> tuple:
    """
    Finds shortest paths in the given graph from a given source.

    Parameters
    ==========

    graph: Graph
        The graph under consideration.
    algorithm: str
        The algorithm to be used. Currently, the following algorithms
        are implemented,

        'bellman_ford' -> Bellman-Ford algorithm as given in [1].

        'dijkstra' -> Dijkstra algorithm as given in [2].
    source: str
        The name of the source the node.
    target: str
        The name of the target node.
        Optional, by default, all pair shortest paths
        are returned.
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Returns
    =======

    (distances, predecessors): (dict, dict)
        If target is not provided and algorithm used
        is 'bellman_ford'/'dijkstra'.
    (distances[target], predecessors): (float, dict)
        If target is provided and algorithm used is
        'bellman_ford'/'dijkstra'.

    Examples
    ========

    >>> from pydatastructs import Graph, AdjacencyListGraphNode
    >>> from pydatastructs import shortest_paths
    >>> V1 = AdjacencyListGraphNode("V1")
    >>> V2 = AdjacencyListGraphNode("V2")
    >>> V3 = AdjacencyListGraphNode("V3")
    >>> G = Graph(V1, V2, V3)
    >>> G.add_edge('V2', 'V3', 10)
    >>> G.add_edge('V1', 'V2', 11)
    >>> shortest_paths(G, 'bellman_ford', 'V1')
    ({'V1': 0, 'V2': 11, 'V3': 21}, {'V1': None, 'V2': 'V1', 'V3': 'V2'})
    >>> shortest_paths(G, 'dijkstra', 'V1')
    ({'V2': 11, 'V3': 21, 'V1': 0}, {'V1': None, 'V2': 'V1', 'V3': 'V2'})

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm
    .. [2] https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    """
    raise_if_backend_is_not_python(
        shortest_paths, kwargs.get('backend', Backend.PYTHON))
    import pydatastructs.graphs.algorithms as algorithms
    func = "_" + algorithm + "_" + graph._impl
    if not hasattr(algorithms, func):
        raise NotImplementedError(
        "Currently %s algorithm isn't implemented for "
        "finding shortest paths in graphs."%(algorithm))
    return getattr(algorithms, func)(graph, source, target)

def _bellman_ford_adjacency_list(graph: Graph, source: str, target: str) -> tuple:
    distances, predecessor = {}, {}

    for v in graph.vertices:
        distances[v] = float('inf')
        predecessor[v] = None
    distances[source] = 0

    edges = graph.edge_weights.values()
    for _ in range(len(graph.vertices) - 1):
        for edge in edges:
            u, v = edge.source.name, edge.target.name
            w = edge.value
            if distances[u] + edge.value < distances[v]:
                distances[v] = distances[u] + w
                predecessor[v] = u

    for edge in edges:
        u, v = edge.source.name, edge.target.name
        w = edge.value
        if distances[u] + w < distances[v]:
            raise ValueError("Graph contains a negative weight cycle.")

    if target != "":
        return (distances[target], predecessor)
    return (distances, predecessor)

_bellman_ford_adjacency_matrix = _bellman_ford_adjacency_list

def _dijkstra_adjacency_list(graph: Graph, start: str, target: str):
    V = len(graph.vertices)
    visited, dist, pred = {}, {}, {}
    for v in graph.vertices:
        visited[v] = False
        pred[v] = None
        if v != start:
            dist[v] = float('inf')
    dist[start] = 0
    pq = PriorityQueue(implementation='binomial_heap')
    for vertex in dist:
        pq.push(vertex, dist[vertex])
    for _ in range(V):
        u = pq.pop()
        visited[u] = True
        for v in graph.vertices:
            edge_str = u + '_' + v
            if (edge_str in graph.edge_weights and graph.edge_weights[edge_str].value > 0 and
                visited[v] is False and dist[v] > dist[u] + graph.edge_weights[edge_str].value):
                dist[v] = dist[u] + graph.edge_weights[edge_str].value
                pred[v] = u
                pq.push(v, dist[v])

    if target != "":
        return (dist[target], pred)
    return dist, pred

_dijkstra_adjacency_matrix = _dijkstra_adjacency_list

def all_pair_shortest_paths(graph: Graph, algorithm: str,
                            **kwargs) -> tuple:
    """
    Finds shortest paths between all pairs of vertices in the given graph.

    Parameters
    ==========

    graph: Graph
        The graph under consideration.
    algorithm: str
        The algorithm to be used. Currently, the following algorithms
        are implemented,

        'floyd_warshall' -> Floyd Warshall algorithm as given in [1].
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Returns
    =======

    (distances, predecessors): (dict, dict)

    Examples
    ========

    >>> from pydatastructs import Graph, AdjacencyListGraphNode
    >>> from pydatastructs import all_pair_shortest_paths
    >>> V1 = AdjacencyListGraphNode("V1")
    >>> V2 = AdjacencyListGraphNode("V2")
    >>> V3 = AdjacencyListGraphNode("V3")
    >>> G = Graph(V1, V2, V3)
    >>> G.add_edge('V2', 'V3', 10)
    >>> G.add_edge('V1', 'V2', 11)
    >>> G.add_edge('V3', 'V1', 5)
    >>> dist, _ = all_pair_shortest_paths(G, 'floyd_warshall')
    >>> dist['V1']['V3']
    21
    >>> dist['V3']['V1']
    5

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
    """
    raise_if_backend_is_not_python(
        all_pair_shortest_paths, kwargs.get('backend', Backend.PYTHON))
    import pydatastructs.graphs.algorithms as algorithms
    func = "_" + algorithm + "_" + graph._impl
    if not hasattr(algorithms, func):
        raise NotImplementedError(
        "Currently %s algorithm isn't implemented for "
        "finding shortest paths in graphs."%(algorithm))
    return getattr(algorithms, func)(graph)

def _floyd_warshall_adjacency_list(graph: Graph):
    dist, next_vertex = {}, {}
    V, E = graph.vertices, graph.edge_weights

    for v in V:
        dist[v] = {}
        next_vertex[v] = {}

    for name, edge in E.items():
        dist[edge.source.name][edge.target.name] = edge.value
        next_vertex[edge.source.name][edge.target.name] = edge.source.name

    for v in V:
        dist[v][v] = 0
        next_vertex[v][v] = v

    for k in V:
        for i in V:
            for j in V:
                dist_i_j = dist.get(i, {}).get(j, float('inf'))
                dist_i_k = dist.get(i, {}).get(k, float('inf'))
                dist_k_j = dist.get(k, {}).get(j, float('inf'))
                next_i_k = next_vertex.get(i + '_' + k, None)
                if dist_i_j > dist_i_k + dist_k_j:
                    dist[i][j] = dist_i_k + dist_k_j
                    next_vertex[i][j] = next_i_k

    return (dist, next_vertex)

_floyd_warshall_adjacency_matrix = _floyd_warshall_adjacency_list

def topological_sort(graph: Graph, algorithm: str,
                     **kwargs) -> list:
    """
    Performs topological sort on the given graph using given algorithm.

    Parameters
    ==========

    graph: Graph
        The graph under consideration.
    algorithm: str
        The algorithm to be used.
        Currently, following are supported,

        'kahn' -> Kahn's algorithm as given in [1].
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Returns
    =======

    list
        The list of topologically sorted vertices.

    Examples
    ========

    >>> from pydatastructs import Graph, AdjacencyListGraphNode, topological_sort
    >>> v_1 = AdjacencyListGraphNode('v_1')
    >>> v_2 = AdjacencyListGraphNode('v_2')
    >>> graph = Graph(v_1, v_2)
    >>> graph.add_edge('v_1', 'v_2')
    >>> topological_sort(graph, 'kahn')
    ['v_1', 'v_2']

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm
    """
    raise_if_backend_is_not_python(
        topological_sort, kwargs.get('backend', Backend.PYTHON))
    import pydatastructs.graphs.algorithms as algorithms
    func = "_" + algorithm + "_" + graph._impl
    if not hasattr(algorithms, func):
        raise NotImplementedError(
        "Currently %s algorithm isn't implemented for "
        "performing topological sort on %s graphs."%(algorithm, graph._impl))
    return getattr(algorithms, func)(graph)

def _kahn_adjacency_list(graph: Graph) -> list:
    S = Queue()
    in_degree = {u: 0 for u in graph.vertices}
    for u in graph.vertices:
        for v in graph.neighbors(u):
            in_degree[v.name] += 1
    for u in graph.vertices:
        if in_degree[u] == 0:
            S.append(u)
            in_degree.pop(u)

    L = []
    while S:
        n = S.popleft()
        L.append(n)
        for m in graph.neighbors(n):
            graph.remove_edge(n, m.name)
            in_degree[m.name] -= 1
            if in_degree[m.name] == 0:
                S.append(m.name)
                in_degree.pop(m.name)

    if in_degree:
        raise ValueError("Graph is not acyclic.")
    return L

def topological_sort_parallel(graph: Graph, algorithm: str, num_threads: int,
                              **kwargs) -> list:
    """
    Performs topological sort on the given graph using given algorithm using
    given number of threads.

    Parameters
    ==========

    graph: Graph
        The graph under consideration.
    algorithm: str
        The algorithm to be used.
        Currently, following are supported,

        'kahn' -> Kahn's algorithm as given in [1].
    num_threads: int
        The maximum number of threads to be used.
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Returns
    =======

    list
        The list of topologically sorted vertices.

    Examples
    ========

    >>> from pydatastructs import Graph, AdjacencyListGraphNode, topological_sort_parallel
    >>> v_1 = AdjacencyListGraphNode('v_1')
    >>> v_2 = AdjacencyListGraphNode('v_2')
    >>> graph = Graph(v_1, v_2)
    >>> graph.add_edge('v_1', 'v_2')
    >>> topological_sort_parallel(graph, 'kahn', 1)
    ['v_1', 'v_2']

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm
    """
    raise_if_backend_is_not_python(
        topological_sort_parallel, kwargs.get('backend', Backend.PYTHON))
    import pydatastructs.graphs.algorithms as algorithms
    func = "_" + algorithm + "_" + graph._impl + '_parallel'
    if not hasattr(algorithms, func):
        raise NotImplementedError(
        "Currently %s algorithm isn't implemented for "
        "performing topological sort on %s graphs."%(algorithm, graph._impl))
    return getattr(algorithms, func)(graph, num_threads)

def _kahn_adjacency_list_parallel(graph: Graph, num_threads: int) -> list:
    num_vertices = len(graph.vertices)

    def _collect_source_nodes(graph: Graph) -> list:
        S = []
        in_degree = {u: 0 for u in graph.vertices}
        for u in graph.vertices:
            for v in graph.neighbors(u):
                in_degree[v.name] += 1
        for u in in_degree:
            if in_degree[u] == 0:
                S.append(u)
        return list(S)

    def _job(graph: Graph, u: str):
        for v in graph.neighbors(u):
            graph.remove_edge(u, v.name)

    L = []
    source_nodes = _collect_source_nodes(graph)
    while source_nodes:
        with ThreadPoolExecutor(max_workers=num_threads) as Executor:
            for node in source_nodes:
                L.append(node)
                Executor.submit(_job, graph, node)
        for node in source_nodes:
            graph.remove_vertex(node)
        source_nodes = _collect_source_nodes(graph)

    if len(L) != num_vertices:
        raise ValueError("Graph is not acyclic.")
    return L


def _breadth_first_search_max_flow(graph: Graph, source_node, sink_node, flow_passed, for_dinic=False):
    bfs_queue = Queue()
    parent, currentPathC = {}, {}
    currentPathC[source_node] = float('inf')
    bfs_queue.append(source_node)
    while len(bfs_queue) != 0:
        curr_node = bfs_queue.popleft()
        next_nodes = graph.neighbors(curr_node)
        if len(next_nodes) != 0:
            for next_node in next_nodes:
                capacity = graph.get_edge(curr_node, next_node.name).value
                fp = flow_passed.get((curr_node, next_node.name), 0)
                if capacity and parent.get(next_node.name, False) is False and capacity - fp > 0:
                    parent[next_node.name] = curr_node
                    next_flow = min(currentPathC[curr_node], capacity - fp)
                    currentPathC[next_node.name] = next_flow
                    if next_node.name == sink_node and not for_dinic:
                        return (next_flow, parent)
                    bfs_queue.append(next_node.name)
    return (0, parent)


def _max_flow_edmonds_karp_(graph: Graph, source, sink):
    m_flow = 0
    flow_passed = {}
    new_flow, parent = _breadth_first_search_max_flow(graph, source, sink, flow_passed)
    while new_flow != 0:
        m_flow += new_flow
        current = sink
        while current != source:
            prev = parent[current]
            fp = flow_passed.get((prev, current), 0)
            flow_passed[(prev, current)] = fp + new_flow
            fp = flow_passed.get((current, prev), 0)
            flow_passed[(current, prev)] = fp - new_flow
            current = prev
        new_flow, parent = _breadth_first_search_max_flow(graph, source, sink, flow_passed)
    return m_flow


def _depth_first_search_max_flow_dinic(graph: Graph, u, parent, sink_node, flow, flow_passed):
    if u == sink_node:
        return flow

    next_nodes = graph.neighbors(u)
    if len(next_nodes) != 0:
        for next_node in next_nodes:
            capacity = graph.get_edge(u, next_node.name).value
            fp = flow_passed.get((u, next_node.name), 0)
            parent_cond = parent.get(next_node.name, None)
            if parent_cond and parent_cond == u and capacity - fp > 0:
                path_flow = _depth_first_search_max_flow_dinic(graph,
                                                               next_node.name,
                                                               parent, sink_node,
                                min(flow, capacity - fp), flow_passed)
                if path_flow > 0:
                    fp = flow_passed.get((u, next_node.name), 0)
                    flow_passed[(u, next_node.name)] = fp + path_flow
                    fp = flow_passed.get((next_node.name, u), 0)
                    flow_passed[(next_node.name, u)] = fp - path_flow
                    return path_flow
    return 0


def _max_flow_dinic_(graph: Graph, source, sink):
    max_flow = 0
    flow_passed = {}
    while True:
        next_flow, parent = _breadth_first_search_max_flow(graph, source, sink, flow_passed, True)
        if parent.get(sink, False) is False:
            break

        while True:
            path_flow = _depth_first_search_max_flow_dinic(graph, source,
                                                           parent, sink,
                                                           float('inf'),
                                                           flow_passed)
            if path_flow <= 0:
                break
            max_flow += path_flow

    return max_flow


def max_flow(graph, source, sink, algorithm='edmonds_karp', **kwargs):
    raise_if_backend_is_not_python(
        max_flow, kwargs.get('backend', Backend.PYTHON))

    import pydatastructs.graphs.algorithms as algorithms
    func = "_max_flow_" + algorithm + "_"
    if not hasattr(algorithms, func):
        raise NotImplementedError(
        f"Currently {algorithm} algorithm isn't implemented for "
        "performing max flow on graphs.")
    return getattr(algorithms, func)(graph, source, sink)
