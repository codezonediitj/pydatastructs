#ifndef LINEAR_DATA_STRUCTURES_ONEDIMENSIONALIMPLICITARRAY_HPP
#define LINEAR_DATA_STRUCTURES_ONEDIMENSIONALIMPLICITARRAY_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <cstdlib>
#include "Array.hpp"
#include "../../../../utils/_backend/cpp/utils.hpp"

typedef struct
{
    PyObject_HEAD
        size_t _size;
    PyObject *_dtype;
    PyObject *_function;
} OneDimensionalImplicitArray;

static void OneDimensionalImplicitArray_dealloc(OneDimensionalImplicitArray *self)
{
    Py_XDECREF(self->_dtype);
    Py_XDECREF(self->_function);
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject *>(self));
}

static PyObject *OneDimensionalImplicitArray___new__(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    OneDimensionalImplicitArray *self;
    self = reinterpret_cast<OneDimensionalImplicitArray *>(type->tp_alloc(type, 0));
    size_t len_args = PyObject_Length(args);

    if (len_args < 2)
    {
        PyErr_SetString(PyExc_ValueError, "Too few arguments to create a 1D implicit array, pass the function of the array and the size of the array");
        return NULL;
    }
    if (len_args > 2)
    {
        PyErr_SetString(PyExc_ValueError, "Too many arguments to create an implicit 1D array, pass the function of the array and the size of the array");
        return NULL;
    }

    PyObject *dtype = PyObject_GetItem(kwds, PyUnicode_FromString("dtype"));
    if (dtype == nullptr)
    {
        PyErr_SetString(PyExc_ValueError, "Data type is not defined.");
        return NULL;
    }
    self->_dtype = dtype;
    Py_INCREF(self->_dtype);

    PyObject *args0 = PyObject_GetItem(args, PyZero);
    PyObject *args1 = PyObject_GetItem(args, PyOne);

    if (PyCallable_Check(args0) && PyLong_Check(args1))
    {
        self->_function = args0;
        Py_INCREF(self->_function);
        self->_size = PyLong_AsSize_t(args1);
    }
    else if (PyCallable_Check(args1) && PyLong_Check(args0))
    {
        self->_function = args1;
        Py_INCREF(self->_function);
        self->_size = PyLong_AsSize_t(args0);
    }
    else
    {
        PyErr_SetString(PyExc_TypeError, "Expected one function and one integer for size");
        return NULL;
    }

    return reinterpret_cast<PyObject *>(self);
}

static PyObject *OneDimensionalImplicitArray___getitem__(OneDimensionalImplicitArray *self, PyObject *arg)
{
    size_t idx = PyLong_AsUnsignedLong(arg);
    if (idx >= self->_size)
    {
        PyErr_Format(PyExc_IndexError, "Index, %d, out of range, [%d, %d)", idx, 0, self->_size);
        return NULL;
    }
    PyObject *result = PyObject_CallFunctionObjArgs(self->_function, PyLong_FromSize_t(idx), NULL);
    if (result == NULL)
    {
        return NULL;
    }
    if (raise_exception_if_dtype_mismatch(result, self->_dtype))
    {
        return NULL;
    }
    return result;
}

static Py_ssize_t OneDimensionalImplicitArray___len__(OneDimensionalImplicitArray *self)
{
    return self->_size;
}

static PyObject *OneDimensionalImplicitArray_get_data(OneDimensionalImplicitArray *self, void *closure)
{
    PyObject *list = PyList_New(self->_size);
    if (!list)
    {
        return NULL;
    }
    for (size_t i = 0; i < self->_size; i++)
    {
        PyObject *item = PyObject_CallFunctionObjArgs(self->_function, PyLong_FromSize_t(i), NULL);
        if (item == NULL)
        {
            Py_DECREF(list);
            return NULL;
        }
        PyList_SET_ITEM(list, i, item);
    }
    return list;
}

static PyGetSetDef OneDimensionalImplicitArray_getsetters[] = {
    {"_data", (getter)OneDimensionalImplicitArray_get_data, NULL, "data", NULL},
    {NULL} /* Sentinel */
};

static PyMappingMethods OneDimensionalImplicitArray_PyMappingMethods = {
    (lenfunc)OneDimensionalImplicitArray___len__,
    (binaryfunc)OneDimensionalImplicitArray___getitem__,
    (objobjargproc)0,
};

static PyTypeObject OneDimensionalImplicitArrayType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "OneDimensionalImplicitArray",
    /* tp_basicsize */ sizeof(OneDimensionalImplicitArray),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor)OneDimensionalImplicitArray_dealloc,
    /* tp_print */ 0,
    /* tp_getattr */ 0,
    /* tp_setattr */ 0,
    /* tp_reserved */ 0,
    /* tp_repr */ 0,
    /* tp_as_number */ 0,
    /* tp_as_sequence */ 0,
    /* tp_as_mapping */ &OneDimensionalImplicitArray_PyMappingMethods,
    /* tp_hash  */ 0,
    /* tp_call */ 0,
    /* tp_str */ 0,
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
    /* tp_getset */ OneDimensionalImplicitArray_getsetters,
    /* tp_base */ &ArrayType,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ OneDimensionalImplicitArray___new__,
};

#endif
