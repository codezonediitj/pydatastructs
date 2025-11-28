#include <Python.h>
#include <unordered_map>
#include <queue>
#include <string>
#include <unordered_set>
#include <variant>
#include <deque>
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
            if (get_type_tag(adj_obj) != NodeType_::AdjacencyListGraphNode) continue;

            AdjacencyListGraphNode* adj_node = reinterpret_cast<AdjacencyListGraphNode*>(adj_obj);

            PyObject* node_pyobj = reinterpret_cast<PyObject*>(node);
            PyObject* adj_node_pyobj = reinterpret_cast<PyObject*>(adj_node);

            PyObject* final_args;

            if (varargs && PyTuple_Check(varargs)) {
                Py_ssize_t varargs_size = PyTuple_Size(varargs);
                if (varargs_size == 1) {
                    PyObject* extra_arg = PyTuple_GetItem(varargs, 0);
                    final_args = PyTuple_Pack(3, node_pyobj, adj_node_pyobj, extra_arg);
                } else {
                    PyObject* base_args = PyTuple_Pack(2, node_pyobj, adj_node_pyobj);
                    if (!base_args)
                        return nullptr;
                    final_args = PySequence_Concat(base_args, varargs);
                    Py_DECREF(base_args);
                }
            } else {
                final_args = PyTuple_Pack(2, node_pyobj, adj_node_pyobj);
            }
            if (!final_args)
                return nullptr;

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

static void _visit_kosaraju(AdjacencyListGraph* graph, const std::string& u, 
                            std::unordered_map<std::string, bool>& visited,
                            std::unordered_map<std::string, std::vector<std::string>>& incoming,
                            std::vector<std::string>& L) {
    visited[u] = true;
    AdjacencyListGraphNode* node = graph->node_map[u];
    for (const auto& [v_name, _] : node->adjacent) {
        incoming[v_name].push_back(u);
        if (!visited[v_name]) {
            _visit_kosaraju(graph, v_name, visited, incoming, L);
        }
    }
    L.push_back(u);
}

static void _assign_kosaraju(AdjacencyListGraph* graph, const std::string& u,
                             std::unordered_map<std::string, std::vector<std::string>>& incoming,
                             std::unordered_map<std::string, bool>& assigned,
                             std::unordered_set<std::string>& comp) {
    assigned[u] = true;
    comp.insert(u);
    if (incoming.count(u)) {
        for (const auto& v : incoming[u]) {
            if (!assigned[v]) {
                _assign_kosaraju(graph, v, incoming, assigned, comp);
            }
        }
    }
}

static PyObject* strongly_connected_components_kosaraju_adjacency_list(PyObject* self, PyObject* args, PyObject* kwargs) {
    PyObject* graph_obj;
    static const char* kwlist[] = {"graph", nullptr};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!", const_cast<char**>(kwlist),
                                     &AdjacencyListGraphType, &graph_obj)) {
        return nullptr;
    }

    AdjacencyListGraph* graph = reinterpret_cast<AdjacencyListGraph*>(graph_obj);
    
    std::unordered_map<std::string, bool> visited;
    std::unordered_map<std::string, std::vector<std::string>> incoming;
    std::vector<std::string> L;

    for (const auto& [name, _] : graph->node_map) {
        visited[name] = false;
    }

    for (const auto& [name, _] : graph->node_map) {
        if (!visited[name]) {
            _visit_kosaraju(graph, name, visited, incoming, L);
        }
    }

    std::unordered_map<std::string, bool> assigned;
    for (const auto& [name, _] : graph->node_map) {
        assigned[name] = false;
    }

    PyObject* components = PyList_New(0);
    if (!components) return nullptr;

    for (int i = L.size() - 1; i >= 0; i--) {
        std::unordered_set<std::string> comp;
        if (!assigned[L[i]]) {
            _assign_kosaraju(graph, L[i], incoming, assigned, comp);
            if (!comp.empty()) {
                PyObject* py_comp = PySet_New(nullptr);
                if (!py_comp) {
                    Py_DECREF(components);
                    return nullptr;
                }
                for (const auto& node_name : comp) {
                    PyObject* py_name = PyUnicode_FromString(node_name.c_str());
                    if (!py_name || PySet_Add(py_comp, py_name) < 0) {
                        Py_XDECREF(py_name);
                        Py_DECREF(py_comp);
                        Py_DECREF(components);
                        return nullptr;
                    }
                    Py_DECREF(py_name);
                }
                if (PyList_Append(components, py_comp) < 0) {
                    Py_DECREF(py_comp);
                    Py_DECREF(components);
                    return nullptr;
                }
                Py_DECREF(py_comp);
            }
        }
    }

    return components;
}

