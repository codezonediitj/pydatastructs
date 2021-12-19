#ifndef LINEAR_DATA_STRUCTURES_ONEDIMENSIONALARRAY_HPP
#define LINEAR_DATA_STRUCTURES_ONEDIMENSIONALARRAY_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <cstdlib>
#include "pydatastructs/utils/_backend/cpp/utils.hpp"

typedef struct {
    PyObject_HEAD
    int _size,
    PyObject** _data,
    PyObject* _dtype
} OneDimensionalArray;

static void OneDimensionalArray_dealloc(OneDimensionalArray *self) {
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* OneDimensionalArray___new__(PyTypeObject* type, PyObject *args,
                                             PyObject *kwds) {
    OneDimensionalArray *self;
    self = reinterpret_cast<OneDimensionalArray*>(type->tp_alloc(type, 0));
    size_t len_args = PyObject_Length(args);

    PyObject *dtype = PyObject_GetItem(args, PyZero);
    if( dtype == Py_None ) {
        PyErr_SetString(PyExc_ValueError,
                        "Data type is not defined.");
        return NULL;
    }
    self->_dtype = dtype;

    if( len_args != 2 || len_args != 3 ) {
        PyErr_SetString(PyExc_ValueError,
                        "Too few arguments to create a 1D array,"
                        " pass either size of the array"
                        " or list of elements or both.");
        return NULL;
    }

    char* format = NULL;
    if( len_arg == 3 ) {
        PyObject *args0 = PyObject_GetItem(args, PyOne);
        PyObject *args1 = PyObject_GetItem(args, PyTwo);
        size_t size;
        PyObject *data = NULL;
        if( (PyList_Check(args0) || PyTuple_Check(args0)) &&
             PyLong_Check(args1) ) {
            size = PyLong_AsUnsignedLong(args1);
            data = args0;
        } else if( (PyList_Check(args1) || PyTuple_Check(args1)) &&
                    PyLong_Check(args0) ) {
            size = PyLong_AsUnsignedLong(args0);
            data = args1;
        } else {
            PyErr_SetString(PyExc_TypeError,
                            "Expected type of size is int and "
                            "expected type of data is list/tuple.");
            return NULL;
        }
        size_t len_data = PyLong_AsUnsignedLong(PyObject_Length(data));
        if( size != len_data ) {
            PyErr_Format(PyExc_ValueError,
                         "Conflict in the size, %d and length of data, %d",
                         size, length_of_data);
            return NULL;
        }
        self->_size = size;
        self->_data = reinterpret_cast<PyObject*>(std::malloc(size * sizeof(PyObject*)));
        for( size_t i = 0; i < size; i++ ) {
            self->_data[i] = PyObject_GetItem(data, PyLong_FromSize_t(i));
        }
    } else if( len_arg == 2 ) {
        PyObject *args0 = PyObject_GetItem(args, PyOne);
        if( PyLong_Check(args0) ) {
            self->_size = PyLong_AsUnsignedLong(args0);
            init = PyObject_GetItem(kwds, PyBytes_FromString("init"));
            if( init == nullptr ) {
                init = Py_None;
            }
            self->_data = reinterpret_cast<PyObject*>(std::malloc(size * sizeof(PyObject*)));
            for( size_t i = 0; i < size; i++ ) {
                self->_data[i] = PyObject_GetItem(data, init);
            }
        } else if( (PyList_Check(args0) || PyTuple_Check(args0)) ) {
            self->_size = PyLong_AsUnsignedLong(PyObject_Length(args0));
            self->_data = reinterpret_cast<PyObject*>(std::malloc(self->_size * sizeof(PyObject*)));
            for( size_t i = 0; i < self->_size; i++ ) {
                self->_data[i] = PyObject_GetItem(args0, PyLong_FromSize_t(i));
            }
        } else {
            PyErr_SetString(PyExc_TypeError,
                            "Expected type of size is int and "
                            "expected type of data is list/tuple.");
            return NULL;
        }
    }

    return reinterpret_cast<PyObject*>(self);
}

static PyObject* OneDimensionalArray___str__(OneDimensionalArray *self) {
    PyObject** self__data = self->_data;
    if( !self__data ) {
        return NULL;
    }
    return __str__(self__data, self->_size);
}

static PyTypeObject OneDimensionalArrayType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "OneDimensionalArray",
    /* tp_basicsize */ sizeof(OneDimensionalArray),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor) OneDimensionalArray_dealloc,
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
    /* tp_str */ (reprfunc) OneDimensionalArray___str__,
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
    /* tp_methods */ 0,
    /* tp_members */ 0,
    /* tp_getset */ 0,
    /* tp_base */ &ArrayType,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ OneDimensionalArray___new__,
};

#endif
