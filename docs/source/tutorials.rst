Tutorials
=========

We provide the following tutorials to show how ``pydatastructs`` 
APIs can help in solving complicated data structures and algorithms 
problems easily. For now the problems are abstract. However, we plan 
to add some more examples showing usage of ``pydatastructs`` on real world 
data sets such as `Stanford Large Network Dataset Collection <https://snap.stanford.edu/data/>`_
and `Urban Dictionary Words And Definitions <https://www.kaggle.com/therohk/urban-dictionary-words-dataset>`_.
If you are interested in playing around with the above datasets using our API,
then please feel free to reach out to us on our community channels.

Max-Min Stream
--------------

In this problem, we will be dealing with a stream of integer numbers. We have to 
display the ``k``-th largest and ``k``-th smallest number for all the prefixes of the 
input stream. In simple words, after reading each number, we have to display 
the ``k``-th largest and ``k``-th smallest number up until that number in the stream. 
If the size of the stream is smaller than ``k`` then we will display the minimum 
for ``k``-th smallest and maximum for ``k``-th largest numbers respectively.

**Input Format**

The first line of input will contain the value, ``k``. After that, each line of 
input will contain an integer representing the new number of the stream. The stopping 
point of the stream will be denoted by 0. Note that stopping point i.e., 0 will also 
be considered a part of the input stream.

**Output Format**

Each line of the output should contain two space separated numbers, the first one 
representing the ``k``-th largest/maximum number and the second one representing 
the ``k``-th smallest/minimum number.

>>> from pydatastructs import BinaryHeap, Queue
>>> def modify_heaps(min_heap, max_heap, curr_num, k):
...     min_heap.insert(curr_num)
...     max_heap.insert(curr_num)
...     if min_heap.heap._num > k:
...         min_heap.extract()
...     if max_heap.heap._num > k:
...         max_heap.extract()
...     large, small = (max_heap.heap[0].key, min_heap.heap[0].key)
...     return large, small
... 
>>> min_heap = BinaryHeap(heap_property='min')
>>> max_heap = BinaryHeap(heap_property='max')
>>> k = 2
>>> curr_nums = Queue(items=[4, 5, 8, 0]) # input stream as a list
>>> curr_num = curr_nums.popleft()
>>> large_small = []
>>> while curr_num != 0:
...     large, small = modify_heaps(min_heap, max_heap, curr_num, k)
...     large_small.append((large, small))
...     curr_num = curr_nums.popleft()
... 
>>> large, small = modify_heaps(min_heap, max_heap, curr_num, k)
>>> large_small.append((large, small))
>>> print(large_small)
[(4, 4), (5, 4), (5, 5), (4, 5)]

Minimise Network Delay
----------------------

In this problem there will be a network containing ``N`` nodes, labelled as 1 ... ``N``, and ``E`` edges. 
Any two nodes may be connected by an undirected edge ``E(u, v)`` and introduces a delay of time ``t(u, v)`` 
in transfer of information between the nodes ``u`` and ``v``.

We will be given ``K`` queries where each query contains the source node and the destination node and 
we will be required to determine the minimum time it will take for a piece of information to start from 
the source node and reach at the destination node.

We will assume that the size of information and the processing time at any node doesn’t affect the  travel time.

**Input Format**

The first line will contain a single positive integer ``N``.

The second line will contain a single positive integer ``E``.

Then ``E`` lines will follow, each line containing three space separated integers. 
The first two denoting node labels connected by an undirected edge which introduces 
a time delay denoted by the third integer.

After that the next line will contain a positive integer ``K``.

Then ``K`` lines will follow each containing two space separated node labels, the 
first denoting the source node and the second one denoting the destination node for that query.

**Output Format**

``K`` lines, each containing the minimum time required for the ``k``-th query.

>>> from pydatastructs import Graph, AdjacencyListGraphNode
>>> from pydatastructs.graphs.algorithms import shortest_paths
>>> N = 4
>>> E = 3
>>> nodes = []
>>> for n in range(N):
...     nodes.append(AdjacencyListGraphNode(str(n + 1)))
... 
>>> u_v_t = [(1, 2, 1), (2, 3, 1), (3, 4, 1)] # edges and their time delay
>>> graph = Graph(*nodes)
>>> for e in range(E):
...     u, v, t = u_v_t[e]
...     graph.add_edge(str(u), str(v), t)
...     graph.add_edge(str(v), str(u), t)
... 
>>> K = 3
>>> u_v = [(1, 4), (3, 2), (4, 3)] # queries
>>> delays = []
>>> for k in range(K):
...     u, v = u_v[k]
...     delay = shortest_paths(graph, 'dijkstra', str(u))[0]
...     delays.append(delay[str(v)])
... 
>>> print(delays)
[3, 1, 1]