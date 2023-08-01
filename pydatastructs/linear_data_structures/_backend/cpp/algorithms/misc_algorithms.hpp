#ifndef LINEAR_DATA_STRUCTURES_ALGORITHMS_MISC_ALGORITHMS
#define LINEAR_DATA_STRUCTURES_ALGORITHMS_MISC_ALGORITHMS

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "../arrays/OneDimensionalArray.hpp"
#include "../arrays/DynamicOneDimensionalArray.hpp"
#include "../../../../utils/_backend/cpp/utils.hpp"

// is_ordered
static bool is_ordered_impl(PyObject* array, size_t lower, size_t upper,
    PyObject* comp) {
    for (size_t i = lower + 1; i < upper + 1; i++) {
        PyObject* i_PyObject = PyLong_FromSize_t(i);
        PyObject* i1_PyObject = PyLong_FromSize_t(i-1);
        PyObject* i_item = PyObject_GetItem(array, i_PyObject);
        PyObject* i1_item = PyObject_GetItem(array, i1_PyObject);
        if (i_item == Py_None || i1_item == Py_None) continue;
        if( _comp(i_item, i1_item, comp) == 1 ) {
            printf("%d--\n", i);
            return false;
        }
    }
    return true;
}

static PyObject* is_ordered(PyObject* self, PyObject* args, PyObject* kwds) {
    PyObject *args0 = NULL, *start = NULL, *end = NULL;
    PyObject *comp = NULL, *res = NULL;
    size_t lower, upper;
    args0 = PyObject_GetItem(args, PyZero);
    int is_DynamicOneDimensionalArray = _check_type(args0, &DynamicOneDimensionalArrayType);
    int is_OneDimensionalArray = _check_type(args0, &OneDimensionalArrayType);
    if( !is_DynamicOneDimensionalArray && !is_OneDimensionalArray ) {
        raise_exception_if_not_array(args0);
        return NULL;
    }
    comp = PyObject_GetItem(kwds, PyUnicode_FromString("comp"));
    if( comp == NULL ) {
        PyErr_Clear();
    }
    start = PyObject_GetItem(kwds, PyUnicode_FromString("start"));
    if( start == NULL ) {
        PyErr_Clear();
        lower = 0;
    } else {
        lower = PyLong_AsSize_t(start);
    }
    end = PyObject_GetItem(kwds, PyUnicode_FromString("end"));
    if( end == NULL ) {
        PyErr_Clear();
        upper = PyObject_Length(args0) - 1;
    } else {
        upper = PyLong_AsSize_t(end);
    }

    bool _res = is_ordered_impl(args0, lower, upper, comp);
    res = PyBool_FromLong(_res);
    Py_INCREF(res);
    return res;
}


#endif
