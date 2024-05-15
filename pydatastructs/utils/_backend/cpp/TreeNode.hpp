#ifndef UTILS_TREENODE_HPP
#define UTILS_TREENODE_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include "Node.hpp"

typedef struct {
    PyObject_HEAD
    long key;
    long data;
    PyObject* left; // can store None or a number
    PyObject* right; // can store None or a number
    bool is_root;
    long height;
    PyObject* parent;
    long size;
} TreeNode;

static void TreeNode_dealloc(TreeNode *self) {
    // left and right are long values, no need to dealloc for them
    // TreeNode_dealloc(reinterpret_cast<TreeNode*>(TreeNode->left));
    // TreeNode_dealloc(reinterpret_cast<TreeNode*>(TreeNode->right));
    // Check if other deallocs are needed using Py_XDECREF
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* TreeNode___new__(PyTypeObject* type, PyObject *args, PyObject *kwds) {
    TreeNode *self;
    self = reinterpret_cast<TreeNode*>(type->tp_alloc(type, 0));

    // Check what this is: (python code below:)
    // obj = Node.__new__(cls)

    // Assume that arguments are in the order below. Modify the code such that this is true.
    self->key = reinterpret_cast<long>(PyObject_GetItem(args, PyZero));
    self->data = reinterpret_cast<long>(PyObject_GetItem(args, PyOne));

    Py_INCREF(Py_None);
    self->left = Py_None;
    Py_INCREF(Py_None);
    self->right = Py_None;
    Py_INCREF(Py_None);
    self->parent = Py_None;
    self->height = 0;
    self->size = 1;
    self->is_root = false;

    return reinterpret_cast<PyObject*>(self);
}

static PyObject* TreeNode___str__(TreeNode *self) {
    PyObject* out = Py_BuildValue("(OllO)", self->left, self->key, self->data, self->right);
    Py_INCREF(out);
    return out;
}

static struct PyMemberDef TreeNode_PyMemberDef[] = {
    {"key", T_LONG, offsetof(TreeNode, key), 0, "TreeNode key"},
    {"data", T_LONG, offsetof(TreeNode, data), 0, "TreeNode data"},
    {"height", T_LONG, offsetof(TreeNode, height), 0, "TreeNode height"},
    {"size", T_LONG, offsetof(TreeNode, size), 0, "TreeNode size"},
    {"is_root", T_BOOL, offsetof(TreeNode, is_root), 0, "TreeNode is_root"},
    {"left", T_OBJECT, offsetof(TreeNode, left), 0, "TreeNode left"},
    {"right", T_OBJECT, offsetof(TreeNode, right), 0, "TreeNode right"},
    {"parent", T_OBJECT, offsetof(TreeNode, parent), 0, "TreeNode parent"},
    {NULL},
};

static PyTypeObject TreeNodeType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "TreeNode",
    /* tp_basicsize */ sizeof(TreeNode),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor) TreeNode_dealloc,
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
    /* tp_str */ (reprfunc) TreeNode___str__,
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
    /* tp_members */ TreeNode_PyMemberDef,
    /* tp_getset */ 0,
    /* tp_base */ &NodeType, // Class Node is the base class
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ TreeNode___new__,
};

#endif