static PyObject* strongly_connected_components_kosaraju_adjacency_matrix(PyObject* self, PyObject* args, PyObject* kwargs) {
    PyObject* graph_obj;
    static const char* kwlist[] = {"graph", nullptr};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!", const_cast<char**>(kwlist),
                                     &AdjacencyMatrixGraphType, &graph_obj)) {
        return nullptr;
    }

    AdjacencyMatrixGraph* graph = reinterpret_cast<AdjacencyMatrixGraph*>(graph_obj);
    
    std::unordered_map<std::string, bool> visited;
    std::unordered_map<std::string, std::vector<std::string>> incoming;
    std::vector<std::string> L;

    for (const auto& [name, _] : graph->node_map) {
        visited[name] = false;
    }

    std::function<void(const std::string&)> visit = [&](const std::string& u) {
        visited[u] = true;
        if (graph->matrix.count(u)) {
            for (const auto& [v, connected] : graph->matrix[u]) {
                if (connected) {
                    incoming[v].push_back(u);
                    if (!visited[v]) {
                        visit(v);
                    }
                }
            }
        }
        L.push_back(u);
    };

    for (const auto& [name, _] : graph->node_map) {
        if (!visited[name]) {
            visit(name);
        }
    }

    std::unordered_map<std::string, bool> assigned;
    for (const auto& [name, _] : graph->node_map) {
        assigned[name] = false;
    }

    std::function<void(const std::string&, std::unordered_set<std::string>&)> assign = 
        [&](const std::string& u, std::unordered_set<std::string>& comp) {
        assigned[u] = true;
        comp.insert(u);
        if (incoming.count(u)) {
            for (const auto& v : incoming[u]) {
                if (!assigned[v]) {
                    assign(v, comp);
                }
            }
        }
    };

    PyObject* components = PyList_New(0);
    if (!components) return nullptr;

    for (int i = L.size() - 1; i >= 0; i--) {
        std::unordered_set<std::string> comp;
        if (!assigned[L[i]]) {
            assign(L[i], comp);
            if (!comp.empty()) {
                PyObject* py_comp = PySet_New(nullptr);
                if (!py_comp) {
                    Py_DECREF(components);
                    return nullptr;
                }
                for (const auto& node_name : comp) {
                    PyObject* py_name = PyUnicode_FromString(node_name.c_str());
                    if (!py_name || PySet_Add(py_comp, py_name) < 0) {
                        Py_XDECREF(py_name);
                        Py_DECREF(py_comp);
                        Py_DECREF(components);
                        return nullptr;
                    }
                    Py_DECREF(py_name);
                }
                if (PyList_Append(components, py_comp) < 0) {
                    Py_DECREF(py_comp);
                    Py_DECREF(components);
                    return nullptr;
                }
                Py_DECREF(py_comp);
            }
        }
    }

    return components;
}

static void _tarjan_dfs(const std::string& u, AdjacencyListGraph* graph,
                        int& index, std::vector<std::string>& stack,
                        std::unordered_map<std::string, int>& indices,
                        std::unordered_map<std::string, int>& low_links,
                        std::unordered_map<std::string, bool>& on_stacks,
                        PyObject* components) {
    indices[u] = index;
    low_links[u] = index;
    index++;
    stack.push_back(u);
    on_stacks[u] = true;

    AdjacencyListGraphNode* node = graph->node_map[u];
    for (const auto& [v, _] : node->adjacent) {
        if (indices[v] == -1) {
            _tarjan_dfs(v, graph, index, stack, indices, low_links, on_stacks, components);
            low_links[u] = std::min(low_links[u], low_links[v]);
        } else if (on_stacks[v]) {
            low_links[u] = std::min(low_links[u], low_links[v]);
        }
    }

    if (low_links[u] == indices[u]) {
        PyObject* component = PySet_New(nullptr);
        while (!stack.empty()) {
            std::string w = stack.back();
            stack.pop_back();
            on_stacks[w] = false;
            PyObject* py_name = PyUnicode_FromString(w.c_str());
            PySet_Add(component, py_name);
            Py_DECREF(py_name);
            if (w == u) break;
        }
        PyList_Append(components, component);
        Py_DECREF(component);
    }
}

static PyObject* strongly_connected_components_tarjan_adjacency_list(PyObject* self, PyObject* args, PyObject* kwargs) {
    PyObject* graph_obj;
    static const char* kwlist[] = {"graph", nullptr};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!", const_cast<char**>(kwlist),
                                     &AdjacencyListGraphType, &graph_obj)) {
        return nullptr;
    }

    AdjacencyListGraph* graph = reinterpret_cast<AdjacencyListGraph*>(graph_obj);
    
    int index = 0;
    std::vector<std::string> stack;
    std::unordered_map<std::string, int> indices;
    std::unordered_map<std::string, int> low_links;
    std::unordered_map<std::string, bool> on_stacks;

    for (const auto& [name, _] : graph->node_map) {
        indices[name] = -1;
        low_links[name] = -1;
        on_stacks[name] = false;
    }

    PyObject* components = PyList_New(0);
    if (!components) return nullptr;

    for (const auto& [name, _] : graph->node_map) {
        if (indices[name] == -1) {
            _tarjan_dfs(name, graph, index, stack, indices, low_links, on_stacks, components);
        }
    }

    return components;
}

