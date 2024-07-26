#ifndef TREES_BINARYSEARCHTREE_HPP
#define TREES_BINARYSEARCHTREE_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <cstdlib>
#include <stack>
#include "../../../utils/_backend/cpp/utils.hpp"
#include "../../../utils/_backend/cpp/TreeNode.hpp"
#include "../../../linear_data_structures/_backend/cpp/arrays/ArrayForTrees.hpp"
#include "BinaryTree.hpp"

typedef struct {
    PyObject_HEAD
    BinaryTree* binary_tree;
    ArrayForTrees* tree;
} BinarySearchTree;

static void BinarySearchTree_dealloc(BinarySearchTree *self) {
    BinaryTree_dealloc(self->binary_tree);
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* BinarySearchTree___new__(PyTypeObject* type, PyObject *args, PyObject *kwds) {
    BinarySearchTree *self;
    self = reinterpret_cast<BinarySearchTree*>(type->tp_alloc(type, 0));

    if (PyType_Ready(&BinaryTreeType) < 0) { // This has to be present to finalize a type object. This should be called on all type objects to finish their initialization.
        return NULL;
    }
    PyObject* bt = BinaryTree___new__(&BinaryTreeType, args, kwds);
    self->binary_tree = reinterpret_cast<BinaryTree*>(bt);
    self->tree = reinterpret_cast<BinaryTree*>(bt)->tree;

    return reinterpret_cast<PyObject*>(self);
}

static PyObject* BinarySearchTree___str__(BinarySearchTree *self) {
    return BinaryTree___str__(self->binary_tree);
}

static long BinarySearchTree_left_size(BinarySearchTree* self, TreeNode* node) {
    if (node->left != Py_None) {
        TreeNode* n = reinterpret_cast<TreeNode*>(
            self->binary_tree->tree->_one_dimensional_array->_data[PyLong_AsLong(node->left)]
        );
        return n->size;
    } else {
        return 0;
    }
}

static long BinarySearchTree_right_size(BinarySearchTree* self, TreeNode* node) {
    if (node->right != Py_None) {
        TreeNode* n = reinterpret_cast<TreeNode*>(
            self->binary_tree->tree->_one_dimensional_array->_data[PyLong_AsLong(node->right)]
        );
        return n->size;
    } else {
        return 0;
    }
}

static PyObject* BinarySearchTree__update_size(BinarySearchTree* self, PyObject *args) {
    PyObject *start_idx = PyObject_GetItem(args, PyZero);
    if (self->binary_tree->is_order_statistic) {
        PyObject* walk = start_idx;
        while (walk!=Py_None) {
            TreeNode* node = reinterpret_cast<TreeNode*>(self->binary_tree->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)]);
            node->size = BinarySearchTree_left_size(self, node) + BinarySearchTree_right_size(self, node) + 1;
            walk = node->parent;
        }
    }
    Py_RETURN_NONE;
}

static PyObject* BinarySearchTree_search(BinarySearchTree* self, PyObject* args, PyObject *kwds) {
    Py_INCREF(Py_None);
    PyObject* ret_parent = Py_None;
    PyObject* key;
    static char* keywords[] = {"key","parent", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O|O", keywords, &key, &ret_parent)) { // ret_parent is optional
        return NULL;
    }
    BinaryTree* bt = self->binary_tree;
    Py_INCREF(Py_None);
    PyObject* parent = Py_None;
    PyObject* walk = bt->root_idx;

    if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->key == Py_None) {
        Py_RETURN_NONE;
    }

    while (walk != Py_None) {
        PyObject* curr_key = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->key;

        if (curr_key == key) {
            break;
        }
        parent = walk;

        if (!PyCallable_Check(bt->comparator)) {
            PyErr_SetString(PyExc_ValueError, "comparator should be callable");
            return NULL;
        }
        PyObject* arguments = Py_BuildValue("(OO)", key, curr_key);
        PyObject* res = PyObject_CallObject(bt->comparator, arguments);
        Py_DECREF(arguments);
        if (!PyLong_Check(res)) {
            PyErr_SetString(PyExc_TypeError, "bad return type from comparator");
            return NULL;
        }
        long long comp = PyLong_AsLongLong(res);

        if (comp == 1) {
            walk = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->left;
        }
        else {
            walk = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->right;
        }
    }

    Py_INCREF(Py_None);
    if (ret_parent==Py_None || PyLong_AsLong(ret_parent)==0) {
        return walk;
    }
    else {
        return Py_BuildValue("(OO)",walk,parent);
    }
    Py_RETURN_NONE; // dummy return statement, never executed
}

