#include <Python.h>
#include "Array.hpp"
#include "OneDimensionalArray.hpp"
#include "DynamicArray.hpp"
#include "DynamicOneDimensionalArray.hpp"
#include "ArrayForTrees.hpp"

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

    if (PyType_Ready(&DynamicArrayType) < 0) {
        return NULL;
    }
    Py_INCREF(&DynamicArrayType);
    PyModule_AddObject(arrays, "DynamicArray", reinterpret_cast<PyObject*>(&DynamicArrayType));

    if (PyType_Ready(&DynamicOneDimensionalArrayType) < 0) {
        return NULL;
    }
    Py_INCREF(&DynamicOneDimensionalArrayType);
    PyModule_AddObject(arrays, "DynamicOneDimensionalArray", reinterpret_cast<PyObject*>(&DynamicOneDimensionalArrayType));

    if (PyType_Ready(&ArrayForTreesType) < 0) {
        return NULL;
    }
    Py_INCREF(&ArrayForTreesType);
    PyModule_AddObject(arrays, "ArrayForTrees", reinterpret_cast<PyObject*>(&ArrayForTreesType));

    return arrays;
}