static PyObject* strongly_connected_components_tarjan_adjacency_matrix(PyObject* self, PyObject* args, PyObject* kwargs) {
    PyObject* graph_obj;
    static const char* kwlist[] = {"graph", nullptr};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!", const_cast<char**>(kwlist),
                                     &AdjacencyMatrixGraphType, &graph_obj)) {
        return nullptr;
    }

    AdjacencyMatrixGraph* graph = reinterpret_cast<AdjacencyMatrixGraph*>(graph_obj);
    
    int index = 0;
    std::vector<std::string> stack;
    std::unordered_map<std::string, int> indices;
    std::unordered_map<std::string, int> low_links;
    std::unordered_map<std::string, bool> on_stacks;

    for (const auto& [name, _] : graph->node_map) {
        indices[name] = -1;
        low_links[name] = -1;
        on_stacks[name] = false;
    }

    PyObject* components = PyList_New(0);
    if (!components) return nullptr;

    std::function<void(const std::string&)> tarjan_dfs = [&](const std::string& u) {
        indices[u] = index;
        low_links[u] = index;
        index++;
        stack.push_back(u);
        on_stacks[u] = true;

        if (graph->matrix.count(u)) {
            for (const auto& [v, connected] : graph->matrix[u]) {
                if (!connected) continue;
                if (indices[v] == -1) {
                    tarjan_dfs(v);
                    low_links[u] = std::min(low_links[u], low_links[v]);
                } else if (on_stacks[v]) {
                    low_links[u] = std::min(low_links[u], low_links[v]);
                }
            }
        }

        if (low_links[u] == indices[u]) {
            PyObject* component = PySet_New(nullptr);
            while (!stack.empty()) {
                std::string w = stack.back();
                stack.pop_back();
                on_stacks[w] = false;
                PyObject* py_name = PyUnicode_FromString(w.c_str());
                PySet_Add(component, py_name);
                Py_DECREF(py_name);
                if (w == u) break;
            }
            PyList_Append(components, component);
            Py_DECREF(component);
        }
    };

    for (const auto& [name, _] : graph->node_map) {
        if (indices[name] == -1) {
            tarjan_dfs(name);
        }
    }

    return components;
}

#include <functional>

static PyObject* all_pair_shortest_paths_floyd_warshall_adjacency_list(PyObject* self, PyObject* args, PyObject* kwargs) {
    PyObject* graph_obj;
    static const char* kwlist[] = {"graph", nullptr};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!", const_cast<char**>(kwlist),
                                     &AdjacencyListGraphType, &graph_obj)) {
        return nullptr;
    }

    AdjacencyListGraph* graph = reinterpret_cast<AdjacencyListGraph*>(graph_obj);
    
    PyObject* dist_dict = PyDict_New();
    PyObject* next_dict = PyDict_New();
    if (!dist_dict || !next_dict) {
        Py_XDECREF(dist_dict);
        Py_XDECREF(next_dict);
        return nullptr;
    }

    for (const auto& [v_name, _] : graph->node_map) {
        PyObject* v_dist = PyDict_New();
        PyObject* v_next = PyDict_New();
        if (!v_dist || !v_next) {
            Py_XDECREF(v_dist);
            Py_XDECREF(v_next);
            Py_DECREF(dist_dict);
            Py_DECREF(next_dict);
            return nullptr;
        }
        PyDict_SetItemString(dist_dict, v_name.c_str(), v_dist);
        PyDict_SetItemString(next_dict, v_name.c_str(), v_next);
        Py_DECREF(v_dist);
        Py_DECREF(v_next);
    }

    for (const auto& [edge_key, edge] : graph->edges) {
        size_t delim = edge_key.find('_');
        std::string u_name = edge_key.substr(0, delim);
        std::string v_name = edge_key.substr(delim + 1);
        
        double weight = 0.0;
        if (edge->value_type == DataType::Int)
            weight = static_cast<double>(std::get<int64_t>(edge->value));
        else if (edge->value_type == DataType::Double)
            weight = std::get<double>(edge->value);
        else
            continue;

        PyObject* u_dist = PyDict_GetItemString(dist_dict, u_name.c_str());
        PyObject* u_next = PyDict_GetItemString(next_dict, u_name.c_str());
        
        PyObject* weight_obj = PyFloat_FromDouble(weight);
        PyObject* source_str = PyUnicode_FromString(u_name.c_str());
        
        PyDict_SetItemString(u_dist, v_name.c_str(), weight_obj);
        PyDict_SetItemString(u_next, v_name.c_str(), source_str);
        
        Py_DECREF(weight_obj);
        Py_DECREF(source_str);
    }

    for (const auto& [v_name, _] : graph->node_map) {
        PyObject* v_dist = PyDict_GetItemString(dist_dict, v_name.c_str());
        PyObject* v_next = PyDict_GetItemString(next_dict, v_name.c_str());
        
        PyObject* zero = PyFloat_FromDouble(0.0);
        PyObject* v_str = PyUnicode_FromString(v_name.c_str());
        
        PyDict_SetItemString(v_dist, v_name.c_str(), zero);
        PyDict_SetItemString(v_next, v_name.c_str(), v_str);
        
        Py_DECREF(zero);
        Py_DECREF(v_str);
    }

    for (const auto& [k_name, _] : graph->node_map) {
        for (const auto& [i_name, __] : graph->node_map) {
            PyObject* i_dist = PyDict_GetItemString(dist_dict, i_name.c_str());
            PyObject* i_next = PyDict_GetItemString(next_dict, i_name.c_str());
            
            for (const auto& [j_name, ___] : graph->node_map) {
                PyObject* k_dist = PyDict_GetItemString(dist_dict, k_name.c_str());
                
                PyObject* dist_i_j_obj = PyDict_GetItemString(i_dist, j_name.c_str());
                PyObject* dist_i_k_obj = PyDict_GetItemString(i_dist, k_name.c_str());
                PyObject* dist_k_j_obj = PyDict_GetItemString(k_dist, j_name.c_str());
                
                double dist_i_j = dist_i_j_obj ? PyFloat_AsDouble(dist_i_j_obj) : INFINITY;
                double dist_i_k = dist_i_k_obj ? PyFloat_AsDouble(dist_i_k_obj) : INFINITY;
                double dist_k_j = dist_k_j_obj ? PyFloat_AsDouble(dist_k_j_obj) : INFINITY;
                
                if (dist_i_j > dist_i_k + dist_k_j) {
                    PyObject* new_dist = PyFloat_FromDouble(dist_i_k + dist_k_j);
                    PyDict_SetItemString(i_dist, j_name.c_str(), new_dist);
                    Py_DECREF(new_dist);
                    
                    PyObject* next_i_k = PyDict_GetItemString(i_next, k_name.c_str());
                    if (next_i_k) {
                        PyDict_SetItemString(i_next, j_name.c_str(), next_i_k);
                    }
                }
            }
        }
    }

    for (const auto& [i_name, _] : graph->node_map) {
        PyObject* i_next = PyDict_GetItemString(next_dict, i_name.c_str());
        PyObject* i_dist = PyDict_GetItemString(dist_dict, i_name.c_str());
        for (const auto& [j_name, __] : graph->node_map) {
            if (i_name == j_name) continue;
            
            PyObject* dist_val = PyDict_GetItemString(i_dist, j_name.c_str());
            double dist = dist_val ? PyFloat_AsDouble(dist_val) : INFINITY;
            
            if (dist == INFINITY) {
                PyDict_SetItemString(i_next, j_name.c_str(), Py_None);
            } else {
                PyObject* next_val = PyDict_GetItemString(i_next, j_name.c_str());
                if (!next_val) {
                    PyDict_SetItemString(i_next, j_name.c_str(), Py_None);
                }
            }
        }
    }

    PyObject* result = PyTuple_New(2);
    if (!result) {
        Py_DECREF(dist_dict);
        Py_DECREF(next_dict);
        return nullptr;
    }

    PyTuple_SetItem(result, 0, dist_dict);
    PyTuple_SetItem(result, 1, next_dict);
    return result;
}

