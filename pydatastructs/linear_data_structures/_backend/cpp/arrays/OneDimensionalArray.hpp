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
    if (self->_data) {
        for (size_t i = 0; i < self->_size; i++) {
            Py_XDECREF(self->_data[i]);
        }
        std::free(self->_data);
        self->_data = nullptr;
    }
    Py_XDECREF(self->_dtype);
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static void cleanup_partial_data(PyObject** data, size_t count) {
    if (data) {
        for (size_t i = 0; i < count; i++) {
            Py_XDECREF(data[i]);
        }
        std::free(data);
    }
}

static PyObject* OneDimensionalArray___new__(PyTypeObject* type, PyObject *args,
                                             PyObject *kwds) {
    OneDimensionalArray *self;
    self = reinterpret_cast<OneDimensionalArray*>(type->tp_alloc(type, 0));
    if (!self) return NULL;

    self->_data = nullptr;
    self->_dtype = nullptr;
    self->_size = 0;

    size_t len_args = PyObject_Length(args);
    if (len_args < 0) return NULL;

    PyObject *dtype = PyObject_GetItem(args, PyZero);
    if (!dtype) return NULL;

    if (dtype == Py_None) {
        Py_DECREF(dtype);
        PyErr_SetString(PyExc_ValueError, "Data type is not defined.");
        return NULL;
    }

    self->_dtype = dtype;

    if (len_args != 2 && len_args != 3) {
        PyErr_SetString(PyExc_ValueError,
                        "Too few arguments to create a 1D array,"
                        " pass either size of the array"
                        " or list of elements or both.");
        return NULL;
    }

    if (len_args == 3) {
        PyObject *args0 = PyObject_GetItem(args, PyOne);
        PyObject *args1 = PyObject_GetItem(args, PyTwo);
        if (!args0 || !args1) {
            Py_XDECREF(args0);
            Py_XDECREF(args1);
            return NULL;
        }
        size_t size;
        PyObject *data = NULL;
        if ((PyList_Check(args0) || PyTuple_Check(args0)) && PyLong_Check(args1)) {
            size = PyLong_AsUnsignedLong(args1);
            data = args0;
        } else if ((PyList_Check(args1) || PyTuple_Check(args1)) && PyLong_Check(args0)) {
            size = PyLong_AsUnsignedLong(args0);
            data = args1;
        } else {
            Py_DECREF(args0);
            Py_DECREF(args1);
            PyErr_SetString(PyExc_TypeError,
                            "Expected type of size is int and "
                            "expected type of data is list/tuple.");
            return NULL;
        }
        if (PyErr_Occurred()) {
            Py_DECREF(args0);
            Py_DECREF(args1);
            return NULL;
        }
        size_t len_data = PyObject_Length(data);
        if (len_data < 0) {
            Py_DECREF(args0);
            Py_DECREF(args1);
            return NULL;
        }
        if (size != len_data) {
            Py_DECREF(args0);
            Py_DECREF(args1);
            PyErr_Format(PyExc_ValueError,
                         "Conflict in the size, %zu and length of data, %zu",
                         size, len_data);
            return NULL;
        }
        self->_size = size;
        self->_data = reinterpret_cast<PyObject**>(std::calloc(size, sizeof(PyObject*)));
        if (!self->_data) {
            Py_DECREF(args0);
            Py_DECREF(args1);
            PyErr_NoMemory();
            return NULL;
        }
        for (size_t i = 0; i < size; i++) {
            PyObject* idx = PyLong_FromSize_t(i);
            if (!idx) {
                cleanup_partial_data(self->_data, i);
                self->_data = nullptr;
                Py_DECREF(args0);
                Py_DECREF(args1);
                return NULL;
            }

            PyObject* value = PyObject_GetItem(data, idx);
            Py_DECREF(idx);

            if (!value) {
                cleanup_partial_data(self->_data, i);
                self->_data = nullptr;
                Py_DECREF(args0);
                Py_DECREF(args1);
                return NULL;
            }

            if (raise_exception_if_dtype_mismatch(value, self->_dtype)) {
                Py_DECREF(value);
                cleanup_partial_data(self->_data, i);
                self->_data = nullptr;
                Py_DECREF(args0);
                Py_DECREF(args1);
                return NULL;
            }
            self->_data[i] = value;
        }
        Py_DECREF(args0);
        Py_DECREF(args1);

    } else if (len_args == 2) {
        PyObject *args0 = PyObject_GetItem(args, PyOne);
        if (!args0) return NULL;
        if (PyLong_Check(args0)) {
            self->_size = PyLong_AsSize_t(args0);
            if (PyErr_Occurred()) {
                Py_DECREF(args0);
                return NULL;
            }
            PyObject* init = nullptr;
            if (kwds) {
                PyObject* init_key = PyUnicode_FromString("init");
                if (init_key) {
                    init = PyObject_GetItem(kwds, init_key);
                    Py_DECREF(init_key);
                    if (!init) {
                        PyErr_Clear();
                        init = Py_None;
                        Py_INCREF(init);
                    }
                }
            }
            if (!init) {
                init = Py_None;
                Py_INCREF(init);
            }
            if (init != Py_None && raise_exception_if_dtype_mismatch(init, self->_dtype)) {
                Py_DECREF(init);
                Py_DECREF(args0);
                return NULL;
            }
            self->_data = reinterpret_cast<PyObject**>(std::calloc(self->_size, sizeof(PyObject*)));
            if (!self->_data) {
                Py_DECREF(init);
                Py_DECREF(args0);
                PyErr_NoMemory();
                return NULL;
            }

            for (size_t i = 0; i < self->_size; i++) {
                Py_INCREF(init);
                self->_data[i] = init;
            }
            Py_DECREF(init);

        } else if (PyList_Check(args0) || PyTuple_Check(args0)) {
            Py_ssize_t size_ssize = PyObject_Length(args0);
            if (size_ssize < 0) {
                Py_DECREF(args0);
                return NULL;
            }
            self->_size = (size_t)size_ssize;
            self->_data = reinterpret_cast<PyObject**>(std::calloc(self->_size, sizeof(PyObject*)));
            if (!self->_data) {
                Py_DECREF(args0);
                PyErr_NoMemory();
                return NULL;
            }

            for (size_t i = 0; i < self->_size; i++) {
                PyObject* idx = PyLong_FromSize_t(i);
                if (!idx) {
                    cleanup_partial_data(self->_data, i);
                    self->_data = nullptr;
                    Py_DECREF(args0);
                    return NULL;
                }

                PyObject* value = PyObject_GetItem(args0, idx);
                Py_DECREF(idx);

                if (!value) {
                    cleanup_partial_data(self->_data, i);
                    self->_data = nullptr;
                    Py_DECREF(args0);
                    return NULL;
                }

                if (raise_exception_if_dtype_mismatch(value, self->_dtype)) {
                    Py_DECREF(value);
                    cleanup_partial_data(self->_data, i);
                    self->_data = nullptr;
                    Py_DECREF(args0);
                    return NULL;
                }

                self->_data[i] = value;
            }
        } else {
            Py_DECREF(args0);
            PyErr_SetString(PyExc_TypeError,
                            "Expected type of size is int and "
                            "expected type of data is list/tuple.");
            return NULL;
        }
        Py_DECREF(args0);
    }
    return reinterpret_cast<PyObject*>(self);
}

