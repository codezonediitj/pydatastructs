#include <Python.h>
#include "GraphNode.hpp"
#include "AdjacencyMatrixGraphNode.hpp"
#include "GraphEdge.hpp"

static struct PyModuleDef utils_struct = {
        PyModuleDef_HEAD_INIT,
        "_utils",
        0,
        -1,
        NULL,
};

PyMODINIT_FUNC PyInit__utils(void) {
    Py_Initialize();
    PyObject *utils = PyModule_Create(&utils_struct);

    if (PyType_Ready(&GraphNodeCppType) < 0) {
        return NULL;
    }
    Py_INCREF(&GraphNodeCppType);
    PyModule_AddObject(utils, "GraphNodeCpp", reinterpret_cast<PyObject*>(&GraphNodeCppType));

    if (PyType_Ready(&AdjacencyMatrixGraphNodeCppType) < 0) {
        return NULL;
    }
    Py_INCREF(&AdjacencyMatrixGraphNodeCppType);
    PyModule_AddObject(utils, "AdjacencyMatrixGraphNodeCpp", reinterpret_cast<PyObject*>(&AdjacencyMatrixGraphNodeCppType));

    if (PyType_Ready(&GraphEdgeCppType) < 0) {
        return NULL;
    }
    Py_INCREF(&GraphEdgeCppType);
    PyModule_AddObject(utils, "GraphEdgeCpp", reinterpret_cast<PyObject*>(&GraphEdgeCppType));

    return utils;
}
