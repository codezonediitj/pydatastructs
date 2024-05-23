#include <Python.h>
#include "BinaryTree.hpp"
#include "BinarySearchTree.hpp"

static struct PyModuleDef trees_struct = {
    PyModuleDef_HEAD_INIT,
    "_trees",
    0,
    -1,
    NULL,
};

PyMODINIT_FUNC PyInit__trees(void) {
    Py_Initialize();
    PyObject *trees = PyModule_Create(&trees_struct);

    if (PyType_Ready(&BinaryTreeType) < 0) {
        return NULL;
    }
    Py_INCREF(&BinaryTreeType);
    PyModule_AddObject(trees, "BinaryTree", reinterpret_cast<PyObject*>(&BinaryTreeType));

    if (PyType_Ready(&BinarySearchTreeType) < 0) {
        return NULL;
    }
    Py_INCREF(&BinarySearchTreeType);
    PyModule_AddObject(trees, "BinarySearchTree", reinterpret_cast<PyObject*>(&BinarySearchTreeType));

    return trees;
}
