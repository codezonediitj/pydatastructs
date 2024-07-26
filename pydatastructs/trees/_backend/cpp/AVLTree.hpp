#ifndef TREES_AVLTREE_HPP
#define TREES_AVLTREE_HPP

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
} AVLTree;

static void AVLTree_dealloc(AVLTree *self) {
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* AVLTree___new__(PyTypeObject* type, PyObject *args, PyObject *kwds) {
    AVLTree *self;
    self = reinterpret_cast<AVLTree*>(type->tp_alloc(type, 0));

    if (PyType_Ready(&SelfBalancingBinaryTreeType) < 0) { // This has to be present to finalize a type object. This should be called on all type objects to finish their initialization.
        return NULL;
    }
    PyObject* p = SelfBalancingBinaryTree___new__(&SelfBalancingBinaryTreeType, args, kwds);
    self->sbbt = reinterpret_cast<SelfBalancingBinaryTree*>(p);
    self->tree = self->sbbt->bst->binary_tree->tree;

    return reinterpret_cast<PyObject*>(self);
}

static PyObject* AVLTree___str__(AVLTree *self) {
    return BinarySearchTree___str__(self->sbbt->bst);
}

static PyObject* AVLTree_set_tree(AVLTree* self, PyObject *args) {
    ArrayForTrees* arr = reinterpret_cast<ArrayForTrees*>(PyObject_GetItem(args, PyZero));
    self->sbbt->bst->binary_tree->tree = arr;
    self->tree = self->sbbt->bst->binary_tree->tree;
    Py_RETURN_NONE;
}

static PyObject* AVLTree_search(AVLTree* self, PyObject *args, PyObject *kwds) {
    return BinarySearchTree_search(self->sbbt->bst, args, kwds);
}

static long AVLTree_left_height(AVLTree* self, PyObject *args) {
    TreeNode* node = reinterpret_cast<TreeNode*>(PyObject_GetItem(args, PyZero));
    if (node->left != Py_None) {
        BinaryTree* bt = self->sbbt->bst->binary_tree;
        return reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node->left)])->height;
    }
    else {
        return (-1);
    }
}

static long AVLTree_right_height(AVLTree* self, PyObject *args) {
    TreeNode* node = reinterpret_cast<TreeNode*>(PyObject_GetItem(args, PyZero));
    if (node->right != Py_None) {
        BinaryTree* bt = self->sbbt->bst->binary_tree;
        return reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node->right)])->height;
    }
    else {
        return -1;
    }
}

static PyObject* AVLTree_balance_factor(AVLTree* self, PyObject *args) {
    TreeNode* node = reinterpret_cast<TreeNode*>(PyObject_GetItem(args, PyZero));
    return PyLong_FromLong(AVLTree_right_height(self, Py_BuildValue("(O)", node)) - AVLTree_left_height(self, Py_BuildValue("(O)", node)));
}

static PyObject* AVLTree__right_rotate(AVLTree* self, PyObject *args) {
    PyObject* j = PyObject_GetItem(args, PyZero);
    PyObject* k = PyObject_GetItem(args, PyOne);
    BinaryTree* bt = self->sbbt->bst->binary_tree;
    SelfBalancingBinaryTree__right_rotate(self->sbbt, Py_BuildValue("(OO)", j, k));

    long lh = AVLTree_left_height(self, Py_BuildValue("(O)", bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)]));
    long rh = AVLTree_right_height(self, Py_BuildValue("(O)", bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)]));
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)])->height = std::max(lh, rh) + 1;

    if (bt->is_order_statistic == true) {
        long ls = BinarySearchTree_left_size(self->sbbt->bst, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)]));
        long rs = BinarySearchTree_right_size(self->sbbt->bst, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)]));
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)])->size = ls + rs + 1;
    }

    Py_RETURN_NONE;
}

