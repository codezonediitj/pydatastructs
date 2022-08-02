#include <Python.h>
#include "ArrayStack.hpp"

static struct PyModuleDef stack_struct = {
    PyModuleDef_HEAD_INIT,
    .m_name = "_stack",
    .m_doc = "Stack extension type",
    .m_size = -1,
};

PyMODINIT_FUNC PyInit__stack(void) {
    PyObject *stack;

    if (PyType_Ready(&ArrayStackType) < 0)
        return NULL;

    stack = PyModule_Create(&stack_struct);
    if (stack == NULL)
        return NULL;

    Py_INCREF(&ArrayStackType);
    if (PyModule_AddObject(stack, "ArrayStack", reinterpret_cast<PyObject*>(&ArrayStackType)) < 0){
        Py_DECREF(&ArrayStackType);
        Py_DECREF(stack);
        return NULL;
    };

    return stack;
}