static PyObject* all_pair_shortest_paths_floyd_warshall_adjacency_matrix(PyObject* self, PyObject* args, PyObject* kwargs) {
    PyObject* graph_obj;
    static const char* kwlist[] = {"graph", nullptr};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!", const_cast<char**>(kwlist),
                                     &AdjacencyMatrixGraphType, &graph_obj)) {
        return nullptr;
    }

    AdjacencyMatrixGraph* graph = reinterpret_cast<AdjacencyMatrixGraph*>(graph_obj);
    
    PyObject* dist_dict = PyDict_New();
    PyObject* next_dict = PyDict_New();
    if (!dist_dict || !next_dict) {
        Py_XDECREF(dist_dict);
        Py_XDECREF(next_dict);
        return nullptr;
    }

    for (const auto& [v_name, _] : graph->node_map) {
        PyObject* v_dist = PyDict_New();
        PyObject* v_next = PyDict_New();
        if (!v_dist || !v_next) {
            Py_XDECREF(v_dist);
            Py_XDECREF(v_next);
            Py_DECREF(dist_dict);
            Py_DECREF(next_dict);
            return nullptr;
        }
        PyDict_SetItemString(dist_dict, v_name.c_str(), v_dist);
        PyDict_SetItemString(next_dict, v_name.c_str(), v_next);
        Py_DECREF(v_dist);
        Py_DECREF(v_next);
    }

    for (const auto& [u_name, neighbors] : graph->matrix) {
        for (const auto& [v_name, connected] : neighbors) {
            if (!connected) continue;
            
            std::string edge_key = make_edge_key(u_name, v_name);
            if (graph->edge_weights.count(edge_key) == 0) continue;
            
            GraphEdge* edge = graph->edge_weights[edge_key];
            
            double weight = 0.0;
            if (edge->value_type == DataType::Int)
                weight = static_cast<double>(std::get<int64_t>(edge->value));
            else if (edge->value_type == DataType::Double)
                weight = std::get<double>(edge->value);
            else
                continue;

            PyObject* u_dist = PyDict_GetItemString(dist_dict, u_name.c_str());
            PyObject* u_next = PyDict_GetItemString(next_dict, u_name.c_str());
            
            PyObject* weight_obj = PyFloat_FromDouble(weight);
            PyObject* source_str = PyUnicode_FromString(u_name.c_str());
            
            PyDict_SetItemString(u_dist, v_name.c_str(), weight_obj);
            PyDict_SetItemString(u_next, v_name.c_str(), source_str);
            
            Py_DECREF(weight_obj);
            Py_DECREF(source_str);
        }
    }

    for (const auto& [v_name, _] : graph->node_map) {
        PyObject* v_dist = PyDict_GetItemString(dist_dict, v_name.c_str());
        PyObject* v_next = PyDict_GetItemString(next_dict, v_name.c_str());
        
        PyObject* zero = PyFloat_FromDouble(0.0);
        PyObject* v_str = PyUnicode_FromString(v_name.c_str());
        
        PyDict_SetItemString(v_dist, v_name.c_str(), zero);
        PyDict_SetItemString(v_next, v_name.c_str(), v_str);
        
        Py_DECREF(zero);
        Py_DECREF(v_str);
    }

    for (const auto& [k_name, _] : graph->node_map) {
        for (const auto& [i_name, __] : graph->node_map) {
            PyObject* i_dist = PyDict_GetItemString(dist_dict, i_name.c_str());
            PyObject* i_next = PyDict_GetItemString(next_dict, i_name.c_str());
            
            for (const auto& [j_name, ___] : graph->node_map) {
                PyObject* k_dist = PyDict_GetItemString(dist_dict, k_name.c_str());
                
                PyObject* dist_i_j_obj = PyDict_GetItemString(i_dist, j_name.c_str());
                PyObject* dist_i_k_obj = PyDict_GetItemString(i_dist, k_name.c_str());
                PyObject* dist_k_j_obj = PyDict_GetItemString(k_dist, j_name.c_str());
                
                double dist_i_j = dist_i_j_obj ? PyFloat_AsDouble(dist_i_j_obj) : INFINITY;
                double dist_i_k = dist_i_k_obj ? PyFloat_AsDouble(dist_i_k_obj) : INFINITY;
                double dist_k_j = dist_k_j_obj ? PyFloat_AsDouble(dist_k_j_obj) : INFINITY;
                
                if (dist_i_j > dist_i_k + dist_k_j) {
                    PyObject* new_dist = PyFloat_FromDouble(dist_i_k + dist_k_j);
                    PyDict_SetItemString(i_dist, j_name.c_str(), new_dist);
                    Py_DECREF(new_dist);
                    
                    PyObject* next_i_k = PyDict_GetItemString(i_next, k_name.c_str());
                    if (next_i_k) {
                        PyDict_SetItemString(i_next, j_name.c_str(), next_i_k);
                    }
                }
            }
        }
    }

    for (const auto& [i_name, _] : graph->node_map) {
        PyObject* i_next = PyDict_GetItemString(next_dict, i_name.c_str());
        PyObject* i_dist = PyDict_GetItemString(dist_dict, i_name.c_str());
        for (const auto& [j_name, __] : graph->node_map) {
            if (i_name == j_name) continue;
            
            PyObject* dist_val = PyDict_GetItemString(i_dist, j_name.c_str());
            double dist = dist_val ? PyFloat_AsDouble(dist_val) : INFINITY;
            
            if (dist == INFINITY) {
                PyDict_SetItemString(i_next, j_name.c_str(), Py_None);
            } else {
                PyObject* next_val = PyDict_GetItemString(i_next, j_name.c_str());
                if (!next_val) {
                    PyDict_SetItemString(i_next, j_name.c_str(), Py_None);
                }
            }
        }
    }

    PyObject* result = PyTuple_New(2);
    if (!result) {
        Py_DECREF(dist_dict);
        Py_DECREF(next_dict);
        return nullptr;
    }

    PyTuple_SetItem(result, 0, dist_dict);
    PyTuple_SetItem(result, 1, next_dict);
    return result;
}

