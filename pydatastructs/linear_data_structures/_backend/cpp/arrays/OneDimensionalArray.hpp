#ifndef LINEAR_DATA_STRUCTURES_ONEDIMENSIONALARRAY_HPP
#define LINEAR_DATA_STRUCTURES_ONEDIMENSIONALARRAY_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <cstdlib>
#include "Array.hpp"
#include "../../../../utils/_backend/cpp/utils.hpp"

typedef struct {
    PyObject_HEAD
    size_t _size;
    PyObject** _data;
    PyObject* _dtype;
} OneDimensionalArray;

static void OneDimensionalArray_dealloc(OneDimensionalArray *self) {
    std::free(self->_data);
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* OneDimensionalArray___new__(PyTypeObject* type, PyObject *args,
                                             PyObject *kwds) {
    OneDimensionalArray *self;
    self = reinterpret_cast<OneDimensionalArray*>(type->tp_alloc(type, 0));
    size_t len_args = PyObject_Length(args);

    PyObject *dtype = PyObject_GetItem(args, PyZero);
    if ( dtype == Py_None ) {
        PyErr_SetString(PyExc_ValueError,
                        "Data type is not defined.");
        return NULL;
    }
    self->_dtype = dtype;

    if ( len_args != 2 && len_args != 3 ) {
        PyErr_SetString(PyExc_ValueError,
                        "Too few arguments to create a 1D array,"
                        " pass either size of the array"
                        " or list of elements or both.");
        return NULL;
    }

    if ( len_args == 3 ) {
        PyObject *args0 = PyObject_GetItem(args, PyOne);
        PyObject *args1 = PyObject_GetItem(args, PyTwo);
        size_t size;
        PyObject *data = NULL;
        if ( (PyList_Check(args0) || PyTuple_Check(args0)) &&
             PyLong_Check(args1) ) {
            size = PyLong_AsUnsignedLong(args1);
            data = args0;
        } else if ( (PyList_Check(args1) || PyTuple_Check(args1)) &&
                    PyLong_Check(args0) ) {
            size = PyLong_AsUnsignedLong(args0);
            data = args1;
        } else {
            PyErr_SetString(PyExc_TypeError,
                            "Expected type of size is int and "
                            "expected type of data is list/tuple.");
            return NULL;
        }
        size_t len_data = PyObject_Length(data);
        if ( size != len_data ) {
            PyErr_Format(PyExc_ValueError,
                         "Conflict in the size, %d and length of data, %d",
                         size, len_data);
            return NULL;
        }
        self->_size = size;
        self->_data = reinterpret_cast<PyObject**>(std::malloc(size * sizeof(PyObject*)));
        for( size_t i = 0; i < size; i++ ) {
            PyObject* value = PyObject_GetItem(data, PyLong_FromSize_t(i));
            if ( raise_exception_if_dtype_mismatch(value, self->_dtype) ) {
                return NULL;
            }
            self->_data[i] = value;
        }
    } else if ( len_args == 2 ) {
        PyObject *args0 = PyObject_GetItem(args, PyOne);
        if ( PyLong_Check(args0) ) {
            self->_size = PyLong_AsSize_t(args0);
            PyObject* init = PyObject_GetItem(kwds, PyUnicode_FromString("init"));
            if ( init == nullptr ) {
                PyErr_Clear();
                init = Py_None;
            } else if ( raise_exception_if_dtype_mismatch(init, self->_dtype) ) {
                return NULL;
            }
            self->_data = reinterpret_cast<PyObject**>(std::malloc(self->_size * sizeof(PyObject*)));
            for( size_t i = 0; i < self->_size; i++ ) {
                self->_data[i] = init;
            }
        } else if ( (PyList_Check(args0) || PyTuple_Check(args0)) ) {
            self->_size = PyObject_Length(args0);
            self->_data = reinterpret_cast<PyObject**>(std::malloc(self->_size * sizeof(PyObject*)));
            for( size_t i = 0; i < self->_size; i++ ) {
                PyObject* value = PyObject_GetItem(args0, PyLong_FromSize_t(i));
                if ( raise_exception_if_dtype_mismatch(value, self->_dtype) ) {
                    return NULL;
                }
                self->_data[i] = value;
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

static PyObject* OneDimensionalArray___getitem__(OneDimensionalArray *self,
                                                 PyObject* arg) {
    size_t idx = PyLong_AsUnsignedLong(arg);
    if ( idx >= self->_size ) {
        PyErr_Format(PyExc_IndexError,
                     "Index, %d, out of range, [%d, %d)",
                     idx, 0, self->_size);
        return NULL;
    }
    Py_INCREF(self->_data[idx]);
    return self->_data[idx];
}

static int OneDimensionalArray___setitem__(OneDimensionalArray *self,
                                                 PyObject* arg, PyObject* value) {
    size_t idx = PyLong_AsUnsignedLong(arg);
    if ( value == Py_None ) {
        self->_data[idx] = value;
    } else if ( !set_exception_if_dtype_mismatch(value, self->_dtype) ) {
        self->_data[idx] = value;
    }
    return 0;
}

static PyObject* OneDimensionalArray_fill(OneDimensionalArray *self, PyObject *args) {
    PyObject* value = PyObject_GetItem(args, PyZero);
    if ( raise_exception_if_dtype_mismatch(value, self->_dtype) ) {
        return NULL;
    }

    for( size_t i = 0; i < self->_size; i++ ) {
        self->_data[i] = value;
    }

    Py_RETURN_NONE;
}

static Py_ssize_t OneDimensionalArray___len__(OneDimensionalArray *self) {
    return self->_size;
}

static PyObject* OneDimensionalArray___str__(OneDimensionalArray *self) {
    PyObject** self__data = self->_data;
    return __str__(self__data, self->_size);
}

static PyMappingMethods OneDimensionalArray_PyMappingMethods = {
    (lenfunc) OneDimensionalArray___len__,
    (binaryfunc) OneDimensionalArray___getitem__,
    (objobjargproc) OneDimensionalArray___setitem__,
};

static struct PyMethodDef OneDimensionalArray_PyMethodDef[] = {
    {"fill", (PyCFunction) OneDimensionalArray_fill, METH_VARARGS, NULL},
    {NULL}
};

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
    /* tp_as_mapping */ &OneDimensionalArray_PyMappingMethods,
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
    /* tp_methods */ OneDimensionalArray_PyMethodDef,
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