static PyObject* OneDimensionalArray___getitem__(OneDimensionalArray *self,
                                                 PyObject* arg) {
    if (!PyLong_Check(arg)) {
        PyErr_SetString(PyExc_TypeError, "Index must be an integer");
        return NULL;
    }

    long long idx_ll = PyLong_AsLongLong(arg);
    if (PyErr_Occurred()) return NULL;

    if (idx_ll < 0 || idx_ll >= (long long)self->_size) {
        PyErr_Format(PyExc_IndexError,
                     "Index %lld out of range [0, %zu)",
                     idx_ll, self->_size);
        return NULL;
    }

    size_t idx = (size_t)idx_ll;
    PyObject* result = self->_data[idx];

    Py_INCREF(result);
    return result;
}

static int OneDimensionalArray___setitem__(OneDimensionalArray *self,
                                          PyObject* arg, PyObject* value) {
    if (!PyLong_Check(arg)) {
        PyErr_SetString(PyExc_TypeError, "Index must be an integer");
        return -1;
    }

    if (!value) {
        PyErr_SetString(PyExc_ValueError, "Cannot delete array elements");
        return -1;
    }

    long long idx_ll = PyLong_AsLongLong(arg);
    if (PyErr_Occurred()) return -1;

    if (idx_ll < 0 || idx_ll >= (long long)self->_size) {
        PyErr_Format(PyExc_IndexError,
                     "Index %lld out of range [0, %zu)",
                     idx_ll, self->_size);
        return -1;
    }

    size_t idx = (size_t)idx_ll;

    if (value != Py_None) {
        if (set_exception_if_dtype_mismatch(value, self->_dtype)) {
            return -1;
        }
    }
    PyObject* old_value = self->_data[idx];
    Py_INCREF(value);
    self->_data[idx] = value;
    Py_XDECREF(old_value);

    return 0;
}

static PyObject* OneDimensionalArray_fill(OneDimensionalArray *self, PyObject *args) {
    if (PyTuple_Size(args) != 1) {
        PyErr_SetString(PyExc_TypeError, "fill() takes exactly one argument");
        return NULL;
    }

    PyObject* value = PyTuple_GetItem(args, 0);  // Borrowed reference
    if (!value) return NULL;

    if (value != Py_None && raise_exception_if_dtype_mismatch(value, self->_dtype)) {
        return NULL;
    }

    for (size_t i = 0; i < self->_size; i++) {
        PyObject* old_value = self->_data[i];
        Py_INCREF(value);
        self->_data[i] = value;
        Py_XDECREF(old_value);
    }

    Py_RETURN_NONE;
}

static Py_ssize_t OneDimensionalArray___len__(OneDimensionalArray *self) {
    return (Py_ssize_t)self->_size;
}

static PyObject* OneDimensionalArray___str__(OneDimensionalArray *self) {
    return __str__(self->_data, self->_size);
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
