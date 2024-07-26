#ifndef TREES_REDBLACKTREE_HPP
#define TREES_REDBLACKTREE_HPP

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
} RedBlackTree;

static void RedBlackTree_dealloc(RedBlackTree *self) {
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* RedBlackTree___new__(PyTypeObject* type, PyObject *args, PyObject *kwds) {
    RedBlackTree *self;
    self = reinterpret_cast<RedBlackTree*>(type->tp_alloc(type, 0));

    if (PyType_Ready(&SelfBalancingBinaryTreeType) < 0) { // This has to be present to finalize a type object. This should be called on all type objects to finish their initialization.
        return NULL;
    }
    PyObject* p = SelfBalancingBinaryTree___new__(&SelfBalancingBinaryTreeType, args, kwds);
    self->sbbt = reinterpret_cast<SelfBalancingBinaryTree*>(p);
    self->tree = reinterpret_cast<SelfBalancingBinaryTree*>(p)->bst->binary_tree->tree;

    return reinterpret_cast<PyObject*>(self);
}

static PyObject* RedBlackTree___str__(RedBlackTree *self) {
    return BinarySearchTree___str__(self->sbbt->bst);
}

static PyObject* RedBlackTree__get_parent(RedBlackTree *self, PyObject* args) {
    long node_idx = PyLong_AsLong(PyObject_GetItem(args, PyZero));
    BinaryTree* bt = self->sbbt->bst->binary_tree;
    PyObject* parent = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[node_idx])->parent;
    return parent;
}

static PyObject* RedBlackTree__get_grand_parent(RedBlackTree *self, PyObject* args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    PyObject* parent_idx = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));

    BinaryTree* bt = self->sbbt->bst->binary_tree;
    PyObject* grand_parent = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent_idx)])->parent;
    return grand_parent;
}

static PyObject* RedBlackTree__get_sibling(RedBlackTree *self, PyObject* args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    PyObject* parent_idx = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));

    if (parent_idx == Py_None) {
        Py_RETURN_NONE;
    }

    BinaryTree* bt = self->sbbt->bst->binary_tree;
    TreeNode* node = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent_idx)]);
    if (node_idx == node->left) {
        PyObject* sibling_idx = node->right;
        return sibling_idx;
    }
    else {
        PyObject* sibling_idx = node->left;
        return sibling_idx;
    }

    Py_RETURN_NONE;
}

static PyObject* RedBlackTree__get_uncle(RedBlackTree *self, PyObject* args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    PyObject* parent_idx = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));

    PyObject* uncle = RedBlackTree__get_sibling(self, Py_BuildValue("(O)", parent_idx));
    return uncle;
}

static PyObject* RedBlackTree__is_onleft(RedBlackTree *self, PyObject* args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    PyObject* parent_idx = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));

    BinaryTree* bt = self->sbbt->bst->binary_tree;
    if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent_idx)])->left == node_idx) {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}

static PyObject* RedBlackTree__is_onright(RedBlackTree *self, PyObject* args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    if (RedBlackTree__is_onleft(self, Py_BuildValue("(O)", node_idx)) == Py_False) {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}

static PyObject* RedBlackTree___fix_insert(RedBlackTree *self, PyObject* args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    BinaryTree* bt = self->sbbt->bst->binary_tree;
    while (RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx)) != Py_None && reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx)))])->color == 1 && reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->color == 1) {
        PyObject* parent_idx = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));
        PyObject* grand_parent_idx = RedBlackTree__get_grand_parent(self, Py_BuildValue("(O)", node_idx));
        PyObject* uncle_idx = RedBlackTree__get_uncle(self, Py_BuildValue("(O)", node_idx));

        if (uncle_idx != Py_None && reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(uncle_idx)])->color == 1) {
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(uncle_idx)])->color = 0;
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent_idx)])->color = 0;
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(grand_parent_idx)])->color = 1;
            node_idx = grand_parent_idx;
        }
        else {
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->is_root = false;
            if (RedBlackTree__is_onright(self, Py_BuildValue("(O)", parent_idx)) == Py_True) {
                if (RedBlackTree__is_onleft(self, Py_BuildValue("(O)", node_idx)) == Py_True) {
                    SelfBalancingBinaryTree__right_rotate(self->sbbt, Py_BuildValue("(OO)", parent_idx, node_idx));
                    node_idx = parent_idx;
                    parent_idx = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));
                }
                node_idx = parent_idx;
                parent_idx = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));
                SelfBalancingBinaryTree__left_rotate(self->sbbt, Py_BuildValue("(OO)", parent_idx, node_idx));
            }
            else if (RedBlackTree__is_onleft(self, Py_BuildValue("(O)", parent_idx)) == Py_True) {
                if (RedBlackTree__is_onright(self, Py_BuildValue("(O)", node_idx)) == Py_True) {
                    SelfBalancingBinaryTree__left_rotate(self->sbbt, Py_BuildValue("(OO)", parent_idx, node_idx));
                    node_idx = parent_idx;
                    parent_idx = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));
                }
                node_idx = parent_idx;
                parent_idx = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));
                SelfBalancingBinaryTree__right_rotate(self->sbbt, Py_BuildValue("(OO)", parent_idx, node_idx));
            }
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->color = 0;
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent_idx)])->color = 1;
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->is_root = true;
        }
        if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->is_root) {
            break;
        }
    }
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->color = 0;
    Py_RETURN_NONE;
}

