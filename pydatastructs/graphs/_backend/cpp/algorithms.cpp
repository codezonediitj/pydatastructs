#include <Python.h>
#include "bfs.hpp"

static PyMethodDef bfs_PyMethodDef[] = {
    {"bfs", (PyCFunction)bfs, METH_VARARGS | METH_KEYWORDS, "Breadth-First Search"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef bfs_module = {
    PyModuleDef_HEAD_INIT,
    "_bfs",
    "BFS algorithms module",
    -1,
    bfs_PyMethodDef
};

PyMODINIT_FUNC PyInit__bfs(void) {
    PyObject *module = PyModule_Create(&bfs_module);
    if (module == NULL) return NULL;
    return module;
}