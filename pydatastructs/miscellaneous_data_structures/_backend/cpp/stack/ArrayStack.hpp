#ifndef MISCELLANEOUS_DATA_STRUCTURES_ARRAYSTACK_HPP
#define MISCELLANEOUS_DATA_STRUCTURES_ARRAYSTACK_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <cstdlib>
#include <iostream>
#include <structmember.h>
#include "../../../../linear_data_structures/_backend/cpp/arrays/DynamicOneDimensionalArray.hpp"

typedef struct {
    PyObject_HEAD
    DynamicOneDimensionalArray* _items;
} ArrayStack;

static void ArrayStack_dealloc(ArrayStack *self) {
    DynamicOneDimensionalArray_dealloc(self->_items);
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* ArrayStack__new__(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    // args can be just the data type or a list of initial values and the data type

    ArrayStack *self = reinterpret_cast<ArrayStack*>(type->tp_alloc(type, 0));
    size_t len_args = PyObject_Length(args);

    if (len_args != 1 && len_args != 2) {
        PyErr_SetString(PyExc_ValueError,
                        "Too few arguments to create the stack,"
                        " pass either only the dtype, or"
                        " a list of initial values and the dtype");
        return NULL;
    }

    PyObject* items = NULL;
    PyObject* doda_kwds = Py_BuildValue("{}");
    if (len_args == 1) {
        // If the only argument is the dtype, redefine the args as a tuple (dtype, 0)
        // where 0 is the initial array size
        PyObject* dtype = PyObject_GetItem(args, PyZero);
        PyObject* extended_args = PyTuple_Pack(2, dtype, PyLong_FromLong(0));

        items = DynamicOneDimensionalArray___new__(&DynamicOneDimensionalArrayType, extended_args, doda_kwds);
    } else {
        // If the user provides dtype and initial values list, let the array initializer handle the checks.

        PyObject* doda_args = PyTuple_Pack(2, PyObject_GetItem(args, PyOne), PyObject_GetItem(args, PyZero));
        items = DynamicOneDimensionalArray___new__(&DynamicOneDimensionalArrayType, doda_args, doda_kwds);
    }

    if (!items) {
        return NULL;
    }

    DynamicOneDimensionalArray* tmp = self->_items;
    self->_items = reinterpret_cast<DynamicOneDimensionalArray*>(items);

    return reinterpret_cast<PyObject*>(self);
}

static PyObject* ArrayStack_push(ArrayStack *self, PyObject* args) {
    size_t len_args = PyObject_Length(args);
    if (len_args != 1) {
        PyErr_SetString(PyExc_ValueError, "Expected one argument");
        return NULL;
    }

    DynamicOneDimensionalArray_append(self->_items, args);

    Py_RETURN_NONE;
}

static PyObject* ArrayStack__str__(ArrayStack* self){
    return DynamicOneDimensionalArray___str__(self->_items);
}

static struct PyMethodDef ArrayStack_PyMethodDef[] = {
        {"push", (PyCFunction) ArrayStack_push, METH_VARARGS, NULL},
        {NULL}
};

static PyTypeObject ArrayStackType = {
        /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "ArrayStack",
        /* tp_basicsize */ sizeof(ArrayStack),
        /* tp_itemsize */ 0,
        /* tp_dealloc */ (destructor) ArrayStack_dealloc,
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
        /* tp_str */ (reprfunc) ArrayStack__str__,
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
        /* tp_methods */ ArrayStack_PyMethodDef,
        /* tp_members */ 0,
        /* tp_getset */ 0,
        /* tp_base */ 0,
        /* tp_dict */ 0,
        /* tp_descr_get */ 0,
        /* tp_descr_set */ 0,
        /* tp_dictoffset */ 0,
        /* tp_init */ 0,
        /* tp_alloc */ 0,
        /* tp_new */ ArrayStack__new__,
};


#endif
