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
        int source_id;
        int target_id;
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
    std::unordered_set<int> visited;

    PyObject* mst_graph = PyObject_CallObject(reinterpret_cast<PyObject*>(&AdjacencyListGraphType), nullptr);
    AdjacencyListGraph* mst = reinterpret_cast<AdjacencyListGraph*>(mst_graph);

    int start_id = graph->nodes[0]->internal_id;
    visited.insert(start_id);

    AdjacencyListGraphNode* start_node = graph->id_map[start_id];
    std::string start_name = graph->id_to_name[start_id];

    Py_INCREF(start_node);
    mst->nodes.push_back(start_node);
    mst->node_map[start_name] = start_node;
    mst->id_map[start_id] = start_node;
    mst->id_to_name[start_id] = start_name;
    mst->name_to_id[start_name] = start_id;

    for (const auto& [adj_name, _] : start_node->adjacent) {
        int adj_id = graph->name_to_id[adj_name];
        std::string key = make_edge_key(start_name, adj_name);
        GraphEdge* edge = graph->edges[key];

        EdgeTuple et;
        et.source_id = start_id;
        et.target_id = adj_id;
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

        if (visited.count(edge.target_id)) continue;
        visited.insert(edge.target_id);

        int u_id = edge.source_id;
        int v_id = edge.target_id;
        std::string u_name = graph->id_to_name[u_id];
        std::string v_name = graph->id_to_name[v_id];

        for (auto [id, name] : std::vector<std::pair<int, std::string>>{{u_id, u_name}, {v_id, v_name}}) {
            if (!mst->id_map.count(id)) {
                AdjacencyListGraphNode* node = graph->id_map[id];
                Py_INCREF(node);
                mst->nodes.push_back(node);
                mst->node_map[name] = node;
                mst->id_map[id] = node;
                mst->id_to_name[id] = name;
                mst->name_to_id[name] = id;
            }
        }

        AdjacencyListGraphNode* u = mst->id_map[u_id];
        AdjacencyListGraphNode* v = mst->id_map[v_id];

        Py_INCREF(v);
        Py_INCREF(u);
        u->adjacent[v_name] = reinterpret_cast<PyObject*>(v);
        v->adjacent[u_name] = reinterpret_cast<PyObject*>(u);

        std::string key_uv = make_edge_key(u_name, v_name);
        GraphEdge* new_edge = PyObject_New(GraphEdge, &GraphEdgeType);
        PyObject_Init(reinterpret_cast<PyObject*>(new_edge), &GraphEdgeType);
        new (&new_edge->value) std::variant<std::monostate, int64_t, double, std::string>(edge.value);
        new_edge->value_type = edge.value_type;
        Py_INCREF(u);
        Py_INCREF(v);
        new_edge->source = reinterpret_cast<PyObject*>(u);
        new_edge->target = reinterpret_cast<PyObject*>(v);
        mst->edges[key_uv] = new_edge;

        std::string key_vu = make_edge_key(v_name, u_name);
        GraphEdge* new_edge_rev = PyObject_New(GraphEdge, &GraphEdgeType);
        PyObject_Init(reinterpret_cast<PyObject*>(new_edge_rev), &GraphEdgeType);
        new (&new_edge_rev->value) std::variant<std::monostate, int64_t, double, std::string>(edge.value);
        new_edge_rev->value_type = edge.value_type;
        Py_INCREF(u);
        Py_INCREF(v);
        new_edge_rev->source = reinterpret_cast<PyObject*>(v);
        new_edge_rev->target = reinterpret_cast<PyObject*>(u);
        mst->edges[key_vu] = new_edge_rev;

        AdjacencyListGraphNode* next_node = graph->id_map[v_id];
        for (const auto& [adj_name, _] : next_node->adjacent) {
            int adj_id = graph->name_to_id[adj_name];
            if (visited.count(adj_id)) continue;

            std::string key = make_edge_key(v_name, adj_name);
            GraphEdge* adj_edge = graph->edges[key];

            EdgeTuple adj_et;
            adj_et.source_id = v_id;
            adj_et.target_id = adj_id;
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


static PyObject* shortest_paths_dijkstra_adjacency_list(PyObject* self, PyObject* args, PyObject* kwargs) {
    PyObject* graph_obj;
    const char* source_name;
    const char* target_name = "";

    static const char* kwlist[] = {"graph", "source_node", "target_node", nullptr};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!s|s", const_cast<char**>(kwlist),
                                     &AdjacencyListGraphType, &graph_obj,
                                     &source_name, &target_name)) {
        return nullptr;
    }

    AdjacencyListGraph* graph = reinterpret_cast<AdjacencyListGraph*>(graph_obj);
    const size_t V = graph->node_map.size();

    std::vector<std::vector<std::pair<int, double>>> adj(V);
    for (const auto& [edge_key, edge] : graph->edges) {
        size_t delim = edge_key.find('_');
        std::string u_name = edge_key.substr(0, delim);
        std::string v_name = edge_key.substr(delim + 1);
        int u = graph->name_to_id[u_name];
        int v = graph->name_to_id[v_name];

        double weight = 0.0;
        if (edge->value_type == DataType::Int)
            weight = static_cast<double>(std::get<int64_t>(edge->value));
        else if (edge->value_type == DataType::Double)
            weight = std::get<double>(edge->value);
        else
            continue;

        if (weight < 0) continue;
        adj[u].emplace_back(v, weight);
    }

    std::vector<double> dist(V, std::numeric_limits<double>::infinity());
    std::vector<int> pred(V, -1);
    using PQEntry = std::pair<double, int>;
    std::priority_queue<PQEntry, std::vector<PQEntry>, std::greater<>> pq;

    int source_id = graph->name_to_id[source_name];
    dist[source_id] = 0.0;
    pq.push({0.0, source_id});

    while (!pq.empty()) {
        auto [u_dist, u_id] = pq.top(); pq.pop();
        if (u_dist > dist[u_id]) continue;

        for (const auto& [v_id, weight] : adj[u_id]) {
            double new_dist = dist[u_id] + weight;
            if (new_dist < dist[v_id]) {
                dist[v_id] = new_dist;
                pred[v_id] = u_id;
                pq.push({new_dist, v_id});
            }
        }
    }

    PyObject* dist_dict = PyDict_New();
    PyObject* pred_dict = PyDict_New();
    if (!dist_dict || !pred_dict) return nullptr;

    for (int id = 0; id < static_cast<int>(V); ++id) {
        const std::string& name = graph->id_to_name[id];
        PyObject* dval = PyFloat_FromDouble(dist[id]);
        if (!dval || PyDict_SetItemString(dist_dict, name.c_str(), dval) < 0) {
            Py_XDECREF(dval);
            Py_DECREF(dist_dict);
            Py_DECREF(pred_dict);
            return nullptr;
        }
        Py_DECREF(dval);
    }

    for (int id = 0; id < static_cast<int>(V); ++id) {
        const std::string& name = graph->id_to_name[id];
        PyObject* py_pred;
        if (pred[id] == -1) {
            Py_INCREF(Py_None);
            py_pred = Py_None;
        } else {
            py_pred = PyUnicode_FromString(graph->id_to_name[pred[id]].c_str());
            if (!py_pred) {
                Py_DECREF(dist_dict);
                Py_DECREF(pred_dict);
                return nullptr;
            }
        }

        if (PyDict_SetItemString(pred_dict, name.c_str(), py_pred) < 0) {
            Py_DECREF(py_pred);
            Py_DECREF(dist_dict);
            Py_DECREF(pred_dict);
            return nullptr;
        }
        Py_DECREF(py_pred);
    }

    if (strlen(target_name) > 0) {
        int target_id = graph->name_to_id[target_name];
        PyObject* out = PyTuple_New(2);
        if (!out) {
            Py_DECREF(dist_dict);
            Py_DECREF(pred_dict);
            return nullptr;
        }

        PyObject* dist_val = PyFloat_FromDouble(dist[target_id]);
        if (!dist_val) {
            Py_DECREF(out);
            Py_DECREF(dist_dict);
            Py_DECREF(pred_dict);
            return nullptr;
        }

        PyTuple_SetItem(out, 0, dist_val);
        PyTuple_SetItem(out, 1, pred_dict);
        Py_DECREF(dist_dict);
        return out;
    }

    PyObject* result = PyTuple_New(2);
    if (!result) {
        Py_DECREF(dist_dict);
        Py_DECREF(pred_dict);
        return nullptr;
    }

    PyTuple_SetItem(result, 0, dist_dict);
    PyTuple_SetItem(result, 1, pred_dict);
    return result;
}
