#ifndef TREES_SPLAYTREE_HPP
#define TREES_SPLAYTREE_HPP

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

typedef struct {
    PyObject_HEAD
    SelfBalancingBinaryTree* sbbt;
    ArrayForTrees* tree;
} SplayTree;

static void SplayTree_dealloc(SplayTree *self) {
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* SplayTree___new__(PyTypeObject* type, PyObject *args, PyObject *kwds) {
    SplayTree *self;
    self = reinterpret_cast<SplayTree*>(type->tp_alloc(type, 0));

    if (PyType_Ready(&SelfBalancingBinaryTreeType) < 0) { // This has to be present to finalize a type object. This should be called on all type objects to finish their initialization.
        return NULL;
    }
    PyObject* p = SelfBalancingBinaryTree___new__(&SelfBalancingBinaryTreeType, args, kwds);
    self->sbbt = reinterpret_cast<SelfBalancingBinaryTree*>(p);
    self->tree = reinterpret_cast<SelfBalancingBinaryTree*>(p)->bst->binary_tree->tree;

    return reinterpret_cast<PyObject*>(self);
}

static PyObject* SplayTree___str__(SplayTree *self) {
    return BinarySearchTree___str__(self->sbbt->bst);
}

static PyObject* SplayTree__zig(SplayTree *self, PyObject* args) {
    PyObject* x = PyObject_GetItem(args, PyZero);
    PyObject* p = PyObject_GetItem(args, PyOne);
    BinaryTree* bt = self->sbbt->bst->binary_tree;

    if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(p)])->left == x) {
        SelfBalancingBinaryTree__right_rotate(self->sbbt, Py_BuildValue("(OO)", p, x));
    }
    else {
        SelfBalancingBinaryTree__left_rotate(self->sbbt, Py_BuildValue("(OO)", p, x));
    }

    Py_RETURN_NONE;
}

static PyObject* SplayTree__zig_zig(SplayTree *self, PyObject* args) {
    PyObject* x = PyObject_GetItem(args, PyZero);
    PyObject* p = PyObject_GetItem(args, PyOne);
    BinaryTree* bt = self->sbbt->bst->binary_tree;

    SelfBalancingBinaryTree__right_rotate(self->sbbt, Py_BuildValue("(OO)", reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(p)])->parent, p));
    SelfBalancingBinaryTree__right_rotate(self->sbbt, Py_BuildValue("(OO)", p, x));

    Py_RETURN_NONE;
}

static PyObject* SplayTree__zig_zag(SplayTree *self, PyObject* args) {
    PyObject* p = PyObject_GetItem(args, PyZero);
    BinaryTree* bt = self->sbbt->bst->binary_tree;

    SelfBalancingBinaryTree__left_right_rotate(self->sbbt, Py_BuildValue("(OO)", reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(p)])->parent, p));

    Py_RETURN_NONE;
}

static PyObject* SplayTree__zag_zag(SplayTree *self, PyObject* args) {
    PyObject* x = PyObject_GetItem(args, PyZero);
    PyObject* p = PyObject_GetItem(args, PyOne);
    BinaryTree* bt = self->sbbt->bst->binary_tree;

    SelfBalancingBinaryTree__left_rotate(self->sbbt, Py_BuildValue("(OO)", reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(p)])->parent, p));
    SelfBalancingBinaryTree__left_rotate(self->sbbt, Py_BuildValue("(OO)", p, x));

    Py_RETURN_NONE;
}

static PyObject* SplayTree__zag_zig(SplayTree *self, PyObject* args) {
    PyObject* p = PyObject_GetItem(args, PyZero);
    BinaryTree* bt = self->sbbt->bst->binary_tree;

    SelfBalancingBinaryTree__right_left_rotate(self->sbbt, Py_BuildValue("(OO)", reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(p)])->parent, p));

    Py_RETURN_NONE;
}

