#ifndef ADJACENCY_LIST_GRAPH_NODE_HPP
#define ADJACENCY_LIST_GRAPH_NODE_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <string>
#include <unordered_map>
#include "GraphNode.hpp"
#include <variant>

extern PyTypeObject AdjacencyListGraphNodeType;

typedef struct {
    PyObject_HEAD
    NodeType_ type_tag;
    std::string name;
    int internal_id;
    std::variant<std::monostate, int64_t, double, std::string, PyObject *> data;
    DataType data_type;
    std::unordered_map<std::string, PyObject*> adjacent;
} AdjacencyListGraphNode;

static void AdjacencyListGraphNode_dealloc(AdjacencyListGraphNode* self) {
    if (self->data_type == DataType::PyObject) {
        Py_XDECREF(std::get<PyObject*>(self->data));
    }

    for (auto& pair : self->adjacent) {
        Py_XDECREF(pair.second);
    }
    self->adjacent.clear();
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* AdjacencyListGraphNode_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    AdjacencyListGraphNode* self = PyObject_New(AdjacencyListGraphNode, &AdjacencyListGraphNodeType);
    if (!self) return NULL;
    self->type_tag = NodeType_::AdjacencyListGraphNode;
    new (&self->adjacent) std::unordered_map<std::string, PyObject*>();
    new (&self->name) std::string();
    new (&self->data) std::variant<std::monostate, int64_t, double, std::string, PyObject*>();
    self->data_type = DataType::None;
    self->data = std::monostate{};
    self->internal_id = -1;

    static char* kwlist[] = { "name", "data", "adjacency_list", NULL };
    const char* name;
    PyObject* data = Py_None;
    PyObject* adjacency_list = Py_None;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "s|OO", kwlist, &name, &data, &adjacency_list)) {
        PyErr_SetString(PyExc_ValueError, "Invalid arguments: Expected (str, object, list)");
        return NULL;
    }

    self->name = std::string(name);

    if (data == Py_None) {
        self->data_type = DataType::None;
        self->data = std::monostate{};
    } else if (PyLong_Check(data)) {
        self->data_type = DataType::Int;
        self->data = static_cast<int64_t>(PyLong_AsLongLong(data));
    } else if (PyFloat_Check(data)) {
        self->data_type = DataType::Double;
        self->data = PyFloat_AsDouble(data);
    } else if (PyUnicode_Check(data)) {
        const char* str = PyUnicode_AsUTF8(data);
        self->data_type = DataType::String;
        self->data = std::string(str);
    } else {
        self->data_type = DataType::PyObject;
        Py_INCREF(data);
        self->data = data;
    }

    if (PyList_Check(adjacency_list)) {
        Py_ssize_t size = PyList_Size(adjacency_list);
        for (Py_ssize_t i = 0; i < size; i++) {
            PyObject* node = PyList_GetItem(adjacency_list, i);

            if (!PyObject_IsInstance(node, (PyObject*)&AdjacencyListGraphNodeType)) {
                PyErr_SetString(PyExc_TypeError, "Adjacency list must contain only AdjacencyListGraphNode instances");
                return NULL;
            }

            const char* adj_name = (reinterpret_cast<AdjacencyListGraphNode*>(node))->name.c_str();
            std::string str = std::string(adj_name);
            Py_INCREF(node);
            self->adjacent[str] = node;
        }
    }

    return reinterpret_cast<PyObject*>(self);
}

static PyObject* AdjacencyListGraphNode_add_adjacent_node(AdjacencyListGraphNode* self, PyObject* args) {
    const char* name;
    PyObject* data = Py_None;
    if (!PyArg_ParseTuple(args, "s|O", &name, &data)) {
        PyErr_SetString(PyExc_ValueError, "Invalid arguments: Expected (str, object)");
        return NULL;
    }

    if (self->adjacent.find(name) == self->adjacent.end()) {
        PyObject* new_node = PyObject_CallFunction(reinterpret_cast<PyObject*>(&AdjacencyListGraphNodeType), "sO", name, data);
        if (!new_node) {
            PyErr_SetString(PyExc_RuntimeError, "Failed to create adjacent node");
            return NULL;
        }
        self->adjacent[name] = new_node;
        Py_INCREF(new_node);
    } else {
        Py_XDECREF(self->adjacent[name]);
        Py_INCREF(data);
        self->adjacent[name] = data;
    }
    Py_RETURN_NONE;
}

static PyObject* AdjacencyListGraphNode_remove_adjacent_node(AdjacencyListGraphNode* self, PyObject* args) {
    const char* name;
    if (!PyArg_ParseTuple(args, "s", &name)) {
        PyErr_SetString(PyExc_ValueError, "Invalid arguments: Expected (str)");
        return NULL;
    }

    auto it = self->adjacent.find(name);
    if (it != self->adjacent.end()) {
        Py_XDECREF(it->second);
        self->adjacent.erase(it);
        Py_RETURN_NONE;
    } else {
        PyErr_SetString(PyExc_ValueError, "Node is not adjacent");
        return NULL;
    }
}

