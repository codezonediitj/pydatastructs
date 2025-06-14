#ifndef ADJACENCY_MATRIX_GRAPH_HPP
#define ADJACENCY_MATRIX_GRAPH_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <vector>
#include <unordered_map>
#include <string>
#include "AdjacencyMatrixGraphNode.hpp"
#include "GraphEdge.hpp"
#include "GraphNode.hpp"

extern PyTypeObject AdjacencyMatrixGraphNodeType;

typedef struct {
    PyObject_HEAD
    PyObject* dict;
    std::vector<AdjacencyMatrixGraphNode *> nodes;
    std::unordered_map<std::string, std::unordered_map<std::string,bool> > matrix;
    std::unordered_map<std::string, AdjacencyMatrixGraphNode *> node_map;
    std::unordered_map<std::string, GraphEdge *> edge_weights;
} AdjacencyMatrixGraph;

static void AdjacencyMatrixGraph_dealloc(AdjacencyMatrixGraph* self)
{
    for (auto& pair : self->edge_weights) {
        Py_XDECREF(pair.second);
    }
    self->edge_weights.clear();

    for (AdjacencyMatrixGraphNode* node : self->nodes) {
        Py_XDECREF(node);
    }
    self->nodes.clear();

    self->node_map.clear();
    self->matrix.clear();

    Py_XDECREF(self->dict);

    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* AdjacencyMatrixGraph_new(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
    AdjacencyMatrixGraph* self;
    self = reinterpret_cast<AdjacencyMatrixGraph*>(type->tp_alloc(type, 0));
    if (self != NULL) {
        new (&self->nodes) std::vector<AdjacencyMatrixGraphNode*>();
        new (&self->node_map) std::unordered_map<std::string, AdjacencyMatrixGraphNode*>();
        new (&self->matrix) std::unordered_map<std::string, std::unordered_map<std::string, bool> >();
        new (&self->edge_weights) std::unordered_map<std::string, GraphEdge*>();

        PyObject* vertices;
        if (!PyArg_ParseTuple(args, "O", &vertices)) {
            Py_DECREF(self);
            return NULL;
        }

        if (!PyTuple_Check(vertices)) {
            PyErr_SetString(PyExc_TypeError, "Expected a tuple of vertices");
            Py_DECREF(self);
            return NULL;
        }

        Py_ssize_t len = PyTuple_Size(vertices);
        for (Py_ssize_t i = 0; i < len; ++i) {
            PyObject* item = PyTuple_GetItem(vertices, i);
            if (!PyObject_TypeCheck(item, &AdjacencyMatrixGraphNodeType)) {
                PyErr_SetString(PyExc_TypeError, "All elements must be AdjacencyMatrixGraphNode instances");
                Py_DECREF(self);
                return NULL;
            }
            Py_INCREF(item);
            AdjacencyMatrixGraphNode* node = reinterpret_cast<AdjacencyMatrixGraphNode*>(item);
            std::string name =(reinterpret_cast<GraphNode*>(node))->name;
            self->nodes.push_back(node);
            self->node_map[name] = node;
            self->matrix[name] = std::unordered_map<std::string, bool>();
        }

        PyObject* impl_str = PyUnicode_FromString("adjacency_matrix");

        if (PyObject_SetAttrString(reinterpret_cast<PyObject*>(self), "_impl", impl_str) < 0) {
        Py_DECREF(impl_str);
        PyErr_SetString(PyExc_RuntimeError, "Failed to set _impl attribute");
        return NULL;
        }

        Py_DECREF(impl_str);
    }
    return reinterpret_cast<PyObject*>(self);
}

static PyObject* AdjacencyMatrixGraph_add_edge(AdjacencyMatrixGraph* self, PyObject* args, PyObject* kwds)
{
    const char *source, *target;
    PyObject *cost_obj = Py_None;
    static char* kwlist[] = {"source", "target", "cost", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "ss|O", kwlist, &source, &target, &cost_obj))
        return NULL;

    std::string src(source);
    std::string dst(target);

    if (self->matrix.find(src) == self->matrix.end() ||
        self->matrix.find(dst) == self->matrix.end()) {
        PyErr_Format(PyExc_ValueError, "Vertex %s or %s not in graph", source, target);
        return NULL;
    }

    self->matrix[src][dst] = true;

    if (cost_obj != Py_None) {
    double cost = PyFloat_AsDouble(cost_obj);
    if (PyErr_Occurred()) return NULL;

    PyObject* cost_pyfloat = PyFloat_FromDouble(cost);
    if (!cost_pyfloat) return NULL;

    PyObject* args = Py_BuildValue("OOO", reinterpret_cast<PyObject*>(self->node_map[src]), reinterpret_cast<PyObject*>(self->node_map[dst]), cost_pyfloat);
    Py_DECREF(cost_pyfloat);
    if (!args) return NULL;

    PyObject* edge_obj = PyObject_CallObject(reinterpret_cast<PyObject*>(&GraphEdgeType), args);
    Py_DECREF(args);
    if (!edge_obj) return NULL;

    self->edge_weights[src + "_" + dst] = reinterpret_cast<GraphEdge*>(edge_obj);
    }

    Py_RETURN_NONE;
}

static PyObject* AdjacencyMatrixGraph_remove_edge(AdjacencyMatrixGraph* self, PyObject* args)
{
    const char *source, *target;
    if (!PyArg_ParseTuple(args, "ss", &source, &target))
        return NULL;

    std::string src(source);
    std::string dst(target);

    if (self->matrix.find(src) != self->matrix.end()) {
        self->matrix[src][dst] = false;
        self->edge_weights.erase(src + "_" + dst);
    }

    Py_RETURN_NONE;
}