static PyObject* topological_sort_kahn_adjacency_list(PyObject* self, PyObject* args, PyObject* kwargs) {
    PyObject* graph_obj;
    static const char* kwlist[] = {"graph", nullptr};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!", const_cast<char**>(kwlist),
                                     &AdjacencyListGraphType, &graph_obj)) {
        return nullptr;
    }

    AdjacencyListGraph* graph = reinterpret_cast<AdjacencyListGraph*>(graph_obj);
    
    std::deque<std::string> S;
    std::unordered_map<std::string, int> in_degree;
    
    for (const auto& [name, _] : graph->node_map) {
        in_degree[name] = 0;
    }
    
    for (const auto& [u_name, u_node] : graph->node_map) {
        for (const auto& [v_name, _] : u_node->adjacent) {
            in_degree[v_name]++;
        }
    }
    
    for (const auto& [name, degree] : in_degree) {
        if (degree == 0) {
            S.push_back(name);
        }
    }
    
    PyObject* L = PyList_New(0);
    if (!L) return nullptr;
    
    while (!S.empty()) {
        std::string n = S.front();
        S.pop_front();
        
        PyObject* py_name = PyUnicode_FromString(n.c_str());
        if (!py_name || PyList_Append(L, py_name) < 0) {
            Py_XDECREF(py_name);
            Py_DECREF(L);
            return nullptr;
        }
        Py_DECREF(py_name);
        
        AdjacencyListGraphNode* node = graph->node_map[n];
        std::vector<std::string> neighbors_to_process;
        for (const auto& [m_name, _] : node->adjacent) {
            neighbors_to_process.push_back(m_name);
        }
        
        for (const auto& m_name : neighbors_to_process) {
            std::string key_nm = make_edge_key(n, m_name);
            if (graph->edges.count(key_nm)) {
                GraphEdge* edge = graph->edges[key_nm];
                Py_DECREF(edge);
                graph->edges.erase(key_nm);
            }
            
            node->adjacent.erase(m_name);
            
            in_degree[m_name]--;
            if (in_degree[m_name] == 0) {
                S.push_back(m_name);
            }
        }
    }
    
    for (const auto& [name, degree] : in_degree) {
        if (degree > 0) {
            Py_DECREF(L);
            PyErr_SetString(PyExc_ValueError, "Graph is not acyclic.");
            return nullptr;
        }
    }
    
    return L;
}

