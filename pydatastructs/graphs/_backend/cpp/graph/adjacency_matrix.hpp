#ifndef GRAPHS_ADJACENCYMATRIX_HPP
#define GRAPHS_ADJACENCYMATRIX_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <cstdlib>
#include <string>
#include "../../../../utils/_backend/cpp/utils.hpp"

typedef struct {
    PyObject_HEAD
    size_t n_vertices;
    PyObject** vertices;
    PyObject* matrix;
    PyObject* edge_weights;
} AdjacencyMatrix;

static void AdjacencyMatrix_dealloc(AdjacencyMatrix *self) {
    std::free(self->vertices);
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* AdjacencyMatrix__new__(PyTypeObject* type, PyObject *vertices_objs, PyObject *kwds) {
    AdjacencyMatrix *self;
    self = reinterpret_cast<AdjacencyMatrix *>(type->tp_alloc(type, 0));

    self->n_vertices = PyObject_Length(vertices_objs);
    self->vertices = reinterpret_cast<PyObject**>(std::malloc(self->n_vertices * sizeof(PyObject*)));

    self->matrix = PyDict_New();
    if (self->matrix == NULL) {
        PyErr_SetString(PyExc_ValueError, "Cannot initialize matrix");
    }
    for (long i = 0; i < self->n_vertices; i++) {
        PyObject *vertex_i = PyObject_GetItem(vertices_objs, PyLong_FromLong(i));
        PyObject *vertex_name = PyObject_GetAttrString(vertex_i, "name");

        self->vertices[i] = vertex_name;

        if (PyObject_SetAttr(reinterpret_cast<PyObject*>(self), vertex_name, vertex_i) == -1) {
            PyErr_SetString(PyExc_ValueError, ("Cannot add vertex index #"+std::to_string(i)+" to graph").c_str());
        }

        PyObject *new_empty_dict = PyDict_New();
        if (new_empty_dict == NULL) {
            PyErr_SetString(PyExc_ValueError, "Cannot instantiate empty dict");
        }
        if (PyDict_SetItem(self->matrix, vertex_name, new_empty_dict) == -1) {
            PyErr_SetString(PyExc_ValueError, "Cannot add vertex to matrix");
        }
    }

    self->edge_weights = PyDict_New();
    if (self->edge_weights == NULL) {
        PyErr_SetString(PyExc_ValueError, "Cannot initialize edge weights dict");
    }

    return reinterpret_cast<PyObject*>(self);
}

static PyObject* AdjacencyMatrix__str__(AdjacencyMatrix *self) {
    return __str__(self->vertices, self->n_vertices);
}

static PyTypeObject AdjacencyMatrixType = {
        /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "AdjacencyMatrix",
        /* tp_basicsize */ sizeof(AdjacencyMatrix),
        /* tp_itemsize */ 0,
        /* tp_dealloc */ (destructor) AdjacencyMatrix_dealloc,
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
        /* tp_str */ (reprfunc) AdjacencyMatrix__str__,
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
        /* tp_base */ 0,
        /* tp_dict */ 0,
        /* tp_descr_get */ 0,
        /* tp_descr_set */ 0,
        /* tp_dictoffset */ 0,
        /* tp_init */ 0,
        /* tp_alloc */ 0,
        /* tp_new */ AdjacencyMatrix__new__,
};

#endif