static PyObject* AVLTree__left_right_rotate(AVLTree* self, PyObject *args) {
    PyObject* j = PyObject_GetItem(args, PyZero);
    PyObject* k = PyObject_GetItem(args, PyOne);
    BinaryTree* bt = self->sbbt->bst->binary_tree;
    SelfBalancingBinaryTree__left_right_rotate(self->sbbt, Py_BuildValue("(OO)", j, k));

    long lh = AVLTree_left_height(self, Py_BuildValue("(O)", bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)]));
    long rh = AVLTree_right_height(self, Py_BuildValue("(O)", bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)]));
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)])->height = std::max(lh, rh) + 1;

    lh = AVLTree_left_height(self, Py_BuildValue("(O)", bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)]));
    rh = AVLTree_right_height(self, Py_BuildValue("(O)", bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)]));
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)])->height = std::max(lh, rh) + 1;

    if (bt->is_order_statistic == true) {
        long ls = BinarySearchTree_left_size(self->sbbt->bst, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)]));
        long rs = BinarySearchTree_right_size(self->sbbt->bst, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)]));
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)])->size = ls + rs + 1;

        ls = BinarySearchTree_left_size(self->sbbt->bst, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)]));
        rs = BinarySearchTree_right_size(self->sbbt->bst, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)]));
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)])->size = ls + rs + 1;
    }

    Py_RETURN_NONE;
}

static PyObject* AVLTree__right_left_rotate(AVLTree* self, PyObject *args) {
    PyObject* j = PyObject_GetItem(args, PyZero);
    PyObject* k = PyObject_GetItem(args, PyOne);
    BinaryTree* bt = self->sbbt->bst->binary_tree;
    SelfBalancingBinaryTree__right_left_rotate(self->sbbt, Py_BuildValue("(OO)", j, k));

    long lh = AVLTree_left_height(self, Py_BuildValue("(O)", bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)]));
    long rh = AVLTree_right_height(self, Py_BuildValue("(O)", bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)]));
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)])->height = std::max(lh, rh) + 1;

    lh = AVLTree_left_height(self, Py_BuildValue("(O)", bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)]));
    rh = AVLTree_right_height(self, Py_BuildValue("(O)", bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)]));
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)])->height = std::max(lh, rh) + 1;

    if (bt->is_order_statistic == true) {
        long ls = BinarySearchTree_left_size(self->sbbt->bst, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)]));
        long rs = BinarySearchTree_right_size(self->sbbt->bst, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)]));
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)])->size = ls + rs + 1;

        ls = BinarySearchTree_left_size(self->sbbt->bst, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)]));
        rs = BinarySearchTree_right_size(self->sbbt->bst, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)]));
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)])->size = ls + rs + 1;
    }

    Py_RETURN_NONE;
}

static PyObject* AVLTree__left_rotate(AVLTree* self, PyObject *args) {
    PyObject* j = PyObject_GetItem(args, PyZero);
    PyObject* k = PyObject_GetItem(args, PyOne);
    BinaryTree* bt = self->sbbt->bst->binary_tree;
    SelfBalancingBinaryTree__left_rotate(self->sbbt, Py_BuildValue("(OO)", j, k));

    long lh = AVLTree_left_height(self, Py_BuildValue("(O)", bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)]));
    long rh = AVLTree_right_height(self, Py_BuildValue("(O)", bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)]));
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)])->height = std::max(lh, rh) + 1;

    lh = AVLTree_left_height(self, Py_BuildValue("(O)", bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)]));
    rh = AVLTree_right_height(self, Py_BuildValue("(O)", bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)]));
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(k)])->height = std::max(lh, rh) + 1;

    if (bt->is_order_statistic == true) {
        long ls = BinarySearchTree_left_size(self->sbbt->bst, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)]));
        long rs = BinarySearchTree_right_size(self->sbbt->bst, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)]));
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(j)])->size = ls + rs + 1;
    }

    Py_RETURN_NONE;
}

