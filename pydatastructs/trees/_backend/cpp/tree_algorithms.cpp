#include <Python.h>
#include "trees.hpp" // Header file containing C++ implementations of wrapper functions of tree data structures

// Method definitions
static PyMethodDef trees_PyMethodDef[] = {
    {"binary_tree", (PyCFunction) binary_tree, METH_VARARGS, ""},
    // Add method definitions for other tree data structures over here.
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

// Sentinel info:
// The sentinel entry {NULL, NULL, 0, NULL} is used to indicate the end of the method definition array.
// When the Python interpreter processes this array, it stops iterating over the array when it encounters this sentinel entry.

// Module structure
static struct PyModuleDef trees_module = {
    PyModuleDef_HEAD_INIT,
    "_trees",
    NULL,
    -1,
    trees_PyMethodDef
};

// Module initialization function
PyMODINIT_FUNC PyInit__trees(void) {
    PyObject *module;
    module = PyModule_Create(&trees_module);
    if (module == NULL)
        return NULL;
    return module;
}
