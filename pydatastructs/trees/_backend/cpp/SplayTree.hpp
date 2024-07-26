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
#include "BinaryTreeTraversal.hpp"
#include "BinarySearchTree.hpp"
#include "SelfBalancingBinaryTree.hpp"

typedef struct {
    PyObject_HEAD
    SelfBalancingBinaryTree* sbbt;
    ArrayForTrees* tree;
    PyTypeObject* type;
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
    self->type = type;

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
    if (e == Py_None) {
        Py_RETURN_NONE;
    }
    SplayTree_splay(self, Py_BuildValue("(OO)", e, p));
    PyObject* status = SelfBalancingBinaryTree_delete(self->sbbt, Py_BuildValue("(O)", x), PyDict_New());

    return status;
}

static PyObject* SplayTree_join(SplayTree *self, PyObject* args) {
    SplayTree* other = reinterpret_cast<SplayTree*>(PyObject_GetItem(args, PyZero));
    BinaryTree* bt = self->sbbt->bst->binary_tree;
    BinaryTree* obt = other->sbbt->bst->binary_tree;

    PyObject* maxm = bt->root_idx;
    while (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(maxm)])->right != Py_None) {
        maxm = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(maxm)])->right;
    }
    PyObject* minm = obt->root_idx;
    while (reinterpret_cast<TreeNode*>(obt->tree->_one_dimensional_array->_data[PyLong_AsLong(minm)])->left != Py_None) {
        minm = reinterpret_cast<TreeNode*>(obt->tree->_one_dimensional_array->_data[PyLong_AsLong(minm)])->left;
    }

    if (!PyCallable_Check(bt->comparator)) {
        PyErr_SetString(PyExc_ValueError, "comparator should be callable");
        return NULL;
    }
    PyObject* arguments = Py_BuildValue("(OO)", reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(maxm)])->key, reinterpret_cast<TreeNode*>(obt->tree->_one_dimensional_array->_data[PyLong_AsLong(minm)])->key);
    PyObject* cres = PyObject_CallObject(bt->comparator, arguments);
    Py_DECREF(arguments);
    if (!PyLong_Check(cres)) {
        PyErr_SetString(PyExc_TypeError, "bad return type from comparator");
        return NULL;
    }
    long long comp = PyLong_AsLongLong(cres);
    if (comp == 0) {
        PyErr_SetString(PyExc_ValueError, "Elements of existing Splay Tree aren't less than that of the new Splay tree.");
        return NULL;
    }

    SplayTree_splay(self, Py_BuildValue("(OO)", maxm, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(maxm)])->parent));
    long idx_update = bt->tree->_one_dimensional_array->_size;
    long n = obt->tree->_one_dimensional_array->_size;
    for (int i=0; i<n; i++) {
        PyObject* node = obt->tree->_one_dimensional_array->_data[i];
        if (node != Py_None) {
            TreeNode* treenode = reinterpret_cast<TreeNode*>(node);
            if (PyType_Ready(&TreeNodeType) < 0) { // This has to be present to finalize a type object. This should be called on all type objects to finish their initialization.
                return NULL;
            }
            TreeNode* node_copy = reinterpret_cast<TreeNode*>(TreeNode___new__(&TreeNodeType, Py_BuildValue("(OO)", treenode->key, treenode->data), PyDict_New()));
            if (treenode->left != Py_None) {
                node_copy->left = PyLong_FromLong(PyLong_AsLong(treenode->left) + idx_update);
            }
            if (treenode->right != Py_None) {
                node_copy->right = PyLong_FromLong(PyLong_AsLong(treenode->right) + idx_update);
            }
            ArrayForTrees_append(bt->tree, Py_BuildValue("(O)", node_copy));
        }
        else {
            ArrayForTrees_append(bt->tree, Py_BuildValue("(O)", node));
        }
    }
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->right = PyLong_FromLong(PyLong_AsLong(obt->root_idx) + idx_update);

    Py_RETURN_NONE;
}

