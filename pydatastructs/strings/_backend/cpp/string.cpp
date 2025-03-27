#include <Python.h>
#include "algorithms/algorithms.hpp"
#include "trie/trie.hpp"
#include "utils/_backend/cpp/string.hpp"

// Python wrapper for KMP algorithm
static PyObject* py_kmp_search(PyObject* self, PyObject* args) {
    PyObject *text_obj, *query_obj;
    if (!PyArg_ParseTuple(args, "OO", &text_obj, &query_obj)) {
        return NULL;
    }
    std::string text = pyobj_to_string(text_obj);
    std::string query = pyobj_to_string(query_obj);
    std::vector<int> positions = kmp_search(text, query);
    return vector_to_pylist(positions);
}

// Python wrapper for Rabin-Karp algorithm
static PyObject* py_rabin_karp_search(PyObject* self, PyObject* args) {
    PyObject *text_obj, *query_obj;
    if (!PyArg_ParseTuple(args, "OO", &text_obj, &query_obj)) {
        return NULL;
    }
    std::string text = pyobj_to_string(text_obj);
    std::string query = pyobj_to_string(query_obj);
    std::vector<int> positions = rabin_karp_search(text, query);
    return vector_to_pylist(positions);
}

// Python wrapper for Boyer-Moore algorithm
static PyObject* py_boyer_moore_search(PyObject* self, PyObject* args) {
    PyObject *text_obj, *query_obj;
    if (!PyArg_ParseTuple(args, "OO", &text_obj, &query_obj)) {
        return NULL;
    }
    std::string text = pyobj_to_string(text_obj);
    std::string query = pyobj_to_string(query_obj);
    std::vector<int> positions = boyer_moore_search(text, query);
    return vector_to_pylist(positions);
}

// Python wrapper for Z-function algorithm
static PyObject* py_z_function_search(PyObject* self, PyObject* args) {
    PyObject *text_obj, *query_obj;
    if (!PyArg_ParseTuple(args, "OO", &text_obj, &query_obj)) {
        return NULL;
    }
    std::string text = pyobj_to_string(text_obj);
    std::string query = pyobj_to_string(query_obj);
    std::vector<int> positions = z_function_search(text, query);
    return vector_to_pylist(positions);
}

// Define the module's method table
static PyMethodDef StringsMethods[] = {
    {"kmp_search", py_kmp_search, METH_VARARGS, "Perform KMP search"},
    {"rabin_karp_search", py_rabin_karp_search, METH_VARARGS, "Perform Rabin-Karp search"},
    {"boyer_moore_search", py_boyer_moore_search, METH_VARARGS, "Perform Boyer-Moore search"},
    {"z_function_search", py_z_function_search, METH_VARARGS, "Perform Z-function search"},
    {NULL, NULL, 0, NULL}
};

// Define the module
static struct PyModuleDef stringsmodule = {
    PyModuleDef_HEAD_INIT,
    "_strings",
    NULL,
    -1,
    StringsMethods
};

// Module initialization function
PyMODINIT_FUNC PyInit__strings(void) {
    return PyModule_Create(&stringsmodule);
}