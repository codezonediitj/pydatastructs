#ifndef TREES_BINARYINDEXEDTREE_HPP
#define TREES_BINARYINDEXEDTREE_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <cstdlib>
#include "../../../utils/_backend/cpp/utils.hpp"
#include "../../../utils/_backend/cpp/TreeNode.hpp"
#include "../../../linear_data_structures/_backend/cpp/arrays/ArrayForTrees.hpp"
#include "../../../linear_data_structures/_backend/cpp/arrays/DynamicOneDimensionalArray.hpp"

// Copied  binary trees and changed the name to BinaryIndexedTree
// Start from the struct

typedef struct {
    PyObject_HEAD
    OneDimensionalArray* array;
    PyObject* tree;
    PyObject* flag;
} BinaryIndexedTree;

static void BinaryIndexedTree_dealloc(BinaryIndexedTree *self) {
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* BinaryIndexedTree___new__(PyTypeObject* type, PyObject *args, PyObject *kwds) {
    BinaryIndexedTree *self;
    self = reinterpret_cast<BinaryIndexedTree*>(type->tp_alloc(type, 0));

    // Python code is such that arguments  are: type(array[0]) and array

    if (PyType_Ready(&OneDimensionalArrayType) < 0) { // This has to be present to finalize a type object. This should be called on all type objects to finish their initialization.
        return NULL;
    }
    PyObject* _one_dimensional_array = OneDimensionalArray___new__(&OneDimensionalArrayType, args, kwds);
    if ( !_one_dimensional_array ) {
        return NULL;
    }
    self->array = reinterpret_cast<OneDimensionalArray*>(_one_dimensional_array);
    self->tree = PyList_New(self->array->_size+2);
    for(int i=0;i<self->array->_size+2;i++){
        PyList_SetItem(self->tree, i, PyZero);
    }
    self->flag = PyList_New(self->array->_size);
    for(int i=0;i<self->array->_size;i++){
        PyList_SetItem(self->tree, i, PyZero);
    }

    return reinterpret_cast<PyObject*>(self);
}


static struct PyMethodDef BinaryIndexedTree_PyMethodDef[] = {
    {NULL}
};

static PyMemberDef BinaryIndexedTree_PyMemberDef[] = {
    {"array", T_OBJECT_EX, offsetof(BinaryIndexedTree, array), 0, "array"},
    {"tree", T_OBJECT_EX, offsetof(BinaryIndexedTree, tree), 0, "tree"},
    {"flag", T_OBJECT_EX, offsetof(BinaryIndexedTree, flag), 0, "flag"},
    {NULL}  /* Sentinel */
};


static PyTypeObject BinaryIndexedTreeType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "BinaryIndexedTree",
    /* tp_basicsize */ sizeof(BinaryIndexedTree),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor) BinaryIndexedTree_dealloc,
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
    /* tp_methods */ BinaryIndexedTree_PyMethodDef,
    /* tp_members */ BinaryIndexedTree_PyMemberDef,
    /* tp_getset */ 0,
    /* tp_base */ &PyBaseObject_Type,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ BinaryIndexedTree___new__,
};

#endif
