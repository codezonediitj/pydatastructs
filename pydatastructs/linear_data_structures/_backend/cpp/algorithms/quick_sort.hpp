#ifndef LINEAR_DATA_STRUCTURES_ALGORITHMS_QUICK_SORT_HPP
#define LINEAR_DATA_STRUCTURES_ALGORITHMS_QUICK_SORT_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "../arrays/OneDimensionalArray.hpp"
#include "../arrays/DynamicOneDimensionalArray.hpp"
#include "../../../../utils/_backend/cpp/utils.hpp"
#include <stack>
#include <iostream>

static PyObject* call_pick_pivot_element(PyObject* pick_pivot_element,
    size_t low, size_t high,
    OneDimensionalArray* array) {
    if( pick_pivot_element ) {
        return PyObject_CallFunctionObjArgs(pick_pivot_element,
                                            PyLong_FromSize_t(low),
                                            PyLong_FromSize_t(high),
                                            reinterpret_cast<PyObject*>(array));
    }

    return array->_data[high];
}

OneDimensionalArray* quick_sort_impl(OneDimensionalArray* array, size_t lower, size_t upper,
    PyObject* comp, PyObject* pick_pivot_element) {
    return array;
}

static PyObject* quick_sort(PyObject* self, PyObject* args, PyObject* kwds) {
    PyObject *args0 = NULL, *start = NULL, *end = NULL;
    PyObject *comp = NULL, *pick_pivot_element = NULL;
    size_t lower, upper;
    args0 = PyObject_GetItem(args, PyZero);
    int is_DynamicOneDimensionalArray = _check_type(args0, &DynamicOneDimensionalArrayType);
    int is_OneDimensionalArray = _check_type(args0, &OneDimensionalArrayType);
    if( !is_DynamicOneDimensionalArray && !is_OneDimensionalArray ) {
        std::cout<<"args0.type: "<<args0->ob_type->tp_name<<" "<<DynamicOneDimensionalArrayType.tp_name<<std::endl;
        raise_exception_if_not_array(args0);
        return NULL;
    }
    comp = PyObject_GetItem(kwds, PyUnicode_FromString("comp"));
    if( comp == NULL ) {
        PyErr_Clear();
    }
    pick_pivot_element = PyObject_GetItem(kwds, PyUnicode_FromString("pick_pivot_element"));
    if( pick_pivot_element == NULL ) {
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

    OneDimensionalArray* array = NULL;
    int force_modify = 0;
    if( is_DynamicOneDimensionalArray ) {
        array = reinterpret_cast<DynamicOneDimensionalArray*>(args0)->_one_dimensional_array;
        force_modify = 1;
    } else {
        array = reinterpret_cast<OneDimensionalArray*>(args0);
    }

    std::cout<<lower<<" "<<upper<<std::endl;
    array = quick_sort_impl(array, lower, upper, comp, pick_pivot_element);
    if( force_modify ) {
        DynamicOneDimensionalArray__modify(reinterpret_cast<DynamicOneDimensionalArray*>(args0),
                                           PyTuple_Pack(1, Py_True));
    }
    return reinterpret_cast<PyObject*>(array);
}

#endif
