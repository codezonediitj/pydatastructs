#ifndef GRAPH_NODE_HPP
#define GRAPH_NODE_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <string>
#include <variant>
#include "Node.hpp"

enum class DataType {
    None,
    Int,
    Double,
    String,
    PyObject
};

typedef struct {
    PyObject_HEAD
    NodeType_ type_tag;
    std::string name;
    int internal_id;
    std::variant<std::monostate, int64_t, double, std::string, PyObject *> data;
    DataType data_type;
} GraphNode;

static void GraphNode_dealloc(GraphNode* self) {
    if (self->data_type == DataType::PyObject) {
        Py_XDECREF(std::get<PyObject*>(self->data));
    }
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* GraphNode_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    GraphNode* self = reinterpret_cast<GraphNode*>(type->tp_alloc(type, 0));
    if (!self) return NULL;
    self->type_tag = NodeType_::GraphNode;

    new (&self->name) std::string();
    new (&self->data) std::variant<std::monostate, int64_t, double, std::string, PyObject*>();
    self->data_type = DataType::None;

    static char* kwlist[] = { "name", "data", NULL };
    const char* name;
    PyObject* data = Py_None;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "s|O", kwlist, &name, &data)) {
        PyErr_SetString(PyExc_ValueError, "Invalid arguments: Expected (str, object)");
        return NULL;
    }

    self->name = std::string(name);
    self->internal_id = -1;
    if (data == Py_None)
    {
        self->data = std::monostate{};
        self->data_type = DataType::None;
    }
    else if (PyLong_Check(data))
    {
        self->data = static_cast<int64_t>(PyLong_AsLongLong(data));
        self->data_type = DataType::Int;
    }
    else if (PyFloat_Check(data))
    {
        self->data = PyFloat_AsDouble(data);
        self->data_type = DataType::Double;
    }
    else if (PyUnicode_Check(data))
    {
        const char* s = PyUnicode_AsUTF8(data);
        self->data = std::string(s);
        self->data_type = DataType::String;
    }
    else
    {
        self->data = data;
        self->data_type = DataType::PyObject;
        Py_INCREF(data);
    }

    return reinterpret_cast<PyObject*>(self);
}

static PyObject* GraphNode_str(GraphNode* self) {
    std::string repr = "('" + self->name + "', ";

    switch (self->data_type) {
        case DataType::None:
            repr += "None";
            break;
        case DataType::Int:
            repr += std::to_string(std::get<int64_t>(self->data));
            break;
        case DataType::Double:
            repr += std::to_string(std::get<double>(self->data));
            break;
        case DataType::String:
            repr += "'" + std::get<std::string>(self->data) + "'";
            break;
        case DataType::PyObject: {
            PyObject* repr_obj = PyObject_Repr(std::get<PyObject*>(self->data));
            if (repr_obj) {
                const char* repr_cstr = PyUnicode_AsUTF8(repr_obj);
                repr += repr_cstr ? repr_cstr : "<unprintable>";
                Py_DECREF(repr_obj);
            } else {
                repr += "<error in repr>";
            }
            break;
        }
    }

    repr += ")";
    return PyUnicode_FromString(repr.c_str());
}

static PyObject* GraphNode_get(GraphNode* self, void *closure) {
    const char* attr = reinterpret_cast<const char*>(closure);
    if (strcmp(attr, "name") == 0) {
        return PyUnicode_FromString(self->name.c_str());
    } else if (strcmp(attr, "data") == 0) {
        switch (self->data_type) {
            case DataType::None:
                Py_RETURN_NONE;
            case DataType::Int:
                return PyLong_FromLongLong(std::get<int64_t>(self->data));
            case DataType::Double:
                return PyFloat_FromDouble(std::get<double>(self->data));
            case DataType::String:
                return PyUnicode_FromString(std::get<std::string>(self->data).c_str());
            case DataType::PyObject:
                Py_INCREF(std::get<PyObject*>(self->data));
                return std::get<PyObject*>(self->data);
        }
    }
    Py_RETURN_NONE;
}

static int GraphNode_set(GraphNode* self, PyObject *value, void *closure) {
    const char* attr = reinterpret_cast<const char*>(closure);
    if (!value) {
        PyErr_SetString(PyExc_ValueError, "Cannot delete attributes");
        return -1;
    }

    if (strcmp(attr, "name") == 0) {
        if (!PyUnicode_Check(value)) {
            PyErr_SetString(PyExc_TypeError, "name must be a string");
            return -1;
        }
        self->name = PyUnicode_AsUTF8(value);
    } else if (strcmp(attr, "data") == 0) {
        if (self->data_type == DataType::PyObject) {
            Py_XDECREF(std::get<PyObject*>(self->data));
        }

        if (value == Py_None) {
            self->data = std::monostate{};
            self->data_type = DataType::None;
        } else if (PyLong_Check(value)) {
            self->data = static_cast<int64_t>(PyLong_AsLongLong(value));
            self->data_type = DataType::Int;
        } else if (PyFloat_Check(value)) {
            self->data = PyFloat_AsDouble(value);
            self->data_type = DataType::Double;
        } else if (PyUnicode_Check(value)) {
            self->data = std::string(PyUnicode_AsUTF8(value));
            self->data_type = DataType::String;
        } else {
            Py_INCREF(value);
            self->data = value;
            self->data_type = DataType::PyObject;
        }
    } else {
        PyErr_SetString(PyExc_AttributeError, "Unknown attribute");
        return -1;
    }

    return 0;
}

static PyGetSetDef GraphNode_getsetters[] = {
    {
        const_cast<char*>("name"),
        reinterpret_cast<getter>(GraphNode_get),
        reinterpret_cast<setter>(GraphNode_set),
        const_cast<char*>("name"),
        reinterpret_cast<void*>(const_cast<char*>("name"))
    },
    {
        const_cast<char*>("data"),
        reinterpret_cast<getter>(GraphNode_get),
        reinterpret_cast<setter>(GraphNode_set),
        const_cast<char*>("data"),
        reinterpret_cast<void*>(const_cast<char*>("data"))
    },
    {nullptr}
};

static struct PyMemberDef GraphNode_PyMemberDef[] = {
    {"type_tag", T_INT, offsetof(GraphNode, type_tag), 0, "GraphNode type_tag"},
    {NULL},
};


static PyTypeObject GraphNodeType = {
        /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "GraphNode",
        /* tp_basicsize */ sizeof(GraphNode),
        /* tp_itemsize */ 0,
        /* tp_dealloc */ (destructor) GraphNode_dealloc,
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
        /* tp_str */ (reprfunc) GraphNode_str,
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
        /* tp_members */ GraphNode_PyMemberDef,
        /* tp_getset */ GraphNode_getsetters,
        /* tp_base */ &PyBaseObject_Type,
        /* tp_dict */ 0,
        /* tp_descr_get */ 0,
        /* tp_descr_set */ 0,
        /* tp_dictoffset */ 0,
        /* tp_init */ 0,
        /* tp_alloc */ 0,
        /* tp_new */ GraphNode_new,
};

#endif
