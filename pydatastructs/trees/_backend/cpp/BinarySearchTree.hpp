#ifndef TREES_BINARYSEARCHTREE_HPP
#define TREES_BINARYSEARCHTREE_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <iostream>
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
    BinaryTree_dealloc(self->binary_tree);
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* BinarySearchTree___new__(PyTypeObject* type, PyObject *args, PyObject *kwds) {
    BinarySearchTree *self;
    self = reinterpret_cast<BinarySearchTree*>(type->tp_alloc(type, 0));

    if (PyType_Ready(&BinaryTreeType) < 0) { // This has to be present to finalize a type object. This should be called on all type objects to finish their initialization.
        return NULL;
    }
    PyObject* bt = BinaryTree___new__(&BinaryTreeType, args, kwds);
    self->binary_tree = reinterpret_cast<BinaryTree*>(bt);

    return reinterpret_cast<PyObject*>(self);
}

static PyObject* BinarySearchTree___str__(BinarySearchTree *self) {
    return BinaryTree___str__(self->binary_tree);
}

static long BinarySearchTree_left_size(BinarySearchTree* self, TreeNode* node) {
    if (node->left != Py_None) {
        TreeNode* n = reinterpret_cast<TreeNode*>(
            self->binary_tree->tree->_one_dimensional_array->_data[PyLong_AsLong(node->left)]
        );
        return n->size;
    } else {
        return 0;
    }
}

static long BinarySearchTree_right_size(BinarySearchTree* self, TreeNode* node) {
    if (node->right != Py_None) {
        TreeNode* n = reinterpret_cast<TreeNode*>(
            self->binary_tree->tree->_one_dimensional_array->_data[PyLong_AsLong(node->right)]
        );
        return n->size;
    } else {
        return 0;
    }
}

static PyObject* BinarySearchTree__update_size(BinarySearchTree* self, PyObject *args) {
    PyObject *start_idx = PyObject_GetItem(args, PyZero);
    if(self->binary_tree->is_order_statistic){
        PyObject* walk = start_idx;
        while(walk!=Py_None){
            TreeNode* node = reinterpret_cast<TreeNode*>(self->binary_tree->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)]);
            node->size = BinarySearchTree_left_size(self, node) + BinarySearchTree_right_size(self, node) + 1;
            walk = node->parent; // Parent is a long or a Py_None, hence, it is a PyObject
        }
    }
    Py_RETURN_NONE;
}

static PyObject* BinarySearchTree_search(BinarySearchTree* self, PyObject* args, PyObject *kwds) {
    Py_INCREF(Py_None);
    PyObject* ret_parent = Py_None;
    PyObject* key;
    static char* keywords[] = {"key","parent", NULL};
    if(!PyArg_ParseTupleAndKeywords(args, kwds, "O|O", keywords, &key, &ret_parent)){ // ret_parent is optional
        return NULL;
    }
    BinaryTree* bt = self->binary_tree;
    PyObject* parent = Py_None;
    PyObject* walk = PyLong_FromLong(bt->root_idx); // root_idx is size_t, change it to long if needed

    if(reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->key == Py_None){
        Py_RETURN_NONE;
    }

    while(walk != Py_None){
        PyObject* curr_key = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->key;

        if(curr_key == key){
            break;
        }
        parent = walk;

        // The comparator has been tested. It works fine. :)
        if (!PyCallable_Check(bt->comparator)) {
            PyErr_SetString(PyExc_ValueError, "comparator should be callable");
            return NULL;
        }
        PyObject* arguments = Py_BuildValue("OO", key, curr_key);
        PyObject* res = PyObject_CallObject(bt->comparator, arguments);
        Py_DECREF(arguments);
        if (!PyLong_Check(res)) {
            PyErr_SetString(PyExc_TypeError, "bad return type from comparator");
            return NULL;
        }
        long long comp = PyLong_AsLongLong(res);

        if(comp == 1){
            walk = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->left;
        }
        else{
            walk = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->right;
        }
    }

    Py_INCREF(Py_None);
    if(ret_parent==Py_None || PyLong_AsLong(ret_parent)==0){
        return walk;
    }
    else{
        return Py_BuildValue("OO",walk,parent);
    }
    Py_RETURN_NONE; // dummy return statement, never executed
}

