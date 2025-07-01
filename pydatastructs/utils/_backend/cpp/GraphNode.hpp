#ifndef GRAPH_NODE_HPP
#define GRAPH_NODE_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <string>
#include <variant>

enum class DataType {
    None,
    Int,
    Double,
    String
};

typedef struct {
    PyObject_HEAD
    std::string name;
    std::variant<std::monostate, int64_t, double, std::string> data;
    DataType data_type;
} GraphNode;

static void GraphNode_dealloc(GraphNode* self){
    self->name.~basic_string();
    self->data.~decltype(self->data)();
    Py_TYPE(self)->tp_free(reinterpret_cast<PyTypeObject*>(self));
}

static PyObject* GraphNode_new(PyTypeObject* type, PyObject* args, PyObject* kwds){
    GraphNode* self;
    self = reinterpret_cast<GraphNode*>(type->tp_alloc(type,0));
    new (&self->name) std::string();
    new (&self->data) std::variant<std::monostate, int64_t, double, std::string>();
    self->data_type = DataType::None;
    if (!self) return NULL;

    static char* kwlist[] = { "name", "data", NULL };
    const char* name;
    PyObject* data = Py_None;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "s|O", kwlist, &name, &data)) {
        PyErr_SetString(PyExc_ValueError, "Invalid arguments: Expected (str, object)");
        return NULL;
    }

    self->name = std::string(name);

    if (data == Py_None) {
        self->data = std::monostate{};
        self->data_type = DataType::None;
    } else if (PyLong_Check(data)) {
        self->data = static_cast<int64_t>(PyLong_AsLongLong(data));
        self->data_type = DataType::Int;
    } else if (PyFloat_Check(data)) {
        self->data = PyFloat_AsDouble(data);
        self->data_type = DataType::Double;
    } else if (PyUnicode_Check(data)) {
        const char* s = PyUnicode_AsUTF8(data);
        self->data = std::string(s);
        self->data_type = DataType::String;
    } else {
        PyErr_SetString(PyExc_TypeError, "data must be int, float, str, or None");
        return NULL;
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
    }
    repr += ")";
    return PyUnicode_FromString(repr.c_str());
}

static PyObject* GraphNode_get(GraphNode* self, void *closure) {
    if (closure == (void*)"name") {
        return PyUnicode_FromString(self->name.c_str());
    } else if (closure == (void*)"data") {
        switch (self->data_type) {
            case DataType::None:
                Py_RETURN_NONE;
            case DataType::Int:
                return PyLong_FromLongLong(std::get<int64_t>(self->data));
            case DataType::Double:
                return PyFloat_FromDouble(std::get<double>(self->data));
            case DataType::String:
                return PyUnicode_FromString(std::get<std::string>(self->data).c_str());
        }
    }
    Py_RETURN_NONE;
}

static int GraphNode_set(GraphNode* self, PyObject *value, void *closure) {
    if (!value) {
        PyErr_SetString(PyExc_ValueError, "Cannot delete attributes");
        return -1;
    }

    if (closure == (void*)"name") {
        if (!PyUnicode_Check(value)) {
            PyErr_SetString(PyExc_TypeError, "name must be a string");
            return -1;
        }
        self->name = PyUnicode_AsUTF8(value);
    }
    else if (closure == (void*)"data") {
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
            PyErr_SetString(PyExc_TypeError, "data must be int, float, str, or None");
            return -1;
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
        /* tp_members */ 0,
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
