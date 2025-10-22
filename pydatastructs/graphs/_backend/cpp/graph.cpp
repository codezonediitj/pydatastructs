#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "AdjacencyList.hpp"
#include "AdjacencyMatrix.hpp"
#include "AdjacencyListGraphNode.hpp"
#include "AdjacencyMatrixGraphNode.hpp"
#include "GraphEdge.hpp"
#include "GraphNode.hpp"
#include "graph_bindings.hpp"
#include "Algorithms.hpp"

static PyMethodDef GraphMethods[] = {
    {"bfs_adjacency_list", (PyCFunction)breadth_first_search_adjacency_list, METH_VARARGS | METH_KEYWORDS, "Run BFS on adjacency list with callback"},
    {"bfs_adjacency_matrix", (PyCFunction)breadth_first_search_adjacency_matrix, METH_VARARGS | METH_KEYWORDS, "Run BFS on adjacency matrix with callback"},
    {"dfs_adjacency_list", (PyCFunction)depth_first_search_adjacency_list, METH_VARARGS | METH_KEYWORDS, "Run DFS on adjacency list with callback"},
    {"dfs_adjacency_matrix", (PyCFunction)depth_first_search_adjacency_matrix, METH_VARARGS | METH_KEYWORDS, "Run DFS on adjacency matrix with callback"},
    {"minimum_spanning_tree_prim_adjacency_list", (PyCFunction)minimum_spanning_tree_prim_adjacency_list, METH_VARARGS | METH_KEYWORDS, "Run Prim's algorithm on adjacency list"},
    {"shortest_paths_dijkstra_adjacency_list", (PyCFunction)shortest_paths_dijkstra_adjacency_list, METH_VARARGS | METH_KEYWORDS, "Dijkstra's algorithm for adjacency list graphs"},
    {"shortest_paths_bellman_ford_adjacency_list", (PyCFunction)shortest_paths_bellman_ford_adjacency_list, METH_VARARGS | METH_KEYWORDS, "Bellman-Ford algorithm for adjacency list graphs"},  // Add this line
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef graph_module = {
    PyModuleDef_HEAD_INIT,
    "_graph",
    "C++ module for graphs",
    -1,
    GraphMethods,
};

PyMODINIT_FUNC PyInit__graph(void) {
    PyObject* m;

    if (PyType_Ready(&GraphNodeType) < 0)
        return NULL;

    if (PyType_Ready(&AdjacencyListGraphNodeType) < 0)
        return NULL;

    if (PyType_Ready(&AdjacencyMatrixGraphNodeType) < 0)
        return NULL;

    if (PyType_Ready(&GraphEdgeType) < 0)
        return NULL;

    if (PyType_Ready(&AdjacencyListGraphType) < 0)
        return NULL;

    if (PyType_Ready(&AdjacencyMatrixGraphType) < 0)
        return NULL;

    m = PyModule_Create(&graph_module);
    if (m == NULL)
        return NULL;

    Py_INCREF(&GraphNodeType);
    PyModule_AddObject(m, "GraphNode", (PyObject*)&GraphNodeType);

    Py_INCREF(&AdjacencyListGraphNodeType);
    PyModule_AddObject(m, "AdjacencyListGraphNode", (PyObject*)&AdjacencyListGraphNodeType);

    Py_INCREF(&AdjacencyMatrixGraphNodeType);
    PyModule_AddObject(m, "AdjacencyMatrixGraphNode", (PyObject*)&AdjacencyMatrixGraphNodeType);

    Py_INCREF(&GraphEdgeType);
    PyModule_AddObject(m, "GraphEdge", (PyObject*)&GraphEdgeType);

    Py_INCREF(&AdjacencyListGraphType);
    if (PyModule_AddObject(m, "AdjacencyListGraph", (PyObject*)&AdjacencyListGraphType) < 0) {
        Py_DECREF(&AdjacencyListGraphType);
        Py_DECREF(m);
        return NULL;
    }

    Py_INCREF(&AdjacencyMatrixGraphType);
    if (PyModule_AddObject(m, "AdjacencyMatrixGraph", (PyObject*)&AdjacencyMatrixGraphType) < 0) {
        Py_DECREF(&AdjacencyMatrixGraphType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