static PyObject* RedBlackTree_insert(RedBlackTree *self, PyObject* args) {
    Py_INCREF(Py_None);
    PyObject* key = Py_None;
    Py_INCREF(Py_None);
    PyObject* data = Py_None;
    if (!PyArg_ParseTuple(args, "O|O", &key, &data)) { // data is optional
        return NULL;
    }
    SelfBalancingBinaryTree_insert(self->sbbt, Py_BuildValue("(OO)", key, data));
    PyObject* node_idx = SelfBalancingBinaryTree_search(self->sbbt, Py_BuildValue("(O)", key), PyDict_New());

    BinaryTree* bt = self->sbbt->bst->binary_tree;
    TreeNode* node = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)]);

    if (PyType_Ready(&TreeNodeType) < 0) { // This has to be present to finalize a type object. This should be called on all type objects to finish their initialization.
        return NULL;
    }
    TreeNode* new_node = reinterpret_cast<TreeNode*>(TreeNode___new__(&TreeNodeType, Py_BuildValue("(OO)", key, data), PyDict_New()));
    new_node->parent = node->parent;
    new_node->left = node->left;
    new_node->right = node->right;
    bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)] = reinterpret_cast<PyObject*>(new_node);

    if (node->is_root) {
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->is_root = true;
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->color = 0;
    }
    else if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->parent)])->color == 1) {
        RedBlackTree___fix_insert(self, Py_BuildValue("(O)", node_idx));
    }

    Py_RETURN_NONE;
}

static PyObject* RedBlackTree_lower_bound(RedBlackTree* self, PyObject *args, PyObject *kwds) {
    return BinarySearchTree_lower_bound(self->sbbt->bst, args, kwds);
}

static PyObject* RedBlackTree_upper_bound(RedBlackTree* self, PyObject *args, PyObject *kwds) {
    return BinarySearchTree_upper_bound(self->sbbt->bst, args, kwds);
}

static PyObject* RedBlackTree__find_predecessor(RedBlackTree* self, PyObject *args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    BinaryTree* bt = self->sbbt->bst->binary_tree;

    while (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->right != Py_None) {
        node_idx = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->right;
    }
    return node_idx;
}

static PyObject* RedBlackTree__is_leaf(RedBlackTree* self, PyObject *args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    BinaryTree* bt = self->sbbt->bst->binary_tree;
    if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->left == Py_None && reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->right == Py_None) {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}

static PyObject* RedBlackTree__has_two_child(RedBlackTree* self, PyObject *args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    BinaryTree* bt = self->sbbt->bst->binary_tree;
    if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->left != Py_None && reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->right != Py_None) {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}

