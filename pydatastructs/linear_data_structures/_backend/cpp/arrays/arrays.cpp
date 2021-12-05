#include <Python.h>
#include "Array.hpp"

static struct PyModuleDef arrays_struct = {
    PyModuleDef_HEAD_INIT,
    "_arrays",
    0,
    -1,
    NULL,
};

PyMODINIT_FUNC PyInit__arrays(void) {
    Py_Initialize();
    PyObject *arrays = PyModule_Create(&arrays_struct);

    if (PyType_Ready(&ArrayType) < 0) {
        return NULL;
    }
    Py_INCREF(&ArrayType);
    PyModule_AddObject(arrays, "Array", (PyObject*) &ArrayType);

    return arrays;
}
