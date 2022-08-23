#include <Python.h>
#include "adjacency_matrix.hpp"
#include "../../../../utils/_backend/cpp/AdjacencyMatrixGraphNode.hpp"
#include "../../../../utils/_backend/cpp/GraphNode.hpp"

static struct PyModuleDef graph_struct = {
        PyModuleDef_HEAD_INIT,
        "_graph",
        0,
        -1,
        NULL,
};

PyMODINIT_FUNC PyInit__graph(void) {
    Py_Initialize();
    PyObject *graph = PyModule_Create(&graph_struct);

    if (PyType_Ready(&AdjacencyMatrixType) < 0) {
        return NULL;
    }
    Py_INCREF(&AdjacencyMatrixType);
    PyModule_AddObject(graph, "AdjacencyMatrix", reinterpret_cast<PyObject*>(&AdjacencyMatrixType));

    return graph;
}