static PyObject* topological_sort_kahn_adjacency_matrix(PyObject* self, PyObject* args, PyObject* kwargs) {
    PyObject* graph_obj;
    static const char* kwlist[] = {"graph", nullptr};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!", const_cast<char**>(kwlist),
                                     &AdjacencyMatrixGraphType, &graph_obj)) {
        return nullptr;
    }

    AdjacencyMatrixGraph* graph = reinterpret_cast<AdjacencyMatrixGraph*>(graph_obj);
    
    std::deque<std::string> S;
    std::unordered_map<std::string, int> in_degree;
    
    for (const auto& [name, _] : graph->node_map) {
        in_degree[name] = 0;
    }
    
    for (const auto& [u_name, neighbors] : graph->matrix) {
        for (const auto& [v_name, connected] : neighbors) {
            if (connected) {
                in_degree[v_name]++;
            }
        }
    }
    
    for (const auto& [name, degree] : in_degree) {
        if (degree == 0) {
            S.push_back(name);
        }
    }
    
    PyObject* L = PyList_New(0);
    if (!L) return nullptr;
    
    while (!S.empty()) {
        std::string n = S.front();
        S.pop_front();
        
        PyObject* py_name = PyUnicode_FromString(n.c_str());
        if (!py_name || PyList_Append(L, py_name) < 0) {
            Py_XDECREF(py_name);
            Py_DECREF(L);
            return nullptr;
        }
        Py_DECREF(py_name);
        
        if (graph->matrix.count(n)) {
            std::vector<std::string> neighbors_to_process;
            for (const auto& [m_name, connected] : graph->matrix[n]) {
                if (connected) {
                    neighbors_to_process.push_back(m_name);
                }
            }
            
            for (const auto& m_name : neighbors_to_process) {
                graph->matrix[n][m_name] = false;
                
                std::string key_nm = make_edge_key(n, m_name);
                if (graph->edge_weights.count(key_nm)) {
                    GraphEdge* edge = graph->edge_weights[key_nm];
                    Py_DECREF(edge);
                    graph->edge_weights.erase(key_nm);
                }
                
                in_degree[m_name]--;
                if (in_degree[m_name] == 0) {
                    S.push_back(m_name);
                }
            }
        }
    }
    
    for (const auto& [name, degree] : in_degree) {
        if (degree > 0) {
            Py_DECREF(L);
            PyErr_SetString(PyExc_ValueError, "Graph is not acyclic.");
            return nullptr;
        }
    }
    
    return L;
}

static PyObject* breadth_first_search_max_flow_adjacency_list(PyObject* self, PyObject* args, PyObject* kwargs) {
    PyObject* graph_obj;
    const char* source_name;
    const char* sink_name;
    PyObject* flow_passed_dict;
    int for_dinic = 0;
    
    static const char* kwlist[] = {"graph", "source_node", "sink_node", "flow_passed", "for_dinic", nullptr};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!ssO!|p", const_cast<char**>(kwlist),
                                     &AdjacencyListGraphType, &graph_obj,
                                     &source_name, &sink_name,
                                     &PyDict_Type, &flow_passed_dict,
                                     &for_dinic)) {
        return nullptr;
    }

    AdjacencyListGraph* graph = reinterpret_cast<AdjacencyListGraph*>(graph_obj);
    
    std::deque<std::string> bfs_queue;
    std::unordered_map<std::string, std::string> parent;
    std::unordered_map<std::string, double> currentPathC;
    
    currentPathC[source_name] = INFINITY;
    bfs_queue.push_back(source_name);
    
    while (!bfs_queue.empty()) {
        std::string curr_node = bfs_queue.front();
        bfs_queue.pop_front();
        
        AdjacencyListGraphNode* node = graph->node_map[curr_node];
        if (node->adjacent.empty()) continue;
        
        for (const auto& [next_name, _] : node->adjacent) {
            std::string edge_key = make_edge_key(curr_node, next_name);
            if (!graph->edges.count(edge_key)) continue;
            
            GraphEdge* edge = graph->edges[edge_key];
            double capacity = 0.0;
            if (edge->value_type == DataType::Int)
                capacity = static_cast<double>(std::get<int64_t>(edge->value));
            else if (edge->value_type == DataType::Double)
                capacity = std::get<double>(edge->value);
            else
                continue;
            
            PyObject* key_tuple = PyTuple_Pack(2, 
                PyUnicode_FromString(curr_node.c_str()),
                PyUnicode_FromString(next_name.c_str()));
            PyObject* fp_obj = PyDict_GetItem(flow_passed_dict, key_tuple);
            double fp = fp_obj ? PyFloat_AsDouble(fp_obj) : 0.0;
            Py_DECREF(key_tuple);
            
            if (capacity && parent.find(next_name) == parent.end() && capacity - fp > 0) {
                parent[next_name] = curr_node;
                double next_flow = std::min(currentPathC[curr_node], capacity - fp);
                currentPathC[next_name] = next_flow;
                
                if (next_name == sink_name && !for_dinic) {
                    PyObject* parent_dict = PyDict_New();
                    for (const auto& [k, v] : parent) {
                        PyDict_SetItemString(parent_dict, k.c_str(), PyUnicode_FromString(v.c_str()));
                    }
                    PyObject* result = PyTuple_Pack(2, PyFloat_FromDouble(next_flow), parent_dict);
                    Py_DECREF(parent_dict);
                    return result;
                }
                bfs_queue.push_back(next_name);
            }
        }
    }
    
    PyObject* parent_dict = PyDict_New();
    for (const auto& [k, v] : parent) {
        PyDict_SetItemString(parent_dict, k.c_str(), PyUnicode_FromString(v.c_str()));
    }
    PyObject* result = PyTuple_Pack(2, PyFloat_FromDouble(0.0), parent_dict);
    Py_DECREF(parent_dict);
    return result;
}