static PyObject* BinarySearchTree_insert(BinarySearchTree* self, PyObject* args) {
    Py_INCREF(Py_None);
    PyObject* key = Py_None;
    Py_INCREF(Py_None);
    PyObject* data = Py_None;
    if(!PyArg_ParseTuple(args, "O|O", &key, &data)){ // ret_parent is optional
        return NULL;
    }

    PyObject* parent = PyLong_FromLong(0);

    PyObject* res = BinarySearchTree_search(self, Py_BuildValue("(O)",key), PyDict_New()); // keywords should be a dictionary, so empty dictionary here as no keywords
    BinaryTree* bt = self->binary_tree;
    if(res != Py_None){
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(res)])->data = data;
        Py_RETURN_NONE;
    }

    PyObject* walk = PyLong_FromLong(bt->root_idx);
    if(reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->key == Py_None){
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->key = key;
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->data = data;
        Py_RETURN_NONE;
    }

    if (PyType_Ready(&TreeNodeType) < 0) { // This has to be present to finalize a type object. This should be called on all type objects to finish their initialization.
        return NULL;
    }
    TreeNode* new_node = reinterpret_cast<TreeNode*>(TreeNode___new__(&TreeNodeType, Py_BuildValue("(OO)", key, data), PyDict_New()));
    PyObject* prev_node = PyLong_FromLong(bt->root_idx);
    bool flag = true;

    while(flag){
        PyObject* curr_key = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->key;
        if (!PyCallable_Check(bt->comparator)) {
            PyErr_SetString(PyExc_ValueError, "comparator should be callable");
            return NULL;
        }
        PyObject* arguments = Py_BuildValue("OO", key, curr_key);
        PyObject* cres = PyObject_CallObject(bt->comparator, arguments);
        Py_DECREF(arguments);
        if (!PyLong_Check(cres)) {
            PyErr_SetString(PyExc_TypeError, "bad return type from comparator");
            return NULL;
        }
        long long comp = PyLong_AsLongLong(cres);

        if(comp==0){
            if(reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->right == Py_None) {
                new_node->parent = prev_node;
                ArrayForTrees_append(bt->tree, Py_BuildValue( "[O]", reinterpret_cast<PyObject*>(new_node)) );
                reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->right = PyLong_FromLong(bt->size);
                bt->size = bt->size + 1;
                flag = false;
            }
            prev_node = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->right;
            walk = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->right;
        }
        else{
            if(reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->left == Py_None) {
                new_node->parent = prev_node;
                ArrayForTrees_append(bt->tree, Py_BuildValue( "[O]", reinterpret_cast<PyObject*>(new_node)) );
                reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->left = PyLong_FromLong(bt->size);
                bt->size = bt->size + 1;
                flag = false;
            }
            prev_node = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->left;
            walk = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->left;
        }
    }
    BinarySearchTree__update_size(self, Py_BuildValue("(O)",walk));
    Py_RETURN_NONE;
}

static PyObject* BinarySearchTree_delete(BinarySearchTree* self, PyObject *args, PyObject *kwds) {
    Py_INCREF(Py_None);
    PyObject* key = Py_None;
    key = PyObject_GetItem(args, PyZero);
    PyObject* kwd_parent = PyDict_New();
    PyDict_SetItemString(kwd_parent, "parent", PyLong_FromLong(1));
    PyObject* tup = BinarySearchTree_search(self, Py_BuildValue("(O)",key), kwd_parent);
    PyObject* walk = PyTuple_GetItem(tup, 0);
    PyObject* parent = PyTuple_GetItem(tup, 1);
    Py_INCREF(Py_None);
    PyObject* a = Py_None;
    if(walk == Py_None){
        Py_RETURN_NONE;
    }
    BinaryTree* bt = self->binary_tree;
    if(reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->left == Py_None && reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->right == Py_None) {
        if(parent == Py_None){
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[bt->root_idx])->data = Py_None;
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[bt->root_idx])->key = Py_None;
        }
        else{
            if(reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent)])->left == walk){
                Py_INCREF(Py_None);
                reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent)])->left = Py_None;
            }
            else{
                Py_INCREF(Py_None);
                reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent)])->right = Py_None;
            }
            a = parent;
            PyObject* par_key = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent)])->key;
            PyObject* root_key = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[bt->root_idx])->key;
            PyObject* new_indices = ArrayForTrees_delete(bt->tree, Py_BuildValue("(O)",walk));
            // bt->size = bt->size - 1; // TO DO: Fix b.insert(12,12), b.delete(12), b.insert(12)
            if(new_indices != Py_None){
                a = PyDict_GetItem(new_indices, par_key);
                bt->root_idx = PyLong_AsLong(PyDict_GetItem(new_indices, root_key));
            }
        }
        BinarySearchTree__update_size(self, Py_BuildValue("(O)",a));
    }
    else if(reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->left != Py_None && reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->right != Py_None) {
        PyObject* twalk = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->right;
        PyObject* par = walk;
        bool flag = false;
        while(reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(twalk)])->left != Py_None) {
            flag = true;
            par = twalk;
            twalk = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(twalk)])->left;
        }
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->data = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(twalk)])->data;
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->key = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(twalk)])->key;
        if (flag) {
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(par)])->left = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(twalk)])->right;
        }
        else {
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(par)])->right = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(twalk)])->right;
        }

        if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(twalk)])->right != Py_None) {
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(twalk)])->right)])->parent = par;
        }

        if(twalk != Py_None){
            a = par;
            PyObject* par_key = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(par)])->key;
            PyObject* root_key = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[bt->root_idx])->key;
            PyObject* new_indices = ArrayForTrees_delete(bt->tree, Py_BuildValue("(O)",twalk));
            if(new_indices != Py_None){
                a = PyDict_GetItem(new_indices, par_key);
                bt->root_idx = PyLong_AsLong(PyDict_GetItem(new_indices, root_key));
            }
        }
        BinarySearchTree__update_size(self, Py_BuildValue("(O)",a));
    }
    Py_RETURN_TRUE;
}

static struct PyMethodDef BinarySearchTree_PyMethodDef[] = {
    {"insert", (PyCFunction) BinarySearchTree_insert, METH_VARARGS | METH_KEYWORDS, NULL},
    {"delete", (PyCFunction) BinarySearchTree_delete, METH_VARARGS | METH_KEYWORDS, NULL},
    {"search", (PyCFunction) BinarySearchTree_search, METH_VARARGS | METH_KEYWORDS, NULL},
    {NULL}
};


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
    /* tp_str */ (reprfunc) BinarySearchTree___str__,
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
    /* tp_members */ 0,
    /* tp_getset */ 0,
    /* tp_base */ &BinaryTreeType,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ BinarySearchTree___new__,
};

#endif
