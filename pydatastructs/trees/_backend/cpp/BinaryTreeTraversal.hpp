#ifndef TREES_BINARYTREETRAVERSAL_HPP
#define TREES_BINARYTREETRAVERSAL_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <cstdlib>
#include <stack>
#include <string>
#include "../../../utils/_backend/cpp/utils.hpp"
#include "../../../utils/_backend/cpp/TreeNode.hpp"
#include "../../../linear_data_structures/_backend/cpp/arrays/ArrayForTrees.hpp"
#include "BinaryTree.hpp"
#include "BinarySearchTree.hpp"

typedef struct {
    PyObject_HEAD
    BinaryTree* tree;
} BinaryTreeTraversal;

static void BinaryTreeTraversal_dealloc(BinaryTreeTraversal *self) {
    BinaryTree_dealloc(self->tree);
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* BinaryTreeTraversal___new__(PyTypeObject* type, PyObject *args, PyObject *kwds) {
    BinaryTreeTraversal *self;
    self = reinterpret_cast<BinaryTreeTraversal*>(type->tp_alloc(type, 0));

    PyObject* tree = PyObject_GetItem(args, PyZero);
    if (PyType_Ready(&BinarySearchTreeType) < 0) { // This has to be present to finalize a type object. This should be called on all type objects to finish their initialization.
        return NULL;
    }
    if (PyObject_IsInstance(tree, (PyObject *)&BinarySearchTreeType)) {
        self->tree = reinterpret_cast<BinarySearchTree*>(tree)->binary_tree;
    }
    else {
        PyErr_SetString(PyExc_ValueError, "Not a supported type for BinaryTreeTraversal.");
        return NULL;
    }
    return reinterpret_cast<PyObject*>(self);
}

static PyObject* BinaryTreeTraversal__pre_order(BinaryTreeTraversal* self, PyObject *args){
    long node = PyLong_AsLong(PyObject_GetItem(args, PyZero));
    PyObject* visit = PyList_New(0);
    ArrayForTrees* tree = self->tree->tree;
    long size = self->tree->size;
    std::stack<long> s;
    s.push(node);

    while (!s.empty()) {
        node = s.top();
        s.pop();
        TreeNode* curr_node = reinterpret_cast<TreeNode*>(tree->_one_dimensional_array->_data[node]);
        PyList_Append(visit, reinterpret_cast<PyObject*>(curr_node));
        if (curr_node->right != Py_None) {
            s.push(PyLong_AsLong(curr_node->right));
        }
        if (curr_node->left != Py_None) {
            s.push(PyLong_AsLong(curr_node->left));
        }
    }
    return visit;
}

static PyObject* BinaryTreeTraversal__in_order(BinaryTreeTraversal* self, PyObject *args){
    PyObject* node = PyObject_GetItem(args, PyZero);
    PyObject* visit = PyList_New(0);
    ArrayForTrees* tree = self->tree->tree;
    long size = self->tree->size;
    std::stack<PyObject*> s;

    while (!s.empty() || node != Py_None) {
        if (node != Py_None) {
            s.push(node);
            node = reinterpret_cast<TreeNode*>(tree->_one_dimensional_array->_data[PyLong_AsLong(node)])->left;
        }
        else {
            node = s.top();
            s.pop();
            TreeNode* curr_node = reinterpret_cast<TreeNode*>(tree->_one_dimensional_array->_data[PyLong_AsLong(node)]);
            PyList_Append(visit, reinterpret_cast<PyObject*>(curr_node));
            node = curr_node->right;
        }
    }
    return visit;
}

static PyObject* BinaryTreeTraversal_depth_first_search(BinaryTreeTraversal* self, PyObject *args, PyObject *kwds) {
    Py_INCREF(Py_None);
    PyObject* node = Py_None;
    PyObject* order = PyUnicode_FromString("in_order");
    static char* keywords[] = {"node","order", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|OO", keywords, &node, &order)) {
        return NULL;
    }
    if (node == Py_None) {
        node = self->tree->root_idx;
    }
    if (PyUnicode_Compare(order, PyUnicode_FromString("pre_order")) == 0) {
        return BinaryTreeTraversal__pre_order(self, Py_BuildValue("(O)", node));
    }
    else if (PyUnicode_Compare(order, PyUnicode_FromString("in_order")) == 0) {
        return BinaryTreeTraversal__in_order(self, Py_BuildValue("(O)", node));
    }
    else {
        PyErr_SetString(PyExc_NotImplementedError, "This traversal is not implemented yet or does not exist. Supported traversals: \"pre_order\"");
        return NULL;
    }
}

static struct PyMethodDef BinaryTreeTraversal_PyMethodDef[] = {
    {"_pre_order", (PyCFunction) BinaryTreeTraversal__pre_order, METH_VARARGS, NULL},
    {"_in_order", (PyCFunction) BinaryTreeTraversal__pre_order, METH_VARARGS, NULL},
    {"depth_first_search", (PyCFunction) BinaryTreeTraversal_depth_first_search, METH_VARARGS | METH_KEYWORDS, NULL},
    {NULL}
};


static PyTypeObject BinaryTreeTraversalType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "BinaryTreeTraversal",
    /* tp_basicsize */ sizeof(BinaryTreeTraversal),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor) BinaryTreeTraversal_dealloc,
    /* tp_print */ 0,
    /* tp_getattr */ 0,
    /* tp_setattr */ 0,
    /* tp_reserved */ 0,
    /* tp_repr */ 0,
    /* tp_as_number */ 0,
    /* tp_as_sequence */ 0,
    /* tp_as_mapping */ 0,
    /* tp_hash  */ 0,
    /* tp_call */ 0,
    /* tp_str */ 0,
    /* tp_getattro */ 0,
    /* tp_setattro */ 0,
    /* tp_as_buffer */ 0,
    /* tp_flags */ Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    /* tp_doc */ 0,
    /* tp_traverse */ 0,
    /* tp_clear */ 0,
    /* tp_richcompare */ 0,
    /* tp_weaklistoffset */ 0,
    /* tp_iter */ 0,
    /* tp_iternext */ 0,
    /* tp_methods */ BinaryTreeTraversal_PyMethodDef,
    /* tp_members */ 0,
    /* tp_getset */ 0,
    /* tp_base */ &PyBaseObject_Type,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ BinaryTreeTraversal___new__,
};

#endif
