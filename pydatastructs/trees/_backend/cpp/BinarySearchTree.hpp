#ifndef TREES_BINARYSEARCHTREE_HPP
#define TREES_BINARYSEARCHTREE_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <cstdlib>
#include "../../../utils/_backend/cpp/utils.hpp"
#include "../../../utils/_backend/cpp/TreeNode.hpp"
#include "../../../linear_data_structures/_backend/cpp/arrays/ArrayForTrees.hpp"
#include "BinaryTree.hpp"

typedef struct {
    PyObject_HEAD
    BinaryTree* binary_tree;
} BinarySearchTree;

static void BinarySearchTree_dealloc(BinarySearchTree *self) {
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

// How to allocate without __new__()?

static int BinarySearchTree_left_size(BinarySearchTree* self, TreeNode* node) {
    if (node->left != Py_None) {
        return self->binary_tree->tree->_dynamic_one_dimensional_array->_one_dimensional_array->_data[node->left]->size;
    } else {
        return 0;
    }
}

static int BinarySearchTree_right_size(BinarySearchTree* self, TreeNode* node) {
    if (node->right != Py_None) {
        return self->binary_tree->tree->_dynamic_one_dimensional_array->_one_dimensional_array->_data[node->right]->size;
    } else {
        return 0;
    }
}

static PyObject* BinarySearchTree__update_size(PyTypeObject* type, PyObject *args, PyObject *kwds) {
    PyObject *start_idx = PyObject_GetItem(args, PyZero);
    if(self->binary_tree->is_order_statistic){
        PyObject* walk = start_idx;
        while(walk!=Py_None){
            self->binary_tree->_dynamic_one_dimensional_array->_one_dimensional_array->_data[walk]->size = BinarySearchTree_left_size(self->binary_tree->_dynamic_one_dimensional_array->_one_dimensional_array->_data[walk]) + BinarySearchTree_right_size(self->binary_tree->_dynamic_one_dimensional_array->_one_dimensional_array->_data[walk]) + 1;
            walk = self->binary_tree->_dynamic_one_dimensional_array->_one_dimensional_array->_data[walk]->parent;
        }
    }
}

// static PyObject* BinarySearchTree_insert(PyTypeObject* type, PyObject *args, PyObject *kwds) {
//     PyErr_SetString(PyExc_ValueError, "This is an abstract method."); // Currently of type ValueError, change type if needed later
//     return NULL;
// }

// static PyObject* BinaryTree_delete(PyTypeObject* type, PyObject *args, PyObject *kwds) {
//     PyErr_SetString(PyExc_ValueError, "This is an abstract method."); // Currently of type ValueError, change type if needed later
//     return NULL;
// }

// static PyObject* BinaryTree_search(PyTypeObject* type, PyObject *args, PyObject *kwds) {
//     PyErr_SetString(PyExc_ValueError, "This is an abstract method."); // Currently of type ValueError, change type if needed later
//     return NULL;
// }

// static PyObject* BinaryTree___str__(BinaryTree *self) {
//     long size = reinterpret_cast<ArrayForTrees*>(self->tree)->_last_pos_filled+1;
//     PyObject* list = PyList_New(size);
//     for(int i=0;i<size;i++){
//         TreeNode* node = reinterpret_cast<TreeNode*>(reinterpret_cast<ArrayForTrees*>(self->tree)->_dynamic_one_dimensional_array->_one_dimensional_array->_data[i]); // check this
//         if(reinterpret_cast<PyObject*>(node) != Py_None){
//             PyObject* out = Py_BuildValue("(OllO)", node->left, node->key, node->data, node->right);
//             Py_INCREF(out);
//             PyList_SET_ITEM(list, i, out);
//         }
//         else{
//             PyObject* empty_string = PyUnicode_FromString("");
//             PyList_SET_ITEM(list, i, empty_string);
//         }
//     }
//     return PyObject_Str(list); // use this or __str()__ (that is defined in utils)?
// }

// static struct PyMethodDef BinaryTree_PyMethodDef[] = {
//     {"insert", (PyCFunction) BinaryTree_insert, METH_VARARGS | METH_KEYWORDS, NULL},
//     {"delete", (PyCFunction) BinaryTree_delete, METH_VARARGS | METH_KEYWORDS, NULL},
//     {"search", (PyCFunction) BinaryTree_search, METH_VARARGS | METH_KEYWORDS, NULL},
//     {NULL}
// };

// // Check if PyMemberDef is actually needed:
// static PyMemberDef BinaryTree_PyMemberDef[] = {
//     {"root_idx", T_PYSSIZET, offsetof(BinaryTree, root_idx), READONLY, "Index of the root node"},
//     {"comparator", T_OBJECT, offsetof(BinaryTree, comparator), 0, "Comparator function"},
//     {"tree", T_OBJECT, offsetof(BinaryTree, tree), 0, "Tree"},
//     {"size", T_PYSSIZET, offsetof(BinaryTree, size), READONLY, "Size of the tree"},
//     {"is_order_statistic", T_BOOL, offsetof(BinaryTree, is_order_statistic), 0, "Whether the tree is ordered statically or not"},
//     {NULL}  /* Sentinel */
// };


static PyTypeObject BinarySearchTreeType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "BinarySearchTree",
    /* tp_basicsize */ sizeof(BinarySearchTree),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor) BinarySearchTree_dealloc,
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
    /* tp_methods */ BinarySearchTree_PyMethodDef,
    /* tp_members */ BinarySearchTree_PyMemberDef,
    /* tp_getset */ 0,
    /* tp_base */ &BinaryTreeType,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ 0,
};

#endif
