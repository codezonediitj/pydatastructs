#ifndef BFS_HPP
#define BFS_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <queue>
#include <unordered_map>

struct Graph {
    PyObject* adj_list;
};

static PyObject* bfs_impl(PyObject* graph, PyObject* start_vertex, PyObject* visited = NULL) {
    if (!PyDict_Check(graph)) {
        PyErr_SetString(PyExc_TypeError, "Graph must be a dictionary");
        return NULL;
    }

    std::queue<PyObject*> q;
    PyObject* visited_dict = visited ? visited : PyDict_New();

    q.push(start_vertex);
    PyDict_SetItem(visited_dict, start_vertex, Py_True);

    PyObject* result = PyList_New(0);

    while (!q.empty()) {
        PyObject* vertex = q.front();
        q.pop();

        PyList_Append(result, vertex);

        PyObject* neighbors = PyDict_GetItem(graph, vertex);
        if (neighbors && PyList_Check(neighbors)) {
            Py_ssize_t size = PyList_Size(neighbors);
            for (Py_ssize_t i = 0; i < size; i++) {
                PyObject* neighbor = PyList_GetItem(neighbors, i);
                if (!PyDict_Contains(visited_dict, neighbor)) {
                    q.push(neighbor);
                    PyDict_SetItem(visited_dict, neighbor, Py_True);
                }
            }
        }
    }

    if (!visited) Py_DECREF(visited_dict);
    return result;
}

static PyObject* bfs(PyObject* self, PyObject* args, PyObject* kwds) {
    PyObject *graph = NULL, *start_vertex = NULL;
    static char *kwlist[] = {"graph", "start_vertex", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "OO", kwlist, &graph, &start_vertex)) {
        return NULL;
    }

    PyObject* result = bfs_impl(graph, start_vertex);
    if (result == NULL) return NULL;
    Py_INCREF(result);
    return result;
}

#endif
