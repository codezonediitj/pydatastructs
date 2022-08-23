#ifndef UTILS_GRAPHEDGE_HPP
#define UTILS_GRAPHEDGE_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"
#include "GraphNode.hpp"


typedef struct {
    PyObject_HEAD
    GraphNodeCpp* source;
    GraphNodeCpp* target;
    PyObject* value;
} GraphEdgeCpp;

static void GraphEdgeCpp_dealloc(GraphEdgeCpp *self) {
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* GraphEdgeCpp__new__(PyTypeObject* type, PyObject *args, PyObject *kwds) {
    GraphEdgeCpp *self;
    self = reinterpret_cast<GraphEdgeCpp*>(type->tp_alloc(type, 0));

    static char *kwlist[] = {"node1", "node2", "value", NULL};
    PyObject *source, *target, *value = Py_None;
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "OO|O", kwlist, &source, &target, &value)) {
        PyErr_SetString(PyExc_ValueError, "Error creating GraphEdgeCpp bad arguments");
        return NULL;
    }

    if (source == NULL || !PyObject_IsInstance(source, reinterpret_cast<PyObject*>(&GraphNodeCppType))) {
        PyErr_SetString(PyExc_ValueError, "Error in argument `source`");
        return NULL;
    }

    if (target == NULL || !PyObject_IsInstance(target, reinterpret_cast<PyObject*>(&GraphNodeCppType))) {
        PyErr_SetString(PyExc_ValueError, "Error in argument `target`");
        return NULL;
    }

    self->source = reinterpret_cast<GraphNodeCpp*>(source);
    self->target = reinterpret_cast<GraphNodeCpp*>(target);
    self->value = value;

    return reinterpret_cast<PyObject*>(self);
}

static PyObject* GraphEdgeCpp__str__(GraphEdgeCpp *self) {
    return PyUnicode_FromString(("('" + self->source->name + "', '" + self->target->name + "')").c_str());
}

static PyObject* GraphEdgeCpp_get_source(GraphEdgeCpp* self, void *closure) {
    Py_INCREF(self->source);
    return reinterpret_cast<PyObject*>(self->source);
}

static int GraphEdgeCpp_set_source(GraphEdgeCpp* self, PyObject *value, void *closure) {
    if (value == NULL) {
        PyErr_SetString(PyExc_ValueError, "value is NULL");
        return -1;
    }
    if (!PyObject_IsInstance(value, reinterpret_cast<PyObject*>(&GraphNodeCppType))) {
        PyErr_SetString(PyExc_TypeError, "value must be a GraphNodeCpp instance");
        return -1;
    }

    PyObject *tmp = reinterpret_cast<PyObject*>(self->source);
    Py_INCREF(value);
    self->source = reinterpret_cast<GraphNodeCpp*>(value);
    Py_DECREF(tmp);
    return 0;
}

static PyObject* GraphEdgeCpp_get_target(GraphEdgeCpp* self, void *closure) {
    Py_INCREF(self->target);
    return reinterpret_cast<PyObject*>(self->target);
}

static int GraphEdgeCpp_set_target(GraphEdgeCpp* self, PyObject *value, void *closure) {
    if (value == NULL) {
        PyErr_SetString(PyExc_ValueError, "value is NULL");
        return -1;
    }
    if (!PyObject_IsInstance(value, reinterpret_cast<PyObject*>(&GraphNodeCppType))) {
        PyErr_SetString(PyExc_TypeError, "value must be a GraphNodeCpp instance");
        return -1;
    }

    PyObject *tmp = reinterpret_cast<PyObject*>(self->target);
    Py_INCREF(value);
    self->target = reinterpret_cast<GraphNodeCpp*>(value);
    Py_DECREF(tmp);
    return 0;
}

static PyGetSetDef GraphEdgeCpp_get_setters[] = {
        {"source", (getter) GraphEdgeCpp_get_source, (setter) GraphEdgeCpp_set_source, "graph edge source", NULL},
        {"target", (getter) GraphEdgeCpp_get_target, (setter) GraphEdgeCpp_set_target, "graph edge target", NULL},
        {NULL},
};

static PyMemberDef GraphEdgeCpp_members[] = {
        {"value", T_OBJECT_EX, offsetof(GraphEdgeCpp, value), 0, "graph edge value"},
        {NULL}  /* Sentinel */
};

static PyTypeObject GraphEdgeCppType = {
        /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "GraphEdgeCpp",
        /* tp_basicsize */ sizeof(GraphEdgeCpp),
        /* tp_itemsize */ 0,
        /* tp_dealloc */ (destructor) GraphEdgeCpp_dealloc,
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
        /* tp_str */ (reprfunc) GraphEdgeCpp__str__,
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
        /* tp_members */ GraphEdgeCpp_members,
        /* tp_getset */ GraphEdgeCpp_get_setters,
        /* tp_base */ 0,
        /* tp_dict */ 0,
        /* tp_descr_get */ 0,
        /* tp_descr_set */ 0,
        /* tp_dictoffset */ 0,
        /* tp_init */ 0,
        /* tp_alloc */ 0,
        /* tp_new */ GraphEdgeCpp__new__,
};

#endif
