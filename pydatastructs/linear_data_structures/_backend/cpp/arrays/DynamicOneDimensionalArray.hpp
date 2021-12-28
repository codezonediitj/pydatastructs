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
} DynamicOneDimensionalArray;

static void DynamicOneDimensionalArray_dealloc(DynamicOneDimensionalArray *self) {
    OneDimensionalArray_dealloc(self->_one_dimensional_array);
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* DynamicOneDimensionalArray___new__(PyTypeObject* type, PyObject *args,
                                                    PyObject *kwds) {
    DynamicOneDimensionalArray *self;
    self = reinterpret_cast<DynamicOneDimensionalArray*>(type->tp_alloc(type, 0));
    PyObject* _one_dimensional_array = OneDimensionalArray___new__(&OneDimensionalArrayType, args, kwds);
    if( !_one_dimensional_array ) {
        return NULL;
    }
    self->_one_dimensional_array = reinterpret_cast<OneDimensionalArray*>(_one_dimensional_array);

    PyObject* _load_factor = PyObject_GetItem(kwds, PyUnicode_FromString("load_factor"));
    if( _load_factor == nullptr ) {
        PyErr_Clear();
        self->_load_factor = 0.25;
    } else {
        _load_factor = PyFloat_FromString(PyObject_Str(_load_factor));
        if( !_load_factor ) {
            return NULL;
        }
        self->_load_factor = PyFloat_AS_DOUBLE(_load_factor);
    }
    if( self->_one_dimensional_array->_size == 0 or
        self->_one_dimensional_array->_data[0] == Py_None ) {
        self->_num = 0;
    } else {
        self->_num = self->_one_dimensional_array->_size;
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
    return OneDimensionalArray___str__(self->_one_dimensional_array);
}

static PyMappingMethods DynamicOneDimensionalArray_PyMappingMethods = {
    (lenfunc) DynamicOneDimensionalArray___len__,
    (binaryfunc) DynamicOneDimensionalArray___getitem__,
    (objobjargproc) DynamicOneDimensionalArray___setitem__,
};

static struct PyMethodDef DynamicOneDimensionalArray_PyMethodDef[] = {
    {"fill", (PyCFunction) DynamicOneDimensionalArray_fill, METH_VARARGS, NULL},
    {NULL}
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
    /* tp_members */ 0,
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
