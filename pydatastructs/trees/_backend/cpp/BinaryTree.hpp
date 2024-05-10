#ifndef TREES_BINARY_TREE_HPP
#define TREES_BINARY_TREE_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <cstdlib>
#include "../../../utils/_backend/cpp/utils.hpp"

typedef struct {
    PyObject_HEAD
    size_t root_idx;
    PyObject* comparator;
    PyObject* tree;
    size_t size;
    bool is_ordered_stastic;
} BinaryTree;

static void BinaryTree_dealloc(BinaryTree *self) {
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* BinaryTree___new__(PyTypeObject* type, PyObject *args, PyObject *kwds) {
    BinaryTree *self;
    self = reinterpret_cast<BinaryTree*>(type->tp_alloc(type, 0));

    PyObject *key = PyObject_GetItem(args, PyZero);
    PyObject *root_data = PyObject_GetItem(args, PyOne);
    PyObject *comp = PyObject_GetItem(args, PyTwo);
    PyObject *is_order_statistic = PyObject_GetItem(args, PyThree);
    if( (key == Py_None) && (root_data != Py_None) ) {
        PyErr_SetString(PyExc_ValueError, "Key required.");
        return NULL;
    }

    key = root_data == Py_None ? Py_None : key;
    root = TreeNode(key, root_data)
    root.is_root = True
    obj.root_idx = 0
    obj.tree, obj.size = ArrayForTrees(TreeNode, [root]), 1
    obj.comparator = lambda key1, key2: key1 < key2 \
                    if comp is None else comp
    obj.is_order_statistic = is_order_statistic
    return obj

    return reinterpret_cast<PyObject*>(self);
}



#endif
