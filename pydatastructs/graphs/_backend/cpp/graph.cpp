#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "AdjacencyList.hpp"
#include "AdjacencyMatrix.hpp"
#include "AdjacencyListGraphNode.hpp"
#include "AdjacencyMatrixGraphNode.hpp"
#include "AdjacencyListLLVM.hpp"
#include "graph_bindings.hpp"

#ifdef __cplusplus
extern "C" {
#endif

PyMODINIT_FUNC PyInit__graph(void);

#ifdef __cplusplus
}
#endif

static PyMethodDef module_methods[] = {
    {"initialize_llvm_backend", initialize_llvm_backend, METH_VARARGS,
     "Initialize LLVM backend with compiled function pointers"},
    {nullptr, nullptr, 0, nullptr}
};

static struct PyModuleDef graph_module = {
    PyModuleDef_HEAD_INIT,
    "_graph",
    "C++ module for graphs",
    -1,
    module_methods,
};

PyMODINIT_FUNC PyInit__graph(void) {
    PyObject* m;

    if (PyType_Ready(&AdjacencyListGraphType) < 0)
        return NULL;

    if (PyType_Ready(&AdjacencyListGraphNodeType) < 0)
        return NULL;

    if (PyType_Ready(&AdjacencyMatrixGraphType) < 0)
        return NULL;

    if (PyType_Ready(&AdjacencyMatrixGraphNodeType) < 0)
        return NULL;

    if (PyType_Ready(&AdjacencyListGraphLLVMType) < 0) {
        return nullptr;
    }
    m = PyModule_Create(&graph_module);
    if (m == NULL)
        return NULL;

    Py_INCREF(&AdjacencyListGraphType);
    if (PyModule_AddObject(m, "AdjacencyListGraph", (PyObject*)&AdjacencyListGraphType) < 0) {
        Py_DECREF(&AdjacencyListGraphType);
        Py_DECREF(m);
        return NULL;
    }

    Py_INCREF(&AdjacencyListGraphNodeType);
    if (PyModule_AddObject(m, "AdjacencyListGraphNode", (PyObject*)&AdjacencyListGraphNodeType) < 0) {
        Py_DECREF(&AdjacencyListGraphNodeType);
        Py_DECREF(m);
        return NULL;
    }

    Py_INCREF(&AdjacencyMatrixGraphType);
    if (PyModule_AddObject(m, "AdjacencyMatrixGraph", (PyObject*)&AdjacencyMatrixGraphType) < 0) {
        Py_DECREF(&AdjacencyMatrixGraphType);
        Py_DECREF(m);
        return NULL;
    }

    Py_INCREF(&AdjacencyListGraphLLVMType);
    if (PyModule_AddObject(m, "AdjacencyListGraphLLVM", (PyObject*)&AdjacencyListGraphLLVMType) < 0) {
        Py_DECREF(&AdjacencyListGraphLLVMType);
        Py_DECREF(m);
        return nullptr;
    }

    return m;
}
