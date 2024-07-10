#ifndef TREES_CARTESIANTREE_HPP
#define TREES_CARTESIANTREE_HPP

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
} CartesianTree;

static void CartesianTree_dealloc(CartesianTree *self) {
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* CartesianTree___new__(PyTypeObject* type, PyObject *args, PyObject *kwds) {
    CartesianTree *self;
    self = reinterpret_cast<CartesianTree*>(type->tp_alloc(type, 0));

    if (PyType_Ready(&SelfBalancingBinaryTreeType) < 0) { // This has to be present to finalize a type object. This should be called on all type objects to finish their initialization.
        return NULL;
    }
    PyObject* p = SelfBalancingBinaryTree___new__(&SelfBalancingBinaryTreeType, args, kwds);
    self->sbbt = reinterpret_cast<SelfBalancingBinaryTree*>(p);
    self->tree = reinterpret_cast<SelfBalancingBinaryTree*>(p)->bst->binary_tree->tree;

    return reinterpret_cast<PyObject*>(self);
}

static PyObject* CartesianTree___str__(CartesianTree *self) {
    return BinarySearchTree___str__(self->sbbt->bst);
}

static PyObject* CartesianTree_search(CartesianTree* self, PyObject *args, PyObject *kwds) {
    return BinarySearchTree_search(self->sbbt->bst, args, kwds);
}

static PyObject* Cartesian_Tree__bubble_up(CartesianTree* self, PyObject *args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    BinaryTree* bt = self->sbbt->bst->binary_tree;
    TreeNode* node = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)]);
    PyObject* parent_idx = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->parent;
    TreeNode* parent = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent_idx)]);

    while ((node->parent != Py_None) && (parent->priority > node->priority)) {
        if (parent->right == node_idx) {
            SelfBalancingBinaryTree__left_rotate(self->sbbt, Py_BuildValue("OO", parent_idx, node_idx));
        }
        else {
            SelfBalancingBinaryTree__right_rotate(self->sbbt, Py_BuildValue("OO", parent_idx, node_idx));
        }
        node = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)]);
        parent_idx = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->parent;
        if (parent_idx != Py_None) {
            parent = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent_idx)]);
        }
    }
    if (node->parent == Py_None) {
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->is_root = true;
    }
    Py_RETURN_NONE;
}

static PyObject* Cartesian_Tree__trickle_down(CartesianTree* self, PyObject *args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    BinaryTree* bt = self->sbbt->bst->binary_tree;
    TreeNode* node = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)]);
    while (node->left != Py_None || node->right != Py_None) {
        if (node->left == Py_None) {
            SelfBalancingBinaryTree__left_rotate(self->sbbt, Py_BuildValue("OO", node_idx, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->right));
        }
        else if (node->right == Py_None) {
            SelfBalancingBinaryTree__right_rotate(self->sbbt, Py_BuildValue("OO", node_idx, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->left));
        }
        else if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node->left)])->priority < reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node->right)])->priority) {
            SelfBalancingBinaryTree__right_rotate(self->sbbt, Py_BuildValue("OO", node_idx, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->left));
        }
        else {
            SelfBalancingBinaryTree__left_rotate(self->sbbt, Py_BuildValue("OO", node_idx, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->right));
        }
        node = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)]);
    }
    Py_RETURN_NONE;
}


static struct PyMethodDef CartesianTree_PyMethodDef[] = {
    // {"insert", (PyCFunction) CartesianTree_insert, METH_VARARGS, NULL},
    // {"delete", (PyCFunction) CartesianTree_delete, METH_VARARGS | METH_KEYWORDS, NULL},
    {"search", (PyCFunction) CartesianTree_search, METH_VARARGS | METH_KEYWORDS, NULL},
    {NULL}
};

static PyMemberDef CartesianTree_PyMemberDef[] = {
    {"tree", T_OBJECT_EX, offsetof(CartesianTree, tree), 0, "tree"},
    {NULL}  /* Sentinel */
};


static PyTypeObject CartesianTreeType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "CartesianTree",
    /* tp_basicsize */ sizeof(CartesianTree),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor) CartesianTree_dealloc,
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
    /* tp_str */ (reprfunc) CartesianTree___str__,
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
    /* tp_methods */ CartesianTree_PyMethodDef,
    /* tp_members */ CartesianTree_PyMemberDef,
    /* tp_getset */ 0,
    /* tp_base */ &SelfBalancingBinaryTreeType,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ CartesianTree___new__,
};

#endif
