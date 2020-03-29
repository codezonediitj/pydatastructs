"""
Contains all the algorithms associated with graph
data structure.
"""
from collections import deque as Queue
from concurrent.futures import ThreadPoolExecutor
from pydatastructs.utils import GraphEdge
from pydatastructs.utils.misc_util import _comp
from pydatastructs.miscellaneous_data_structures import (
    DisjointSetForest, PriorityQueue)
from pydatastructs.graphs.graph import Graph
from pydatastructs.linear_data_structures.algorithms import merge_sort_parallel
import math

__all__ = [
    'breadth_first_search',
    'breadth_first_search_parallel',
    'minimum_spanning_tree',
    'minimum_spanning_tree_parallel',
    'LCA_range_minquery',
    'LCA_binary_lifting'
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
    visited, layers = dict(), dict()
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
    e = dict()
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

def minimum_spanning_tree(graph, algorithm):
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
        'kruskal' -> Kruskal's algorithm as given in
                     [1].
        'prim' -> Prim's algorithm as given in [2].
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
    e = [dict() for _ in range(num_threads)]
    v2q = dict()
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

def minimum_spanning_tree_parallel(graph, algorithm, num_threads):
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
        'kruskal' -> Kruskal's algorithm as given in
                     [1].
        'prim' -> Prim's algorithm as given in [2].
    num_threads: int
        The number of threads to be used.
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
    import pydatastructs.graphs.algorithms as algorithms
    func = "_minimum_spanning_tree_parallel_" + algorithm + "_" + graph._impl
    if not hasattr(algorithms, func):
        raise NotImplementedError(
        "Currently %s algoithm for %s implementation of graphs "
        "isn't implemented for finding minimum spanning trees."
        %(algorithm, graph._impl))
    return getattr(algorithms, func)(graph, num_threads)


class LCA_binary_lifting:
    """
    To query Lowest common ancestor between two nodes a and b of a connected Graph with 
    no cycles
    Algorithm used here is Binary Lifting 
    Class functions
    ===============
    constructor : takes number of vertices of a graph


    preprocess(graph, node)
    =====================
    to do the pre processing needed to done before querying
        Parameters
        ===========
        graph:Graph
            The graph on which you want to query LCA
        node: int
            Root node of the tree
        Returns
        =======
        NULL


    lca(u , v)
    ==========
    to get lowest common ancestor between nodes u and v
        Parameters
        ===========
        a: str
            first node
        b: str
            second node
        Returns
        ========
        str: LCA of u, v

    """
    def __init__(self, n):
        self.parent = [[-1 for i in range((2+int((math.log(n)/math.log(2)))))] for j in range(n)] 
        self.n = n
        self.logn = int(math.log(n)/math.log(2))+1
        self.level = [0]*n
        self.count = 0
        self.mapping = dict()
        self.revmap = ['']*n

    def dfs(self, graph, node, par):
        self.mapping[node] = self.count
        self.revmap[self.count] = node
        self.count = self.count + 1
        next_nodes = graph.neighbors(node)
        for next_node in next_nodes:
            if next_node.name != par :
                self.dfs(graph, next_node.name, node)

    def traverse(self, graph, node, par):
        x = self.mapping[node]
        self.parent[x][0] = par
        for i in range(1,self.logn+1):
            if self.parent[x][i-1] < 0:
                self.parent[x][i] = -1
            else:
                self.parent[x][i] = self.parent[(self.parent[x][i-1])][i-1]
        
        next_nodes = graph.neighbors(node)
        for next_node in next_nodes:
            if self.mapping[next_node.name] != par :
                self.level[self.mapping[next_node.name]] = self.level[x]+1
                self.traverse(graph, next_node.name, x)

    def preprocess(self, graph, node):
        self.node = node
        self.dfs(graph, node, '')
        self.traverse(graph, node, -1)

    def lca(self, a , b):
        u = self.mapping[a]
        v = self.mapping[b]

        if ((u > self.n) or (v > self.n)):
            return ''
        if self.level[u] < self.level[v]:
            temp = u
            u = v
            v = temp
        for i in reversed(range(0,1+self.logn)):
            if (self.level[u]-(1<<i)) >= self.level[v]:
                u = self.parent[u][i]
        if u == v:
            if u < 0:
                return self.node
            return self.revmap[u]
        for i in reversed(range(0,1+self.logn)):
            if self.parent[u][i] != self.parent[v][i]:
                u = self.parent[u][i]
                v = self.parent[v][i]
        if self.parent[u][0] < 0:
            return self.node
        return self.revmap[self.parent[u][0]]





class LCA_range_minquery:
    """
    To query Lowest common ancestor between two nodes a and b of a connected Graph with 
    no cycles
    Algorithm used here is Range Minimum Query with Eulars tour and DataStructure 
    used is Segment Tree 
    Class functions
    ===============
    constructor : takes number of vertices of a graph


    preprocess(graph, node)
    =====================
    to do the pre processing needed to done before querying
        Parameters
        ===========
        graph:Graph
            The graph on which you want to query LCA
        node: int
            Root node of the tree
        Returns
        =======
        NULL


    lca(u , v)
    ==========
    to get lowest common ancestor between nodes u and v
        Parameters
        ===========
        a: str
            first node
        b: str
            second node
        Returns
        ========
        str: LCA of u, v


    to Check
    ========

        from pydatastructs.graphs import Graph
        from pydatastructs.utils import AdjacencyListGraphNode
        v_1 = AdjacencyListGraphNode('0')
        v_2 = AdjacencyListGraphNode('1')
        v_3 = AdjacencyListGraphNode('2')
        v_4 = AdjacencyListGraphNode('3')
        v_5 = AdjacencyListGraphNode('4')
        g = Graph(v_1, v_2,v_3,v_4,v_5)
        g.add_edge('0', '2')
        g.add_edge('0', '1')
        g.add_edge('1', '3')
        g.add_edge('1', '4')

        No change even if this part is not added(ie same for directed and undirected)
        ==========
        g.add_edge('2','0')
        g.add_edge('1','0')
        g.add_edge('3','1')
        g.add_edge('4','1')
        =============

        x= LCA_binary_lifting(5)
        x.preprocess(g, '0')
        print(x.lca('3','4'))

    """
    def __init__(self, n):
        self.eular = [0]*(2*n-1)
        self.n = n
        self.fst_occur = [0]*(n)
        self.level = [0]*(2*n-1)
        self.ind = 0
        self.seg_tree = [0]*(4*n+2)
        self.count = 0
        self.mapping = dict()
        self.revmap = ['']*n

    def dfs(self, graph, node, par):
        self.mapping[node] = self.count
        self.revmap[self.count] = node
        self.count = self.count + 1
        next_nodes = graph.neighbors(node)
        # print(next_nodes)
        for next_node in next_nodes:
            # print(next_node)
            if next_node.name != par :
                self.dfs(graph, next_node.name, node)
                

    def traverse(self, graph, node, par, lev):
        self.fst_occur[self.mapping[node]] = self.ind
        self.eular[self.ind] = self.mapping[node]
        self.level[self.ind] = lev
        self.ind = self.ind +1
        next_nodes = graph.neighbors(node)
        for next_node in next_nodes:
            if self.mapping[next_node.name] != par :
                self.traverse(graph, next_node.name, self.mapping[node], lev+1)
                self.eular[self.ind] = self.mapping[node]
                self.level[self.ind] = lev
                self.ind = self.ind +1

    def build(self, a, b, node):
        # print(a)
        # print(b)
        if a == b:
            self.seg_tree[node] = a
            return 
        else:
            self.build(a, int((a+b)/2), 2*node)
            self.build(1+int((a+b)/2), b, 2*node+1)
            if self.level[self.seg_tree[2*node]] < self.level[self.seg_tree[2*node+1]]:
                self.seg_tree[node] = self.seg_tree[2*node]
            else:
                self.seg_tree[node] = self.seg_tree[2*node+1]


    def query(self, x, y, a, b, node):
        if x == y:
            return x
        if x <= a and y >= b:
            return self.seg_tree[node]
        elif y <= int((a+b)/2):
            return self.query(x, y, a, int((a+b)/2), 2*node)
        elif x > int((a+b)/2):
            return self.query(x, y, int((a+b)/2)+1, b, 2*node+1)
        else:
            h = self.query(x, y, a, int((a+b)/2), 2*node)
            k = self.query(x, y, int((a+b)/2)+1, b, 2*node+1)
            if self.level[h] < self.level[k]:
                return h
            else:
                return k


    def preprocess(self, graph, node):
        self.dfs(graph, node, 'usless_stuff')
        self.traverse(graph, node, -1, 0)
        self.build(0, self.ind-1, 1)


    def lca(self, a , b):
        u = self.mapping[a]
        v = self.mapping[b]
        if u > self.n or v > self.n:
            return -1
        x = self.fst_occur[u]
        y = self.fst_occur[v]
        if x > y:
            temp = x
            x = y
            y = temp
        i = self.query(x, y, 0, self.ind-1, 1)
        return self.revmap[self.eular[i]]