static PyObject* BinarySearchTree_insert(BinarySearchTree* self, PyObject* args) {
    Py_INCREF(Py_None);
    PyObject* key = Py_None;
    Py_INCREF(Py_None);
    PyObject* data = Py_None;
    if (!PyArg_ParseTuple(args, "O|O", &key, &data)) { // data is optional
        return NULL;
    }

    PyObject* parent = PyLong_FromLong(0);

    PyObject* res = BinarySearchTree_search(self, Py_BuildValue("(O)",key), PyDict_New()); // keywords should be a dictionary, so empty dictionary here as no keywords
    BinaryTree* bt = self->binary_tree;
    if (res != Py_None) {
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(res)])->data = data;
        Py_RETURN_NONE;
    }

    PyObject* walk = PyLong_FromLong(PyLong_AsLong(bt->root_idx));
    if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->key == Py_None) {
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->key = key;
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->data = data;
        Py_RETURN_NONE;
    }

    if (PyType_Ready(&TreeNodeType) < 0) { // This has to be present to finalize a type object. This should be called on all type objects to finish their initialization.
        return NULL;
    }
    TreeNode* new_node = reinterpret_cast<TreeNode*>(TreeNode___new__(&TreeNodeType, Py_BuildValue("(OO)", key, data), PyDict_New()));
    PyObject* prev_node = PyLong_FromLong(PyLong_AsLong(bt->root_idx));
    bool flag = true;

    while (flag) {
        PyObject* curr_key = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->key;
        if (!PyCallable_Check(bt->comparator)) {
            PyErr_SetString(PyExc_ValueError, "comparator should be callable");
            return NULL;
        }
        PyObject* arguments = Py_BuildValue("(OO)", key, curr_key);
        PyObject* cres = PyObject_CallObject(bt->comparator, arguments);
        Py_DECREF(arguments);
        if (!PyLong_Check(cres)) {
            PyErr_SetString(PyExc_TypeError, "bad return type from comparator");
            return NULL;
        }
        long long comp = PyLong_AsLongLong(cres);

        if (comp==0) {
            if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->right == Py_None) {
                new_node->parent = prev_node;
                ArrayForTrees_append(bt->tree, Py_BuildValue( "[O]", reinterpret_cast<PyObject*>(new_node)) );
                reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->right = PyLong_FromLong(bt->size);
                bt->size = bt->size + 1;
                flag = false;
            }
            prev_node = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->right;
            walk = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->right;
        }
        else {
            if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->left == Py_None) {
                new_node->parent = prev_node;
                ArrayForTrees_append(bt->tree, Py_BuildValue( "[O]", reinterpret_cast<PyObject*>(new_node)) );
                reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->left = PyLong_FromLong(bt->size);
                bt->size = bt->size + 1;
                flag = false;
            }
            prev_node = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->left;
            walk = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->left;
        }
    }
    BinarySearchTree__update_size(self, Py_BuildValue("(O)",walk));
    Py_RETURN_NONE;
}

