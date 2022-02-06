#include <Python.h>
#include "quick_sort.hpp"

static PyMethodDef SpamMethods[] = {
    {"quick_sort", (PyCFunctionWithKeywords) quick_sort,
     METH_VARARGS | METH_KEYWORDS, ""},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef algorithms_struct = {
    PyModuleDef_HEAD_INIT,
    "_algorithms",
    0,
    -1,
    NULL,
};

PyMODINIT_FUNC PyInit__arrays(void) {
    Py_Initialize();
    PyObject *algorithms = PyModule_Create(&algorithms_struct);
    return algorithms;
}
