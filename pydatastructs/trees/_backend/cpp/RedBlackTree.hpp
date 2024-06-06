#ifndef TREES_REDBLACKTREE_HPP
#define TREES_REDBLACKTREE_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <cstdlib>
#include "../../../utils/_backend/cpp/utils.hpp"
#include "../../../utils/_backend/cpp/TreeNode.hpp"
#include "../../../linear_data_structures/_backend/cpp/arrays/ArrayForTrees.hpp"
#include "../../../linear_data_structures/_backend/cpp/arrays/DynamicOneDimensionalArray.hpp"
#include "BinarySearchTree.hpp"
#include "SelfBalancingBinaryTree.hpp"

typedef struct {
    PyObject_HEAD
    SelfBalancingBinaryTree* sbbt;
    ArrayForTrees* tree;
} RedBlackTree;

static void RedBlackTree_dealloc(RedBlackTree *self) {
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* RedBlackTree___new__(PyTypeObject* type, PyObject *args, PyObject *kwds) {
    RedBlackTree *self;
    self = reinterpret_cast<RedBlackTree*>(type->tp_alloc(type, 0));

    if (PyType_Ready(&SelfBalancingBinaryTreeType) < 0) { // This has to be present to finalize a type object. This should be called on all type objects to finish their initialization.
        return NULL;
    }
    PyObject* p = SelfBalancingBinaryTree___new__(&SelfBalancingBinaryTreeType, args, kwds);
    self->sbbt = reinterpret_cast<SelfBalancingBinaryTree*>(p);
    self->tree = reinterpret_cast<SelfBalancingBinaryTree*>(p)->bst->binary_tree->tree;

    return reinterpret_cast<PyObject*>(self);
}

static PyObject* RedBlackTree___str__(RedBlackTree *self) {
    return BinarySearchTree___str__(self->sbbt->bst);
}



static struct PyMethodDef RedBlackTree_PyMethodDef[] = {
    {NULL}
};

static PyMemberDef RedBlackTree_PyMemberDef[] = {
    {"tree", T_OBJECT_EX, offsetof(RedBlackTree, tree), 0, "tree"},
    {NULL}  /* Sentinel */
};


static PyTypeObject RedBlackTreeType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "RedBlackTree",
    /* tp_basicsize */ sizeof(RedBlackTree),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor) RedBlackTree_dealloc,
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
    /* tp_str */ (reprfunc) RedBlackTree___str__,
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
    /* tp_methods */ RedBlackTree_PyMethodDef,
    /* tp_members */ RedBlackTree_PyMemberDef,
    /* tp_getset */ 0,
    /* tp_base */ &SelfBalancingBinaryTreeType,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ RedBlackTree___new__,
};

#endif
