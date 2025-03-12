#ifndef ADJACENCY_MATRIX_GRAPH_NODE_HPP
#define ADJACENCY_MATRIX_GRAPH_NODE_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <string>
#include "GraphNode.hpp"

typedef struct {
    GraphNode super;
} AdjacencyMatrixGraphNode;

static void AdjacencyMatrixGraphNode_dealloc(AdjacencyMatrixGraphNode* self){
    Py_XDECREF(self->super.data);
    Py_TYPE(self)->tp_free(reinterpret_cast<PyTypeObject*>(self));
}xf

static PyObject* AdjacencyMatrixGraphNode_new(PyTypeObject* type, PyObject* args, PyObject* kwds){
    PyObject* base_obj = GraphNode_new(type, args, kwds);
    if (!base_obj) {
        return NULL;
    }

    AdjacencyMatrixGraphNode* self = reinterpret_cast<AdjacencyMatrixGraphNode*>(base_obj);

    return reinterpret_cast<PyObject*>(self);
}

PyTypeObject AdjacencyMatrixGraphNodeType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "AdjacencyMatrixGraphNode",
    /* tp_basicsize */ sizeof(AdjacencyMatrixGraphNode),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor)AdjacencyMatrixGraphNode_dealloc,
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
    /* tp_str */ 0,
    /* tp_getattro */ 0,
    /* tp_setattro */ 0,
    /* tp_as_buffer */ 0,
    /* tp_flags */ Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    /* tp_doc */ "Node Data Structure for an Adjacency Matrix Graph",
    /* tp_traverse */ 0,
    /* tp_clear */ 0,
    /* tp_richcompare */ 0,
    /* tp_weaklistoffset */ 0,
    /* tp_iter */ 0,
    /* tp_iternext */ 0,
    /* tp_methods */ 0,
    /* tp_members */ 0,
    /* tp_getset */ 0,
    /* tp_base */ &GraphNodeType,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ AdjacencyMatrixGraphNode_new,
};

#endif
