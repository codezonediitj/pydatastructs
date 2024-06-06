#include <Python.h>
#include "BinaryTree.hpp"
#include "BinarySearchTree.hpp"
#include "BinaryTreeTraversal.hpp"
#include "SelfBalancingBinaryTree.hpp"
#include "RedBlackTree.hpp"

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

    if (PyType_Ready(&BinaryTreeTraversalType) < 0) {
        return NULL;
    }
    Py_INCREF(&BinaryTreeTraversalType);
    PyModule_AddObject(trees, "BinaryTreeTraversal", reinterpret_cast<PyObject*>(&BinaryTreeTraversalType));

    if (PyType_Ready(&SelfBalancingBinaryTreeType) < 0) {
        return NULL;
    }
    Py_INCREF(&SelfBalancingBinaryTreeType);
    PyModule_AddObject(trees, "SelfBalancingBinaryTree", reinterpret_cast<PyObject*>(&SelfBalancingBinaryTreeType));

    if (PyType_Ready(&RedBlackTreeType) < 0) {
        return NULL;
    }
    Py_INCREF(&RedBlackTreeType);
    PyModule_AddObject(trees, "RedBlackTree", reinterpret_cast<PyObject*>(&RedBlackTreeType));

    return trees;
}
