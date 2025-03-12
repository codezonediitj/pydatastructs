#ifndef GRAPH_NODE_HPP
#define GRAPH_NODE_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <string>

typedef struct {
    PyObject_HEAD
    std::string name;
    PyObject* data;
} GraphNode;

static void GraphNode_dealloc(GraphNode* self){
    Py_XDECREF(self->data);
    Py_TYPE(self)->tp_free(reinterpret_cast<PyTypeObject*>(self));
}

static PyObject* GraphNode_new(PyTypeObject* type, PyObject* args, PyObject* kwds){
    GraphNode* self;
    self = reinterpret_cast<GraphNode*>(type->tp_alloc(type,0));
    if (!self) return NULL;

    static char* kwlist[] = { "name", "data", NULL };
    const char* name;
    PyObject* data = Py_None;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "s|O", kwlist, &name, &data)) {
        PyErr_SetString(PyExc_ValueError, "Invalid arguments: Expected (str, object)");
        return NULL;
    }

    self->name = std::string(name);
    Py_INCREF(data);
    self->data = data;

    return reinterpret_cast<PyObject*>(self);
}

static PyObject* GraphNode_str(GraphNode* self) {
    return PyUnicode_FromString(("('" + self->name + "', " + PyUnicode_AsUTF8(PyObject_Str(self->data)) + ")").c_str());
}

static PyObject* GraphNode_get(GraphNode* self, void *closure) {
    if (closure == (void*)"name") {
        return PyUnicode_FromString(self->name.c_str());
    }
    if (closure == (void*)"data") {
        Py_INCREF(self->data);
        return self->data;
    }
    Py_RETURN_NONE;
}

static int GraphNode_set(GraphNode* self, PyObject *value, void *closure) {
    if (value == NULL) {
        PyErr_SetString(PyExc_ValueError, "value is NULL");
        return -1;
    }

    if (closure == (void*)"name") {
        if (!PyUnicode_Check(value)) {
            PyErr_SetString(PyExc_TypeError, "value to be set must be a string");
            return -1;
        }
        self->name = PyUnicode_AsUTF8(value);
    }
    else if (closure == (void*)"data") {
        PyObject *tmp = self->data;
        Py_INCREF(value);
        self->data = value;
        Py_DECREF(tmp);
    }
    else {
        PyErr_SetString(PyExc_AttributeError, "Unknown attribute");
        return -1;
    }

    return 0;
}

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
        /* tp_getset */ 0,
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