static PyObject* max_flow_edmonds_karp_adjacency_list(PyObject* self, PyObject* args, PyObject* kwargs) {
    PyObject* graph_obj;
    const char* source_name;
    const char* sink_name;
    
    static const char* kwlist[] = {"graph", "source", "sink", nullptr};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!ss", const_cast<char**>(kwlist),
                                     &AdjacencyListGraphType, &graph_obj,
                                     &source_name, &sink_name)) {
        return nullptr;
    }

    AdjacencyListGraph* graph = reinterpret_cast<AdjacencyListGraph*>(graph_obj);
    
    double m_flow = 0.0;
    PyObject* flow_passed_dict = PyDict_New();
    if (!flow_passed_dict) return nullptr;
    
    PyObject* bfs_args = Py_BuildValue("(OssOi)", graph_obj, source_name, sink_name, flow_passed_dict, 0);
    PyObject* bfs_result = breadth_first_search_max_flow_adjacency_list(self, bfs_args, nullptr);
    Py_DECREF(bfs_args);
    if (!bfs_result) {
        Py_DECREF(flow_passed_dict);
        return nullptr;
    }
    
    PyObject* new_flow_obj = PyTuple_GetItem(bfs_result, 0);
    PyObject* parent_dict = PyTuple_GetItem(bfs_result, 1);
    double new_flow = PyFloat_AsDouble(new_flow_obj);
    
    while (new_flow != 0.0) {
        m_flow += new_flow;
        std::string current = sink_name;
        
        while (current != source_name) {
            PyObject* prev_obj = PyDict_GetItemString(parent_dict, current.c_str());
            if (!prev_obj) break;
            
            const char* prev_cstr = PyUnicode_AsUTF8(prev_obj);
            std::string prev = prev_cstr;
            
            PyObject* key_tuple_forward = PyTuple_Pack(2,
                PyUnicode_FromString(prev.c_str()),
                PyUnicode_FromString(current.c_str()));
            PyObject* fp_forward = PyDict_GetItem(flow_passed_dict, key_tuple_forward);
            double fp_forward_val = fp_forward ? PyFloat_AsDouble(fp_forward) : 0.0;
            PyDict_SetItem(flow_passed_dict, key_tuple_forward, PyFloat_FromDouble(fp_forward_val + new_flow));
            Py_DECREF(key_tuple_forward);
            
            PyObject* key_tuple_backward = PyTuple_Pack(2,
                PyUnicode_FromString(current.c_str()),
                PyUnicode_FromString(prev.c_str()));
            PyObject* fp_backward = PyDict_GetItem(flow_passed_dict, key_tuple_backward);
            double fp_backward_val = fp_backward ? PyFloat_AsDouble(fp_backward) : 0.0;
            PyDict_SetItem(flow_passed_dict, key_tuple_backward, PyFloat_FromDouble(fp_backward_val - new_flow));
            Py_DECREF(key_tuple_backward);
            
            current = prev;
        }
        
        Py_DECREF(bfs_result);
        bfs_args = Py_BuildValue("(OssOi)", graph_obj, source_name, sink_name, flow_passed_dict, 0);
        bfs_result = breadth_first_search_max_flow_adjacency_list(self, bfs_args, nullptr);
        Py_DECREF(bfs_args);
        if (!bfs_result) {
            Py_DECREF(flow_passed_dict);
            return nullptr;
        }
        
        new_flow_obj = PyTuple_GetItem(bfs_result, 0);
        parent_dict = PyTuple_GetItem(bfs_result, 1);
        new_flow = PyFloat_AsDouble(new_flow_obj);
    }
    
    Py_DECREF(bfs_result);
    Py_DECREF(flow_passed_dict);
    
    return PyFloat_FromDouble(m_flow);
}