static PyObject* AdjacencyListGraphNode_get_name(AdjacencyListGraphNode* self, void* closure) {
    return PyUnicode_FromString(self->name.c_str());
}

static int AdjacencyListGraphNode_set_name(AdjacencyListGraphNode* self, PyObject* value, void* closure) {
    if (!PyUnicode_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "name must be a string");
        return -1;
    }
    self->name = PyUnicode_AsUTF8(value);
    return 0;
}

static PyObject* AdjacencyListGraphNode_get_data(AdjacencyListGraphNode* self, void* closure) {
    switch (self->data_type) {
        case DataType::Int:
            return PyLong_FromLongLong(std::get<int64_t>(self->data));
        case DataType::Double:
            return PyFloat_FromDouble(std::get<double>(self->data));
        case DataType::String:
            return PyUnicode_FromString(std::get<std::string>(self->data).c_str());
        case DataType::PyObject:
            Py_INCREF(std::get<PyObject*>(self->data));
            return std::get<PyObject*>(self->data);
        case DataType::None:
        default:
            Py_RETURN_NONE;
    }
}

static int AdjacencyListGraphNode_set_data(AdjacencyListGraphNode* self, PyObject* value, void* closure) {
    if (self->data_type == DataType::PyObject) {
        Py_XDECREF(std::get<PyObject*>(self->data));
    }

    if (value == Py_None) {
        self->data_type = DataType::None;
        self->data = std::monostate{};
    } else if (PyLong_Check(value)) {
        self->data_type = DataType::Int;
        self->data = static_cast<int64_t>(PyLong_AsLongLong(value));
    } else if (PyFloat_Check(value)) {
        self->data_type = DataType::Double;
        self->data = PyFloat_AsDouble(value);
    } else if (PyUnicode_Check(value)) {
        const char* str = PyUnicode_AsUTF8(value);
        if (!str) {
            PyErr_SetString(PyExc_ValueError, "Invalid UTF-8 string.");
            return -1;
        }
        self->data_type = DataType::String;
        self->data = std::string(str);
    } else {
        self->data_type = DataType::PyObject;
        Py_INCREF(value);
        self->data = value;
    }
    return 0;
}

static PyObject* AdjacencyListGraphNode_get_adjacent(AdjacencyListGraphNode* self, void* closure) {
    PyObject* py_dict = PyDict_New();
    if (!py_dict) return NULL;

    for (const auto& pair : self->adjacent) {
        PyDict_SetItemString(py_dict, pair.first.c_str(), pair.second);
    }

    return py_dict;
}

static int AdjacencyListGraphNode_set_adjacent(AdjacencyListGraphNode* self, PyObject* value, void* closure) {
    if (!PyDict_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "adjacent must be a dictionary");
        return -1;
    }

    self->adjacent.clear();

    PyObject *key, *val;
    Py_ssize_t pos = 0;
    while (PyDict_Next(value, &pos, &key, &val)) {
        if (!PyUnicode_Check(key) || !PyObject_IsInstance(val, (PyObject*)&AdjacencyListGraphNodeType)) {
            PyErr_SetString(PyExc_TypeError, "Keys must be strings and values must be AdjacencyListGraphNode instances");
            return -1;
        }

        const char* key_str = PyUnicode_AsUTF8(key);
        Py_INCREF(val);
        self->adjacent[key_str] = val;
    }

    return 0;
}

static struct PyMemberDef AdjacencyListGraphNode_PyMemberDef[] = {
    {"type_tag", T_INT, offsetof(AdjacencyListGraphNode, type_tag), 0, "AdjacencyListGraphNode type_tag"},
    {NULL},
};

static PyGetSetDef AdjacencyListGraphNode_getsetters[] = {
    {"name", (getter)AdjacencyListGraphNode_get_name, (setter)AdjacencyListGraphNode_set_name, "Get or set node name", NULL},
    {"data", (getter)AdjacencyListGraphNode_get_data, (setter)AdjacencyListGraphNode_set_data, "Get or set node data", NULL},
    {"adjacent", (getter)AdjacencyListGraphNode_get_adjacent, (setter)AdjacencyListGraphNode_set_adjacent, "Get or set adjacent nodes", NULL},
    {NULL}
};

static PyMethodDef AdjacencyListGraphNode_methods[] = {
    {"add_adjacent_node", (PyCFunction)AdjacencyListGraphNode_add_adjacent_node, METH_VARARGS, "Add adjacent node"},
    {"remove_adjacent_node", (PyCFunction)AdjacencyListGraphNode_remove_adjacent_node, METH_VARARGS, "Remove adjacent node"},
    {NULL}
};


#endif
