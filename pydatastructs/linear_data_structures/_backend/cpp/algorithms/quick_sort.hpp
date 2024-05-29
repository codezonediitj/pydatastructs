#ifndef LINEAR_DATA_STRUCTURES_ALGORITHMS_QUICK_SORT_HPP
#define LINEAR_DATA_STRUCTURES_ALGORITHMS_QUICK_SORT_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "../arrays/OneDimensionalArray.hpp"
#include "../arrays/DynamicOneDimensionalArray.hpp"
#include "../../../../utils/_backend/cpp/utils.hpp"
#include <stack>

static PyObject* call_pick_pivot_element(PyObject* pick_pivot_element,
    size_t low, size_t high, PyObject* array) {
    PyObject* high_PyObject = PyLong_FromSize_t(high);
    if ( pick_pivot_element ) {
        return PyObject_CallFunctionObjArgs(pick_pivot_element,
                                            PyLong_FromSize_t(low),
                                            high_PyObject,
                                            array);
    }

    return PyObject_GetItem(array, high_PyObject);
}

static size_t quick_sort_partition(size_t low, size_t high,
    PyObject* pick_pivot_element, PyObject* comp, PyObject* array) {
    int64_t i = low - 1;
    PyObject* x = call_pick_pivot_element(pick_pivot_element, low, high, array);
    for( size_t j = low; j < high; j++ ) {
        PyObject* j_PyObject = PyLong_FromSize_t(j);
        if ( _comp(PyObject_GetItem(array, j_PyObject), x, comp) == 1 ) {
            i = i + 1;
            PyObject* i_PyObject = PyLong_FromLongLong(i);
            PyObject* tmp = PyObject_GetItem(array, i_PyObject);
            PyObject_SetItem(array, i_PyObject,
                             PyObject_GetItem(array, j_PyObject));
            PyObject_SetItem(array, j_PyObject, tmp);
        }
    }
    PyObject* i_PyObject = PyLong_FromLongLong(i + 1);
    PyObject* high_PyObject = PyLong_FromSize_t(high);
    PyObject* tmp = PyObject_GetItem(array, i_PyObject);
    PyObject_SetItem(array, i_PyObject,
                        PyObject_GetItem(array, high_PyObject));
    PyObject_SetItem(array, high_PyObject, tmp);
    return i + 1;
}

static PyObject* quick_sort_impl(PyObject* array, size_t lower, size_t upper,
    PyObject* comp, PyObject* pick_pivot_element) {

    size_t low, high, p;
    std::stack<size_t> rstack;

    rstack.push(lower);
    rstack.push(upper);

    while ( !rstack.empty() ) {
        high = rstack.top();
        rstack.pop();
        low = rstack.top();
        rstack.pop();
        p = quick_sort_partition(low, high, pick_pivot_element,
                                 comp, array);
        if ( p - 1 > low ) {
            rstack.push(low);
            rstack.push(p - 1);
        }
        if ( p + 1 < high ) {
            rstack.push(p + 1);
            rstack.push(high);
        }
    }

    return array;
}

static PyObject* quick_sort(PyObject* self, PyObject* args, PyObject* kwds) {
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
    pick_pivot_element = PyObject_GetItem(kwds, PyUnicode_FromString("pick_pivot_element"));
    if ( pick_pivot_element == NULL ) {
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

    args0 = quick_sort_impl(args0, lower, upper, comp, pick_pivot_element);
    if ( is_DynamicOneDimensionalArray ) {
        PyObject_CallMethod(args0, "_modify", "O", Py_True);
    }
    Py_INCREF(args0);
    return args0;
}

#endif
