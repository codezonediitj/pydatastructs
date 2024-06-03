#include <Python.h>
#include "Node.hpp"
#include "TreeNode.hpp"

static struct PyModuleDef nodes_struct = {
    PyModuleDef_HEAD_INIT,
    "_nodes",
    0,
    -1,
    NULL,
};

PyMODINIT_FUNC PyInit__nodes(void) {
    Py_Initialize();
    PyObject *nodes = PyModule_Create(&nodes_struct);

    if (PyType_Ready(&NodeType) < 0) {
        return NULL;
    }
    Py_INCREF(&NodeType);
    PyModule_AddObject(nodes, "Node", reinterpret_cast<PyObject*>(&NodeType));

    if (PyType_Ready(&TreeNodeType) < 0) {
        return NULL;
    }
    Py_INCREF(&TreeNodeType);
    PyModule_AddObject(nodes, "TreeNode", reinterpret_cast<PyObject*>(&TreeNodeType));

    return nodes;
}
