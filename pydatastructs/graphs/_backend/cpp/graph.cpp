#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "AdjacencyList.hpp"
#include "AdjacencyListGraphNode.hpp"
#include "graph_bindings.hpp"



static struct PyModuleDef graph_module = {
    PyModuleDef_HEAD_INIT,
    "_graph",
    "C++ module for graphs",
    -1,
    NULL,
};

PyMODINIT_FUNC PyInit__graph(void) {
    PyObject* m;

    if (PyType_Ready(&AdjacencyListGraphType) < 0)
        return NULL;

    if (PyType_Ready(&AdjacencyListGraphNodeType) < 0)
        return NULL;

    m = PyModule_Create(&graph_module);
    if (m == NULL)
        return NULL;

    Py_INCREF(&AdjacencyListGraphType);
    if (PyModule_AddObject(m, "AdjacencyListGraph", (PyObject*)&AdjacencyListGraphType) < 0) {
        Py_DECREF(&AdjacencyListGraphType);
        Py_DECREF(m);
        return NULL;
    }

    Py_INCREF(&AdjacencyListGraphNodeType);
    if (PyModule_AddObject(m, "AdjacencyListGraphNode", (PyObject*)&AdjacencyListGraphNodeType) < 0) {
        Py_DECREF(&AdjacencyListGraphNodeType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}