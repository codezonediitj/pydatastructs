#ifndef ADJACENCY_LIST_GRAPH_HPP
#define ADJACENCY_LIST_GRAPH_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <vector>
#include <unordered_map>
#include <string>
#include <algorithm>
#include "AdjacencyListGraphNode.hpp"
#include "GraphEdge.hpp"
#include "../../../utils/_backend/cpp/utils.hpp"

extern PyTypeObject AdjacencyListGraphType;

typedef struct {

    PyObject_HEAD
    PyObject* dict;
    std::vector<AdjacencyListGraphNode *> nodes;
    std::unordered_map<std::string, GraphEdge*> edges;
    std::unordered_map<std::string, AdjacencyListGraphNode*> node_map;
    std::unordered_map<int, AdjacencyListGraphNode*> id_map;
    std::unordered_map<int, std::string> id_to_name;
    std::unordered_map<std::string, int> name_to_id;
    int next_id;

} AdjacencyListGraph;

static void AdjacencyListGraph_dealloc(AdjacencyListGraph* self) {
    for (AdjacencyListGraphNode* node : self->nodes) {
        Py_XDECREF(node);
    }
    self->nodes.clear();

    for (auto& pair : self->edges) {
        Py_XDECREF(pair.second);
    }
    self->edges.clear();

    self->node_map.clear();
    self->id_map.clear();
    self->id_to_name.clear();
    self->name_to_id.clear();

    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* AdjacencyListGraph_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    AdjacencyListGraph* self = reinterpret_cast<AdjacencyListGraph*>(type->tp_alloc(type, 0));
    if (!self)
        return NULL;

    new (&self->nodes) std::vector<AdjacencyListGraphNode*>();
    new (&self->edges) std::unordered_map<std::string, GraphEdge*>();
    new (&self->node_map) std::unordered_map<std::string, AdjacencyListGraphNode*>();
    new (&self->id_map) std::unordered_map<int, AdjacencyListGraphNode*>();
    new (&self->id_to_name) std::unordered_map<int, std::string>();
    new (&self->name_to_id) std::unordered_map<std::string, int>();

    self->next_id = 0;

    Py_ssize_t num_args = PyTuple_Size(args);
    for (Py_ssize_t i = 0; i < num_args; ++i) {
        PyObject* node_obj = PyTuple_GetItem(args, i);
        AdjacencyListGraphNode* node = reinterpret_cast<AdjacencyListGraphNode*>(node_obj);
        if (get_type_tag(node_obj) != NodeType_::AdjacencyListGraphNode) {
            PyErr_SetString(PyExc_TypeError, "All arguments must be AdjacencyListGraphNode instances");
            return NULL;
        }

        if (self->node_map.find(node->name) != self->node_map.end()) {
            PyErr_Format(PyExc_ValueError, "Duplicate node with name '%s'", node->name.c_str());
            return NULL;
        }

        node->internal_id = self->next_id++;

        Py_INCREF(node);
        self->nodes.push_back(node);
        self->node_map[node->name] = node;
        self->id_map[node->internal_id] = node;
        self->id_to_name[node->internal_id] = node->name;
        self->name_to_id[node->name] = node->internal_id;
    }

    PyObject* impl_str = PyUnicode_FromString("adjacency_list");
    if (PyObject_SetAttrString(reinterpret_cast<PyObject*>(self), "_impl", impl_str) < 0) {
        Py_DECREF(impl_str);
        PyErr_SetString(PyExc_RuntimeError, "Failed to set _impl attribute");
        return NULL;
    }

    Py_DECREF(impl_str);
    return reinterpret_cast<PyObject*>(self);
}

static std::string make_edge_key(const std::string& source, const std::string& target) {
    return source + "_" + target;
}

static PyObject* AdjacencyListGraph_add_vertex(AdjacencyListGraph* self, PyObject* args) {
    PyObject* node_obj;

    if (!PyArg_ParseTuple(args, "O", &node_obj)) {
        PyErr_SetString(PyExc_ValueError, "Expected a single AdjacencyListGraphNode object");
        return NULL;
    }

    if (get_type_tag(node_obj) != NodeType_::AdjacencyListGraphNode) {
        PyErr_SetString(PyExc_TypeError, "Object is not an AdjacencyListGraphNode");
        return NULL;
    }

    AdjacencyListGraphNode* node = reinterpret_cast<AdjacencyListGraphNode*>(node_obj);

    if (self->node_map.find(node->name) != self->node_map.end()) {
        PyErr_SetString(PyExc_ValueError, "Node with this name already exists");
        return NULL;
    }

    node->internal_id = self->next_id++;

    Py_INCREF(node);
    self->nodes.push_back(node);
    self->node_map[node->name] = node;
    self->id_map[node->internal_id] = node;
    self->id_to_name[node->internal_id] = node->name;
    self->name_to_id[node->name] = node->internal_id;

    Py_RETURN_NONE;
}


