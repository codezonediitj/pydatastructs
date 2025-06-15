#include <Python.h>
#include "Algorithms.hpp"

static PyTypeObject* get_adjacency_list_graph_type() {
    static PyTypeObject* cached_type = nullptr;

    if (cached_type != nullptr) return cached_type;

    PyObject* graph_mod = PyImport_ImportModule("pydatastructs.graphs._backend.cpp._graph");
    if (!graph_mod) {
        PyErr_SetString(PyExc_ImportError, "[algorithms] Failed to import _graph module");
        return nullptr;
    }

    PyObject* type_obj = PyObject_GetAttrString(graph_mod, "AdjacencyListGraph");
    Py_DECREF(graph_mod);

    if (!type_obj || !PyType_Check(type_obj)) {
        Py_XDECREF(type_obj);
        PyErr_SetString(PyExc_TypeError, "[algorithms] AdjacencyListGraph is not a type object");
        return nullptr;
    }

    cached_type = reinterpret_cast<PyTypeObject*>(type_obj);
    return cached_type;
}

extern PyTypeObject* get_adjacency_list_graph_type();

static PyMethodDef AlgorithmsMethods[] = {
    {"bfs_adjacency_list", (PyCFunction)bfs_adjacency_list, METH_VARARGS | METH_KEYWORDS, "Run BFS with callback"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef algorithms_module = {
    PyModuleDef_HEAD_INIT,
    "_algorithms", NULL, -1, AlgorithmsMethods
};

PyMODINIT_FUNC PyInit__algorithms(void) {
    PyObject* graph_mod = PyImport_ImportModule("pydatastructs.graphs._backend.cpp._graph");
    if (!graph_mod) return nullptr;
    Py_DECREF(graph_mod);

    return PyModule_Create(&algorithms_module);
}
