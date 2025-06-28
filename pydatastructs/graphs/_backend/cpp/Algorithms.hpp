#include <Python.h>
#include <unordered_map>
#include <queue>
#include <string>
#include <unordered_set>
#include "AdjacencyList.hpp"
#include "AdjacencyMatrix.hpp"


static PyObject* breadth_first_search_adjacency_list(PyObject* self, PyObject* args, PyObject* kwargs) {
    PyObject* graph_obj;
    const char* source_name;
    PyObject* operation;
    PyObject* varargs = nullptr;
    PyObject* kwargs_dict = nullptr;

    static const char* kwlist[] = {"graph", "source_node", "operation", "args", "kwargs", nullptr};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!sO|OO", const_cast<char**>(kwlist),
                                     &AdjacencyListGraphType, &graph_obj,
                                     &source_name, &operation,
                                     &varargs, &kwargs_dict)) {
        return nullptr;
    }

    AdjacencyListGraph* cpp_graph = reinterpret_cast<AdjacencyListGraph*>(graph_obj);

    auto it = cpp_graph->node_map.find(source_name);
    AdjacencyListGraphNode* start_node = it->second;

    std::unordered_set<std::string> visited;
    std::queue<AdjacencyListGraphNode*> q;

    q.push(start_node);
    visited.insert(start_node->name);

    while (!q.empty()) {
    AdjacencyListGraphNode* node = q.front();
    q.pop();

    for (const auto& [adj_name, adj_obj] : node->adjacent) {
        if (visited.count(adj_name)) continue;
        if (!PyObject_IsInstance(adj_obj, (PyObject*)&AdjacencyListGraphNodeType)) continue;

        AdjacencyListGraphNode* adj_node = reinterpret_cast<AdjacencyListGraphNode*>(adj_obj);

        PyObject* base_args = PyTuple_Pack(2,
                                           reinterpret_cast<PyObject*>(node),
                                           reinterpret_cast<PyObject*>(adj_node));
        if (!base_args)
            return nullptr;

        PyObject* final_args;
        if (varargs && PyTuple_Check(varargs)) {
            final_args = PySequence_Concat(base_args, varargs);
            Py_DECREF(base_args);
            if (!final_args)
                return nullptr;
        } else {
            final_args = base_args;
        }

        PyObject* result = PyObject_Call(operation, final_args, kwargs_dict);
        Py_DECREF(final_args);

        if (!result)
            return nullptr;

        Py_DECREF(result);

        visited.insert(adj_name);
        q.push(adj_node);
    }
    }
    if (PyErr_Occurred()) {
        return nullptr;
    }

    Py_RETURN_NONE;
}

static PyObject* breadth_first_search_adjacency_matrix(PyObject* self, PyObject* args, PyObject* kwargs) {
    PyObject* graph_obj;
    const char* source_name;
    PyObject* operation;
    PyObject* varargs = nullptr;
    PyObject* kwargs_dict = nullptr;

    static const char* kwlist[] = {"graph", "source_node", "operation", "args", "kwargs", nullptr};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!sO|OO", const_cast<char**>(kwlist),
                                     &AdjacencyMatrixGraphType, &graph_obj,
                                     &source_name, &operation,
                                     &varargs, &kwargs_dict)) {
        return nullptr;
    }

    AdjacencyMatrixGraph* cpp_graph = reinterpret_cast<AdjacencyMatrixGraph*>(graph_obj);

    auto it = cpp_graph->node_map.find(source_name);
    if (it == cpp_graph->node_map.end()) {
        PyErr_SetString(PyExc_KeyError, "Source node not found in graph");
        return nullptr;
    }
    AdjacencyMatrixGraphNode* start_node = it->second;

    std::unordered_set<std::string> visited;
    std::queue<AdjacencyMatrixGraphNode*> q;

    q.push(start_node);
    visited.insert(source_name);

    while (!q.empty()) {
        AdjacencyMatrixGraphNode* node = q.front();
        q.pop();

        std::string node_name = reinterpret_cast<GraphNode*>(node)->name;
        auto& neighbors = cpp_graph->matrix[node_name];

        for (const auto& [adj_name, connected] : neighbors) {
            if (!connected || visited.count(adj_name)) continue;

            auto adj_it = cpp_graph->node_map.find(adj_name);
            if (adj_it == cpp_graph->node_map.end()) continue;

            AdjacencyMatrixGraphNode* adj_node = adj_it->second;

            PyObject* base_args = PyTuple_Pack(2,
                                               reinterpret_cast<PyObject*>(node),
                                               reinterpret_cast<PyObject*>(adj_node));
            if (!base_args) return nullptr;

            PyObject* final_args;
            if (varargs && PyTuple_Check(varargs)) {
                final_args = PySequence_Concat(base_args, varargs);
                Py_DECREF(base_args);
                if (!final_args) return nullptr;
            } else {
                final_args = base_args;
            }

            PyObject* result = PyObject_Call(operation, final_args, kwargs_dict);
            Py_DECREF(final_args);
            if (!result) return nullptr;
            Py_DECREF(result);

            visited.insert(adj_name);
            q.push(adj_node);
        }
    }

    if (PyErr_Occurred()) {
        return nullptr;
    }

    Py_RETURN_NONE;
}