static PyObject* AVLTree__balance_insertion(AVLTree* self, PyObject *args) {
    PyObject* curr = PyObject_GetItem(args, PyZero);
    PyObject* last = PyObject_GetItem(args, PyOne);
    BinaryTree* bt = self->sbbt->bst->binary_tree;

    PyObject* walk = last;
    std::queue<PyObject*> path;
    path.push(curr);
    path.push(last);

    while (walk != Py_None) {
        long lh = AVLTree_left_height(self, Py_BuildValue("(O)", bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)]));
        long rh = AVLTree_right_height(self, Py_BuildValue("(O)", bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)]));
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->height = std::max(lh, rh) + 1;

        if (bt->is_order_statistic == true) {
            long ls = BinarySearchTree_left_size(self->sbbt->bst, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)]));
            long rs = BinarySearchTree_right_size(self->sbbt->bst, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)]));
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->size = ls + rs + 1;
        }

        last = path.front();
        path.pop();
        PyObject*  last2last = path.front();
        path.pop();
        long bf = PyLong_AsLong(AVLTree_balance_factor(self, Py_BuildValue("(O)", bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])));
        if (bf != 1 && bf != 0 && bf != -1) {
            PyObject* l = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->left;
            if (l != Py_None && l == last && reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(l)])->left == last2last) {
                AVLTree__right_rotate(self, Py_BuildValue("(OO)", walk, last));
            }

            PyObject* r = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->right;
            if (r != Py_None && r == last && reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(r)])->right == last2last) {
                AVLTree__left_rotate(self, Py_BuildValue("(OO)", walk, last));
            }

            if (l != Py_None && l == last && reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(l)])->right == last2last) {
                AVLTree__left_right_rotate(self, Py_BuildValue("(OO)", walk, last));
            }

            if (r != Py_None && r == last && reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(r)])->left == last2last) {
                AVLTree__right_left_rotate(self, Py_BuildValue("(OO)", walk, last));
            }
        }
        path.push(walk);
        path.push(last);
        walk = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->parent;
    }

    Py_RETURN_NONE;
}

static PyObject* AVLTree_insert(AVLTree* self, PyObject *args) {
    Py_INCREF(Py_None);
    PyObject* key = Py_None;
    Py_INCREF(Py_None);
    PyObject* data = Py_None;
    if (!PyArg_ParseTuple(args, "O|O", &key, &data)) { // data is optional
        return NULL;
    }
    SelfBalancingBinaryTree_insert(self->sbbt, Py_BuildValue("(OO)", key, data));
    BinaryTree* bt = self->sbbt->bst->binary_tree;
    long s = bt->size - 1;
    AVLTree__balance_insertion(self, Py_BuildValue("(OO)", PyLong_FromLong(s), reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[s])->parent));

    Py_RETURN_NONE;
}

static PyObject* AVLTree_rank(AVLTree* self, PyObject *args) {
    return BinarySearchTree_rank(self->sbbt->bst, args);
}

static PyObject* AVLTree_select(AVLTree* self, PyObject *args) {
    return BinarySearchTree_select(self->sbbt->bst, args);
}

static PyObject* AVLTree__balance_delete(AVLTree* self, PyObject *args) {
    PyObject* start_idx = PyObject_GetItem(args, PyZero);
    PyObject* key = PyObject_GetItem(args, PyOne);
    BinaryTree* bt = self->sbbt->bst->binary_tree;

    PyObject* walk = start_idx;
    while (walk != Py_None) {
        long lh = AVLTree_left_height(self, Py_BuildValue("(O)", bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)]));
        long rh = AVLTree_right_height(self, Py_BuildValue("(O)", bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)]));
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->height = std::max(lh, rh) + 1;

        if (bt->is_order_statistic == true) {
            long ls = BinarySearchTree_left_size(self->sbbt->bst, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)]));
            long rs = BinarySearchTree_right_size(self->sbbt->bst, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)]));
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->size = ls + rs + 1;
        }

        long bf = PyLong_AsLong(AVLTree_balance_factor(self, Py_BuildValue("(O)", bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])));
        if (bf != 1 && bf != 0 && bf != -1) {
            if (bf < 0) {
                PyObject* b = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->left;
                if (PyLong_AsLong(AVLTree_balance_factor(self, Py_BuildValue("(O)", bt->tree->_one_dimensional_array->_data[PyLong_AsLong(b)]))) <= 0) {
                    AVLTree__right_rotate(self, Py_BuildValue("(OO)", walk, b));
                }
                else {
                    AVLTree__left_right_rotate(self, Py_BuildValue("(OO)", walk, b));
                }
            }
            else {
                PyObject* b = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->right;
                if (PyLong_AsLong(AVLTree_balance_factor(self, Py_BuildValue("(O)", bt->tree->_one_dimensional_array->_data[PyLong_AsLong(b)]))) >= 0) {
                    AVLTree__left_rotate(self, Py_BuildValue("(OO)", walk, b));
                }
                else {
                    AVLTree__right_left_rotate(self, Py_BuildValue("(OO)", walk, b));
                }
            }
        }
        walk = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->parent;
    }

    Py_RETURN_NONE;
}