static PyObject* SplayTree_splay(SplayTree *self, PyObject* args) {
    PyObject* x = PyObject_GetItem(args, PyZero);
    PyObject* p = PyObject_GetItem(args, PyOne);
    BinaryTree* bt = self->sbbt->bst->binary_tree;

    while (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(x)])->parent != Py_None) {
        if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(p)])->parent == Py_None) {
            SplayTree__zig(self, Py_BuildValue("(OO)", x, p));
        }
        else if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(p)])->left == x && reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(p)])->parent)])->left == p) {
            SplayTree__zig_zig(self, Py_BuildValue("(OO)", x, p));
        }
        else if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(p)])->right == x && reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(p)])->parent)])->right == p) {
            SplayTree__zag_zag(self, Py_BuildValue("(OO)", x, p));
        }
        else if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(p)])->left == x && reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(p)])->parent)])->right == p) {
            SplayTree__zag_zig(self, Py_BuildValue("(O)", p));
        }
        else {
            SplayTree__zig_zag(self, Py_BuildValue("(O)", p));
        }
        p = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(x)])->parent;
    }

    Py_RETURN_NONE;
}

static PyObject* SplayTree_insert(SplayTree *self, PyObject* args) {
    PyObject* key = PyObject_GetItem(args, PyZero);
    PyObject* x = PyObject_GetItem(args, PyOne);
    BinaryTree* bt = self->sbbt->bst->binary_tree;

    SelfBalancingBinaryTree_insert(self->sbbt, args);
    PyObject* kwd_parent = PyDict_New();
    PyDict_SetItemString(kwd_parent, "parent", PyLong_FromLong(1));
    PyObject* tup = SelfBalancingBinaryTree_search(self->sbbt, Py_BuildValue("(O)", key), kwd_parent);
    PyObject* e = PyTuple_GetItem(tup, 0);
    PyObject* p = PyTuple_GetItem(tup, 1);
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[bt->size-1])->parent = p;
    SplayTree_splay(self, Py_BuildValue("(OO)", e, p));

    Py_RETURN_NONE;
}

static PyObject* SplayTree_delete(SplayTree *self, PyObject* args) {
    PyObject* x = PyObject_GetItem(args, PyZero);
    BinaryTree* bt = self->sbbt->bst->binary_tree;

    PyObject* kwd_parent = PyDict_New();
    PyDict_SetItemString(kwd_parent, "parent", PyLong_FromLong(1));
    PyObject* tup = SelfBalancingBinaryTree_search(self->sbbt, Py_BuildValue("(O)", x), kwd_parent);
    PyObject* e = PyTuple_GetItem(tup, 0);
    PyObject* p = PyTuple_GetItem(tup, 1);
    if (e == Py_None){
        Py_RETURN_NONE;
    }
    SplayTree_splay(self, Py_BuildValue("(OO)", e, p));
    PyObject* status = SelfBalancingBinaryTree_delete(self->sbbt, Py_BuildValue("(O)", x), PyDict_New());
    return status;
}


static struct PyMethodDef SplayTree_PyMethodDef[] = {
    {"insert", (PyCFunction) SplayTree_insert, METH_VARARGS, NULL},
    {"delete", (PyCFunction) SplayTree_delete, METH_VARARGS, NULL},
    {NULL}
};

static PyMemberDef SplayTree_PyMemberDef[] = {
    {"tree", T_OBJECT_EX, offsetof(SplayTree, tree), 0, "tree"},
    {NULL}  /* Sentinel */
};


static PyTypeObject SplayTreeType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "SplayTree",
    /* tp_basicsize */ sizeof(SplayTree),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor) SplayTree_dealloc,
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
    /* tp_str */ (reprfunc) SplayTree___str__,
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
    /* tp_methods */ SplayTree_PyMethodDef,
    /* tp_members */ SplayTree_PyMemberDef,
    /* tp_getset */ 0,
    /* tp_base */ &SelfBalancingBinaryTreeType,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ SplayTree___new__,
};

#endif