static PyObject* BinarySearchTree_delete(BinarySearchTree* self, PyObject *args, PyObject *kwds) {
    Py_INCREF(Py_None);
    PyObject* key = Py_None;
    Py_INCREF(Py_None);
    PyObject* balancing_info = Py_None;
    static char* keywords[] = {"key","balancing_info", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O|O", keywords, &key, &balancing_info)) {
        return NULL;
    }
    PyObject* kwd_parent = PyDict_New();
    PyDict_SetItemString(kwd_parent, "parent", PyLong_FromLong(1));
    PyObject* tup = BinarySearchTree_search(self, Py_BuildValue("(O)",key), kwd_parent);
    PyObject* walk = PyTuple_GetItem(tup, 0);
    PyObject* parent = PyTuple_GetItem(tup, 1);
    Py_INCREF(Py_None);
    PyObject* a = Py_None;
    if (walk == Py_None) {
        Py_RETURN_NONE;
    }
    BinaryTree* bt = self->binary_tree;
    if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->left == Py_None && reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->right == Py_None) {
        if (parent == Py_None) {
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->data = Py_None;
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->key = Py_None;
        }
        else {
            if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent)])->left == walk) {
                Py_INCREF(Py_None);
                reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent)])->left = Py_None;
            }
            else {
                Py_INCREF(Py_None);
                reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent)])->right = Py_None;
            }
            a = parent;
            PyObject* par_key = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent)])->key;
            PyObject* root_key = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->key;
            PyObject* new_indices = ArrayForTrees_delete(bt->tree, Py_BuildValue("(O)",walk));
            if (new_indices != Py_None) {
                a = PyDict_GetItem(new_indices, par_key);
                bt->root_idx = PyDict_GetItem(new_indices, root_key);
            }
        }
        BinarySearchTree__update_size(self, Py_BuildValue("(O)",a));
    }
    else if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->left != Py_None && reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->right != Py_None) {
        PyObject* twalk = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->right;
        PyObject* par = walk;
        bool flag = false;
        while (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(twalk)])->left != Py_None) {
            flag = true;
            par = twalk;
            twalk = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(twalk)])->left;
        }
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->data = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(twalk)])->data;
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->key = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(twalk)])->key;
        if (flag) {
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(par)])->left = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(twalk)])->right;
        }
        else {
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(par)])->right = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(twalk)])->right;
        }

        if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(twalk)])->right != Py_None) {
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(twalk)])->right)])->parent = par;
        }

        if (twalk != Py_None) {
            a = par;
            PyObject* par_key = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(par)])->key;
            PyObject* root_key = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->key;
            PyObject* new_indices = ArrayForTrees_delete(bt->tree, Py_BuildValue("(O)",twalk));
            if (new_indices != Py_None) {
                a = PyDict_GetItem(new_indices, par_key);
                bt->root_idx = PyDict_GetItem(new_indices, root_key);
            }
        }
        BinarySearchTree__update_size(self, Py_BuildValue("(O)",a));
    }
    else {
        PyObject* child;
        if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->left != Py_None) {
            child = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->left;
        }
        else {
            child = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->right;
        }
        if (parent == Py_None) {
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->left = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(child)])->left;
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->right = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(child)])->right;
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->data = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(child)])->data;
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->key = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(child)])->key;
            Py_INCREF(Py_None);
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->parent = Py_None;
            PyObject* root_key = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->key;
            PyObject* new_indices = ArrayForTrees_delete(bt->tree, Py_BuildValue("(O)",child));
            if (new_indices != Py_None) {
                bt->root_idx = PyDict_GetItem(new_indices, root_key);
            }
        }
        else {
            if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent)])->left == walk) {
                reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent)])->left = child;
            }
            else {
                reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent)])->right = child;
            }
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(child)])->parent = parent;
            a = parent;
            PyObject* par_key = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent)])->key;
            PyObject* root_key = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->key;
            PyObject* new_indices = ArrayForTrees_delete(bt->tree, Py_BuildValue("(O)",walk));
            if (new_indices != Py_None) {
                parent = PyDict_GetItem(new_indices, par_key);
                reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(child)])->parent = PyDict_GetItem(new_indices, root_key);
                a = PyDict_GetItem(new_indices, root_key);
                bt->root_idx = PyDict_GetItem(new_indices, root_key);
            }
            BinarySearchTree__update_size(self, Py_BuildValue("(O)",a));
        }
    }

    if (balancing_info != Py_None) {
        if (PyLong_AsLong(balancing_info) == 1) {
            return a;
        }
    }
    Py_RETURN_TRUE;
}

