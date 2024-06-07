#ifndef TREES_REDBLACKTREE_HPP
#define TREES_REDBLACKTREE_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <cstdlib>
#include <iostream>
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

static PyObject* RedBlackTree__get_parent(RedBlackTree *self, PyObject* args) {
    long node_idx = PyLong_AsLong(PyObject_GetItem(args, PyZero));
    BinaryTree* bt = self->sbbt->bst->binary_tree;
    PyObject* parent = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[node_idx])->parent;
    return parent;
}

static PyObject* RedBlackTree__get_grand_parent(RedBlackTree *self, PyObject* args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    PyObject* parent_idx = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));

    BinaryTree* bt = self->sbbt->bst->binary_tree;
    PyObject* grand_parent = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent_idx)])->parent;
    return grand_parent;
}

static PyObject* RedBlackTree__get_sibling(RedBlackTree *self, PyObject* args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    PyObject* parent_idx = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));

    if (parent_idx == Py_None) {
        Py_RETURN_NONE;
    }

    BinaryTree* bt = self->sbbt->bst->binary_tree;
    TreeNode* node = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent_idx)]);
    if (node_idx == node->left) {
        PyObject* sibling_idx = node->right;
        return sibling_idx;
    }
    else {
        PyObject* sibling_idx = node->left;
        return sibling_idx;
    }

    Py_RETURN_NONE;
}

static PyObject* RedBlackTree__get_uncle(RedBlackTree *self, PyObject* args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    PyObject* parent_idx = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));

    PyObject* uncle = RedBlackTree__get_sibling(self, Py_BuildValue("(O)", parent_idx));
    return uncle;
}

static PyObject* RedBlackTree__is_onleft(RedBlackTree *self, PyObject* args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    PyObject* parent_idx = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));

    BinaryTree* bt = self->sbbt->bst->binary_tree;
    if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent_idx)])->left == node_idx) {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}

static PyObject* RedBlackTree__is_onright(RedBlackTree *self, PyObject* args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    if (RedBlackTree__is_onleft(self, Py_BuildValue("(O)", node_idx)) == Py_False) {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}

static PyObject* RedBlackTree___fix_insert(RedBlackTree *self, PyObject* args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    BinaryTree* bt = self->sbbt->bst->binary_tree;
    while (RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx)) != Py_None && reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx)))])->color == 1 && reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->color == 1) {
        PyObject* parent_idx = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));
        PyObject* grand_parent_idx = RedBlackTree__get_grand_parent(self, Py_BuildValue("(O)", node_idx));
        PyObject* uncle_idx = RedBlackTree__get_uncle(self, Py_BuildValue("(O)", node_idx));

        if(uncle_idx != Py_None && reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(uncle_idx)])->color == 1) {
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(uncle_idx)])->color = 0;
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent_idx)])->color = 0;
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(grand_parent_idx)])->color = 1;
            node_idx = grand_parent_idx;
        }
        else {
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->is_root = false;
            if (RedBlackTree__is_onright(self, Py_BuildValue("(O)", parent_idx)) == Py_True) {
                if (RedBlackTree__is_onleft(self, Py_BuildValue("(O)", node_idx)) == Py_True) {
                    SelfBalancingBinaryTree__right_rotate(self->sbbt, Py_BuildValue("(OO)", parent_idx, node_idx));
                    node_idx = parent_idx;
                    parent_idx = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));
                }
                node_idx = parent_idx;
                parent_idx = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));
                SelfBalancingBinaryTree__left_rotate(self->sbbt, Py_BuildValue("(OO)", parent_idx, node_idx));
            }
            else if (RedBlackTree__is_onleft(self, Py_BuildValue("(O)", parent_idx)) == Py_True) {
                if (RedBlackTree__is_onright(self, Py_BuildValue("(O)", node_idx)) == Py_True) {
                    SelfBalancingBinaryTree__left_rotate(self->sbbt, Py_BuildValue("(OO)", parent_idx, node_idx));
                    node_idx = parent_idx;
                    parent_idx = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));
                }
                node_idx = parent_idx;
                parent_idx = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));
                SelfBalancingBinaryTree__right_rotate(self->sbbt, Py_BuildValue("(OO)", parent_idx, node_idx));
            }
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->color = 0;
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent_idx)])->color = 1;
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->is_root = true;
        }
        if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->is_root) {
            break;
        }
    }
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->color = 0;
    Py_RETURN_NONE;
}

static PyObject* RedBlackTree_insert(RedBlackTree *self, PyObject* args) {
    Py_INCREF(Py_None);
    PyObject* key = Py_None;
    Py_INCREF(Py_None);
    PyObject* data = Py_None;
    if (!PyArg_ParseTuple(args, "O|O", &key, &data)) { // data is optional
        return NULL;
    }
    SelfBalancingBinaryTree_insert(self->sbbt, Py_BuildValue("(OO)", key, data));
    PyObject* node_idx = SelfBalancingBinaryTree_search(self->sbbt, Py_BuildValue("(O)", key), PyDict_New());

    BinaryTree* bt = self->sbbt->bst->binary_tree;
    TreeNode* node = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)]);

    if (PyType_Ready(&TreeNodeType) < 0) { // This has to be present to finalize a type object. This should be called on all type objects to finish their initialization.
        return NULL;
    }
    TreeNode* new_node = reinterpret_cast<TreeNode*>(TreeNode___new__(&TreeNodeType, Py_BuildValue("(OO)", key, data), PyDict_New()));
    new_node->parent = node->parent;
    new_node->left = node->left;
    new_node->right = node->right;
    bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)] = reinterpret_cast<PyObject*>(new_node);

    if (node->is_root) {
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->is_root = true;
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->color = 0;
    }
    else if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->parent)])->color == 1) {
        RedBlackTree___fix_insert(self, Py_BuildValue("(O)", node_idx));
    }

    Py_RETURN_NONE;
}

static struct PyMethodDef RedBlackTree_PyMethodDef[] = {
    {"insert", (PyCFunction) RedBlackTree_insert, METH_VARARGS, NULL},
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
