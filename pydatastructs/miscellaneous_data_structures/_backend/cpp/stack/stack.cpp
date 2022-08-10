#include <Python.h>
#include "ArrayStack.hpp"

static struct PyModuleDef stack_struct = {
    PyModuleDef_HEAD_INIT,
    "_stack",
    0,
    -1,
    NULL,
};

PyMODINIT_FUNC PyInit__stack(void) {
    Py_Initialize();
    PyObject *stack = PyModule_Create(&stack_struct);

    if (PyType_Ready(&ArrayStackType) < 0) {
        return NULL;
    }
    Py_INCREF(&ArrayStackType);
    PyModule_AddObject(stack, "ArrayStack", reinterpret_cast<PyObject*>(&ArrayStackType));

    if (PyType_Ready(&ArrayType) < 0) {
        return NULL;
    }
    Py_INCREF(&ArrayType);
    PyModule_AddObject(stack, "Array", reinterpret_cast<PyObject*>(&ArrayType));

    if (PyType_Ready(&OneDimensionalArrayType) < 0) {
        return NULL;
    }
    Py_INCREF(&OneDimensionalArrayType);
    PyModule_AddObject(stack, "OneDimensionalArray", reinterpret_cast<PyObject*>(&OneDimensionalArrayType));

    if (PyType_Ready(&DynamicArrayType) < 0) {
        return NULL;
    }
    Py_INCREF(&DynamicArrayType);
    PyModule_AddObject(stack, "DynamicArray", reinterpret_cast<PyObject*>(&DynamicArrayType));

    if (PyType_Ready(&DynamicOneDimensionalArrayType) < 0) {
        return NULL;
    }
    Py_INCREF(&DynamicOneDimensionalArrayType);
    PyModule_AddObject(stack, "DynamicOneDimensionalArray", reinterpret_cast<PyObject*>(&DynamicOneDimensionalArrayType));


    return stack;
}
