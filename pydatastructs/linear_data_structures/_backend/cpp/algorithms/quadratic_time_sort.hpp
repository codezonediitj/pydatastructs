#ifndef LINEAR_DATA_STRUCTURES_ALGORITHMS_QUADRATIC_TIME_SORT_HPP
#define LINEAR_DATA_STRUCTURES_ALGORITHMS_QUADRATIC_TIME_SORT_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "../arrays/OneDimensionalArray.hpp"
#include "../arrays/DynamicOneDimensionalArray.hpp"
#include "../../../../utils/_backend/cpp/utils.hpp"

// Bubble Sort
static PyObject* bubble_sort_impl(PyObject* array, size_t lower, size_t upper,
    PyObject* comp, size_t arr_length) {
    for (size_t i = 0; i < arr_length - 1; i++) {
        for (size_t j = lower; j < upper; j++) {
            PyObject* j_PyObject = PyLong_FromSize_t(j);
            PyObject* j1_PyObject = PyLong_FromSize_t(j+1);
            if ( _comp(PyObject_GetItem(array, j_PyObject),
                        PyObject_GetItem(array, j1_PyObject), comp) != 1 ) {
                PyObject* tmp = PyObject_GetItem(array, j1_PyObject);
                PyObject_SetItem(array, j1_PyObject,
                                PyObject_GetItem(array, j_PyObject));
                PyObject_SetItem(array, j_PyObject, tmp);
            }
        }
    }
    return array;
}


static PyObject* bubble_sort(PyObject* self, PyObject* args, PyObject* kwds) {
    PyObject *args0 = NULL, *start = NULL, *end = NULL;
    PyObject *comp = NULL, *pick_pivot_element = NULL;
    size_t lower, upper, arr_length;
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
    arr_length = PyObject_Length(args0);

    args0 = bubble_sort_impl(args0, lower, upper, comp, arr_length);
    if ( is_DynamicOneDimensionalArray ) {
        PyObject_CallMethod(args0, "_modify", "O", Py_True);
    }
    Py_INCREF(args0);
    return args0;
}


// Selection Sort
static PyObject* selection_sort_impl(PyObject* array, size_t lower, size_t upper,
    PyObject* comp) {
    for (size_t i = lower; i < upper + 1; i++) {
        PyObject* j_min_PyObject = PyLong_FromSize_t(i);
        PyObject* i_PyObject = PyLong_FromSize_t(i);
        for (size_t j = i + 1; j < upper + 1; j++) {
            PyObject* j_PyObject = PyLong_FromSize_t(j);
            if ( _comp(PyObject_GetItem(array, j_min_PyObject),
                        PyObject_GetItem(array, j_PyObject), comp) != 1 ) {
                j_min_PyObject = j_PyObject;
            }
        }
        PyObject* tmp = PyObject_GetItem(array, j_min_PyObject);
        PyObject_SetItem(array, j_min_PyObject,
                        PyObject_GetItem(array, i_PyObject));
        PyObject_SetItem(array, i_PyObject, tmp);
    }
    return array;
}


static PyObject* selection_sort(PyObject* self, PyObject* args, PyObject* kwds) {
    PyObject *args0 = NULL, *start = NULL, *end = NULL;
    PyObject *comp = NULL, *pick_pivot_element = NULL;
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

    args0 = selection_sort_impl(args0, lower, upper, comp);
    if ( is_DynamicOneDimensionalArray ) {
        PyObject_CallMethod(args0, "_modify", "O", Py_True);
    }
    Py_INCREF(args0);
    return args0;
}


// Insertion Sort
static PyObject* insertion_sort_impl(PyObject* array, size_t lower, size_t upper,
    PyObject* comp) {
    for (size_t i = lower + 1; i < upper + 1; i++) {
        PyObject* i_PyObject = PyLong_FromSize_t(i);
        PyObject* temp = PyObject_GetItem(array, i_PyObject);
        size_t j = i;
        while (j > lower && _comp(PyObject_GetItem(array, PyLong_FromSize_t(j-1)),
                        temp, comp) != 1) {
            PyObject_SetItem(array, PyLong_FromSize_t(j),
                        PyObject_GetItem(array, PyLong_FromSize_t(j-1)));
            j -= 1;
        }
        PyObject_SetItem(array, PyLong_FromSize_t(j), temp);
    }
    return array;
}

static PyObject* insertion_sort(PyObject* self, PyObject* args, PyObject* kwds) {
    PyObject *args0 = NULL, *start = NULL, *end = NULL;
    PyObject *comp = NULL, *pick_pivot_element = NULL;
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

    args0 = insertion_sort_impl(args0, lower, upper, comp);
    if ( is_DynamicOneDimensionalArray ) {
        PyObject_CallMethod(args0, "_modify", "O", Py_True);
    }
    Py_INCREF(args0);
    return args0;
}


#endif
