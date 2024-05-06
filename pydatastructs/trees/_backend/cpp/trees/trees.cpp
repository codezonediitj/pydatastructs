#include <Python.h>
#include "binary_search_tree.hpp" // Include your binary search tree header file

static struct PyModuleDef binary_search_tree_struct = {
    PyModuleDef_HEAD_INIT,
    "_binary_search_tree",
    0,
    -1,
    NULL,
};

PyMODINIT_FUNC PyInit__binary_search_tree(void) {
    Py_Initialize();
    PyObject *binary_search_tree = PyModule_Create(&binary_search_tree_struct);

    // Initialize and add your binary search tree types to the module
    if (PyType_Ready(&BinarySearchTreeType) < 0) {
        return NULL;
    }
    Py_INCREF(&BinarySearchTreeType);
    PyModule_AddObject(binary_search_tree, "BinarySearchTree", reinterpret_cast<PyObject*>(&BinarySearchTreeType));

    return binary_search_tree;
}
