#include <Python.h>
#include "binary_search_tree.hpp" // Assuming this header contains the declaration of BinarySearchTree class

static struct PyModuleDef trees_struct = {
    PyModuleDef_HEAD_INIT,
    "_trees",
    0,
    -1,
    NULL
};

PyMODINIT_FUNC PyInit__trees(void) {
    Py_Initialize();
    PyObject *trees = PyModule_Create(&trees_struct);

    if (PyType_Ready(&BinarySearchTreeType) < 0) {
        return NULL;
    }
    Py_INCREF(&BinarySearchTreeType);
    PyModule_AddObject(trees, "BinarySearchTree", reinterpret_cast<PyObject*>(&BinarySearchTreeType));

    return trees;
}
