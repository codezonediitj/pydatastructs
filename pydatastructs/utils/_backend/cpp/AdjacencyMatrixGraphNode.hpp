#ifndef UTILS_ADJACENCYMATRIXGRAPHNODE_HPP
#define UTILS_ADJACENCYMATRIXGRAPHNODE_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <string>
#include "GraphNode.hpp"
#include "utils.hpp"


typedef struct {
    // Inheritance
    GraphNodeCpp super;
} AdjacencyMatrixGraphNodeCpp;


static void AdjacencyMatrixGraphNodeCpp_dealloc(AdjacencyMatrixGraphNodeCpp *self) {
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* AdjacencyMatrixGraphNodeCpp__new__(PyTypeObject* type, PyObject *args, PyObject *kwds) {
    AdjacencyMatrixGraphNodeCpp *self;
    self = reinterpret_cast<AdjacencyMatrixGraphNodeCpp*>(type->tp_alloc(type, 0));

    static char *kwlist[] = {"name", "data", NULL};
    PyObject* name, *data = Py_None;
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O|O", kwlist, &name, &data)) {
        PyErr_SetString(PyExc_ValueError, "Error creating AdjacencyMatrixGraphNode bad arguments");
        return NULL;
    }

    std::string name_str = PyObject_AsStdString(name);
    self->super.name = name_str;
    self->super.data = data;

    return reinterpret_cast<PyObject*>(self);
}

static PyTypeObject AdjacencyMatrixGraphNodeCppType = {
        /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "AdjacencyMatrixGraphNodeCpp",
        /* tp_basicsize */ sizeof(AdjacencyMatrixGraphNodeCpp),
        /* tp_itemsize */ 0,
        /* tp_dealloc */ (destructor) AdjacencyMatrixGraphNodeCpp_dealloc,
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
        /* tp_flags */  Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
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
        /* tp_base */ &GraphNodeCppType,
        /* tp_dict */ 0,
        /* tp_descr_get */ 0,
        /* tp_descr_set */ 0,
        /* tp_dictoffset */ 0,
        /* tp_init */ 0,
        /* tp_alloc */ 0,
        /* tp_new */ AdjacencyMatrixGraphNodeCpp__new__,
};

#endif
