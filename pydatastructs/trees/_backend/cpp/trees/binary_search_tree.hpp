#include <Python.h>
#include <structmember.h>

// Define TreeNode struct.
// Defines a C struct TreeNode that represents a node in the binary search tree.
// It contains pointers to key, data, left, right, and parent.
typedef struct {
    PyObject_HEAD
    PyObject* key;
    PyObject* data;
    PyObject* left;
    PyObject* right;
    PyObject* parent;
    PyObject* size;
} TreeNode;

// Define BinarySearchTree class.
// Defines a C struct BinarySearchTree that represents the binary search tree.
// It extends the BinaryTree class.
typedef struct {
    PyObject_VAR_HEAD
    PyObject* left_size;
    PyObject* right_size;
    PyObject* _update_size;
    PyObject* insert;
    PyObject* search;
    PyObject* _bound_helper;
    PyObject* lower_bound;
    PyObject* tree;  // Define tree attribute
    PyObject* root_idx; // Define root_idx attribute
} BinarySearchTree;


// Type object for TreeNode
static PyTypeObject TreeNodeType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "TreeNode",                     /* tp_name */
    sizeof(TreeNode),               /* tp_basicsize */
    0,                              /* tp_itemsize */
    0,                              /* tp_dealloc */
    0,                              /* tp_print */
    0,                              /* tp_getattr */
    0,                              /* tp_setattr */
    0,                              /* tp_reserved */
    0,                              /* tp_repr */
    0,                              /* tp_as_number */
    0,                              /* tp_as_sequence */
    0,                              /* tp_as_mapping */
    0,                              /* tp_hash */
    0,                              /* tp_call */
    0,                              /* tp_str */
    0,                              /* tp_getattro */
    0,                              /* tp_setattro */
    0,                              /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,             /* tp_flags */
    "TreeNode objects",             /* tp_doc */
};


// Deallocation function for BinarySearchTree.
// Defines a deallocation function for BinarySearchTree.
static void BinarySearchTree_dealloc(BinarySearchTree* self) {
    Py_XDECREF(self->left_size);
    Py_XDECREF(self->right_size);
    Py_XDECREF(self->_update_size);
    Py_XDECREF(self->insert);
    Py_XDECREF(self->search);
    Py_XDECREF(self->_bound_helper);
    Py_XDECREF(self->lower_bound);
    Py_XDECREF(self->tree);  // Release memory for the tree attribute

    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

// Object creation function for BinarySearchTree.
// Defines a new object creation function for BinarySearchTree.
static PyObject* BinarySearchTree_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    BinarySearchTree* self;
    self = reinterpret_cast<BinarySearchTree*>(type->tp_alloc(type, 0));

    // Initialize tree attribute as an empty list
    if (self != NULL) {
        self->tree = PyList_New(0);
        if (self->tree == NULL) {
            Py_DECREF(self);
            return NULL;
        }
    }
    return reinterpret_cast<PyObject*>(self);
}

// Method to update the size of nodes in the tree.
static PyObject* BinarySearchTree_update_size(BinarySearchTree* self, PyObject* args) {
    PyObject* start_idx;

    if (!PyArg_ParseTuple(args, "O", &start_idx)) {
        return NULL;
    }

    // Walk through the tree and update sizes
    PyObject* walk = start_idx;
    while (walk != Py_None) {
        // Get the node at walk index
        TreeNode* node = (TreeNode*)PyList_GetItem(self->tree, PyLong_AsSsize_t(walk));
        if (node == NULL) {
            PyErr_SetString(PyExc_IndexError, "Invalid node index");
            return NULL;
        }

        // Calculate size of current node
        PyObject* left_size = PyObject_CallMethod((PyObject*)self, "left_size", "O", (PyObject*)node);
        PyObject* right_size = PyObject_CallMethod((PyObject*)self, "right_size", "O", (PyObject*)node);
        if (left_size == NULL || right_size == NULL) {
            Py_XDECREF(left_size);
            Py_XDECREF(right_size);
            return NULL;
        }
        PyObject* size = PyNumber_Add(PyNumber_Add(left_size, right_size), PyLong_FromLong(1));
        if (size == NULL) {
            Py_DECREF(left_size);
            Py_DECREF(right_size);
            return NULL;
        }

        // Update size attribute of current node
        Py_XDECREF(node->size);
        node->size = size;

        // Move to parent node
        PyObject* parent = node->parent;
        Py_XDECREF(walk);
        walk = parent;
    }

    Py_RETURN_NONE;
}

