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

static int BinarySearchTree_left_size(BinarySearchTree* self, TreeNode* node) {
    if (node->left != Py_None) {
        TreeNode* n = reinterpret_cast<TreeNode*>(
            self->binary_tree->tree->_one_dimensional_array->_data[PyLong_AsLong(node->left)]
        );
        return n->size;
    } else {
        return 0;
    }
}

static int BinarySearchTree_right_size(BinarySearchTree* self, TreeNode* node) {
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
}

static PyObject* BinarySearchTree_search(BinarySearchTree* self, PyObject* args, PyObject *kwds) {
    // std::cout<<"BST search()"<<std::endl;
    Py_INCREF(Py_None);
    PyObject* ret_parent = Py_None;
    PyObject* key;
    static char* keywords[] = {"key","parent", NULL};
    if(!PyArg_ParseTupleAndKeywords(args, kwds, "O|O", keywords, &key, &ret_parent)){ // ret_parent is optional
        return NULL;
    }
    // std::cout<<"BST2"<<std::endl;
    BinaryTree* bt = self->binary_tree;
    PyObject* parent = Py_None;
    PyObject* walk = PyLong_FromLong(bt->root_idx); // root_idx is size_t, change it to long if needed

    // TO DO: Currently, key is a long, as it can't be None
    // if self.tree[walk].key is None:
    //     return None

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
        // std::cout<<"comp result: "<<comp<<std::endl;

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
    // std::cout<<PyLong_AsLong(key)<<std::endl;
    // if(data!=Py_None) std::cout<<PyLong_AsLong(data)<<std::endl;

    PyObject* parent = PyLong_FromLong(0);

    PyObject* res = BinarySearchTree_search(self, Py_BuildValue("(O)",key), PyDict_New()); // keywords should be a dictionary, so empty dictionary here as no keywords
    // std::cout<<PyLong_AsLong(res)<<std::endl;
    if(res != Py_None){
        reinterpret_cast<TreeNode*>(self->binary_tree->tree->_one_dimensional_array->_data[PyLong_AsLong(res)])->data = data;
        Py_RETURN_NONE;
    }

    long walk = self->binary_tree->root_idx;
    // if(reinterpret_cast<TreeNode*>(self->binary_tree->tree->_one_dimensional_array->_data[PyLong_AsLong(res)])->key == Py_None){

    // }

    Py_RETURN_NONE;
}

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

static struct PyMethodDef BinarySearchTree_PyMethodDef[] = {
    {"insert", (PyCFunction) BinarySearchTree_insert, METH_VARARGS | METH_KEYWORDS, NULL},
    // {"delete", (PyCFunction) BinarySearchTree_delete, METH_VARARGS | METH_KEYWORDS, NULL},
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