static PyObject* RedBlackTree__has_one_child(RedBlackTree* self, PyObject *args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    if (RedBlackTree__is_leaf(self, Py_BuildValue("(O)", node_idx)) == Py_False && RedBlackTree__has_two_child(self, Py_BuildValue("(O)", node_idx)) ==  Py_False) {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}

static PyObject* RedBlackTree__transplant_values(RedBlackTree* self, PyObject *args) {
    PyObject* node_idx1 = PyObject_GetItem(args, PyZero);
    PyObject* node_idx2 = PyObject_GetItem(args, PyOne);
    BinaryTree* bt = self->sbbt->bst->binary_tree;

    PyObject* parent = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx1)])->parent;
    if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx1)])->is_root == true && RedBlackTree__has_one_child(self, Py_BuildValue("(O)", node_idx1)) == Py_True) {
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->key = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx2)])->key;
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->data = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx2)])->data;
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->left = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx2)])->left;
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->right = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx2)])->right;
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx1)])->parent == Py_None;

        return reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->key;
    }
    else {
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx1)])->key = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx2)])->key;
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx1)])->data = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx2)])->data;
    }
    Py_RETURN_NONE;
}

static PyObject* RedBlackTree___has_red_child(RedBlackTree* self, PyObject *args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    BinaryTree* bt = self->sbbt->bst->binary_tree;
    PyObject* left_idx = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->left;
    PyObject* right_idx = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->right;
    if ((left_idx != Py_None && reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(left_idx)])->color == 1) || (right_idx != Py_None && reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(right_idx)])->color == 1)) {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}

static PyObject* RedBlackTree__replace_node(RedBlackTree* self, PyObject *args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    if (RedBlackTree__is_leaf(self, Py_BuildValue("(O)", node_idx)) == Py_True) {
        Py_RETURN_NONE;
    }
    else if (RedBlackTree__has_one_child(self, Py_BuildValue("(O)", node_idx)) == Py_True) {
        BinaryTree* bt = self->sbbt->bst->binary_tree;
        PyObject* child;

        if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->left != Py_None) {
            child = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->left;
        }
        else {
            child = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->right;
        }
        return child;
    }
    else {
        BinaryTree* bt = self->sbbt->bst->binary_tree;
        PyObject* node = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->left;
        return RedBlackTree__find_predecessor(self, Py_BuildValue("(O)", node));
    }
    Py_RETURN_NONE;
}

static PyObject* RedBlackTree___walk1_walk_isblack(RedBlackTree* self, PyObject *args) {
    PyObject* color = PyObject_GetItem(args, PyZero);
    PyObject* node_idx1 = PyObject_GetItem(args, PyOne);
    BinaryTree* bt = self->sbbt->bst->binary_tree;

    if ((node_idx1 == Py_None || reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx1)])->color == 0) && (color == PyZero)) {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}

static PyObject* RedBlackTree___left_left_sublingcase(RedBlackTree* self, PyObject *args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    BinaryTree* bt = self->sbbt->bst->binary_tree;

    PyObject* left_idx = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->left;
    PyObject* parent = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));
    long parent_color = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent)])->color;
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(left_idx)])->color = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->color;
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->color = parent_color;
    SelfBalancingBinaryTree__right_rotate(self->sbbt, Py_BuildValue("(OO)", parent, node_idx));

    Py_RETURN_NONE;
}

static PyObject* RedBlackTree___right_left_sublingcase(RedBlackTree* self, PyObject *args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    BinaryTree* bt = self->sbbt->bst->binary_tree;

    PyObject* left_idx = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->left;
    PyObject* parent = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));
    long parent_color = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent)])->color;
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(left_idx)])->color = parent_color;
    SelfBalancingBinaryTree__right_rotate(self->sbbt, Py_BuildValue("(OO)", node_idx, left_idx));
    PyObject* child = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));
    SelfBalancingBinaryTree__left_rotate(self->sbbt, Py_BuildValue("(OO)", parent, child));

    Py_RETURN_NONE;
}

static PyObject* RedBlackTree___left_right_sublingcase(RedBlackTree* self, PyObject *args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    BinaryTree* bt = self->sbbt->bst->binary_tree;

    PyObject* right_idx = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->right;
    PyObject* parent = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));
    long parent_color = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent)])->color;
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(right_idx)])->color = parent_color;
    SelfBalancingBinaryTree__left_rotate(self->sbbt, Py_BuildValue("(OO)", node_idx, right_idx));
    PyObject* child = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));
    SelfBalancingBinaryTree__right_rotate(self->sbbt, Py_BuildValue("(OO)", parent, child));

    Py_RETURN_NONE;
}