static PyObject* BinarySearchTree__bound_helper(BinarySearchTree* self, PyObject *args) {
    // This function is only called internally, so all arguments are passed in proper order
    PyObject *node_idx = PyObject_GetItem(args, PyZero);
    PyObject *bound_key = PyObject_GetItem(args, PyOne);
    PyObject *is_upper = PyObject_GetItem(args, PyTwo);
    BinaryTree* bt = self->binary_tree;
    if (node_idx == Py_None) {
        Py_RETURN_NONE;
    }
    if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->key == Py_None) {
        Py_RETURN_NONE;
    }
    if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->key == bound_key) {
        if (is_upper == Py_False) {
            return reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->key;
        }
        else {
            return BinarySearchTree__bound_helper(self, Py_BuildValue("(OOO)",reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->right, bound_key, is_upper));
        }
    }

    if (!PyCallable_Check(bt->comparator)) {
        PyErr_SetString(PyExc_ValueError, "comparator should be callable");
        return NULL;
    }
    PyObject* arguments = Py_BuildValue("(OO)", reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->key, bound_key);
    PyObject* cres = PyObject_CallObject(bt->comparator, arguments);
    Py_DECREF(arguments);
    if (!PyLong_Check(cres)) {
        PyErr_SetString(PyExc_TypeError, "bad return type from comparator");
        return NULL;
    }
    long long comp = PyLong_AsLongLong(cres);

    if (comp == 1) {
        return BinarySearchTree__bound_helper(self, Py_BuildValue("(OOO)",reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->right, bound_key, is_upper));
    }
    else {
        PyObject* res_bound = BinarySearchTree__bound_helper(self, Py_BuildValue("(OOO)",reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->left, bound_key, is_upper));
        if (res_bound != Py_None) {
            return res_bound;
        }
        else {
            return reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->key;
        }
    }
}

static PyObject* BinarySearchTree_lower_bound(BinarySearchTree* self, PyObject *args, PyObject* kwds) {
    PyObject* key = PyObject_GetItem(args, PyZero);
    return BinarySearchTree__bound_helper(self, Py_BuildValue("(OOO)", self->binary_tree->root_idx, key, Py_False));
}

static PyObject* BinarySearchTree_upper_bound(BinarySearchTree* self, PyObject *args, PyObject* kwds) {
    PyObject* key = PyObject_GetItem(args, PyZero);
    return BinarySearchTree__bound_helper(self, Py_BuildValue("(OOO)", self->binary_tree->root_idx, key, Py_True));
}

static PyObject* BinarySearchTree__simple_path(BinarySearchTree* self, PyObject *args) {
    PyObject* key = PyObject_GetItem(args, PyZero);
    PyObject* root = PyObject_GetItem(args, PyOne);
    std::stack<long> stack;
    stack.push(PyLong_AsLong(root));
    PyObject* path = PyList_New(0);
    long node_idx = -1;
    BinaryTree* bt = self->binary_tree;

    while (!stack.empty()) {
        long node = stack.top();
        stack.pop();
        if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[node])->key == key) {
            node_idx = node;
            break;
        }
        if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[node])->left != Py_None) {
            stack.push(PyLong_AsLong(reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[node])->left));
        }
        if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[node])->right != Py_None) {
            stack.push(PyLong_AsLong(reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[node])->right));
        }
    }
    if (node_idx == -1) {
        return path;
    }
    while (node_idx != 0) {
        PyList_Append(path, PyLong_FromLong(node_idx));
        node_idx = PyLong_AsLong(reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[node_idx])->parent);
    }
    PyList_Append(path, PyLong_FromLong(0));
    PyList_Reverse(path);
    return path;
}

