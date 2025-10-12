#include <Python.h>
#include "GraphNode.hpp"
#include "AdjacencyListGraphNode.hpp"
#include "AdjacencyMatrixGraphNode.hpp"
#include "GraphEdge.hpp"
#include "graph_bindings.hpp"

PyTypeObject GraphNodeType = {
        /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "GraphNode",
        /* tp_basicsize */ sizeof(GraphNode),
        /* tp_itemsize */ 0,
        /* tp_dealloc */ (destructor) GraphNode_dealloc,
        /* tp_print */ 0,
        /* tp_getattr */ 0,
        /* tp_setattr */ 0,
        /* tp_reserved */ 0,
        /* tp_repr */ 0,
        /* tp_as_number */ 0,
        /* tp_as_sequence */ 0,
        /* tp_as_mapping */ 0,
        /* tp_hash  */ 0,
        /* tp_call */ 0,
        /* tp_str */ (reprfunc) GraphNode_str,
        /* tp_getattro */ 0,
        /* tp_setattro */ 0,
        /* tp_as_buffer */ 0,
        /* tp_flags */ Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
        /* tp_doc */ 0,
        /* tp_traverse */ 0,
        /* tp_clear */ 0,
        /* tp_richcompare */ 0,
        /* tp_weaklistoffset */ 0,
        /* tp_iter */ 0,
        /* tp_iternext */ 0,
        /* tp_methods */ 0,
        /* tp_members */ GraphNode_PyMemberDef,
        /* tp_getset */ GraphNode_getsetters,
        /* tp_base */ &PyBaseObject_Type,
        /* tp_dict */ 0,
        /* tp_descr_get */ 0,
        /* tp_descr_set */ 0,
        /* tp_dictoffset */ 0,
        /* tp_init */ 0,
        /* tp_alloc */ 0,
        /* tp_new */ GraphNode_new,
};

PyTypeObject AdjacencyListGraphNodeType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "AdjacencyListGraphNode",
    /* tp_basicsize */ sizeof(AdjacencyListGraphNode),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor)AdjacencyListGraphNode_dealloc,
    /* tp_print */ 0,
    /* tp_getattr */ 0,
    /* tp_setattr */ 0,
    /* tp_reserved */ 0,
    /* tp_repr */ 0,
    /* tp_as_number */ 0,
    /* tp_as_sequence */ 0,
    /* tp_as_mapping */ 0,
    /* tp_hash */ 0,
    /* tp_call */ 0,
    /* tp_str */ (reprfunc)GraphNode_str,
    /* tp_getattro */ 0,
    /* tp_setattro */ 0,
    /* tp_as_buffer */ 0,
    /* tp_flags */ Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    /* tp_doc */ "Node Data Structure for an Adjacency List Graph",
    /* tp_traverse */ 0,
    /* tp_clear */ 0,
    /* tp_richcompare */ 0,
    /* tp_weaklistoffset */ 0,
    /* tp_iter */ 0,
    /* tp_iternext */ 0,
    /* tp_methods */ AdjacencyListGraphNode_methods,
    /* tp_members */ AdjacencyListGraphNode_PyMemberDef,
    /* tp_getset */ AdjacencyListGraphNode_getsetters,
    /* tp_base */ &GraphNodeType,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ AdjacencyListGraphNode_new,
};

PyTypeObject AdjacencyMatrixGraphNodeType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "AdjacencyMatrixGraphNode",
    /* tp_basicsize */ sizeof(AdjacencyMatrixGraphNode),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor)AdjacencyMatrixGraphNode_dealloc,
    /* tp_print */ 0,
    /* tp_getattr */ 0,
    /* tp_setattr */ 0,
    /* tp_reserved */ 0,
    /* tp_repr */ 0,
    /* tp_as_number */ 0,
    /* tp_as_sequence */ 0,
    /* tp_as_mapping */ 0,
    /* tp_hash */ 0,
    /* tp_call */ 0,
    /* tp_str */ 0,
    /* tp_getattro */ 0,
    /* tp_setattro */ 0,
    /* tp_as_buffer */ 0,
    /* tp_flags */ Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    /* tp_doc */ "Node Data Structure for an Adjacency Matrix Graph",
    /* tp_traverse */ 0,
    /* tp_clear */ 0,
    /* tp_richcompare */ 0,
    /* tp_weaklistoffset */ 0,
    /* tp_iter */ 0,
    /* tp_iternext */ 0,
    /* tp_methods */ 0,
    /* tp_members */ 0,
    /* tp_getset */ 0,
    /* tp_base */ &GraphNodeType,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ AdjacencyMatrixGraphNode_new,
};

PyTypeObject GraphEdgeType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "GraphEdge",
    /* tp_basicsize */ sizeof(GraphEdge),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor)GraphEdge_dealloc,
    /* tp_print */ 0,
    /* tp_getattr */ 0,
    /* tp_setattr */ 0,
    /* tp_reserved */ 0,
    /* tp_repr */ 0,
    /* tp_as_number */ 0,
    /* tp_as_sequence */ 0,
    /* tp_as_mapping */ 0,
    /* tp_hash */ 0,
    /* tp_call */ 0,
    /* tp_str */ (reprfunc)GraphEdge_str,
    /* tp_getattro */ 0,
    /* tp_setattro */ 0,
    /* tp_as_buffer */ 0,
    /* tp_flags */ Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    /* tp_doc */ "Data Structure for a Graph Edge",
    /* tp_traverse */ 0,
    /* tp_clear */ 0,
    /* tp_richcompare */ 0,
    /* tp_weaklistoffset */ 0,
    /* tp_iter */ 0,
    /* tp_iternext */ 0,
    /* tp_methods */ 0,
    /* tp_members */ 0,
    /* tp_getset */ GraphEdge_getsetters,
    /* tp_base */ 0,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ GraphEdge_new,
};


static struct PyModuleDef graph_utils_struct = {
    PyModuleDef_HEAD_INIT,
    "_graph_utils",
    0,
    -1,
    NULL,
};

PyMODINIT_FUNC PyInit__graph_utils(void) {
    Py_Initialize();
    PyObject *utils = PyModule_Create(&graph_utils_struct);

    if (PyType_Ready(&GraphNodeType) < 0) {
        return NULL;
    }
    Py_INCREF(&GraphNodeType);
    PyModule_AddObject(utils, "GraphNode", reinterpret_cast<PyObject*>(&GraphNodeType));

    if (PyType_Ready(&AdjacencyMatrixGraphNodeType) < 0) {
        return NULL;
    }
    Py_INCREF(&AdjacencyMatrixGraphNodeType);
    PyModule_AddObject(utils, "AdjacencyMatrixGraphNode", reinterpret_cast<PyObject*>(&AdjacencyMatrixGraphNodeType));

    if (PyType_Ready(&AdjacencyListGraphNodeType) < 0) {
        return NULL;
    }
    Py_INCREF(&AdjacencyListGraphNodeType);
    PyModule_AddObject(utils, "AdjacencyListGraphNode", reinterpret_cast<PyObject*>(&AdjacencyListGraphNodeType));

    if (PyType_Ready(&GraphEdgeType) < 0) {
        return NULL;
    }
    Py_INCREF(&GraphEdgeType);
    PyModule_AddObject(utils, "GraphEdge", reinterpret_cast<PyObject*>(&GraphEdgeType));

    return utils;
}
