#include <Python.h>
#include <unordered_map>
#include <queue>
#include <string>
#include <unordered_set>
#include <variant>
#include "GraphEdge.hpp"
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

static PyObject* minimum_spanning_tree_prim_adjacency_list(PyObject* self, PyObject* args, PyObject* kwargs) {

    PyObject* graph_obj;
    static const char* kwlist[] = {"graph", nullptr};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!", const_cast<char**>(kwlist),
                                     &AdjacencyListGraphType, &graph_obj)) {
        return nullptr;
    }

    AdjacencyListGraph* graph = reinterpret_cast<AdjacencyListGraph*>(graph_obj);

    struct EdgeTuple {
        std::string source;
        std::string target;
        std::variant<std::monostate, int64_t, double, std::string> value;
        DataType value_type;

        bool operator>(const EdgeTuple& other) const {
            if (value_type != other.value_type)
                return value_type > other.value_type;
            if (std::holds_alternative<int64_t>(value))
                return std::get<int64_t>(value) > std::get<int64_t>(other.value);
            if (std::holds_alternative<double>(value))
                return std::get<double>(value) > std::get<double>(other.value);
            if (std::holds_alternative<std::string>(value))
                return std::get<std::string>(value) > std::get<std::string>(other.value);
            return false;
        }
    };

    std::priority_queue<EdgeTuple, std::vector<EdgeTuple>, std::greater<>> pq;
    std::unordered_set<std::string> visited;

    PyObject* mst_graph = PyObject_CallObject(reinterpret_cast<PyObject*>(&AdjacencyListGraphType), nullptr);
    AdjacencyListGraph* mst = reinterpret_cast<AdjacencyListGraph*>(mst_graph);

    std::string start = graph->node_map.begin()->first;
    visited.insert(start);

    AdjacencyListGraphNode* start_node = graph->node_map[start];

    Py_INCREF(start_node);
    mst->nodes.push_back(start_node);
    mst->node_map[start] = start_node;

    for (const auto& [adj_name, _] : start_node->adjacent) {
        std::string key = make_edge_key(start, adj_name);
        GraphEdge* edge = graph->edges[key];
        EdgeTuple et;
        et.source = start;
        et.target = adj_name;
        et.value_type = edge->value_type;

        switch (edge->value_type) {
            case DataType::Int:
                et.value = std::get<int64_t>(edge->value);
                break;
            case DataType::Double:
                et.value = std::get<double>(edge->value);
                break;
            case DataType::String:
                et.value = std::get<std::string>(edge->value);
                break;
            default:
                et.value = std::monostate{};
        }

        pq.push(et);
    }

    while (!pq.empty()) {
        EdgeTuple edge = pq.top();
        pq.pop();

        if (visited.count(edge.target)) continue;
        visited.insert(edge.target);

        for (const std::string& name : {edge.source, edge.target}) {
            if (!mst->node_map.count(name)) {
                AdjacencyListGraphNode* node = graph->node_map[name];
                Py_INCREF(node);
                mst->nodes.push_back(node);
                mst->node_map[name] = node;
            }
        }

        AdjacencyListGraphNode* u = mst->node_map[edge.source];
        AdjacencyListGraphNode* v = mst->node_map[edge.target];

        Py_INCREF(v);
        Py_INCREF(u);
        u->adjacent[edge.target] = reinterpret_cast<PyObject*>(v);
        v->adjacent[edge.source] = reinterpret_cast<PyObject*>(u);

        std::string key_uv = make_edge_key(edge.source, edge.target);
        GraphEdge* new_edge = PyObject_New(GraphEdge, &GraphEdgeType);
        PyObject_Init(reinterpret_cast<PyObject*>(new_edge), &GraphEdgeType);
        new (&new_edge->value) std::variant<std::monostate, int64_t, double, std::string>(edge.value);
        new_edge->value_type = edge.value_type;
        Py_INCREF(u);
        Py_INCREF(v);
        new_edge->source = reinterpret_cast<PyObject*>(u);
        new_edge->target = reinterpret_cast<PyObject*>(v);
        mst->edges[key_uv] = new_edge;

        std::string key_vu = make_edge_key(edge.target, edge.source);
        GraphEdge* new_edge_rev = PyObject_New(GraphEdge, &GraphEdgeType);
        PyObject_Init(reinterpret_cast<PyObject*>(new_edge_rev), &GraphEdgeType);
        new (&new_edge_rev->value) std::variant<std::monostate, int64_t, double, std::string>(edge.value);
        new_edge_rev->value_type = edge.value_type;
        Py_INCREF(u);
        Py_INCREF(v);
        new_edge_rev->source = reinterpret_cast<PyObject *>(v);
        new_edge_rev->target = reinterpret_cast<PyObject*>(u);
        mst->edges[key_vu] = new_edge_rev;

        AdjacencyListGraphNode* next_node = graph->node_map[edge.target];

        for (const auto& [adj_name, _] : next_node->adjacent) {
            if (visited.count(adj_name)) continue;
            std::string key = make_edge_key(edge.target, adj_name);
            GraphEdge* adj_edge = graph->edges[key];
            EdgeTuple adj_et;
            adj_et.source = edge.target;
            adj_et.target = adj_name;
            adj_et.value_type = adj_edge->value_type;

            switch (adj_edge->value_type) {
                case DataType::Int:
                    adj_et.value = std::get<int64_t>(adj_edge->value);
                    break;
                case DataType::Double:
                    adj_et.value = std::get<double>(adj_edge->value);
                    break;
                case DataType::String:
                    adj_et.value = std::get<std::string>(adj_edge->value);
                    break;
                default:
                    adj_et.value = std::monostate{};
            }

            pq.push(adj_et);
        }
    }
    return reinterpret_cast<PyObject*>(mst);
}
