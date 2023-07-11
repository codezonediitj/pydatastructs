#include <Python.h>
#include "quick_sort.hpp"
#include "bubble_sort.hpp"

static PyMethodDef algorithms_PyMethodDef[] = {
    {"quick_sort", (PyCFunction) quick_sort,
     METH_VARARGS | METH_KEYWORDS, ""},
    {"bubble_sort", (PyCFunction) bubble_sort,
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