// Method to insert a new node into the tree.
static PyObject* BinarySearchTree_insert(BinarySearchTree* self, PyObject* args) {

    // Check if root_idx is None, initialize it if so
    if (self->root_idx == Py_None) {
        self->root_idx = PyLong_FromLong(0); // Or initialize it to the appropriate value
    }
    
    PyObject* key;
    PyObject* data = NULL;

    if (!PyArg_ParseTuple(args, "O|O", &key, &data)) {
        return NULL;
    }

    // Search for the key in the tree
    PyObject* search_args = PyTuple_Pack(1, key);
    PyObject* res = PyObject_CallMethod((PyObject*)self, "search", "O", search_args);
    Py_DECREF(search_args);
    if (res == NULL) {
        return NULL;
    }

    // If key is found, update data and return
    if (res != Py_None) {
        TreeNode* node = (TreeNode*)PyList_GetItem(self->tree, PyLong_AsSsize_t(res));
        if (node == NULL) {
            PyErr_SetString(PyExc_IndexError, "Invalid node index");
            Py_DECREF(res);
            return NULL;
        }
        Py_XDECREF(node->data);
        node->data = data;
        Py_DECREF(res);
        Py_RETURN_NONE;
    }
    Py_DECREF(res);

    // Insert new node
    PyObject* walk = self->root_idx;
    if (PyObject_RichCompareBool(((TreeNode*)PyList_GetItem(self->tree, PyLong_AsSsize_t(walk)))->key, Py_None, Py_EQ)) {
        ((TreeNode*)PyList_GetItem(self->tree, PyLong_AsSsize_t(walk)))->key = key;
        ((TreeNode*)PyList_GetItem(self->tree, PyLong_AsSsize_t(walk)))->data = data;
        Py_RETURN_NONE;
    }

    // Initialize new node
    TreeNode* new_node = PyObject_New(TreeNode, &TreeNodeType);
    if (new_node == NULL) {
        return NULL;
    }
    new_node->key = key;
    new_node->data = data;
    new_node->left = Py_None;
    new_node->right = Py_None;
    new_node->parent = Py_None;
    new_node->size = PyLong_FromLong(1);

    PyObject* prev_node = self->root_idx;
    bool flag = true;
    while (flag) {
        int cmp = PyObject_RichCompareBool(((TreeNode*)PyList_GetItem(self->tree, PyLong_AsSsize_t(walk)))->key, key, Py_LT);
        if (cmp < 0) {
            PyErr_SetString(PyExc_RuntimeError, "Comparison error");
            Py_DECREF(new_node);
            return NULL;
        }
        if (cmp) {
            if (((TreeNode*)PyList_GetItem(self->tree, PyLong_AsSsize_t(walk)))->right == Py_None) {
                new_node->parent = prev_node;
                PyList_Append(self->tree, (PyObject*)new_node);
                ((TreeNode*)PyList_GetItem(self->tree, PyList_Size(self->tree) - 1))->size = PyLong_FromLong(1);
                ((TreeNode*)PyList_GetItem(self->tree, PyLong_AsSsize_t(walk)))->right = PyLong_FromSsize_t(PyList_Size(self->tree) - 1);
                flag = false;
            }
            prev_node = walk;
            walk = ((TreeNode*)PyList_GetItem(self->tree, PyLong_AsSsize_t(walk)))->right;
        } else {
            if (((TreeNode*)PyList_GetItem(self->tree, PyLong_AsSsize_t(walk)))->left == Py_None) {
                new_node->parent = prev_node;
                PyList_Append(self->tree, (PyObject*)new_node);
                ((TreeNode*)PyList_GetItem(self->tree, PyList_Size(self->tree) - 1))->size = PyLong_FromLong(1);
                ((TreeNode*)PyList_GetItem(self->tree, PyLong_AsSsize_t(walk)))->left = PyLong_FromSsize_t(PyList_Size(self->tree) - 1);
                flag = false;
            }
            prev_node = walk;
            walk = ((TreeNode*)PyList_GetItem(self->tree, PyLong_AsSsize_t(walk)))->left;
        }
    }
    PyObject* update_args = PyTuple_Pack(1, prev_node);
    PyObject* update_res = PyObject_CallMethod((PyObject*)self, "_update_size", "O", update_args);
    Py_DECREF(update_args);
    if (update_res == NULL) {
        Py_DECREF(new_node);
        return NULL;
    }
    Py_DECREF(update_res);

    Py_RETURN_NONE;
}


