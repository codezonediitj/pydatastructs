#ifndef LINEAR_DATA_STRUCTURES_DYNAMIC_ARRAY_HPP
#define LINEAR_DATA_STRUCTURES_DYNAMIC_ARRAY_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include "Array.hpp"

typedef struct {
    PyObject_HEAD
} DynamicArray;

static PyTypeObject DynamicArrayType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "DynamicArray",
    /* tp_basicsize */ sizeof(DynamicArray),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ 0,
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
    /* tp_methods */ 0,
    /* tp_members */ 0,
    /* tp_getset */ 0,
    /* tp_base */ &ArrayType,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ 0,
};

#endif
