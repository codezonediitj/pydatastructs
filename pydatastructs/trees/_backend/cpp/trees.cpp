#include <Python.h>
#include "BinaryTree.hpp"
#include "BinarySearchTree.hpp"
#include "BinaryTreeTraversal.hpp"
#include "SelfBalancingBinaryTree.hpp"
#include "RedBlackTree.hpp"
#include "BinaryIndexedTree.hpp"
#include "SplayTree.hpp"
#include "AVLTree.hpp"
#include "CartesianTree.hpp"
#include "Treap.hpp"

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

    if (PyType_Ready(&BinaryIndexedTreeType) < 0) {
        return NULL;
    }
    Py_INCREF(&BinaryIndexedTreeType);
    PyModule_AddObject(trees, "BinaryIndexedTree", reinterpret_cast<PyObject*>(&BinaryIndexedTreeType));

    if (PyType_Ready(&SplayTreeType) < 0) {
        return NULL;
    }
    Py_INCREF(&SplayTreeType);
    PyModule_AddObject(trees, "SplayTree", reinterpret_cast<PyObject*>(&SplayTreeType));

    if (PyType_Ready(&AVLTreeType) < 0) {
        return NULL;
    }
    Py_INCREF(&AVLTreeType);
    PyModule_AddObject(trees, "AVLTree", reinterpret_cast<PyObject*>(&AVLTreeType));

    if (PyType_Ready(&CartesianTreeType) < 0) {
        return NULL;
    }
    Py_INCREF(&CartesianTreeType);
    PyModule_AddObject(trees, "CartesianTree", reinterpret_cast<PyObject*>(&CartesianTreeType));

    if (PyType_Ready(&TreapType) < 0) {
        return NULL;
    }
    Py_INCREF(&TreapType);
    PyModule_AddObject(trees, "Treap", reinterpret_cast<PyObject*>(&TreapType));

    return trees;
}
