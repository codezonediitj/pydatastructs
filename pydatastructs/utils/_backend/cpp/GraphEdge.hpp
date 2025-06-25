#ifndef GRAPH_EDGE_HPP
#define GRAPH_EDGE_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <string>
#include <variant>
#include <cstdint>
#include "GraphNode.hpp"

extern PyTypeObject GraphEdgeType;

typedef struct {
    PyObject_HEAD
    PyObject* source;
    PyObject* target;
    std::variant<std::monostate, int64_t, double, std::string> value;
    DataType value_type;
} GraphEdge;

static void GraphEdge_dealloc(GraphEdge* self) {
    Py_XDECREF(self->source);
    Py_XDECREF(self->target);
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* GraphEdge_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    GraphEdge* self = PyObject_New(GraphEdge, &GraphEdgeType);
    if (!self) return NULL;

    new (&self->value) std::variant<std::monostate, int64_t, double, std::string>();
    self->value_type = DataType::None;

    static char* kwlist[] = {"node1", "node2", "value", NULL};
    PyObject* node1;
    PyObject* node2;
    PyObject* value = Py_None;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "OO|O", kwlist, &node1, &node2, &value)) {
        PyErr_SetString(PyExc_ValueError, "Expected (GraphNode, GraphNode, optional value)");
        return NULL;
    }

    Py_INCREF(node1);
    Py_INCREF(node2);
    self->source = node1;
    self->target = node2;

    if (value == Py_None) {
        self->value_type = DataType::None;
        self->value = std::monostate{};
    } else if (PyLong_Check(value)) {
        self->value_type = DataType::Int;
        self->value = static_cast<int64_t>(PyLong_AsLongLong(value));
    } else if (PyFloat_Check(value)) {
        self->value_type = DataType::Double;
        self->value = PyFloat_AsDouble(value);
    } else if (PyUnicode_Check(value)) {
        const char* str = PyUnicode_AsUTF8(value);
        self->value_type = DataType::String;
        self->value = std::string(str);
    } else {
        PyErr_SetString(PyExc_TypeError, "Unsupported edge value type (must be int, float, str, or None)");
        return NULL;
    }

    return reinterpret_cast<PyObject*>(self);
}

static PyObject* GraphEdge_str(GraphEdge* self) {
    std::string src = reinterpret_cast<GraphNode*>(self->source)->name;
    std::string tgt = reinterpret_cast<GraphNode*>(self->target)->name;
    std::string val_str;

    switch (self->value_type) {
        case DataType::Int:
            val_str = std::to_string(std::get<int64_t>(self->value));
            break;
        case DataType::Double:
            val_str = std::to_string(std::get<double>(self->value));
            break;
        case DataType::String:
            val_str = std::get<std::string>(self->value);
            break;
        case DataType::None:
        default:
            val_str = "None";
            break;
    }

    return PyUnicode_FromFormat("('%s', '%s', %s)", src.c_str(), tgt.c_str(), val_str.c_str());
}

static PyObject* GraphEdge_get_value(GraphEdge* self, void* closure) {
    switch (self->value_type) {
        case DataType::Int:
            return PyLong_FromLongLong(std::get<int64_t>(self->value));
        case DataType::Double:
            return PyFloat_FromDouble(std::get<double>(self->value));
        case DataType::String:
            return PyUnicode_FromString(std::get<std::string>(self->value).c_str());
        case DataType::None:
        default:
            Py_RETURN_NONE;
    }
}

static int GraphEdge_set_value(GraphEdge* self, PyObject* value) {
    if (value == Py_None) {
        self->value_type = DataType::None;
        self->value = std::monostate{};
    } else if (PyLong_Check(value)) {
        self->value_type = DataType::Int;
        self->value = static_cast<int64_t>(PyLong_AsLongLong(value));
    } else if (PyFloat_Check(value)) {
        self->value_type = DataType::Double;
        self->value = PyFloat_AsDouble(value);
    } else if (PyUnicode_Check(value)) {
        const char* str = PyUnicode_AsUTF8(value);
        self->value_type = DataType::String;
        self->value = std::string(str);
    } else {
        PyErr_SetString(PyExc_TypeError, "Edge value must be int, float, str, or None.");
        return -1;
    }
    return 0;
}

static PyGetSetDef GraphEdge_getsetters[] = {
    {"value", (getter)GraphEdge_get_value, (setter)GraphEdge_set_value, "Get or set edge value", NULL},
    {NULL}
};

inline PyTypeObject GraphEdgeType = {
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