static PyObject* AdjacencyListGraph_is_adjacent(AdjacencyListGraph* self, PyObject* args) {
    const char* node1_name_c;
    const char* node2_name_c;
    if (!PyArg_ParseTuple(args, "ss", &node1_name_c, &node2_name_c))
        return NULL;

    auto it1 = self->name_to_id.find(node1_name_c);
    if (it1 == self->name_to_id.end()) {
        PyErr_SetString(PyExc_KeyError, "node1 not found");
        return NULL;
    }
    int id1 = it1->second;
    AdjacencyListGraphNode* node1 = self->id_map[id1];

    if (node1->adjacent.find(node2_name_c) != node1->adjacent.end()) {
        Py_RETURN_TRUE;
    } else {
        Py_RETURN_FALSE;
    }
}

static PyObject* AdjacencyListGraph_num_vertices(AdjacencyListGraph* self, PyObject* Py_UNUSED(ignored)) {
    return PyLong_FromSize_t(self->nodes.size());
}

static PyObject* AdjacencyListGraph_num_edges(AdjacencyListGraph* self, PyObject* Py_UNUSED(ignored)) {
    return PyLong_FromSize_t(self->edges.size());
}

static PyObject* AdjacencyListGraph_neighbors(AdjacencyListGraph* self, PyObject* args) {
    const char* node_name_c;
    if (!PyArg_ParseTuple(args, "s", &node_name_c))
        return NULL;

    auto it = self->name_to_id.find(node_name_c);
    if (it == self->name_to_id.end()) {
        PyErr_SetString(PyExc_KeyError, "Node not found");
        return NULL;
    }
    int id = it->second;
    AdjacencyListGraphNode* node = self->id_map[id];

    PyObject* neighbors_list = PyList_New(0);
    if (!neighbors_list) return NULL;

    for (const auto& adj_pair : node->adjacent) {
        Py_INCREF(adj_pair.second);
        PyList_Append(neighbors_list, (PyObject*)adj_pair.second);
    }

    return neighbors_list;
}

static PyObject* AdjacencyListGraph_remove_vertex(AdjacencyListGraph* self, PyObject* args) {
    const char* name_c;
    if (!PyArg_ParseTuple(args, "s", &name_c))
        return NULL;

    auto it = self->name_to_id.find(name_c);
    if (it == self->name_to_id.end()) {
        PyErr_SetString(PyExc_KeyError, "Node not found");
        return NULL;
    }

    int id = it->second;
    AdjacencyListGraphNode* node_to_remove = self->id_map[id];
    std::string name = node_to_remove->name;

    auto& nodes_vec = self->nodes;
    nodes_vec.erase(std::remove(nodes_vec.begin(), nodes_vec.end(), node_to_remove), nodes_vec.end());

    self->node_map.erase(name);
    self->id_map.erase(id);
    self->name_to_id.erase(name);
    self->id_to_name.erase(id);

    Py_XDECREF(node_to_remove);

    for (auto& node_pair : self->id_map) {
        AdjacencyListGraphNode* node = node_pair.second;
        auto adj_it = node->adjacent.find(name);
        if (adj_it != node->adjacent.end()) {
            Py_XDECREF(adj_it->second);
            node->adjacent.erase(adj_it);
        }
    }

    for (auto it = self->edges.begin(); it != self->edges.end(); ) {
        const std::string& key = it->first;
        size_t underscore = key.find('_');
        std::string src = key.substr(0, underscore);
        std::string dst = key.substr(underscore + 1);

        if (src == name || dst == name) {
            Py_XDECREF(it->second);
            it = self->edges.erase(it);
        } else {
            ++it;
        }
    }

    Py_RETURN_NONE;
}


static PyObject* AdjacencyListGraph_get_edge(AdjacencyListGraph* self, PyObject* args) {
    const char* source_c;
    const char* target_c;
    if (!PyArg_ParseTuple(args, "ss", &source_c, &target_c))
        return NULL;

    std::string key = make_edge_key(source_c, target_c);
    auto it = self->edges.find(key);
    if (it != self->edges.end()) {
        Py_INCREF(it->second);
        return reinterpret_cast<PyObject*>(it->second);
    }

    Py_RETURN_NONE;
}

static PyObject* AdjacencyListGraph_remove_edge(AdjacencyListGraph* self, PyObject* args) {
    const char* source_c;
    const char* target_c;
    if (!PyArg_ParseTuple(args, "ss", &source_c, &target_c))
        return NULL;

    std::string source(source_c);
    std::string target(target_c);

    auto it_source = self->node_map.find(source);
    auto it_target = self->node_map.find(target);
    if (it_source == self->node_map.end() || it_target == self->node_map.end()) {
        PyErr_SetString(PyExc_KeyError, "Source or target node not found");
        return NULL;
    }

    AdjacencyListGraphNode* source_node = it_source->second;

    auto adj_it = source_node->adjacent.find(target);
    if (adj_it != source_node->adjacent.end()) {
        Py_XDECREF(adj_it->second);
        source_node->adjacent.erase(adj_it);
    }

    std::string key = make_edge_key(source, target);
    auto edge_it = self->edges.find(key);
    if (edge_it != self->edges.end()) {
        Py_XDECREF(edge_it->second);
        self->edges.erase(edge_it);
    }

    Py_RETURN_NONE;
}

