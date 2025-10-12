#ifndef ADJACENCY_MATRIX_GRAPH_NODE_HPP
#define ADJACENCY_MATRIX_GRAPH_NODE_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <string>
#include "GraphNode.hpp"

extern PyTypeObject AdjacencyMatrixGraphNodeType;

typedef struct {
    GraphNode super;
} AdjacencyMatrixGraphNode;

static void AdjacencyMatrixGraphNode_dealloc(AdjacencyMatrixGraphNode* self){
    Py_TYPE(self)->tp_free(reinterpret_cast<PyTypeObject*>(self));
}

static PyObject* AdjacencyMatrixGraphNode_new(PyTypeObject* type, PyObject* args, PyObject* kwds){
    PyObject* base_obj = GraphNode_new(type, args, kwds);
    if (!base_obj) {
        return NULL;
    }

    AdjacencyMatrixGraphNode* self = reinterpret_cast<AdjacencyMatrixGraphNode*>(base_obj);
    self->super.type_tag = NodeType_::AdjacencyMatrixGraphNode;

    return reinterpret_cast<PyObject*>(self);
}

#endif