static double depth_first_search_max_flow_dinic_adjacency_list(
    AdjacencyListGraph* graph,
    const std::string& u,
    std::unordered_map<std::string, std::string>& parent,
    const std::string& sink_node,
    double flow,
    PyObject* flow_passed_dict) {
    
    if (u == sink_node) {
        return flow;
    }
    
    AdjacencyListGraphNode* node = graph->node_map[u];
    if (node->adjacent.empty()) return 0.0;
    
    for (const auto& [next_name, _] : node->adjacent) {
        std::string edge_key = make_edge_key(u, next_name);
        if (!graph->edges.count(edge_key)) continue;
        
        GraphEdge* edge = graph->edges[edge_key];
        double capacity = 0.0;
        if (edge->value_type == DataType::Int)
            capacity = static_cast<double>(std::get<int64_t>(edge->value));
        else if (edge->value_type == DataType::Double)
            capacity = std::get<double>(edge->value);
        else
            continue;
        
        PyObject* key_tuple = PyTuple_Pack(2,
            PyUnicode_FromString(u.c_str()),
            PyUnicode_FromString(next_name.c_str()));
        PyObject* fp_obj = PyDict_GetItem(flow_passed_dict, key_tuple);
        double fp = fp_obj ? PyFloat_AsDouble(fp_obj) : 0.0;
        Py_DECREF(key_tuple);
        
        if (parent.count(next_name) && parent[next_name] == u && capacity - fp > 0) {
            double path_flow = depth_first_search_max_flow_dinic_adjacency_list(
                graph, next_name, parent, sink_node, std::min(flow, capacity - fp), flow_passed_dict);
            
            if (path_flow > 0) {
                PyObject* key_tuple_forward = PyTuple_Pack(2,
                    PyUnicode_FromString(u.c_str()),
                    PyUnicode_FromString(next_name.c_str()));
                PyObject* fp_forward = PyDict_GetItem(flow_passed_dict, key_tuple_forward);
                double fp_forward_val = fp_forward ? PyFloat_AsDouble(fp_forward) : 0.0;
                PyDict_SetItem(flow_passed_dict, key_tuple_forward, PyFloat_FromDouble(fp_forward_val + path_flow));
                Py_DECREF(key_tuple_forward);
                
                PyObject* key_tuple_backward = PyTuple_Pack(2,
                    PyUnicode_FromString(next_name.c_str()),
                    PyUnicode_FromString(u.c_str()));
                PyObject* fp_backward = PyDict_GetItem(flow_passed_dict, key_tuple_backward);
                double fp_backward_val = fp_backward ? PyFloat_AsDouble(fp_backward) : 0.0;
                PyDict_SetItem(flow_passed_dict, key_tuple_backward, PyFloat_FromDouble(fp_backward_val - path_flow));
                Py_DECREF(key_tuple_backward);
                
                return path_flow;
            }
        }
    }
    
    return 0.0;
}

static PyObject* max_flow_dinic_adjacency_list(PyObject* self, PyObject* args, PyObject* kwargs) {
    PyObject* graph_obj;
    const char* source_name;
    const char* sink_name;
    
    static const char* kwlist[] = {"graph", "source", "sink", nullptr};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!ss", const_cast<char**>(kwlist),
                                     &AdjacencyListGraphType, &graph_obj,
                                     &source_name, &sink_name)) {
        return nullptr;
    }

    AdjacencyListGraph* graph = reinterpret_cast<AdjacencyListGraph*>(graph_obj);
    
    double max_flow_val = 0.0;
    PyObject* flow_passed_dict = PyDict_New();
    if (!flow_passed_dict) return nullptr;
    
    while (true) {
        PyObject* bfs_args = Py_BuildValue("(OssOi)", graph_obj, source_name, sink_name, flow_passed_dict, 1);
        PyObject* bfs_result = breadth_first_search_max_flow_adjacency_list(self, bfs_args, nullptr);
        Py_DECREF(bfs_args);
        if (!bfs_result) {
            Py_DECREF(flow_passed_dict);
            return nullptr;
        }
        
        PyObject* parent_dict = PyTuple_GetItem(bfs_result, 1);
        PyObject* sink_parent = PyDict_GetItemString(parent_dict, sink_name);
        
        if (!sink_parent) {
            Py_DECREF(bfs_result);
            break;
        }
        
        std::unordered_map<std::string, std::string> parent_map;
        PyObject *key, *value;
        Py_ssize_t pos = 0;
        while (PyDict_Next(parent_dict, &pos, &key, &value)) {
            parent_map[PyUnicode_AsUTF8(key)] = PyUnicode_AsUTF8(value);
        }
        
        while (true) {
            double path_flow = depth_first_search_max_flow_dinic_adjacency_list(
                graph, source_name, parent_map, sink_name, INFINITY, flow_passed_dict);
            
            if (path_flow <= 0) {
                break;
            }
            max_flow_val += path_flow;
        }
        
        Py_DECREF(bfs_result);
    }
    
    Py_DECREF(flow_passed_dict);
    
    return PyFloat_FromDouble(max_flow_val);
}
