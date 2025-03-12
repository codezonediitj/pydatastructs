#ifndef GRAPH_EDGE_HPP
#define GRAPH_EDGE_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <string>
#include "GraphNode.hpp"

extern PyTypeObject GraphEdgeType;

typedef struct {
    PyObject_HEAD
    PyObject* source;
    PyObject* target;
    PyObject* value;
} GraphEdge;

static void GraphEdge_dealloc(GraphEdge* self) {
    Py_XDECREF(self->source);
    Py_XDECREF(self->target);
    Py_XDECREF(self->value);
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* GraphEdge_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    GraphEdge* self;
    self = reinterpret_cast<GraphEdge*>(type->tp_alloc(type, 0));
    if (!self) return NULL;

    static char* kwlist[] = {"node1", "node2", "value", NULL};
    PyObject* node1;
    PyObject* node2;
    PyObject* value = Py_None;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "OO|O", kwlist, &node1, &node2, &value)) {
        PyErr_SetString(PyExc_ValueError, "Invalid arguments: Expected (GraphNode, GraphNode, optional value)");
        return NULL;
    }

    Py_INCREF(node1);
    Py_INCREF(node2);
    Py_INCREF(value);

    self->source = node1;
    self->target = node2;
    self->value = value;

    return reinterpret_cast<PyObject*>(self);
}

static PyObject* GraphEdge_str(GraphEdge* self) {
    PyObject* source_name = PyObject_GetAttrString(self->source, "name");
    PyObject* target_name = PyObject_GetAttrString(self->target, "name");

    if (!source_name || !target_name) {
        PyErr_SetString(PyExc_AttributeError, "Both nodes must have a 'name' attribute.");
        return NULL;
    }

    PyObject* str_repr = PyUnicode_FromFormat("('%U', '%U')", source_name, target_name);

    Py_XDECREF(source_name);
    Py_XDECREF(target_name);
    return str_repr;
}

PyTypeObject GraphEdgeType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "GraphEdge",
    /* tp_basicsize */ sizeof(GraphEdge),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor)GraphEdge_dealloc,
    /* tp_print */ 0,
    /* tp_getattr */ 0,
    /* tp_setattr */ 0,
    /* tp_reserved */ 0,
    /* tp_repr */ 0,
    /* tp_as_number */ 0,
    /* tp_as_sequence */ 0,
    /* tp_as_mapping */ 0,
    /* tp_hash */ 0,
    /* tp_call */ 0,
    /* tp_str */ (reprfunc)GraphEdge_str,
    /* tp_getattro */ 0,
    /* tp_setattro */ 0,
    /* tp_as_buffer */ 0,
    /* tp_flags */ Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    /* tp_doc */ "Data Structure for a Graph Edge",
    /* tp_traverse */ 0,
    /* tp_clear */ 0,
    /* tp_richcompare */ 0,
    /* tp_weaklistoffset */ 0,
    /* tp_iter */ 0,
    /* tp_iternext */ 0,
    /* tp_methods */ 0,
    /* tp_members */ 0,
    /* tp_getset */ 0,
    /* tp_base */ 0,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ GraphEdge_new,
};

#endif