static PyObject* RedBlackTree___right_right_sublingcase(RedBlackTree* self, PyObject *args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    BinaryTree* bt = self->sbbt->bst->binary_tree;

    PyObject* right_idx = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->right;
    PyObject* parent = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));
    long parent_color = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent)])->color;
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(right_idx)])->color = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->color;
    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)])->color = parent_color;
    SelfBalancingBinaryTree__left_rotate(self->sbbt, Py_BuildValue("(OO)", parent, node_idx));

    Py_RETURN_NONE;
}

static PyObject* RedBlackTree___fix_deletion(RedBlackTree* self, PyObject *args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    BinaryTree* bt = self->sbbt->bst->binary_tree;

    TreeNode* node = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(node_idx)]);
    long color = node->color;
    while (node_idx != bt->root_idx && color == 0) {
        PyObject* sibling_idx = RedBlackTree__get_sibling(self, Py_BuildValue("(O)", node_idx));
        PyObject* parent_idx = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));
        if (sibling_idx == Py_None) {
            node_idx = parent_idx;
            continue;
        }
        else {
            if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(sibling_idx)])->color == 1) {
                reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->is_root = false;
                reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent_idx)])->color = 1;
                reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(sibling_idx)])->color = 0;
                if (RedBlackTree__is_onleft(self, Py_BuildValue("(O)", sibling_idx)) == Py_True) {
                    SelfBalancingBinaryTree__right_rotate(self->sbbt, Py_BuildValue("(OO)", parent_idx, sibling_idx));
                }
                else {
                    SelfBalancingBinaryTree__left_rotate(self->sbbt, Py_BuildValue("(OO)", parent_idx, sibling_idx));
                }
                reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->is_root = true;
                continue;
            }
            else {
                if (RedBlackTree___has_red_child(self, Py_BuildValue("(O)", sibling_idx)) == Py_True) {
                    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->is_root = false;
                    PyObject* left_idx = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(sibling_idx)])->left;
                    if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(sibling_idx)])->left != Py_None && reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(left_idx)])->color == 1) {
                        if (RedBlackTree__is_onleft(self, Py_BuildValue("(O)", sibling_idx)) == Py_True) {
                            RedBlackTree___left_left_sublingcase(self, Py_BuildValue("(O)", sibling_idx));
                        }
                        else {
                            RedBlackTree___right_left_sublingcase(self, Py_BuildValue("(O)", sibling_idx));
                        }
                    }
                    else {
                        if (RedBlackTree__is_onleft(self, Py_BuildValue("(O)", sibling_idx)) == Py_True) {
                            RedBlackTree___left_right_sublingcase(self, Py_BuildValue("(O)", sibling_idx));
                        }
                        else {
                            RedBlackTree___right_right_sublingcase(self, Py_BuildValue("(O)", sibling_idx));
                        }
                    }
                    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->is_root = true;
                    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent_idx)])->color = 0;
                }
                else {
                    reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(sibling_idx)])->color = 1;
                    if (reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent_idx)])->color == 0) {
                        node_idx = parent_idx;
                        continue;
                    }
                    else {
                        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent_idx)])->color = 0;
                    }
                }
            }
        }
        color = 1;
    }
    Py_RETURN_NONE;
}

static PyObject* RedBlackTree__remove_node(RedBlackTree* self, PyObject *args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    BinaryTree* bt = self->sbbt->bst->binary_tree;

    PyObject* parent = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));
    PyObject* a = parent;
    if (RedBlackTree__is_leaf(self, Py_BuildValue("(O)", node_idx)) == Py_True) {
        PyObject* par_key = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent)])->key;
        PyObject* root_key = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->key;
        PyObject* new_indices = ArrayForTrees_delete(bt->tree, Py_BuildValue("(O)", node_idx));
        if (new_indices != Py_None) {
            a = PyDict_GetItem(new_indices, par_key);
            bt->root_idx = PyDict_GetItem(new_indices, root_key);
        }
    }
    else if (RedBlackTree__has_one_child(self, Py_BuildValue("(O)", node_idx)) == Py_True) {
        PyObject* child = RedBlackTree__replace_node(self, Py_BuildValue("(O)", node_idx));
        parent = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));
        PyObject* par_key = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent)])->key;
        PyObject* root_key = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->key;
        PyObject* new_indices = ArrayForTrees_delete(bt->tree, Py_BuildValue("(O)", node_idx));
    }
    BinarySearchTree__update_size(self->sbbt->bst, Py_BuildValue("(O)", a));
    Py_RETURN_NONE;
}