static PyObject* BinarySearchTree__lca_1(BinarySearchTree* self, PyObject* args) {
    long j = PyLong_AsLong(PyObject_GetItem(args, PyZero));
    long k = PyLong_AsLong(PyObject_GetItem(args, PyOne));
    BinaryTree* bt = self->binary_tree;
    PyObject* root = bt->root_idx;
    PyObject* path1 = BinarySearchTree__simple_path(self, Py_BuildValue("(OO)",PyLong_FromLong(j),root));
    PyObject* path2 = BinarySearchTree__simple_path(self, Py_BuildValue("(OO)",PyLong_FromLong(k),root));
    long n = PyLong_AsLong(PyLong_FromSsize_t(PyList_Size(path1)));
    long m = PyLong_AsLong(PyLong_FromSsize_t(PyList_Size(path2)));
    if (n==0 || m==0) {
        PyErr_SetString(PyExc_ValueError, "One of the two paths doesn't exist.");
        return NULL;
    }
    long i = 0;
    j = 0;
    while (i<n && j<m) {
        if (PyList_GetItem(path1, PyLong_AsSsize_t(PyLong_FromLong(i))) != PyList_GetItem(path2, PyLong_AsSsize_t(PyLong_FromLong(j)))) {
            return reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(PyList_GetItem(path1, PyLong_AsSsize_t(PyLong_FromLong(i-1))))])->key;
        }
        i += 1;
        j += 1;
    }

    while (i<n && j<m) {
        if (PyList_GetItem(path1, PyLong_AsSsize_t(PyLong_FromLong(i))) < PyList_GetItem(path2, PyLong_AsSsize_t(PyLong_FromLong(j)))) {
            return reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(PyList_GetItem(path1, PyLong_AsSsize_t(PyLong_FromLong(n-1))))])->key;
        }
        else if (PyList_GetItem(path1, PyLong_AsSsize_t(PyLong_FromLong(i))) > PyList_GetItem(path2, PyLong_AsSsize_t(PyLong_FromLong(j)))) {
            break;
        }
        i += 1;
        j += 1;
    }
    return reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(PyList_GetItem(path2, PyLong_AsSsize_t(PyLong_FromLong(m-1))))])->key;
}

static PyObject* BinarySearchTree__lca_2(BinarySearchTree* self, PyObject* args) {
    PyObject* j = PyObject_GetItem(args, PyZero);
    PyObject* k = PyObject_GetItem(args, PyOne);
    BinaryTree* bt = self->binary_tree;

    PyObject* curr_root = bt->root_idx;
    PyObject* u = BinarySearchTree_search(self, Py_BuildValue("(O)",j), PyDict_New());
    PyObject* v = BinarySearchTree_search(self, Py_BuildValue("(O)",k), PyDict_New());

    if (u==Py_None || v==Py_None) {
        PyErr_SetString(PyExc_ValueError, "One of the nodes doesn't exist.");
        return NULL;
    }

    if (!PyCallable_Check(bt->comparator)) {
        PyErr_SetString(PyExc_ValueError, "comparator should be callable");
        return NULL;
    }
    PyObject* arguments1 = Py_BuildValue("(OO)", reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(u)])->key, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(curr_root)])->key);
    PyObject* cres1 = PyObject_CallObject(bt->comparator, arguments1);
    Py_DECREF(arguments1);
    if (!PyLong_Check(cres1)) {
        PyErr_SetString(PyExc_TypeError, "bad return type from comparator");
        return NULL;
    }
    long long u_left = PyLong_AsLongLong(cres1);

    if (!PyCallable_Check(bt->comparator)) {
        PyErr_SetString(PyExc_ValueError, "comparator should be callable");
        return NULL;
    }
    PyObject* arguments2 = Py_BuildValue("(OO)", reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(v)])->key, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(curr_root)])->key);
    PyObject* cres2 = PyObject_CallObject(bt->comparator, arguments2);
    Py_DECREF(arguments2);
    if (!PyLong_Check(cres2)) {
        PyErr_SetString(PyExc_TypeError, "bad return type from comparator");
        return NULL;
    }
    long long v_left = PyLong_AsLongLong(cres2);

    while (!(u_left ^ v_left)) {
        if (u_left && v_left) {
            curr_root = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(curr_root)])->left;
        }
        else {
            curr_root = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(curr_root)])->right;
        }

        if (curr_root == u || curr_root == v) {
            if (curr_root == Py_None) {
                Py_RETURN_NONE;
            }
            return reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(curr_root)])->key;
        }

        if (!PyCallable_Check(bt->comparator)) {
            PyErr_SetString(PyExc_ValueError, "comparator should be callable");
            return NULL;
        }
        PyObject* arguments1 = Py_BuildValue("(OO)", reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(u)])->key, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(curr_root)])->key);
        PyObject* cres1 = PyObject_CallObject(bt->comparator, arguments1);
        Py_DECREF(arguments1);
        if (!PyLong_Check(cres1)) {
            PyErr_SetString(PyExc_TypeError, "bad return type from comparator");
            return NULL;
        }
        u_left = PyLong_AsLongLong(cres1);

        if (!PyCallable_Check(bt->comparator)) {
            PyErr_SetString(PyExc_ValueError, "comparator should be callable");
            return NULL;
        }
        PyObject* arguments2 = Py_BuildValue("(OO)", reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(v)])->key, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(curr_root)])->key);
        PyObject* cres2 = PyObject_CallObject(bt->comparator, arguments2);
        Py_DECREF(arguments2);
        if (!PyLong_Check(cres2)) {
            PyErr_SetString(PyExc_TypeError, "bad return type from comparator");
            return NULL;
        }
        v_left = PyLong_AsLongLong(cres2);
    }

    if (curr_root == Py_None) {
        Py_RETURN_NONE;
    }
    return reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(curr_root)])->key;
}