static PyObject* AdjacencyListGraph_add_edge(AdjacencyListGraph* self, PyObject* args) {
    const char* source_cstr;
    const char* target_cstr;
    PyObject* value = Py_None;

    if (!PyArg_ParseTuple(args, "ss|O", &source_cstr, &target_cstr, &value)) {
        PyErr_SetString(PyExc_ValueError, "Expected source (str), target (str), and optional weight");
        return NULL;
    }

    std::string source(source_cstr);
    std::string target(target_cstr);

    if (self->node_map.find(source) == self->node_map.end()) {
        PyErr_SetString(PyExc_ValueError, "Source node does not exist");
        return NULL;
    }
    if (self->node_map.find(target) == self->node_map.end()) {
        PyErr_SetString(PyExc_ValueError, "Target node does not exist");
        return NULL;
    }

    AdjacencyListGraphNode* source_node = self->node_map[source];
    AdjacencyListGraphNode* target_node = self->node_map[target];

    PyObject* edge_args = PyTuple_Pack(3, reinterpret_cast<PyObject*>(source_node), reinterpret_cast<PyObject*>(target_node), value);
    if (!edge_args) return NULL;

    PyObject* edge_obj = PyObject_CallObject(reinterpret_cast<PyObject*>(&GraphEdgeType), edge_args);
    Py_DECREF(edge_args);

    if (!edge_obj)
        return NULL;

    std::string key = make_edge_key(source, target);

    auto it = self->edges.find(key);
    if (it != self->edges.end()) {
        Py_XDECREF(it->second);
        it->second = reinterpret_cast<GraphEdge*>(edge_obj);
    } else {
        self->edges[key] = reinterpret_cast<GraphEdge*>(edge_obj);
    }

    auto adj_it = source_node->adjacent.find(target);
    if (adj_it == source_node->adjacent.end()) {
        Py_INCREF(target_node);
        source_node->adjacent[target] = reinterpret_cast<PyObject*>(target_node);
    }

    Py_RETURN_NONE;
}




static PyMethodDef AdjacencyListGraph_methods[] = {
    {"add_vertex", (PyCFunction)AdjacencyListGraph_add_vertex, METH_VARARGS, "Add a vertex to the graph"},
    {"add_edge", (PyCFunction)AdjacencyListGraph_add_edge, METH_VARARGS, "Add an edge to the graph"},
    {"is_adjacent", (PyCFunction)AdjacencyListGraph_is_adjacent, METH_VARARGS, "Check adjacency between two nodes"},
    {"num_vertices", (PyCFunction)AdjacencyListGraph_num_vertices, METH_NOARGS, "Number of vertices"},
    {"num_edges", (PyCFunction)AdjacencyListGraph_num_edges, METH_NOARGS, "Number of edges"},
    {"neighbors", (PyCFunction)AdjacencyListGraph_neighbors, METH_VARARGS, "Get neighbors of a node"},
    {"remove_vertex", (PyCFunction)AdjacencyListGraph_remove_vertex, METH_VARARGS, "Remove a vertex"},
    {"get_edge", (PyCFunction)AdjacencyListGraph_get_edge, METH_VARARGS, "Get edge between source and target"},
    {"remove_edge", (PyCFunction)AdjacencyListGraph_remove_edge, METH_VARARGS, "Remove edge between source and target"},
    {NULL}
};


inline PyTypeObject AdjacencyListGraphType = {
    PyVarObject_HEAD_INIT(NULL, 0)                 // ob_base
    "_graph.AdjacencyListGraph",                   // tp_name
    sizeof(AdjacencyListGraph),                    // tp_basicsize
    0,                                              // tp_itemsize
    (destructor)AdjacencyListGraph_dealloc,        // tp_dealloc
    0,                                              // tp_vectorcall_offset or tp_print (depends on Python version)
    0,                                              // tp_getattr
    0,                                              // tp_setattr
    0,                                              // tp_as_async / tp_reserved
    0,                                              // tp_repr
    0,                                              // tp_as_number
    0,                                              // tp_as_sequence
    0,                                              // tp_as_mapping
    0,                                              // tp_hash
    0,                                              // tp_call
    0,                                              // tp_str
    0,                                              // tp_getattro
    0,                                              // tp_setattro
    0,                                              // tp_as_buffer
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,       // tp_flags
    "Adjacency List Graph",         // tp_doc
    0,                                              // tp_traverse
    0,                                              // tp_clear
    0,                                              // tp_richcompare
    0,                                              // tp_weaklistoffset
    0,                                              // tp_iter
    0,                                              // tp_iternext
    AdjacencyListGraph_methods,                    // tp_methods
    0,                                              // tp_members
    0,                                              // tp_getset
    0,                                              // tp_base
    0,                                              // tp_dict
    0,                                              // tp_descr_get
    0,                                              // tp_descr_set
    offsetof(AdjacencyListGraph, dict),            // tp_dictoffset
    0,                                              // tp_init
    0,                                              // tp_alloc
    AdjacencyListGraph_new                         // tp_new
};

#endif