static PyObject* RedBlackTree__delete_root(RedBlackTree* self, PyObject *args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    PyObject* node_idx1 = PyObject_GetItem(args, PyOne);
    BinaryTree* bt = self->sbbt->bst->binary_tree;

    if (RedBlackTree__is_leaf(self, Py_BuildValue("(O)", node_idx)) == Py_True) {
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->data = Py_None;
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(bt->root_idx)])->key = Py_None;
    }
    else if (RedBlackTree__has_one_child(self, Py_BuildValue("(O)", node_idx)) == Py_True) {
        PyObject* root_key = RedBlackTree__transplant_values(self, Py_BuildValue("(OO)", node_idx, node_idx1));
        PyObject* new_indices = ArrayForTrees_delete(bt->tree, Py_BuildValue("(O)", node_idx1));
        if (new_indices != Py_None) {
            bt->root_idx = PyDict_GetItem(new_indices, root_key);
        }
    }
    Py_RETURN_NONE;
}

static PyObject* RedBlackTree___leaf_case(RedBlackTree* self, PyObject *args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    PyObject* node_idx1 = PyObject_GetItem(args, PyOne);
    BinaryTree* bt = self->sbbt->bst->binary_tree;

    PyObject* walk = node_idx;
    PyObject* walk1 = node_idx1;
    PyObject* parent = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));
    long color = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->color;
    if (parent == Py_None) {
        RedBlackTree__delete_root(self, Py_BuildValue("(OO)", walk, walk1));
    }
    else {
        if (RedBlackTree___walk1_walk_isblack(self, Py_BuildValue("(OO)", PyLong_FromLong(color), walk1)) == Py_True) {
            RedBlackTree___fix_deletion(self, Py_BuildValue("(O)", walk));
        }
        else {
            PyObject* sibling_idx = RedBlackTree__get_sibling(self, Py_BuildValue("(O)", walk));
            if (sibling_idx != Py_None) {
                reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(sibling_idx)])->color = 1;
            }
        }
        if (RedBlackTree__is_onleft(self, Py_BuildValue("(O)", walk)) == Py_True) {
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent)])->left = Py_None;
        }
        else {
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent)])->right = Py_None;
        }
        RedBlackTree__remove_node(self, Py_BuildValue("(O)", walk));
    }
    Py_RETURN_NONE;
}

static PyObject* RedBlackTree___one_child_case(RedBlackTree* self, PyObject *args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    PyObject* node_idx1 = PyObject_GetItem(args, PyOne);
    BinaryTree* bt = self->sbbt->bst->binary_tree;

    PyObject* walk = node_idx;
    PyObject* walk1 = node_idx1;
    long walk_original_color = reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk)])->color;
    PyObject* parent = RedBlackTree__get_parent(self, Py_BuildValue("(O)", node_idx));
    if (parent == Py_None) {
        RedBlackTree__delete_root(self, Py_BuildValue("(OO)", walk, walk1));
    }
    else {
        if (RedBlackTree__is_onleft(self, Py_BuildValue("(O)", walk)) == Py_True) {
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent)])->left = walk1;
        }
        else {
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(parent)])->right = walk1;
        }
        reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk1)])->parent = parent;
        PyObject* a = RedBlackTree__remove_node(self, Py_BuildValue("(O)", walk));
        if (RedBlackTree___walk1_walk_isblack(self, Py_BuildValue("(OO)", PyLong_FromLong(walk_original_color), walk1)) == Py_True) {
            RedBlackTree___fix_deletion(self, Py_BuildValue("(O)", walk1));
        }
        else {
            reinterpret_cast<TreeNode*>(bt->tree->_one_dimensional_array->_data[PyLong_AsLong(walk1)])->color = 0;
        }
    }
    Py_RETURN_NONE;
}

static PyObject* RedBlackTree___two_child_case(RedBlackTree* self, PyObject *args) {
    PyObject* node_idx = PyObject_GetItem(args, PyZero);
    BinaryTree* bt = self->sbbt->bst->binary_tree;

    PyObject* walk = node_idx;
    PyObject* successor = RedBlackTree__replace_node(self, Py_BuildValue("(O)", walk));
    RedBlackTree__transplant_values(self, Py_BuildValue("(OO)", walk, successor));
    walk = successor;
    PyObject* walk1 = RedBlackTree__replace_node(self, Py_BuildValue("(O)", walk));

    PyObject* ret = Py_BuildValue("(OO)", walk, walk1);
    return ret;
}

