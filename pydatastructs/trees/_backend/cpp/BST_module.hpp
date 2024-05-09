//
//  BST_module.h
//  BST
//
//  Created by dwd on 12/27/17.
//  Copyright © 2017 holdendou. All rights reserved.
//

#ifndef BST_module_h
#define BST_module_h

#include <stdio.h>
#include <Python.h>
#include <structmember.h>

typedef struct {
    PyObject_HEAD
    PyObject* key;
    PyObject* data;
    PyObject* left;
    PyObject* right;
} BST;

static PyMemberDef BSTMembers[] = {
    {"key", T_OBJECT_EX, offsetof(BST, key), 0, "key of BST node"},
    {"data", T_OBJECT_EX, offsetof(BST, data), 0, "data of a BST node"},
    {"left", T_OBJECT_EX, offsetof(BST, left), 0, "left child"},
    {"right", T_OBJECT_EX, offsetof(BST, right), 0, "right child"},
    {NULL}
};

static PyObject* BSTListify(BST* self);
static PyObject* BSTInsert(BST* self, PyObject* args, PyObject* kwargs);
static PyObject* BSTSearch(BST* self, PyObject* args);

static PyMethodDef BSTMethods[] = {
    {
        "listify",
        (PyCFunction)BSTListify,
        METH_NOARGS,
        "inorder traversal of the binary tree"
    },
    {
        "insert",
        (PyCFunction)BSTInsert,
        METH_VARARGS | METH_KEYWORDS,
        "insert an element"
    },
    {
        "search",
        (PyCFunction)BSTSearch,
        METH_VARARGS,
        "search for an element in the binary tree"
    },
    {NULL}
};

#endif /* BST_module_h */
