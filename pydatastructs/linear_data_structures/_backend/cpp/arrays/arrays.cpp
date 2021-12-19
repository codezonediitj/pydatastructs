#include <Python.h>
#include "Array.hpp"
#include "OneDimensionalArray.hpp"

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
    PyModule_AddObject(arrays, "Array", reinterpret_cast<PyObject*>(&ArrayType));

    if (PyType_Ready(&OneDimensionalArrayType) < 0) {
        return NULL;
    }
    Py_INCREF(&OneDimensionalArrayType);
    PyModule_AddObject(arrays, "OneDimensionalArray", reinterpret_cast<PyObject*>(&OneDimensionalArrayType));

    return arrays;
}
