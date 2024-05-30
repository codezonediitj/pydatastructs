#ifndef LINEAR_DATA_STRUCTURES_DYNAMICONEDIMENSIONALARRAY_HPP
#define LINEAR_DATA_STRUCTURES_DYNAMICONEDIMENSIONALARRAY_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <cstdlib>
#include "DynamicArray.hpp"
#include "OneDimensionalArray.hpp"
#include "../../../../utils/_backend/cpp/utils.hpp"

typedef struct {
    PyObject_HEAD
    OneDimensionalArray* _one_dimensional_array;
    double _load_factor;
    long _num;
    long _last_pos_filled;
    long _size;
} DynamicOneDimensionalArray;

static void DynamicOneDimensionalArray_dealloc(DynamicOneDimensionalArray *self) {
    OneDimensionalArray_dealloc(self->_one_dimensional_array);
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* DynamicOneDimensionalArray___new__(PyTypeObject* type, PyObject *args,
                                                    PyObject *kwds) {
    DynamicOneDimensionalArray *self;
    self = reinterpret_cast<DynamicOneDimensionalArray*>(type->tp_alloc(type, 0));
    if (PyType_Ready(&OneDimensionalArrayType) < 0) { // This has to be present to finalize a type object. This should be called on all type objects to finish their initialization.
        return NULL;
    }
    PyObject* _one_dimensional_array = OneDimensionalArray___new__(&OneDimensionalArrayType, args, kwds);
    if ( !_one_dimensional_array ) {
        return NULL;
    }
    self->_one_dimensional_array = reinterpret_cast<OneDimensionalArray*>(_one_dimensional_array);
    self->_size = (long) self->_one_dimensional_array->_size;

    PyObject* _load_factor = PyObject_GetItem(kwds, PyUnicode_FromString("load_factor"));
    if ( _load_factor == nullptr ) {
        PyErr_Clear();
        self->_load_factor = 0.25;
    } else {
        _load_factor = PyFloat_FromString(PyObject_Str(_load_factor));
        if ( !_load_factor ) {
            return NULL;
        }
        self->_load_factor = PyFloat_AS_DOUBLE(_load_factor);
    }
    if ( self->_one_dimensional_array->_size == 0 ||
        self->_one_dimensional_array->_data[0] == Py_None ) {
        self->_num = 0;
    } else {
        self->_num = (long) self->_one_dimensional_array->_size;
    }
    self->_last_pos_filled = (long) self->_num - 1;

    return reinterpret_cast<PyObject*>(self);
}

static PyObject* DynamicOneDimensionalArray___getitem__(DynamicOneDimensionalArray *self,
                                                        PyObject* arg) {
    return OneDimensionalArray___getitem__(self->_one_dimensional_array, arg);
}

static int DynamicOneDimensionalArray___setitem__(DynamicOneDimensionalArray *self,
                                                  PyObject* arg, PyObject* value) {
    return OneDimensionalArray___setitem__(self->_one_dimensional_array, arg, value);
}

static PyObject* DynamicOneDimensionalArray_fill(DynamicOneDimensionalArray *self, PyObject *args) {
    return OneDimensionalArray_fill(self->_one_dimensional_array, args);
}

static Py_ssize_t DynamicOneDimensionalArray___len__(DynamicOneDimensionalArray *self) {
    return self->_one_dimensional_array->_size;
}

static PyObject* DynamicOneDimensionalArray___str__(DynamicOneDimensionalArray *self) {
    PyObject** self__data = self->_one_dimensional_array->_data;
    return __str__(self__data, self->_one_dimensional_array->_size, self->_last_pos_filled);
}

static PyObject* DynamicOneDimensionalArray__modify(DynamicOneDimensionalArray *self,
                                                    PyObject* args) {
    PyObject* force = nullptr;
    if ( args ) {
        force = PyObject_GetItem(args, PyZero);
    }
    if ( !force ) {
        PyErr_Clear();
        force = Py_False;
    }

    long i, j;
    PyObject** _data = self->_one_dimensional_array->_data;
    long _size = (long) self->_one_dimensional_array->_size;
    if ( force == Py_True ) {
        i = -1;
        j = _size - 1;
        while ( _data[j] == Py_None) {
            i--;
            j--;
        }
        self->_last_pos_filled = i + _size;
    }

    if ( ((float) self->_num)/((float) _size) < self->_load_factor ) {
        long new_size = 2 * self->_num + 1;
        PyObject** arr_new = reinterpret_cast<PyObject**>(std::malloc(new_size * sizeof(PyObject*)));
        for( i = 0; i < new_size; i++ ) {
            Py_INCREF(Py_None);
            arr_new[i] = Py_None;
        }
        long j = 0;
        for( i = 0; i <= self->_last_pos_filled; i++ ) {
            if ( _data[i] != Py_None ) {
                Py_INCREF(Py_None);
                arr_new[j] = _data[i];
                j += 1;
            }
        }
        self->_last_pos_filled = j - 1;
        self->_one_dimensional_array->_data = arr_new;
        self->_one_dimensional_array->_size = new_size;
        self->_size = new_size;
    }

    Py_RETURN_NONE;
}

static PyObject* DynamicOneDimensionalArray_append(DynamicOneDimensionalArray *self,
                                                    PyObject* args) {
    PyObject* el = PyObject_GetItem(args, PyZero);
    if ( !el ) {
        return NULL;
    }

    long _size = (long) self->_one_dimensional_array->_size;
    PyObject** _data = self->_one_dimensional_array->_data;
    if ( self->_last_pos_filled + 1 == _size ) {
        long new_size = 2 * _size + 1;
        PyObject** arr_new = reinterpret_cast<PyObject**>(std::malloc(new_size * sizeof(PyObject*)));
        long i;
        for( i = 0; i <= self->_last_pos_filled; i++ ) {
            arr_new[i] = _data[i];
        }
        for( ; i < new_size; i++ ) {
            arr_new[i] = Py_None;
        }
        arr_new[self->_last_pos_filled + 1] = el;
        self->_one_dimensional_array->_size = new_size;
        self->_size = new_size;
        self->_one_dimensional_array->_data = arr_new;
    } else {
        _data[self->_last_pos_filled + 1] = el;
    }
    self->_last_pos_filled += 1;
    self->_num += 1;
    return DynamicOneDimensionalArray__modify(self, NULL);
}

static PyObject* DynamicOneDimensionalArray_delete(DynamicOneDimensionalArray *self,
                                                   PyObject* args) {
    PyObject* idx_pyobject = PyObject_GetItem(args, PyZero);
    if ( !idx_pyobject ) {
        return NULL;
    }
    long idx = PyLong_AsLong(idx_pyobject);
    if ( idx == -1 && PyErr_Occurred() ) {
        return NULL;
    }

    PyObject** _data = self->_one_dimensional_array->_data;
    if ( idx <= self->_last_pos_filled && idx >= 0 &&
        _data[idx] != Py_None ) {
        _data[idx] = Py_None;
        self->_num -= 1;
        if ( self->_last_pos_filled == idx ) {
            self->_last_pos_filled -= 1;
        }
        return DynamicOneDimensionalArray__modify(self, NULL);
    }

    Py_RETURN_NONE;
}

static PyMappingMethods DynamicOneDimensionalArray_PyMappingMethods = {
    (lenfunc) DynamicOneDimensionalArray___len__,
    (binaryfunc) DynamicOneDimensionalArray___getitem__,
    (objobjargproc) DynamicOneDimensionalArray___setitem__,
};

static struct PyMethodDef DynamicOneDimensionalArray_PyMethodDef[] = {
    {"fill", (PyCFunction) DynamicOneDimensionalArray_fill, METH_VARARGS, NULL},
    {"_modify", (PyCFunction) DynamicOneDimensionalArray__modify, METH_VARARGS, NULL},
    {"append", (PyCFunction) DynamicOneDimensionalArray_append, METH_VARARGS, NULL},
    {"delete", (PyCFunction) DynamicOneDimensionalArray_delete, METH_VARARGS, NULL},
    {NULL}
};

static struct PyMemberDef DynamicOneDimensionalArray_PyMemberDef[] = {
    {"size", T_LONG,
     offsetof(DynamicOneDimensionalArray, _size),
     READONLY, NULL},
    {"_num", T_LONG,
     offsetof(DynamicOneDimensionalArray, _num),
     READONLY, NULL},
    {"_last_pos_filled", T_LONG,
     offsetof(DynamicOneDimensionalArray, _last_pos_filled),
     READONLY, NULL},
    {NULL},
};

static PyTypeObject DynamicOneDimensionalArrayType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "DynamicOneDimensionalArray",
    /* tp_basicsize */ sizeof(DynamicOneDimensionalArray),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor) DynamicOneDimensionalArray_dealloc,
    /* tp_print */ 0,
    /* tp_getattr */ 0,
    /* tp_setattr */ 0,
    /* tp_reserved */ 0,
    /* tp_repr */ 0,
    /* tp_as_number */ 0,
    /* tp_as_sequence */ 0,
    /* tp_as_mapping */ &DynamicOneDimensionalArray_PyMappingMethods,
    /* tp_hash  */ 0,
    /* tp_call */ 0,
    /* tp_str */ (reprfunc) DynamicOneDimensionalArray___str__,
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
    /* tp_methods */ DynamicOneDimensionalArray_PyMethodDef,
    /* tp_members */ DynamicOneDimensionalArray_PyMemberDef,
    /* tp_getset */ 0,
    /* tp_base */ &DynamicArrayType,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ DynamicOneDimensionalArray___new__,
};

#endif
