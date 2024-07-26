#ifndef TREES_SELFBALANCINGBINARYTREE_HPP
#define TREES_SELFBALANCINGBINARYTREE_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <cstdlib>
#include "../../../utils/_backend/cpp/utils.hpp"
#include "../../../utils/_backend/cpp/TreeNode.hpp"
#include "../../../linear_data_structures/_backend/cpp/arrays/ArrayForTrees.hpp"
#include "../../../linear_data_structures/_backend/cpp/arrays/DynamicOneDimensionalArray.hpp"
#include "BinarySearchTree.hpp"

typedef struct {
    PyObject_HEAD
    BinarySearchTree* bst;
    ArrayForTrees* tree;
} SelfBalancingBinaryTree;

static void SelfBalancingBinaryTree_dealloc(SelfBalancingBinaryTree *self) {
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* SelfBalancingBinaryTree___new__(PyTypeObject* type, PyObject *args, PyObject *kwds) {
    SelfBalancingBinaryTree *self;
    self = reinterpret_cast<SelfBalancingBinaryTree*>(type->tp_alloc(type, 0));

    if (PyType_Ready(&BinarySearchTreeType) < 0) { // This has to be present to finalize a type object. This should be called on all type objects to finish their initialization.
        return NULL;
    }
    PyObject* p = BinarySearchTree___new__(&BinarySearchTreeType, args, kwds);
    self->bst = reinterpret_cast<BinarySearchTree*>(p);
    self->tree = reinterpret_cast<BinarySearchTree*>(p)->binary_tree->tree;

    return reinterpret_cast<PyObject*>(self);
}

static PyObject* SelfBalancingBinaryTree___str__(SelfBalancingBinaryTree *self) {
    return BinarySearchTree___str__(self->bst);
}

static PyObject* SelfBalancingBinaryTree_insert(SelfBalancingBinaryTree* self, PyObject* args) {
    return BinarySearchTree_insert(self->bst, args);
}

static PyObject* SelfBalancingBinaryTree_search(SelfBalancingBinaryTree* self, PyObject *args, PyObject *kwds) {
    return BinarySearchTree_search(self->bst, args, kwds);
}

static PyObject* SelfBalancingBinaryTree_delete(SelfBalancingBinaryTree* self, PyObject *args, PyObject *kwds) {
    return BinarySearchTree_delete(self->bst, args, kwds);
}

static PyObject* SelfBalancingBinaryTree_lower_bound(SelfBalancingBinaryTree* self, PyObject *args, PyObject *kwds) {
    return BinarySearchTree_lower_bound(self->bst, args, kwds);
}

static PyObject* SelfBalancingBinaryTree_upper_bound(SelfBalancingBinaryTree* self, PyObject *args, PyObject *kwds) {
    return BinarySearchTree_upper_bound(self->bst, args, kwds);
}

static PyObject* SelfBalancingBinaryTree__simple_path(SelfBalancingBinaryTree* self, PyObject *args) {
    return BinarySearchTree__simple_path(self->bst, args);
}

static PyObject* SelfBalancingBinaryTree__lca_1(SelfBalancingBinaryTree* self, PyObject *args) {
    return BinarySearchTree__simple_path(self->bst, args);
}

static PyObject* SelfBalancingBinaryTree__lca_2(SelfBalancingBinaryTree* self, PyObject *args) {
    return BinarySearchTree__simple_path(self->bst, args);
}

static PyObject* SelfBalancingBinaryTree_lowest_common_ancestor(SelfBalancingBinaryTree* self, PyObject *args) {
    return BinarySearchTree_lowest_common_ancestor(self->bst, args);
}

static PyObject* SelfBalancingBinaryTree_rank(SelfBalancingBinaryTree* self, PyObject *args) {
    return BinarySearchTree_rank(self->bst, args);
}

static PyObject* SelfBalancingBinaryTree_select(SelfBalancingBinaryTree* self, PyObject *args) {
    return BinarySearchTree_select(self->bst, args);
}

static PyObject* SelfBalancingBinaryTree__right_rotate(SelfBalancingBinaryTree* self, PyObject *args) {
    PyObject* j = PyObject_GetItem(args, PyZero);
    PyObject* k = PyObject_GetItem(args, PyOne);
    BinaryTree* bt = self->bst->binary_tree;
    PyObject* y = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)])->right;
    if (y != Py_None) {
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(y)])->parent = j;
    }
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)])->left = y;
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)])->parent = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)])->parent;
    if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)])->parent != Py_None) {
        if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)])->parent)])->left == j) {
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)])->parent)])->left = k;
        }
        else {
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)])->parent)])->right = k;
        }
    }
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)])->parent = k;
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)])->right = j;
    PyObject* kp = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)])->parent;
    if (kp == Py_None) {
        bt->root_idx = k;
    }
    Py_RETURN_NONE;
}

static PyObject* SelfBalancingBinaryTree__left_rotate(SelfBalancingBinaryTree* self, PyObject *args) {
    PyObject* j = PyObject_GetItem(args, PyZero);
    PyObject* k = PyObject_GetItem(args, PyOne);
    BinaryTree* bt = self->bst->binary_tree;
    PyObject* y = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)])->left;
    if (y != Py_None) {
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(y)])->parent = j;
    }
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)])->right = y;
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)])->parent = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)])->parent;
    if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)])->parent != Py_None) {
        if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)])->parent)])->left == j) {
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)])->parent)])->left = k;
        }
        else {
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)])->parent)])->right = k;
        }
    }
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)])->parent = k;
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)])->left = j;
    PyObject* kp = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)])->parent;
    if (kp == Py_None) {
        bt->root_idx = k;
    }
    Py_RETURN_NONE;
}