static PyObject* SplayTree__pre_order(SplayTree* self, PyObject *args) {
    long node = PyLong_AsLong(PyObject_GetItem(args, PyZero));
    PyObject* visit = PyList_New(0);
    ArrayForTrees* tree = self->sbbt->bst->binary_tree->tree;
    long size = self->sbbt->bst->binary_tree->size;
    std::stack<long> s;
    s.push(node);

    while (!s.empty()) {
        node = s.top();
        s.pop();
        TreeNode* curr_node = reinterpret_cast<TreeNode*>(tree->_one_dimensional_array->_data[node]);
        PyList_Append(visit, reinterpret_cast<PyObject*>(curr_node));
        if (curr_node->right != Py_None) {
            s.push(PyLong_AsLong(curr_node->right));
        }
        if (curr_node->left != Py_None) {
            s.push(PyLong_AsLong(curr_node->left));
        }
    }
    return visit;
}

static PyObject* SplayTree_split(SplayTree *self, PyObject* args) {
    PyObject* x = PyObject_GetItem(args, PyZero);
    BinaryTree* bt = self->sbbt->bst->binary_tree;

    PyObject* kwd_parent = PyDict_New();
    PyDict_SetItemString(kwd_parent, "parent", PyLong_FromLong(1));
    PyObject* tup = SelfBalancingBinaryTree_search(self->sbbt, Py_BuildValue("(O)", x), kwd_parent);
    PyObject* e = PyTuple_GetItem(tup, 0);
    PyObject* p = PyTuple_GetItem(tup, 1);
    if (e == Py_None) {
        Py_RETURN_NONE;
    }
    SplayTree_splay(self, Py_BuildValue("(OO)", e, p));
    if (PyType_Ready(self->type) < 0) { // This has to be present to finalize a type object. This should be called on all type objects to finish their initialization.
        return NULL;
    }

    Py_INCREF(Py_None);
    Py_INCREF(Py_None);
    if (!PyCallable_Check(bt->comparator)) {
            PyErr_SetString(PyExc_ValueError, "comparator should be callable");
            return NULL;
    }
    SplayTree* other = reinterpret_cast<SplayTree*>(SplayTree___new__(self->type, Py_BuildValue("(OOOO)", Py_None, Py_None, bt->comparator, PyZero), PyDict_New()));

    if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->right != Py_None) {
        PyObject* elements = SplayTree__pre_order(self, Py_BuildValue("(O)", reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->right));
        for (int i=0; i<PyList_Size(elements); i++) {
            SelfBalancingBinaryTree_insert(other->sbbt, Py_BuildValue("(OO)", reinterpret_cast<TreeNode*>( PyList_GetItem(elements, i))->key, reinterpret_cast<TreeNode*>( PyList_GetItem(elements, i))->data));
        }
        for (int j=PyList_Size(elements)-1; j>-1; j--) {
            tup = SelfBalancingBinaryTree_search(self->sbbt, Py_BuildValue("(O)", reinterpret_cast<TreeNode*>( PyList_GetItem(elements, j))->key), kwd_parent);
            e = PyTuple_GetItem(tup, 0);
            p = PyTuple_GetItem(tup, 1);
            bt->tree->_one_dimensional_array->_data[PyLong_AsLong(e)] = Py_None;
        }
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->right = Py_None;
    }

    return reinterpret_cast<PyObject*>(other);
}

static PyObject* SplayTree_root_idx(SplayTree *self, void *closure) {
    return self->sbbt->bst->binary_tree->root_idx;
}


static struct PyMethodDef SplayTree_PyMethodDef[] = {
    {"insert", (PyCFunction) SplayTree_insert, METH_VARARGS, NULL},
    {"delete", (PyCFunction) SplayTree_delete, METH_VARARGS, NULL},
    {"join", (PyCFunction) SplayTree_join, METH_VARARGS, NULL},
    {"split", (PyCFunction) SplayTree_split, METH_VARARGS, NULL},
    {NULL}
};

static PyGetSetDef SplayTree_GetterSetters[] = {
    {"root_idx", (getter) SplayTree_root_idx, NULL, "returns the index of the tree's root", NULL},
    {NULL}  /* Sentinel */
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
    /* tp_getset */ SplayTree_GetterSetters,
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
