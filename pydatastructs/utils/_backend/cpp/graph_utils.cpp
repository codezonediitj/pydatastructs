#include <Python.h>
#include "GraphNode.hpp"
#include "AdjacencyListGraphNode.hpp"
#include "AdjacencyMatrixGraphNode.hpp"
#include "GraphEdge.hpp"
#include "graph_bindings.hpp"

static struct PyModuleDef graph_utils_struct = {
    PyModuleDef_HEAD_INIT,
    "_graph_utils",
    0,
    -1,
    NULL,
};

PyMODINIT_FUNC PyInit__graph_utils(void) {
    Py_Initialize();
    PyObject *utils = PyModule_Create(&graph_utils_struct);

    if (PyType_Ready(&GraphNodeType) < 0) {
        return NULL;
    }
    Py_INCREF(&GraphNodeType);
    PyModule_AddObject(utils, "GraphNode", reinterpret_cast<PyObject*>(&GraphNodeType));

    if (PyType_Ready(&AdjacencyMatrixGraphNodeType) < 0) {
        return NULL;
    }
    Py_INCREF(&AdjacencyMatrixGraphNodeType);
    PyModule_AddObject(utils, "AdjacencyMatrixGraphNode", reinterpret_cast<PyObject*>(&AdjacencyMatrixGraphNodeType));

    if (PyType_Ready(&AdjacencyListGraphNodeType) < 0) {
        return NULL;
    }
    Py_INCREF(&AdjacencyListGraphNodeType);
    PyModule_AddObject(utils, "AdjacencyListGraphNode", reinterpret_cast<PyObject*>(&AdjacencyListGraphNodeType));

    if (PyType_Ready(&GraphEdgeType) < 0) {
        return NULL;
    }
    Py_INCREF(&GraphEdgeType);
    PyModule_AddObject(utils, "GraphEdge", reinterpret_cast<PyObject*>(&GraphEdgeType));

    return utils;
}
