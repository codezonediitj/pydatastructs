#ifndef UTILS_GRAPHNODE_HPP
#define UTILS_GRAPHNODE_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <string>
#include "utils.hpp"


typedef struct {
    PyObject_HEAD
    std::string name;
    PyObject* data;
} GraphNodeCpp;

static void GraphNodeCpp_dealloc(GraphNodeCpp *self) {
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* GraphNodeCpp__new__(PyTypeObject* type, PyObject *args, PyObject *kwds) {
    GraphNodeCpp *self;
    self = reinterpret_cast<GraphNodeCpp*>(type->tp_alloc(type, 0));
    return reinterpret_cast<PyObject*>(self);
}

static PyObject* GraphNodeCpp__str__(GraphNodeCpp *self) {
    return PyUnicode_FromString(("('" + self->name + "', " + PyObject_AsStdString(self->data) + ")").c_str());
}

static PyObject* GraphNodeCpp_get_name(GraphNodeCpp* self, void *closure) {
    return PyUnicode_FromString(self->name.c_str());
}

static int GraphNodeCpp_set_name(GraphNodeCpp* self, PyObject *value, void *closure) {
    if (value == NULL) {
        PyErr_SetString(PyExc_ValueError, "value is NULL");
        return -1;
    }

    if (!PyUnicode_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "value to be set must be string");
        return -1;
    }

    self->name = PyObject_AsStdString(value);
    return 0;
}

static PyObject* GraphNodeCpp_get_data(GraphNodeCpp* self, void *closure) {
    Py_INCREF(self->data);
    return self->data;
}

static int GraphNodeCpp_set_data(GraphNodeCpp* self, PyObject *value, void *closure) {
    if (value == NULL) {
        PyErr_SetString(PyExc_ValueError, "value is NULL");
        return -1;
    }

    PyObject *tmp = self->data;
    Py_INCREF(value);
    self->data = value;
    Py_DECREF(tmp);
    return 0;
}

static PyGetSetDef GraphNodeCpp_get_setters[] = {
    {"name", (getter) GraphNodeCpp_get_name, (setter) GraphNodeCpp_set_name, "node name", NULL},
    {"data", (getter) GraphNodeCpp_get_data, (setter) GraphNodeCpp_set_data, "node data", NULL},
    {NULL},
};

static PyTypeObject GraphNodeCppType = {
        /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "GraphNodeCpp",
        /* tp_basicsize */ sizeof(GraphNodeCpp),
        /* tp_itemsize */ 0,
        /* tp_dealloc */ (destructor) GraphNodeCpp_dealloc,
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
        /* tp_str */ (reprfunc) GraphNodeCpp__str__,
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
        /* tp_getset */ GraphNodeCpp_get_setters,
        /* tp_base */ &PyBaseObject_Type,
        /* tp_dict */ 0,
        /* tp_descr_get */ 0,
        /* tp_descr_set */ 0,
        /* tp_dictoffset */ 0,
        /* tp_init */ 0,
        /* tp_alloc */ 0,
        /* tp_new */ GraphNodeCpp__new__,
};

#endif