static PyObject* RedBlackTree_delete(RedBlackTree* self, PyObject *args, PyObject *kwds) {
    PyObject* key = PyObject_GetItem(args, PyZero);
    BinaryTree* bt = self->sbbt->bst->binary_tree;

    PyObject* walk = BinarySearchTree_search(self->sbbt->bst, Py_BuildValue("(O)", key), PyDict_New());
    if (walk != Py_None) {
        PyObject* walk1 = RedBlackTree__replace_node(self, Py_BuildValue("(O)", walk));
        if (RedBlackTree__has_two_child(self, Py_BuildValue("(O)", walk)) == Py_True) {
            PyObject* tup = RedBlackTree___two_child_case(self, Py_BuildValue("(O)", walk));
            walk = PyObject_GetItem(tup, PyZero);
            walk1 = PyObject_GetItem(tup, PyOne);
        }
        if (RedBlackTree__is_leaf(self, Py_BuildValue("(O)", walk)) == Py_True) {
            RedBlackTree___leaf_case(self, Py_BuildValue("(OO)", walk, walk1));
        }
        else if (RedBlackTree__has_one_child(self, Py_BuildValue("(O)", walk)) == Py_True) {
            RedBlackTree___one_child_case(self, Py_BuildValue("(OO)", walk, walk1));
        }
        Py_RETURN_TRUE;
    }
    else {
        Py_RETURN_NONE;
    }
    Py_RETURN_NONE;
}

static PyObject* RedBlackTree_search(RedBlackTree* self, PyObject *args, PyObject *kwds) {
    return BinarySearchTree_search(self->sbbt->bst, args, kwds);
}

static PyObject* RedBlackTree_root_idx(RedBlackTree *self, void *closure) {
    return self->sbbt->bst->binary_tree->root_idx;
}


static struct PyMethodDef RedBlackTree_PyMethodDef[] = {
    {"insert", (PyCFunction) RedBlackTree_insert, METH_VARARGS, NULL},
    {"delete", (PyCFunction) RedBlackTree_delete, METH_VARARGS | METH_KEYWORDS, NULL},
    {"search", (PyCFunction) RedBlackTree_search, METH_VARARGS | METH_KEYWORDS, NULL},
    {"lower_bound", (PyCFunction) RedBlackTree_lower_bound, METH_VARARGS | METH_KEYWORDS, NULL},
    {"upper_bound", (PyCFunction) RedBlackTree_upper_bound, METH_VARARGS | METH_KEYWORDS, NULL},
    {"_get_parent", (PyCFunction) RedBlackTree__get_parent, METH_VARARGS, NULL},
    {"_get_grand_parent", (PyCFunction) RedBlackTree__get_grand_parent, METH_VARARGS, NULL},
    {"_get_sibling", (PyCFunction) RedBlackTree__get_sibling, METH_VARARGS, NULL},
    {"_get_uncle", (PyCFunction) RedBlackTree__get_uncle, METH_VARARGS, NULL},
    {NULL}
};

static PyGetSetDef RedBlackTree_GetterSetters[] = {
    {"root_idx", (getter) RedBlackTree_root_idx, NULL, "returns the index of the tree's root", NULL},
    {NULL}  /* Sentinel */
};

static PyMemberDef RedBlackTree_PyMemberDef[] = {
    {"tree", T_OBJECT_EX, offsetof(RedBlackTree, tree), 0, "tree"},
    {NULL}  /* Sentinel */
};


static PyTypeObject RedBlackTreeType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "RedBlackTree",
    /* tp_basicsize */ sizeof(RedBlackTree),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor) RedBlackTree_dealloc,
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
    /* tp_str */ (reprfunc) RedBlackTree___str__,
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
    /* tp_methods */ RedBlackTree_PyMethodDef,
    /* tp_members */ RedBlackTree_PyMemberDef,
    /* tp_getset */ RedBlackTree_GetterSetters,
    /* tp_base */ &SelfBalancingBinaryTreeType,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ RedBlackTree___new__,
};

#endif