// Method to search for a key in the tree.
static PyObject* BinarySearchTree_search(BinarySearchTree* self, PyObject* args) {
    PyObject* key;

    if (!PyArg_ParseTuple(args, "O", &key)) {
        return NULL;
    }

    // Implement search logic here

    Py_RETURN_NONE;
}

// Method definitions for BinarySearchTree
static PyMethodDef BinarySearchTree_methods[] = {
    {"_update_size", (PyCFunction)BinarySearchTree_update_size, METH_VARARGS, "Updates the size of nodes in the tree."},
    {"insert", (PyCFunction)BinarySearchTree_insert, METH_VARARGS, "Inserts a new node into the tree."},
    {"search", (PyCFunction)BinarySearchTree_search, METH_VARARGS, "Searches for a key in the tree."},
    {NULL}
};

// Type object for BinarySearchTree
static PyTypeObject BinarySearchTreeType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "BinarySearchTree",            /* tp_name */
    sizeof(BinarySearchTree),      /* tp_basicsize */
    0,                             /* tp_itemsize */
    (destructor)BinarySearchTree_dealloc, /* tp_dealloc */
    0,                             /* tp_print */
    0,                             /* tp_getattr */
    0,                             /* tp_setattr */
    0,                             /* tp_reserved */
    0,                             /* tp_repr */
    0,                             /* tp_as_number */
    0,                             /* tp_as_sequence */
    0,                             /* tp_as_mapping */
    0,                             /* tp_hash */
    0,                             /* tp_call */
    0,                             /* tp_str */
    0,                             /* tp_getattro */
    0,                             /* tp_setattro */
    0,                             /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,            /* tp_flags */
    "BinarySearchTree objects",    /* tp_doc */
    0,                             /* tp_traverse */
    0,                             /* tp_clear */
    0,                             /* tp_richcompare */
    0,                             /* tp_weaklistoffset */
    0,                             /* tp_iter */
    0,                             /* tp_iternext */
    BinarySearchTree_methods,      /* tp_methods */
    0,                             /* tp_members */
    0,                             /* tp_getset */
    0,                             /* tp_base */
    0,                             /* tp_dict */
    0,                             /* tp_descr_get */
    0,                             /* tp_descr_set */
    0,                             /* tp_dictoffset */
    0,                             /* tp_init */
    0,                             /* tp_alloc */
    BinarySearchTree_new,          /* tp_new */
};

// Module definition for the binarysearchtree module
static PyModuleDef binarysearchtreemodule = {
    PyModuleDef_HEAD_INIT,
    "binarysearchtree",     // Module name
    NULL,                   // Module documentation
    -1,
    NULL, NULL, NULL, NULL, NULL
};

// Module initialization function
PyMODINIT_FUNC PyInit_binarysearchtree(void) {
    PyObject* m;
    if (PyType_Ready(&BinarySearchTreeType) < 0) {
        return NULL;
    }

    m = PyModule_Create(&binarysearchtreemodule);
    if (m == NULL) {
        return NULL;
    }

    Py_INCREF(&BinarySearchTreeType);
    PyModule_AddObject(m, "BinarySearchTree", reinterpret_cast<PyObject*>(&BinarySearchTreeType));

    return m;
}