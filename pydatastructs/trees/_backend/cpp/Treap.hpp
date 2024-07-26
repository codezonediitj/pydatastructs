#ifndef TREES_TREAP_HPP
#define TREES_TREAP_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <cstdlib>
#include "../../../utils/_backend/cpp/utils.hpp"
#include "../../../utils/_backend/cpp/TreeNode.hpp"
#include "../../../linear_data_structures/_backend/cpp/arrays/ArrayForTrees.hpp"
#include "../../../linear_data_structures/_backend/cpp/arrays/DynamicOneDimensionalArray.hpp"
#include "BinarySearchTree.hpp"
#include "SelfBalancingBinaryTree.hpp"
#include "CartesianTree.hpp"

typedef struct {
    PyObject_HEAD
    CartesianTree* ct;
    ArrayForTrees* tree;
} Treap;

static void Treap_dealloc(Treap *self) {
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* Treap___new__(PyTypeObject* type, PyObject *args, PyObject *kwds) {
    Treap *self;
    self = reinterpret_cast<Treap*>(type->tp_alloc(type, 0));

    if (PyType_Ready(&CartesianTreeType) < 0) { // This has to be present to finalize a type object. This should be called on all type objects to finish their initialization.
        return NULL;
    }
    PyObject* p = CartesianTree___new__(&CartesianTreeType, args, kwds);
    self->ct = reinterpret_cast<CartesianTree*>(p);
    self->tree = reinterpret_cast<CartesianTree*>(p)->sbbt->bst->binary_tree->tree;

    return reinterpret_cast<PyObject*>(self);
}

static PyObject* Treap___str__(Treap *self) {
    return CartesianTree___str__(self->ct);
}

static PyObject* Treap_search(Treap* self, PyObject *args, PyObject *kwds) {
    return CartesianTree_search(self->ct, args, kwds);
}

static PyObject* Treap_delete(Treap* self, PyObject *args, PyObject *kwds) {
    return CartesianTree_delete(self->ct, args, kwds);
}

static PyObject* Treap_insert(Treap *self, PyObject* args) {
    Py_INCREF(Py_None);
    PyObject* key = Py_None;
    Py_INCREF(Py_None);
    PyObject* data = Py_None;
    if (!PyArg_ParseTuple(args, "O|O", &key, &data)) { // data is optional
        return NULL;
    }
    PyObject* priority = PyFloat_FromDouble(((double) rand() / (RAND_MAX)));

    return CartesianTree_insert(self->ct, Py_BuildValue("(OOO)", key, priority, data));
}

static PyObject* Treap_root_idx(Treap *self, void *closure) {
    return self->ct->sbbt->bst->binary_tree->root_idx;
}


static struct PyMethodDef Treap_PyMethodDef[] = {
    {"insert", (PyCFunction) Treap_insert, METH_VARARGS, NULL},
    {"delete", (PyCFunction) Treap_delete, METH_VARARGS | METH_KEYWORDS, NULL},
    {"search", (PyCFunction) Treap_search, METH_VARARGS | METH_KEYWORDS, NULL},
    {NULL} /* Sentinel */
};

static PyGetSetDef Treap_GetterSetters[] = {
    {"root_idx", (getter) Treap_root_idx, NULL, "returns the index of the tree's root", NULL},
    {NULL}  /* Sentinel */
};

static PyMemberDef Treap_PyMemberDef[] = {
    {"tree", T_OBJECT_EX, offsetof(Treap, tree), 0, "tree"},
    {NULL}  /* Sentinel */
};


static PyTypeObject TreapType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "Treap",
    /* tp_basicsize */ sizeof(Treap),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor) Treap_dealloc,
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
    /* tp_str */ (reprfunc) Treap___str__,
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
    /* tp_methods */ Treap_PyMethodDef,
    /* tp_members */ Treap_PyMemberDef,
    /* tp_getset */ Treap_GetterSetters,
    /* tp_base */ &CartesianTreeType,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ Treap___new__,
};

#endif
