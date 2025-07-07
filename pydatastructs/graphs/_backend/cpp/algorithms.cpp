#include <Python.h>
#include "Algorithms.hpp"
#include "AdjacencyList.hpp"
#include "AdjacencyMatrix.hpp"

static PyMethodDef AlgorithmsMethods[] = {
    {"bfs_adjacency_list", (PyCFunction)breadth_first_search_adjacency_list, METH_VARARGS | METH_KEYWORDS, "Run BFS on adjacency list with callback"},
    {"bfs_adjacency_matrix", (PyCFunction)breadth_first_search_adjacency_matrix, METH_VARARGS | METH_KEYWORDS, "Run BFS on adjacency matrix with callback"},
    {"minimum_spanning_tree_prim_adjacency_list", (PyCFunction)minimum_spanning_tree_prim_adjacency_list, METH_VARARGS | METH_KEYWORDS, "Run Prim's algorithm on adjacency list"},
    {"shortest_paths_dijkstra_adjacency_list", (PyCFunction)shortest_paths_dijkstra_adjacency_list, METH_VARARGS | METH_KEYWORDS, "Dijkstra's algorithm for adjacency list graphs"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef algorithms_module = {
    PyModuleDef_HEAD_INIT,
    "_algorithms", NULL, -1, AlgorithmsMethods
};

PyMODINIT_FUNC PyInit__algorithms(void) {
    return PyModule_Create(&algorithms_module);
}
