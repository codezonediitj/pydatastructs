#include <Python.h>
#include <unordered_map>
#include <queue>
#include <string>
#include "AdjacencyList.hpp"

static inline AdjacencyListGraphNode* get_node(AdjacencyListGraph* graph, const std::string& name) {
    auto it = graph->node_map.find(name);
    return (it != graph->node_map.end()) ? it->second : nullptr;
}

static PyObject* bfs_adjacency_list(PyObject* self, PyObject* args, PyObject* kwds) {
    static char* kwlist[] = {(char*)"graph", (char*)"source_node", (char*)"operation", (char*)"extra_arg", NULL};

    PyObject* py_graph = nullptr;
    const char* source_node = nullptr;
    PyObject* operation = nullptr;
    PyObject* extra_arg = nullptr;

    fprintf(stderr, "[bfs] Parsing arguments...\n");

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "OsO|O", kwlist,
                                     &py_graph, &source_node, &operation, &extra_arg)) {
        fprintf(stderr, "[bfs] Failed to parse arguments\n");
        return NULL;
    }

    fprintf(stderr, "[bfs] Arguments parsed:\n");
    fprintf(stderr, "  - source_node: %s\n", source_node);
    fprintf(stderr, "  - extra_arg: %s\n", (extra_arg ? Py_TYPE(extra_arg)->tp_name : "NULL"));
    fprintf(stderr, "[bfs] Checking type of py_graph...\n");
    fprintf(stderr, "        - Expected: %s\n", AdjacencyListGraphType.tp_name);
    fprintf(stderr, "        - Actual:   %s\n", Py_TYPE(py_graph)->tp_name);
    fprintf(stderr, "        - Expected address: %p\n", &AdjacencyListGraphType);
    fprintf(stderr, "        - Actual type addr: %p\n", (void*)Py_TYPE(py_graph));

    fprintf(stderr, "[bfs] Attempting to import _graph...\n");
    PyObject* graph_module = PyImport_ImportModule("_graph");
    if (!graph_module) {
    PyErr_Print();
    PyErr_SetString(PyExc_ImportError, "Could not import _graph module");
    return NULL;
    }

    PyObject* expected_type = PyObject_GetAttrString(graph_module, "AdjacencyListGraph");
    Py_DECREF(graph_module);

    if (!expected_type || !PyType_Check(expected_type)) {
        Py_XDECREF(expected_type);
        PyErr_SetString(PyExc_TypeError, "Could not retrieve AdjacencyListGraph type");
        return NULL;
    }

    if (!PyObject_IsInstance(py_graph, expected_type)) {
        Py_DECREF(expected_type);
        PyErr_SetString(PyExc_TypeError, "Expected an AdjacencyListGraph instance");
        return NULL;
    }

    if (!PyCallable_Check(operation)) {
        PyErr_SetString(PyExc_TypeError, "Expected a callable for operation");
        fprintf(stderr, "[bfs] operation is not callable\n");
        return NULL;
    }

    AdjacencyListGraph* graph = (AdjacencyListGraph*)py_graph;

    if (!get_node(graph, source_node)) {
        PyErr_SetString(PyExc_ValueError, "Source node does not exist in the graph");
        fprintf(stderr, "[bfs] source_node not found in graph\n");
        return NULL;
    }

    fprintf(stderr, "[bfs] Starting BFS from node: %s\n", source_node);

    std::unordered_map<std::string, bool> visited;
    std::queue<std::string> q;

    q.push(source_node);
    visited[source_node] = true;

    while (!q.empty()) {
        std::string curr = q.front();
        q.pop();

        fprintf(stderr, "[bfs] Visiting node: %s\n", curr.c_str());

        auto* curr_node = get_node(graph, curr);
        if (!curr_node) {
            fprintf(stderr, "[bfs] Warning: node %s not found in node_map\n", curr.c_str());
            continue;
        }

        const auto& neighbors = curr_node->adjacent;

        if (!neighbors.empty()) {
            for (const auto& [next_name, _] : neighbors) {
                if (!visited[next_name]) {
                    fprintf(stderr, "[bfs] Considering neighbor: %s\n", next_name.c_str());

                    PyObject* result = nullptr;

                    if (extra_arg)
                        result = PyObject_CallFunction(operation, "ssO", curr.c_str(), next_name.c_str(), extra_arg);
                    else
                        result = PyObject_CallFunction(operation, "ss", curr.c_str(), next_name.c_str());

                    if (!result) {
                        fprintf(stderr, "[bfs] PyObject_CallFunction failed on (%s, %s)\n", curr.c_str(), next_name.c_str());
                        PyErr_Print();
                        return NULL;
                    }

                    int keep_going = PyObject_IsTrue(result);
                    Py_DECREF(result);

                    if (!keep_going) {
                        fprintf(stderr, "[bfs] Operation requested to stop traversal at edge (%s -> %s)\n", curr.c_str(), next_name.c_str());
                        Py_RETURN_NONE;
                    }

                    visited[next_name] = true;
                    q.push(next_name);
                }
            }
        } else {
            fprintf(stderr, "[bfs] Leaf node reached: %s\n", curr.c_str());

            PyObject* result = nullptr;

            if (extra_arg)
                result = PyObject_CallFunction(operation, "sO", curr.c_str(), extra_arg);
            else
                result = PyObject_CallFunction(operation, "s", curr.c_str());

            if (!result) {
                fprintf(stderr, "[bfs] PyObject_CallFunction failed at leaf node (%s)\n", curr.c_str());
                PyErr_Print();
                return NULL;
            }

            int keep_going = PyObject_IsTrue(result);
            Py_DECREF(result);

            if (!keep_going) {
                fprintf(stderr, "[bfs] Operation requested to stop traversal at leaf node %s\n", curr.c_str());
                Py_RETURN_NONE;
            }
        }
    }

    fprintf(stderr, "[bfs] BFS traversal complete\n");
    Py_RETURN_NONE;
}
