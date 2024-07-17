#ifndef TREES_BINARYTREE_HPP
#define TREES_BINARYTREE_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <cstdlib>
#include "../../../utils/_backend/cpp/utils.hpp"
#include "../../../utils/_backend/cpp/TreeNode.hpp"
#include "../../../linear_data_structures/_backend/cpp/arrays/ArrayForTrees.hpp"
#include "../../../linear_data_structures/_backend/cpp/arrays/DynamicOneDimensionalArray.hpp"

typedef struct {
    PyObject_HEAD
    ArrayForTrees* tree;
    PyObject* root_idx;
    PyObject* comparator;
    long size;
    long is_order_statistic;
} BinaryTree;

static void BinaryTree_dealloc(BinaryTree *self) {
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* BinaryTree___new__(PyTypeObject* type, PyObject *args, PyObject *kwds) {
    BinaryTree *self;
    self = reinterpret_cast<BinaryTree*>(type->tp_alloc(type, 0));

    // Assume that arguments are in the order below. Modify the python code such that this is true (ie; pass None for other arguments)
    PyObject *key = PyObject_GetItem(args, PyZero);
    PyObject *root_data = PyObject_GetItem(args, PyOne);
    PyObject *comp = PyObject_GetItem(args, PyTwo);
    PyObject *is_order_statistic = PyObject_GetItem(args, PyThree);
    if ( (key == Py_None) && (root_data != Py_None) ) {
        PyErr_SetString(PyExc_ValueError, "Key required.");
        return NULL;
    }
    Py_INCREF(Py_None);
    key = root_data == Py_None ? Py_None : key;

    if (PyType_Ready(&TreeNodeType) < 0) { // This has to be present to finalize a type object. This should be called on all type objects to finish their initialization.
        return NULL;
    }
    TreeNode* root = reinterpret_cast<TreeNode*>(TreeNode___new__(&TreeNodeType, args, kwds));
    root->is_root = true;
    self->root_idx = PyLong_FromLong(0);

    PyObject* listroot = Py_BuildValue("[O]", root);
    if (PyType_Ready(&ArrayForTreesType) < 0) { // This has to be present to finalize a type object. This should be called on all type objects to finish their initialization.
        return NULL;
    }
    if (PyType_Ready(&DynamicOneDimensionalArrayType) < 0) { // This has to be present to finalize a type object. This should be called on all type objects to finish their initialization.
        return NULL;
    }
    if (PyType_Ready(&TreeNodeType) < 0) { // This has to be present to finalize a type object. This should be called on all type objects to finish their initialization.
        return NULL;
    }

    Py_INCREF(Py_None);
    PyObject* args2 = Py_BuildValue("(OO)", &TreeNodeType, listroot);
    PyObject* kwds2 = Py_BuildValue("()");
    if (PyType_Ready(&DynamicOneDimensionalArrayType) < 0) { // This has to be present to finalize a type object. This should be called on all type objects to finish their initialization.
        return NULL;
    }
    ArrayForTrees* arr = reinterpret_cast<ArrayForTrees*>(ArrayForTrees___new__(&ArrayForTreesType, args2, kwds2));
    if ( !arr ) {
        return NULL;
    }
    self->tree = arr;
    self->size = 1;
    // Python code is modified to ensure comp is never None
    if (!PyCallable_Check(comp)) {
            PyErr_SetString(PyExc_ValueError, "comparator should be callable");
            return NULL;
    }
    self->comparator = comp;
    self->is_order_statistic = PyLong_AsLong(is_order_statistic);

    return reinterpret_cast<PyObject*>(self);
}

static PyObject* BinaryTree_insert(PyTypeObject* type, PyObject *args, PyObject *kwds) {
    PyErr_SetString(PyExc_NotImplementedError, "This is an abstract method.");
    return NULL;
}

static PyObject* BinaryTree_delete(PyTypeObject* type, PyObject *args, PyObject *kwds) {
    PyErr_SetString(PyExc_NotImplementedError, "This is an abstract method.");
    return NULL;
}

static PyObject* BinaryTree_search(PyTypeObject* type, PyObject *args, PyObject *kwds) {
    PyErr_SetString(PyExc_NotImplementedError, "This is an abstract method.");
    return NULL;
}

static PyObject* BinaryTree___str__(BinaryTree *self) {
    long size = self->tree->_last_pos_filled + 1;
    PyObject* list = PyList_New(size);
    for(int i=0;i<size;i++) {
        OneDimensionalArray* oda = self->tree->_one_dimensional_array;
        TreeNode* node = reinterpret_cast<TreeNode*>(oda->_data[i]);
        if (reinterpret_cast<PyObject*>(node) != Py_None) {
            PyObject* out;
            if (node->isCartesianTreeNode == true) {
                out = Py_BuildValue("(OOOOO)", node->left, node->key, PyFloat_FromDouble(node->priority), node->data, node->right);
            }
            else {
                out = Py_BuildValue("(OOOO)", node->left, node->key, node->data, node->right);
            }
            Py_INCREF(out);
            PyList_SET_ITEM(list, i, out);
        }
        else {
            PyObject* empty_string = PyUnicode_FromString("");
            PyList_SET_ITEM(list, i, empty_string);
        }
    }
    return PyObject_Str(list);
}

static struct PyMethodDef BinaryTree_PyMethodDef[] = {
    {"insert", (PyCFunction) BinaryTree_insert, METH_VARARGS | METH_KEYWORDS, NULL},
    {"delete", (PyCFunction) BinaryTree_delete, METH_VARARGS | METH_KEYWORDS, NULL},
    {"search", (PyCFunction) BinaryTree_search, METH_VARARGS | METH_KEYWORDS, NULL},
    {NULL}
};

static PyMemberDef BinaryTree_PyMemberDef[] = {
    {"root_idx", T_OBJECT_EX, offsetof(BinaryTree, root_idx), 0, "Index of the root node"},
    {"comparator", T_OBJECT, offsetof(BinaryTree, comparator), 0, "Comparator function"},
    {"tree", T_OBJECT_EX, offsetof(BinaryTree, tree), 0, "Tree"},
    {"size", T_LONG, offsetof(BinaryTree, size), 0, "Size of the tree"},
    {"is_order_statistic", T_LONG, offsetof(BinaryTree, is_order_statistic), 0, "Whether the tree is ordered statically or not"},
    {NULL}  /* Sentinel */
};


static PyTypeObject BinaryTreeType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "BinaryTree",
    /* tp_basicsize */ sizeof(BinaryTree),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor) BinaryTree_dealloc,
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
    /* tp_str */ (reprfunc) BinaryTree___str__,
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
    /* tp_methods */ BinaryTree_PyMethodDef,
    /* tp_members */ BinaryTree_PyMemberDef,
    /* tp_getset */ 0,
    /* tp_base */ &PyBaseObject_Type,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ BinaryTree___new__,
};

#endif