static PyObject* AdjacencyMatrixGraph_neighbors(AdjacencyMatrixGraph* self, PyObject* args)
{
    const char *node;
    if (!PyArg_ParseTuple(args, "s", &node)) {
        return NULL;
    }

    std::string key(node);
    if (self->matrix.find(key) == self->matrix.end()) {
        PyErr_SetString(PyExc_KeyError, "Node not found");
        return NULL;
    }

    PyObject* list = PyList_New(0);
    for (const auto& pair : self->matrix[key]) {
        if (pair.second) {
            const std::string& neighbor_name = pair.first;
            AdjacencyMatrixGraphNode* neighbor = self->node_map[neighbor_name];
            Py_INCREF(neighbor);
            PyList_Append(list, (PyObject*)neighbor);
        }
    }
    return list;
}


static PyObject* AdjacencyMatrixGraph_num_vertices(AdjacencyMatrixGraph* self, PyObject* Py_UNUSED(ignored))
{
    return PyLong_FromSize_t(self->nodes.size());
}

static PyObject* AdjacencyMatrixGraph_num_edges(AdjacencyMatrixGraph* self, PyObject* Py_UNUSED(ignored))
{
    size_t count = 0;
    for (const auto& row : self->matrix) {
        for (const auto& entry : row.second) {
            if (entry.second)
                count++;
        }
    }
    return PyLong_FromSize_t(count);
}

static PyObject* AdjacencyMatrixGraph_get_edge(AdjacencyMatrixGraph* self, PyObject* args)
{
    const char *source, *target;
    if (!PyArg_ParseTuple(args, "ss", &source, &target))
        return NULL;

    std::string key = std::string(source) + "_" + std::string(target);
    auto it = self->edge_weights.find(key);
    if (it != self->edge_weights.end()) {
        return reinterpret_cast<PyObject*>(it->second);
    }
    Py_RETURN_NONE;
}

static PyObject* AdjacencyMatrixGraph_is_adjacent(AdjacencyMatrixGraph* self, PyObject* args)
{
    const char *source, *target;
    if (!PyArg_ParseTuple(args, "ss", &source, &target))
        return NULL;

    std::string src(source);
    std::string dst(target);
    if (self->matrix.find(src) == self->matrix.end())
        Py_RETURN_FALSE;

    auto& row = self->matrix[src];
    if (row.find(dst) != row.end() && row[dst])
        Py_RETURN_TRUE;

    Py_RETURN_FALSE;
}

static PyMethodDef AdjacencyMatrixGraph_methods[] = {
    {"add_edge", (PyCFunction)AdjacencyMatrixGraph_add_edge, METH_VARARGS | METH_KEYWORDS, "Add an edge between two nodes."},
    {"remove_edge", (PyCFunction)AdjacencyMatrixGraph_remove_edge, METH_VARARGS, "Remove an edge between two nodes."},
    {"neighbors", (PyCFunction)AdjacencyMatrixGraph_neighbors, METH_VARARGS, "Return neighbors of a node."},
    {"num_vertices", (PyCFunction)AdjacencyMatrixGraph_num_vertices, METH_NOARGS, "Return number of vertices."},
    {"num_edges", (PyCFunction)AdjacencyMatrixGraph_num_edges, METH_NOARGS, "Return number of edges."},
    {"get_edge", (PyCFunction)AdjacencyMatrixGraph_get_edge, METH_VARARGS, "Return the edge object between two nodes if exists."},
    {"is_adjacent", (PyCFunction)AdjacencyMatrixGraph_is_adjacent, METH_VARARGS, "Check if there is an edge between two nodes."},
    {NULL}
};

PyTypeObject AdjacencyMatrixGraphType = {
    PyVarObject_HEAD_INIT(NULL, 0)                  // ob_base
    "_graph.AdjacencyMatrixGraph",                  // tp_name
    sizeof(AdjacencyMatrixGraph),                   // tp_basicsize
    0,                                               // tp_itemsize
    (destructor)AdjacencyMatrixGraph_dealloc,       // tp_dealloc
    0,                                               // tp_vectorcall_offset or tp_print (removed in Python 3.9)
    0,                                               // tp_getattr
    0,                                               // tp_setattr
    0,                                               // tp_as_async / tp_reserved
    0,                                               // tp_repr
    0,                                               // tp_as_number
    0,                                               // tp_as_sequence
    0,                                               // tp_as_mapping
    0,                                               // tp_hash
    0,                                               // tp_call
    0,                                               // tp_str
    0,                                               // tp_getattro
    0,                                               // tp_setattro
    0,                                               // tp_as_buffer
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,        // tp_flags
    "Adjacency matrix graph",                        // tp_doc
    0,                                               // tp_traverse
    0,                                               // tp_clear
    0,                                               // tp_richcompare
    0,                                               // tp_weaklistoffset
    0,                                               // tp_iter
    0,                                               // tp_iternext
    AdjacencyMatrixGraph_methods,                   // tp_methods
    0,                                               // tp_members
    0,                                               // tp_getset
    0,                                               // tp_base
    0,                                               // tp_dict
    0,                                               // tp_descr_get
    0,                                               // tp_descr_set
    offsetof(AdjacencyMatrixGraph, dict),           // tp_dictoffset
    0,                                               // tp_init
    0,                                               // tp_alloc
    AdjacencyMatrixGraph_new                        // tp_new
};

#endif
