#include <Python.h>
#include "quick_sort.hpp"
#include "quadratic_time_sort.hpp"
#include "misc_algorithms.hpp"

static PyMethodDef algorithms_PyMethodDef[] = {
    {"quick_sort", (PyCFunction) quick_sort,
     METH_VARARGS | METH_KEYWORDS, ""},
    {"bubble_sort", (PyCFunction) bubble_sort,
     METH_VARARGS | METH_KEYWORDS, ""},
    {"selection_sort", (PyCFunction) selection_sort,
     METH_VARARGS | METH_KEYWORDS, ""},
    {"insertion_sort", (PyCFunction) insertion_sort,
     METH_VARARGS | METH_KEYWORDS, ""},
    {"is_ordered", (PyCFunction) is_ordered,
     METH_VARARGS | METH_KEYWORDS, ""},
    {"linear_search", (PyCFunction) linear_search,
     METH_VARARGS | METH_KEYWORDS, ""},
    {"binary_search", (PyCFunction) binary_search,
     METH_VARARGS | METH_KEYWORDS, ""},
    {"jump_search", (PyCFunction) jump_search,
     METH_VARARGS | METH_KEYWORDS, ""},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef algorithms_struct = {
    PyModuleDef_HEAD_INIT,
    "_algorithms",
    0,
    -1,
    algorithms_PyMethodDef
};

PyMODINIT_FUNC PyInit__algorithms(void) {
    Py_Initialize();
    PyObject *algorithms = PyModule_Create(&algorithms_struct);
    return algorithms;
}
