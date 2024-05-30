#ifndef TREES_BINARYTREETRAVERSAL_HPP
#define TREES_BINARYTREETRAVERSAL_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <cstdlib>
#include <iostream>
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
    PyObject* tree = PyObject_GetItem(args, PyZero);
    if (PyType_Ready(&BinarySearchTreeType) < 0) { // This has to be present to finalize a type object. This should be called on all type objects to finish their initialization.
        return NULL;
    }
    if (PyObject_IsInstance(tree, (PyObject *)&BinarySearchTreeType)) {
        self->tree = reinterpret_cast<BinarySearchTree*>(tree)->binary_tree;
        std::cout<<"here"<<std::endl;
    }
    else {
        PyErr_SetString(PyExc_ValueError, "Not a supported type for BinaryTreeTraversal.");
        return NULL;
    }
    return reinterpret_cast<PyObject*>(self);
}

static struct PyMethodDef BinaryTreeTraversal_PyMethodDef[] = {
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
