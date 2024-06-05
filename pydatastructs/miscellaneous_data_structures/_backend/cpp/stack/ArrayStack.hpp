#ifndef MISCELLANEOUS_DATA_STRUCTURES_ARRAYSTACK_HPP
#define MISCELLANEOUS_DATA_STRUCTURES_ARRAYSTACK_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <cstdlib>
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
    ArrayStack *self = reinterpret_cast<ArrayStack*>(type->tp_alloc(type, 0));

    static char *kwlist[] = {"items", "dtype", NULL};
    PyObject *initial_values = Py_None, *dtype = Py_None;
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|OO", kwlist, &initial_values, &dtype)) {
        PyErr_SetString(PyExc_ValueError, "Error creating ArrayStack");
        return NULL;
    }

    if (initial_values != Py_None && PyType_Check(initial_values)) {
        PyErr_SetString(PyExc_TypeError, "`items` must be an instance of list or tuple, received a type instead\n"
                                         "Did you mean to instantiate an ArrayStack with only the data type? "
                                         "if so, send the type parameter as a named argument "
                                         "for example: dtype=int");
        return NULL;
    }

    PyObject* items = NULL;
    PyObject* doda_kwds = Py_BuildValue("{}");
    if (initial_values == Py_None) {
        // If the only argument is the dtype, redefine the args as a tuple (dtype, 0)
        // where 0 is the initial array size
        PyObject* extended_args = PyTuple_Pack(2, dtype, PyLong_FromLong(0));

        items = DynamicOneDimensionalArray___new__(&DynamicOneDimensionalArrayType, extended_args, doda_kwds);
    } else {
        // If the user provides dtype and initial values list, let the array initializer handle the checks.
        PyObject* doda_args = PyTuple_Pack(2, dtype, initial_values);
        items = DynamicOneDimensionalArray___new__(&DynamicOneDimensionalArrayType, doda_args, doda_kwds);
    }

    if (!items) {
        return NULL;
    }

    DynamicOneDimensionalArray* tmp = self->_items;
    self->_items = reinterpret_cast<DynamicOneDimensionalArray*>(items);

    return reinterpret_cast<PyObject*>(self);
}

static PyObject* ArrayStack_is_empty(ArrayStack *self) {
    bool is_empty = self->_items->_last_pos_filled == -1;

    if (is_empty) {
        Py_RETURN_TRUE;
    }

    Py_RETURN_FALSE;
}

static PyObject* ArrayStack_push(ArrayStack *self, PyObject* args) {
    size_t len_args = PyObject_Length(args);
    if (len_args != 1) {
        PyErr_SetString(PyExc_ValueError, "Expected one argument");
        return NULL;
    }

    if (PyObject_IsTrue(ArrayStack_is_empty(self))) {
        self->_items->_one_dimensional_array->_dtype = reinterpret_cast<PyObject*>(
            Py_TYPE(PyObject_GetItem(args, PyZero))
        );
    }

    DynamicOneDimensionalArray_append(self->_items, args);

    Py_RETURN_NONE;
}

static PyObject* ArrayStack_pop(ArrayStack *self) {
    if (PyObject_IsTrue(ArrayStack_is_empty(self))) {
        PyErr_SetString(PyExc_IndexError, "Stack is empty");
        return NULL;
    }

    PyObject *top_element = DynamicOneDimensionalArray___getitem__(
        self->_items, PyLong_FromLong(self->_items->_last_pos_filled)
    );

    PyObject* last_pos_arg = PyTuple_Pack(1, PyLong_FromLong(self->_items->_last_pos_filled));
    DynamicOneDimensionalArray_delete(self->_items, last_pos_arg);
    return top_element;
}

static PyObject* ArrayStack_peek(ArrayStack *self, void *closure) {
    return DynamicOneDimensionalArray___getitem__(
        self->_items, PyLong_FromLong(self->_items->_last_pos_filled)
    );
}

static Py_ssize_t ArrayStack__len__(ArrayStack *self) {
    return self->_items->_num;
}

static PyObject* ArrayStack__str__(ArrayStack* self) {
    return DynamicOneDimensionalArray___str__(self->_items);
}

static struct PyMethodDef ArrayStack_PyMethodDef[] = {
    {"push", (PyCFunction) ArrayStack_push, METH_VARARGS, NULL},
    {"pop", (PyCFunction) ArrayStack_pop, METH_VARARGS, NULL},
    {NULL}
};

static PyMappingMethods ArrayStack_PyMappingMethods = {
    (lenfunc) ArrayStack__len__,
};

static PyGetSetDef ArrayStack_GetterSetters[] = {
    {"peek", (getter) ArrayStack_peek, NULL, "peek top value", NULL},
    {"is_empty", (getter) ArrayStack_is_empty, NULL, "check if the stack is empty", NULL},
    {NULL}  /* Sentinel */
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
        /* tp_as_mapping */ &ArrayStack_PyMappingMethods,
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
        /* tp_getset */ ArrayStack_GetterSetters,
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