static PyObject* BinarySearchTree_lowest_common_ancestor(BinarySearchTree* self, PyObject* args) {
    Py_INCREF(Py_None);
    PyObject* j = Py_None;
    Py_INCREF(Py_None);
    PyObject* k = Py_None;
    PyObject* algorithm = PyOne;
    if (!PyArg_ParseTuple(args, "OO|O", &j, &k, &algorithm)) { // ret_parent is optional
        return NULL;
    }

    if (algorithm == PyOne) {
        return BinarySearchTree__lca_1(self, Py_BuildValue("(OO)",j,k));
    }
    else {
        return BinarySearchTree__lca_2(self, Py_BuildValue("(OO)",j,k));
    }
}

static PyObject* BinarySearchTree_rank(BinarySearchTree* self, PyObject* args) {
    PyObject* x = PyObject_GetItem(args, PyZero);
    PyObject* walk = BinarySearchTree_search(self, Py_BuildValue("(O)",x), PyDict_New());
    if (walk == Py_None) {
        Py_RETURN_NONE;
    }
    BinaryTree* bt = self->binary_tree;
    long r = BinarySearchTree_left_size(self, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])) + 1;
    while (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->key != reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->key) {
        PyObject* p = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->parent;
        if (walk == reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(p)])->right) {
            r = r + BinarySearchTree_left_size(self, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(p)])) + 1;
        }
        walk = p;
    }
    return PyLong_FromLong(r);
}