static PyObject* SelfBalancingBinaryTree__left_right_rotate(SelfBalancingBinaryTree* self, PyObject *args) {
    PyObject* j = PyObject_GetItem(args, PyZero);
    PyObject* k = PyObject_GetItem(args, PyOne);
    BinaryTree* bt = self->bst->binary_tree;

    PyObject* i = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)])->right;
    PyObject* v = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(i)])->left;
    PyObject* w = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(i)])->right;

    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)])->right = v;
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)])->left = w;

    if (v != Py_None) {
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(v)])->parent = k;
    }
    if (w != Py_None) {
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(w)])->parent = j;
    }

    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(i)])->left = k;
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(i)])->right = j;
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(i)])->parent = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)])->parent;

    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)])->parent = i;
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)])->parent = i;

    PyObject* ip = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(i)])->parent;
    if (ip != Py_None) {
        if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(ip)])->left == j) {
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(ip)])->left = i;
        }
        else {
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(ip)])->right = i;
        }
    }
    else {
        bt->root_idx = i;
    }
    Py_RETURN_NONE;
}

static PyObject* SelfBalancingBinaryTree__right_left_rotate(SelfBalancingBinaryTree* self, PyObject *args) {
    PyObject* j = PyObject_GetItem(args, PyZero);
    PyObject* k = PyObject_GetItem(args, PyOne);
    BinaryTree* bt = self->bst->binary_tree;

    PyObject* i = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)])->left;
    PyObject* v = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(i)])->left;
    PyObject* w = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(i)])->right;

    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)])->left = w;
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)])->right = v;

    if (v != Py_None) {
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(v)])->parent = j;
    }
    if (w != Py_None) {
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(w)])->parent = k;
    }

    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(i)])->right = k;
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(i)])->left = j;
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(i)])->parent = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)])->parent;

    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)])->parent = i;
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)])->parent = i;

    PyObject* ip = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(i)])->parent;
    if (ip != Py_None) {
        if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(ip)])->left == j) {
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(ip)])->left = i;
        }
        else {
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(ip)])->right = i;
        }
    }
    else {
        bt->root_idx = i;
    }
    Py_RETURN_NONE;
}

static PyObject* SelfBalancingBinaryTree_root_idx(SelfBalancingBinaryTree *self, void *closure) {
    return self->bst->binary_tree->root_idx;
}


static struct PyMethodDef SelfBalancingBinaryTree_PyMethodDef[] = {
    {"insert", (PyCFunction) SelfBalancingBinaryTree_insert, METH_VARARGS | METH_KEYWORDS, NULL},
    {"delete", (PyCFunction) SelfBalancingBinaryTree_delete, METH_VARARGS | METH_KEYWORDS, NULL},
    {"search", (PyCFunction) SelfBalancingBinaryTree_search, METH_VARARGS | METH_KEYWORDS, NULL},
    {"lower_bound", (PyCFunction) SelfBalancingBinaryTree_lower_bound, METH_VARARGS | METH_KEYWORDS, NULL},
    {"upper_bound", (PyCFunction) SelfBalancingBinaryTree_upper_bound, METH_VARARGS | METH_KEYWORDS, NULL},
    {"_simple_path", (PyCFunction) SelfBalancingBinaryTree__simple_path, METH_VARARGS, NULL},
    {"_lca_1", (PyCFunction) SelfBalancingBinaryTree__lca_1, METH_VARARGS, NULL},
    {"_lca_2", (PyCFunction) SelfBalancingBinaryTree__lca_2, METH_VARARGS, NULL},
    {"lowest_common_ancestor", (PyCFunction) SelfBalancingBinaryTree_lowest_common_ancestor, METH_VARARGS, NULL},
    {"rank", (PyCFunction) SelfBalancingBinaryTree_rank, METH_VARARGS, NULL},
    {"select", (PyCFunction) SelfBalancingBinaryTree_select, METH_VARARGS, NULL},
    {"_right_rotate", (PyCFunction) SelfBalancingBinaryTree__right_rotate, METH_VARARGS, NULL},
    {"_left_rotate", (PyCFunction) SelfBalancingBinaryTree__left_rotate, METH_VARARGS, NULL},
    {"_left_right_rotate", (PyCFunction) SelfBalancingBinaryTree__left_right_rotate, METH_VARARGS, NULL},
    {"_right_left_rotate", (PyCFunction) SelfBalancingBinaryTree__right_left_rotate, METH_VARARGS, NULL},
    {NULL}
};

static PyGetSetDef SelfBalancingBinaryTree_GetterSetters[] = {
    {"root_idx", (getter) SelfBalancingBinaryTree_root_idx, NULL, "returns the index of the tree's root", NULL},
    {NULL}  /* Sentinel */
};

static PyMemberDef SelfBalancingBinaryTree_PyMemberDef[] = {
    {"tree", T_OBJECT_EX, offsetof(SelfBalancingBinaryTree, tree), 0, "tree"},
    {NULL}  /* Sentinel */
};


static PyTypeObject SelfBalancingBinaryTreeType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "SelfBalancingBinaryTree",
    /* tp_basicsize */ sizeof(SelfBalancingBinaryTree),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor) SelfBalancingBinaryTree_dealloc,
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
    /* tp_str */ (reprfunc) SelfBalancingBinaryTree___str__,
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
    /* tp_methods */ SelfBalancingBinaryTree_PyMethodDef,
    /* tp_members */ SelfBalancingBinaryTree_PyMemberDef,
    /* tp_getset */ SelfBalancingBinaryTree_GetterSetters,
    /* tp_base */ &BinarySearchTreeType,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ SelfBalancingBinaryTree___new__,
};

#endif
