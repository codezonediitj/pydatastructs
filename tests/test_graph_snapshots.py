import unittest
import time
from pydatastructs.graphs import Graph
from pydatastructs.utils import AdjacencyListGraphNode, AdjacencyMatrixGraphNode

class TestGraphSnapshots(unittest.TestCase):
    def test_snapshot_creation(self):
        graph = Graph(implementation='adjacency_list')
        graph.add_vertex(AdjacencyListGraphNode("A"))
        graph.add_vertex(AdjacencyListGraphNode("B"))
        graph.add_edge("A", "B", cost=5)
        graph.add_snapshot()

        self.assertEqual(len(graph.list_snapshots()), 1)

    def test_snapshot_retrieval(self):
        graph = Graph(implementation='adjacency_list')
        graph.add_vertex(AdjacencyListGraphNode("A"))
        graph.add_vertex(AdjacencyListGraphNode("B"))
        graph.add_edge("A", "B", cost=5)
        graph.add_snapshot()
        snapshot_time = graph.list_snapshots()[0]
        retrieved_graph = graph.get_snapshot(snapshot_time)
        self.assertEqual(retrieved_graph.is_adjacent("A", "B"), True)

    def test_invalid_snapshot(self):
        graph = Graph(implementation='adjacency_list')
        with self.assertRaises(ValueError):
            graph.get_snapshot(9999999999) 

if __name__ == '__main__':
    unittest.main()