static PyObject* BinarySearchTree_select(BinarySearchTree* self, PyObject* args) {
    long i = PyLong_AsLong(PyObject_GetItem(args, PyZero));
    i = i - 1;
    if (i < 0) {
        PyErr_SetString(PyExc_ValueError, "Expected a positive integer");
        return NULL;
    }
    BinaryTree* bt = self->binary_tree;
    if (i >= bt->tree->_num) {
        PyErr_SetString(PyExc_ValueError, "Integer passed to select() is greater than the size of the tree.");
        return NULL;
    }
    PyObject* walk = bt->root_idx;
    while (walk != Py_None) {
        long l = BinarySearchTree_left_size(self, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)]));
        if (i == l) {
            return bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)];
        }
        PyObject* left_walk = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->left;
        PyObject* right_walk = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->right;
        if (left_walk == Py_None && right_walk==Py_None) {
            PyErr_SetString(PyExc_IndexError, "The traversal is terminated due to no child nodes ahead.");
            return NULL;
        }
        if (i < l) {
            if (!PyCallable_Check(bt->comparator)) {
                PyErr_SetString(PyExc_ValueError, "comparator should be callable");
                return NULL;
            }
            PyObject* arguments = Py_BuildValue("(OO)", reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(left_walk)])->key, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->key);
            PyObject* cres = PyObject_CallObject(bt->comparator, arguments);
            Py_DECREF(arguments);
            if (!PyLong_Check(cres)) {
                PyErr_SetString(PyExc_TypeError, "bad return type from comparator");
                return NULL;
            }
            long long comp = PyLong_AsLongLong(cres);

            if (left_walk != Py_None && comp) {
                walk = left_walk;
            }
            else {
                walk = right_walk;
            }
        }
        else {
            if (!PyCallable_Check(bt->comparator)) {
                PyErr_SetString(PyExc_ValueError, "comparator should be callable");
                return NULL;
            }
            PyObject* arguments = Py_BuildValue("(OO)", reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(right_walk)])->key, reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->key);
            PyObject* cres = PyObject_CallObject(bt->comparator, arguments);
            Py_DECREF(arguments);
            if (!PyLong_Check(cres)) {
                PyErr_SetString(PyExc_TypeError, "bad return type from comparator");
                return NULL;
            }
            long long comp = PyLong_AsLongLong(cres);

            if (right_walk != Py_None && (!comp)) {
                walk = right_walk;
            }
            else {
                walk = left_walk;
            }
            i = i - (l + 1);
        }
    }
    Py_RETURN_NONE; // dummy return statement, never executed
}

static PyObject* BinarySearchTree_root_idx(BinarySearchTree *self, void *closure) {
    return self->binary_tree->root_idx;
}


static struct PyMethodDef BinarySearchTree_PyMethodDef[] = {
    {"insert", (PyCFunction) BinarySearchTree_insert, METH_VARARGS | METH_KEYWORDS, NULL},
    {"delete", (PyCFunction) BinarySearchTree_delete, METH_VARARGS | METH_KEYWORDS, NULL},
    {"search", (PyCFunction) BinarySearchTree_search, METH_VARARGS | METH_KEYWORDS, NULL},
    {"lower_bound", (PyCFunction) BinarySearchTree_lower_bound, METH_VARARGS | METH_KEYWORDS, NULL},
    {"upper_bound", (PyCFunction) BinarySearchTree_upper_bound, METH_VARARGS | METH_KEYWORDS, NULL},
    {"_simple_path", (PyCFunction) BinarySearchTree__simple_path, METH_VARARGS, NULL},
    {"_lca_1", (PyCFunction) BinarySearchTree__lca_1, METH_VARARGS, NULL},
    {"_lca_2", (PyCFunction) BinarySearchTree__lca_2, METH_VARARGS, NULL},
    {"lowest_common_ancestor", (PyCFunction) BinarySearchTree_lowest_common_ancestor, METH_VARARGS, NULL},
    {"rank", (PyCFunction) BinarySearchTree_rank, METH_VARARGS, NULL},
    {"select", (PyCFunction) BinarySearchTree_select, METH_VARARGS, NULL},
    {NULL}
};

static PyGetSetDef BinarySearchTree_GetterSetters[] = {
    {"root_idx", (getter) BinarySearchTree_root_idx, NULL, "returns the index of the tree's root", NULL},
    {NULL}  /* Sentinel */
};

static PyMemberDef BinarySearchTree_PyMemberDef[] = {
    {"tree", T_OBJECT_EX, offsetof(BinarySearchTree, tree), 0, "tree"},
    {NULL}  /* Sentinel */
};


static PyTypeObject BinarySearchTreeType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "BinarySearchTree",
    /* tp_basicsize */ sizeof(BinarySearchTree),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor) BinarySearchTree_dealloc,
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
    /* tp_str */ (reprfunc) BinarySearchTree___str__,
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
    /* tp_methods */ BinarySearchTree_PyMethodDef,
    /* tp_members */ BinarySearchTree_PyMemberDef,
    /* tp_getset */ BinarySearchTree_GetterSetters,
    /* tp_base */ &BinaryTreeType,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ BinarySearchTree___new__,
};

#endif
