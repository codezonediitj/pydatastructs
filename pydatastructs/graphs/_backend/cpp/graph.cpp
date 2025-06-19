#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "AdjacencyList.hpp"
#include "AdjacencyMatrix.hpp"
#include "AdjacencyListGraphNode.hpp"
#include "AdjacencyMatrixGraphNode.hpp"
#include "graph_bindings.hpp"

#ifdef __cplusplus
extern "C" {
#endif

PyMODINIT_FUNC PyInit__graph(void);

#ifdef __cplusplus
}
#endif

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

    if (PyType_Ready(&AdjacencyMatrixGraphType) < 0)
        return NULL;

    if (PyType_Ready(&AdjacencyMatrixGraphNodeType) < 0)
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

    Py_INCREF(&AdjacencyMatrixGraphType);
    if (PyModule_AddObject(m, "AdjacencyMatrixGraph", (PyObject*)&AdjacencyMatrixGraphType) < 0) {
        Py_DECREF(&AdjacencyMatrixGraphType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
