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
        if ( _comp(i_item, i1_item, comp) == 1 ) {
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
    if ( !is_DynamicOneDimensionalArray && !is_OneDimensionalArray ) {
        raise_exception_if_not_array(args0);
        return NULL;
    }
    comp = PyObject_GetItem(kwds, PyUnicode_FromString("comp"));
    if ( comp == NULL ) {
        PyErr_Clear();
    }
    start = PyObject_GetItem(kwds, PyUnicode_FromString("start"));
    if ( start == NULL ) {
        PyErr_Clear();
        lower = 0;
    } else {
        lower = PyLong_AsSize_t(start);
    }
    end = PyObject_GetItem(kwds, PyUnicode_FromString("end"));
    if ( end == NULL ) {
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

static PyObject* linear_search(PyObject* self, PyObject* args, PyObject* kwds) {
    PyObject *args0 = NULL, *start = NULL, *end = NULL;
    PyObject *value = NULL, *res = NULL, *u = NULL;
    size_t lower, upper;
    args0 = PyObject_GetItem(args, PyZero);
    int is_DynamicOneDimensionalArray = _check_type(args0, &DynamicOneDimensionalArrayType);
    int is_OneDimensionalArray = _check_type(args0, &OneDimensionalArrayType);
    if ( !is_DynamicOneDimensionalArray && !is_OneDimensionalArray ) {
        raise_exception_if_not_array(args0);
        return NULL;
    }
    start = PyObject_GetItem(kwds, PyUnicode_FromString("start"));
    if ( start == NULL ) {
        PyErr_Clear();
        lower = 0;
    } else {
        lower = PyLong_AsSize_t(start);
    }
    end = PyObject_GetItem(kwds, PyUnicode_FromString("end"));
    if ( end == NULL ) {
        PyErr_Clear();
        upper = PyObject_Length(args0) - 1;
    } else {
        upper = PyLong_AsSize_t(end);
    }
    value = PyObject_GetItem(args, PyLong_FromSize_t(1));
    if ( value == NULL ) {
        PyErr_Format(PyExc_ValueError,
                "Expected Value to be not NULL");
    }
    for (size_t i = lower;  i < upper + 1; i++) {
        u = PyObject_GetItem(args0, PyLong_FromSize_t(i));
        int result = PyObject_RichCompareBool(u, value, Py_EQ);
        if ( result == -1 ) {
            PyErr_Format(PyExc_ValueError,
                "Unable to compare %s object with %s object.",
                PyObject_AsString(PyObject_Repr(PyObject_Type(u))),
                PyObject_AsString(PyObject_Repr(PyObject_Type(value)))
            );
        } else if (result == 1) {
            if (i == 0) {
                res = PyZero;
            } else {
                res = PyLong_FromSize_t(i);
            }
            Py_INCREF(res);
            return res;
        }
    }
    res = Py_None;
    Py_INCREF(res);
    return res;
}

static PyObject* binary_search(PyObject* self, PyObject* args, PyObject* kwds) {
    PyObject *args0 = NULL, *start = NULL, *end = NULL;
    PyObject *value = NULL, *res = NULL, *u = NULL, *comp = NULL;
    size_t lower, upper;
    args0 = PyObject_GetItem(args, PyZero);
    int is_DynamicOneDimensionalArray = _check_type(args0, &DynamicOneDimensionalArrayType);
    int is_OneDimensionalArray = _check_type(args0, &OneDimensionalArrayType);
    if ( !is_DynamicOneDimensionalArray && !is_OneDimensionalArray ) {
        raise_exception_if_not_array(args0);
        return NULL;
    }
    comp = PyObject_GetItem(kwds, PyUnicode_FromString("comp"));
    if ( comp == NULL ) {
        PyErr_Clear();
    }
    start = PyObject_GetItem(kwds, PyUnicode_FromString("start"));
    if ( start == NULL ) {
        PyErr_Clear();
        lower = 0;
    } else {
        lower = PyLong_AsSize_t(start);
    }
    end = PyObject_GetItem(kwds, PyUnicode_FromString("end"));
    if ( end == NULL ) {
        PyErr_Clear();
        upper = PyObject_Length(args0) - 1;
    } else {
        upper = PyLong_AsSize_t(end);
    }
    value = PyObject_GetItem(args, PyLong_FromSize_t(1));
    if ( value == NULL ) {
        PyErr_Format(PyExc_ValueError,
                "Expected Value to be not NULL");
    }

    int left = lower, right = upper;
    while (left <= right)
    {
        int middle = left/2 + right/2 + left % 2 * right % 2;
        u = PyObject_GetItem(args0, PyLong_FromSize_t(middle));
        int result = PyObject_RichCompareBool(u, value, Py_EQ);
        if ( result == -1 ) {
            PyErr_Format(PyExc_ValueError,
                "Unable to compare %s object with %s object.",
                PyObject_AsString(PyObject_Repr(PyObject_Type(u))),
                PyObject_AsString(PyObject_Repr(PyObject_Type(value)))
            );
        } else if (result == 1) {
            if (middle == 0) {
                res = PyZero;
            } else {
                res = PyLong_FromSize_t(middle);
            }
            Py_INCREF(res);
            return res;
        }
        if ( _comp(u, value, comp) == 1 ) {
            left = middle + 1;
        } else {
            right = middle - 1;
        }
    }
    res = Py_None;
    Py_INCREF(res);
    return res;
}

static PyObject* jump_search(PyObject* self, PyObject* args, PyObject* kwds) {
    PyObject *args0 = NULL, *start = NULL, *end = NULL;
    PyObject *value = NULL, *res = NULL, *u = NULL, *comp = NULL;
    size_t lower, upper;
    args0 = PyObject_GetItem(args, PyZero);
    int is_DynamicOneDimensionalArray = _check_type(args0, &DynamicOneDimensionalArrayType);
    int is_OneDimensionalArray = _check_type(args0, &OneDimensionalArrayType);
    if ( !is_DynamicOneDimensionalArray && !is_OneDimensionalArray ) {
        raise_exception_if_not_array(args0);
        return NULL;
    }
    comp = PyObject_GetItem(kwds, PyUnicode_FromString("comp"));
    if ( comp == NULL ) {
        PyErr_Clear();
    }
    start = PyObject_GetItem(kwds, PyUnicode_FromString("start"));
    if ( start == NULL ) {
        PyErr_Clear();
        lower = 0;
    } else {
        lower = PyLong_AsSize_t(start);
    }
    end = PyObject_GetItem(kwds, PyUnicode_FromString("end"));
    if ( end == NULL ) {
        PyErr_Clear();
        upper = PyObject_Length(args0) - 1;
    } else {
        upper = PyLong_AsSize_t(end);
    }
    value = PyObject_GetItem(args, PyLong_FromSize_t(1));
    if ( value == NULL ) {
        PyErr_Format(PyExc_ValueError,
                "Expected Value to be not NULL");
    }
    int step = int(sqrt(double(upper - lower + 1)));
    int prev = lower;
    int element_pos = prev;
    u = PyObject_GetItem(args0, PyLong_FromSize_t(element_pos));
    while (element_pos <= upper && _comp(u, value, comp) == 1) {
        prev = element_pos;
        element_pos += step;
        if (element_pos > upper) {
            break;
        }
        u = PyObject_GetItem(args0, PyLong_FromSize_t(element_pos));
    }

    while (prev <= upper) {
        u = PyObject_GetItem(args0, PyLong_FromSize_t(prev));
        int result = PyObject_RichCompareBool(u, value, Py_EQ);
        if ( result == -1 ) {
            PyErr_Format(PyExc_ValueError,
                "Unable to compare %s object with %s object.",
                PyObject_AsString(PyObject_Repr(PyObject_Type(u))),
                PyObject_AsString(PyObject_Repr(PyObject_Type(value)))
            );
        } else if (result == 1) {
            if (prev == 0) {
                res = PyZero;
            } else {
                res = PyLong_FromSize_t(prev);
            }
            Py_INCREF(res);
            return res;
        }
        prev += 1;
    }
    res = Py_None;
    Py_INCREF(res);
    return res;
}

#endif
