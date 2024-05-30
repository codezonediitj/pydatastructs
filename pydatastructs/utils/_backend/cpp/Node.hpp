#ifndef UTILS_NODE_HPP
#define UTILS_NODE_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include "utils.hpp"

typedef struct {
    PyObject_HEAD
} Node;
// Node is an abstract class representing a Node

static void Node_dealloc(Node *self) {
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}


static PyTypeObject NodeType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "Node",
    /* tp_basicsize */ sizeof(Node),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor) Node_dealloc,
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
    /* tp_base */ &PyBaseObject_Type,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ 0,
};

#endif
