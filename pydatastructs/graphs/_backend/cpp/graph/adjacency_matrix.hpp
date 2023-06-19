#ifndef GRAPHS_ADJACENCYMATRIX_HPP
#define GRAPHS_ADJACENCYMATRIX_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <cstdlib>
#include <string>
#include <map>
#include <utility>
#include <vector>
#include "../../../../utils/_backend/cpp/utils.hpp"
#include "../../../../utils/_backend/cpp/GraphEdge.hpp"
#include "../../../../utils/_backend/cpp/AdjacencyMatrixGraphNode.hpp"
#include "../../../../utils/_backend/cpp/GraphNode.hpp"

typedef struct {
    PyObject_HEAD
    size_t n_vertices;
    std::map<int, int> mp;
//    AdjacencyMatrixGraphNodeCpp
//    std::map<std::string, PyObject*> vertices;
//    std::map<std::pair<std::string, std::string>, bool> matrix;
    // GraphEdgeCpp
//    std::map<std::pair<std::string, std::string>, PyObject*> edge_weights;
} AdjacencyMatrix;

static void AdjacencyMatrix_dealloc(AdjacencyMatrix *self) {
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* AdjacencyMatrix__new__(PyTypeObject* type, PyObject *vertices_objs, PyObject *kwds) {
    PyObject* utils_module = PyImport_Import(PyUnicode_FromString("pydatastructs.utils._backend.cpp._utils"));
    PyObject* module_dict = PyModule_GetDict(utils_module);
    PyObject* ImportedAdjacencyMatrixGraphNodeCpp = PyDict_GetItemString(module_dict, "AdjacencyMatrixGraphNodeCpp");

    AdjacencyMatrix *self;
    self = reinterpret_cast<AdjacencyMatrix *>(type->tp_alloc(type, 0));

    self->n_vertices = PyObject_Length(vertices_objs);

    for (long i = 0; i < self->n_vertices; i++) {
        PyObject *vertex_i = PyObject_GetItem(vertices_objs, PyLong_FromLong(i));

        if (vertex_i == NULL || !PyObject_IsInstance(vertex_i, ImportedAdjacencyMatrixGraphNodeCpp)) {
            PyErr_SetString(
                PyExc_TypeError,
                ("Element #"+std::to_string(i)+" of the vertex list is not an instance of GraphNodeCpp").c_str()
            );
            return NULL;
        }

        std::string vertex_name = reinterpret_cast<AdjacencyMatrixGraphNodeCpp*>(vertex_i)->super.name;
        printf("vertex_name: %s\n", vertex_name.c_str());
        printf("%s\n", PyObject_AsStdString(PyObject_Type(vertex_i)).c_str());

//        self->vertices[vertex_name] = vertex_i;
        self->mp[0] = 1;
        printf("AA\n");
    }

    return reinterpret_cast<PyObject*>(self);
}

static PyObject* AdjacencyMatrix__str__(AdjacencyMatrix *self) {
    int i = 0;
    std::string array__str__ = "[";
//    for (auto x: self->vertices) {
//        array__str__.append(PyObject_AsStdString(x.second)));
//        if( i + 1 != self->n_vertices ) {
//            array__str__.append(", ");
//        }
//
//        i++;
//    }
    array__str__.append("]");

    return PyUnicode_FromString(array__str__.c_str());
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