static PyObject* AVLTree_delete(AVLTree* self, PyObject *args, PyObject *kwds) {
    PyObject* key = PyObject_GetItem(args, PyZero);

    PyObject* kwd_bal = PyDict_New();
    PyDict_SetItemString(kwd_bal, "balancing_info", PyLong_FromLong(1));
    PyObject* a = SelfBalancingBinaryTree_delete(self->sbbt, Py_BuildValue("(O)", key), kwd_bal);
    AVLTree__balance_delete(self, Py_BuildValue("(OO)", a, key));

    Py_RETURN_TRUE;
}

static PyObject* AVLTree_root_idx(AVLTree *self, void *closure) {
    return self->sbbt->bst->binary_tree->root_idx;
}


static struct PyMethodDef AVLTree_PyMethodDef[] = {
    {"search", (PyCFunction) AVLTree_search, METH_VARARGS | METH_KEYWORDS, NULL},
    {"insert", (PyCFunction) AVLTree_insert, METH_VARARGS, NULL},
    {"delete", (PyCFunction) AVLTree_delete, METH_VARARGS, NULL},
    {"set_tree", (PyCFunction) AVLTree_set_tree, METH_VARARGS, NULL},
    {"balance_factor", (PyCFunction) AVLTree_balance_factor, METH_VARARGS, NULL},
    {"rank", (PyCFunction) AVLTree_rank, METH_VARARGS, NULL},
    {"select", (PyCFunction) AVLTree_select, METH_VARARGS, NULL},
    {"_left_right_rotate", (PyCFunction) AVLTree__left_right_rotate, METH_VARARGS, NULL},
    {"_right_left_rotate", (PyCFunction) AVLTree__right_left_rotate, METH_VARARGS, NULL},
    {"_left_rotate", (PyCFunction) AVLTree__left_rotate, METH_VARARGS, NULL},
    {"_right_rotate", (PyCFunction) AVLTree__right_rotate, METH_VARARGS, NULL},
    {NULL}
};

static PyGetSetDef AVLTree_GetterSetters[] = {
    {"root_idx", (getter) AVLTree_root_idx, NULL, "returns the index of the tree's root", NULL},
    {NULL}  /* Sentinel */
};

static PyMemberDef AVLTree_PyMemberDef[] = {
    {"tree", T_OBJECT_EX, offsetof(AVLTree, tree), 0, "tree"},
    {NULL}  /* Sentinel */
};


static PyTypeObject AVLTreeType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "AVLTree",
    /* tp_basicsize */ sizeof(AVLTree),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor) AVLTree_dealloc,
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
    /* tp_str */ (reprfunc) AVLTree___str__,
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
    /* tp_methods */ AVLTree_PyMethodDef,
    /* tp_members */ AVLTree_PyMemberDef,
    /* tp_getset */ AVLTree_GetterSetters,
    /* tp_base */ &SelfBalancingBinaryTreeType,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ AVLTree___new__,
};

#endif
