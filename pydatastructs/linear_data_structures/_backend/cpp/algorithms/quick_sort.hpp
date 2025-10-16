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

static PyObject* quick_sort_llvm(PyObject* self, PyObject* args, PyObject* kwds) {
    static const char* kwlist[] = {"arr", "start", "end", "comp", "dtype", NULL};
    PyObject* arr_obj = NULL;
    PyObject* start_obj = NULL;
    PyObject* end_obj = NULL;
    PyObject* comp_obj = NULL;
    const char* dtype_cstr = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O|OOOs", (char**)kwlist,
                                     &arr_obj, &start_obj, &end_obj, &comp_obj, &dtype_cstr)) {
        return NULL;
    }

    Py_ssize_t arr_len_ssize = PyObject_Length(arr_obj);

    size_t arr_len = (size_t)arr_len_ssize;

    bool is_dynamic_array = false;
    PyObject* last_pos_attr = PyUnicode_FromString("_last_pos_filled");
    PyObject* num_attr = PyUnicode_FromString("_num");

    if (last_pos_attr && num_attr && PyObject_HasAttr(arr_obj, last_pos_attr) && PyObject_HasAttr(arr_obj, num_attr)) {
        is_dynamic_array = true;
    }

    Py_XDECREF(last_pos_attr);
    Py_XDECREF(num_attr);

    if (is_dynamic_array) {
        PyObject* size_attr = PyUnicode_FromString("_size");
        if (size_attr && PyObject_HasAttr(arr_obj, size_attr)) {
            PyObject* size_obj = PyObject_GetAttr(arr_obj, size_attr);
            if (size_obj && PyLong_Check(size_obj)) {
                Py_ssize_t size_val = PyLong_AsSsize_t(size_obj);
                if (size_val >= 0) {
                    arr_len = (size_t)size_val;
                }
            }
            Py_XDECREF(size_obj);
        }
        Py_XDECREF(size_attr);
    }

    if (arr_len == 0) {
        Py_INCREF(arr_obj);
        return arr_obj;
    }

    size_t lower = 0;
    size_t upper = arr_len - 1;

    if (start_obj && start_obj != Py_None) {
        Py_ssize_t start_val = PyLong_AsSsize_t(start_obj);
        if (PyErr_Occurred()) return NULL;
        lower = (size_t)start_val;
    }

    if (end_obj && end_obj != Py_None) {
        Py_ssize_t end_val = PyLong_AsSsize_t(end_obj);
        if (PyErr_Occurred()) return NULL;
        upper = (size_t)end_val;
    }

    if (upper < lower || lower >= arr_len) {
        Py_INCREF(arr_obj);
        return arr_obj;
    }

    if (upper >= arr_len) {
        upper = arr_len - 1;
    }

    if (comp_obj && comp_obj != Py_None) {
        PyErr_SetString(PyExc_NotImplementedError, "LLVM backend does not support custom 'comp'.");
        return NULL;
    }

    std::string dtype = (dtype_cstr && *dtype_cstr) ? std::string(dtype_cstr) : std::string();
    auto infer_dtype = [&](PyObject* x) -> std::string {
        if (x == Py_None) return "";
        if (PyFloat_Check(x)) return "float64";
        if (PyLong_Check(x))  return "int64";
        return "float64";
    };

    std::vector<PyObject*> non_none_values;
    size_t none_count = 0;
    const size_t N = upper - lower + 1;

    non_none_values.reserve(N);

    for (size_t i = 0; i < N; i++) {
        size_t actual_index = lower + i;

        if (actual_index >= arr_len) {
            for (PyObject* obj : non_none_values) {
                Py_DECREF(obj);
            }
            PyErr_Format(PyExc_IndexError, "Index %zu out of bounds (array length: %zu)",
                        actual_index, arr_len);
            return NULL;
        }

        PyObject* item = NULL;

        if (PySequence_Check(arr_obj)) {
            item = PySequence_GetItem(arr_obj, (Py_ssize_t)actual_index);
        } else {
            PyObject* index_obj = PyLong_FromSize_t(actual_index);
            if (index_obj) {
                item = PyObject_GetItem(arr_obj, index_obj);
                Py_DECREF(index_obj);
            }
        }

        if (!item) {
            for (PyObject* obj : non_none_values) {
                Py_DECREF(obj);
            }

            if (PyErr_ExceptionMatches(PyExc_IndexError)) {
                PyErr_Format(PyExc_IndexError, "Cannot access index %zu in array", actual_index);
            }
            return NULL;
        }

        if (item == Py_None) {
            none_count++;
            Py_DECREF(item);
        } else {
            non_none_values.push_back(item);
        }
    }

    if (dtype.empty() && !non_none_values.empty()) {
        dtype = infer_dtype(non_none_values[0]);
    }

    if (non_none_values.empty() || dtype.empty()) {
        for (PyObject* obj : non_none_values) {
            Py_DECREF(obj);
        }
        Py_INCREF(arr_obj);
        return arr_obj;
    }

    auto get_addr = [&](const char* dtype_str) -> PyObject* {
        PyObject* sys = PyImport_ImportModule("sys");
        PyObject* sys_path = PyObject_GetAttrString(sys, "path");
        Py_DECREF(sys);

        Py_ssize_t original_len = PyList_Size(sys_path);
        if (original_len == -1) {
            Py_DECREF(sys_path);
            return NULL;
        }

        PyObject* path = PyUnicode_FromString("pydatastructs/linear_data_structures/_backend/cpp/algorithms");
        if (!path) {
            Py_DECREF(sys_path);
            return NULL;
        }

        int append_result = PyList_Append(sys_path, path);
        Py_DECREF(path);

        if (append_result != 0) {
            Py_DECREF(sys_path);
            return NULL;
        }

        PyObject* mod = PyImport_ImportModule("llvm_algorithms");

        if (PyList_SetSlice(sys_path, original_len, original_len + 1, NULL) != 0) {
            PyErr_Clear();
        }
        Py_DECREF(sys_path);
        if (!mod) {
            return NULL;
        }

        PyObject* fn = PyObject_GetAttrString(mod, "get_quick_sort_ptr");
        Py_DECREF(mod);
        if (!fn) {
            return NULL;
        }

        PyObject* arg = PyUnicode_FromString(dtype_str);
        if (!arg) {
            Py_DECREF(fn);
            return NULL;
        }

        PyObject* addr_obj = PyObject_CallFunctionObjArgs(fn, arg, NULL);
        Py_DECREF(fn);
        Py_DECREF(arg);
        if (!addr_obj) {
            return NULL;
        }
        return addr_obj;
    };

    if (N > INT32_MAX) {
        for (PyObject* obj : non_none_values) {
            Py_DECREF(obj);
        }
        PyErr_SetString(PyExc_OverflowError, "Slice length exceeds 32-bit limit for JIT function signature.");
        return NULL;
    }

    if (dtype == "int32" || dtype == "int64") {
        bool is32 = (dtype == "int32");
        PyObject* addr_obj = get_addr(dtype.c_str());
        if (!addr_obj) {
            for (PyObject* obj : non_none_values) {
                Py_DECREF(obj);
            }
            return NULL;
        }

        long long addr = PyLong_AsLongLong(addr_obj);
        Py_DECREF(addr_obj);
        if (addr == -1 && PyErr_Occurred()) {
            for (PyObject* obj : non_none_values) {
                Py_DECREF(obj);
            }
            return NULL;
        }

        if (is32) {
            std::vector<int32_t> buf;
            buf.reserve(non_none_values.size());

            for (size_t i = 0; i < non_none_values.size(); i++) {
                PyObject* obj = non_none_values[i];

                long v = PyLong_AsLong(obj);
                if (PyErr_Occurred()) {
                    for (PyObject* cleanup_obj : non_none_values) {
                        Py_DECREF(cleanup_obj);
                    }
                    return NULL;
                }

                if (v < INT32_MIN || v > INT32_MAX) {
                    for (PyObject* cleanup_obj : non_none_values) {
                        Py_DECREF(cleanup_obj);
                    }
                    PyErr_Format(PyExc_OverflowError, "Value %ld at index %zu out of int32 range", v, i);
                    return NULL;
                }
                buf.push_back((int32_t)v);
            }

            for (PyObject* obj : non_none_values) {
                Py_DECREF(obj);
            }
            non_none_values.clear();

            if (buf.empty()) {
                Py_INCREF(arr_obj);
                return arr_obj;
            }

            try {
                auto fn = reinterpret_cast<void(*)(int32_t*, int32_t)>(addr);
                fn(buf.data(), (int32_t)buf.size());
            } catch (...) {
                PyErr_SetString(PyExc_RuntimeError, "LLVM function call failed");
                return NULL;
            }
            for (size_t i = 0; i < buf.size(); i++) {
                size_t actual_index = lower + i;

                if (actual_index >= arr_len) {
                    PyErr_Format(PyExc_IndexError, "Assignment index %zu out of bounds (array length: %zu)",
                                actual_index, arr_len);
                    return NULL;
                }

                PyObject* new_value = PyLong_FromLong((long)buf[i]);
                if (!new_value) return NULL;
                PyObject* index_obj = PyLong_FromSize_t(actual_index);
                if (!index_obj) {
                    Py_DECREF(new_value);
                    return NULL;
                }

                int result = PyObject_SetItem(arr_obj, index_obj, new_value);
                Py_DECREF(index_obj);
                Py_DECREF(new_value);
            }

            for (size_t i = buf.size(); i < N; i++) {
                size_t actual_index = lower + i;

                PyObject* index_obj = PyLong_FromSize_t(actual_index);
                if (!index_obj) {
                    return NULL;
                }

                Py_INCREF(Py_None);
                int result = PyObject_SetItem(arr_obj, index_obj, Py_None);
                Py_DECREF(index_obj);
            }

        } else {
            std::vector<int64_t> buf;
            buf.reserve(non_none_values.size());

            for (size_t i = 0; i < non_none_values.size(); i++) {
                PyObject* obj = non_none_values[i];
                long long v = PyLong_AsLongLong(obj);
                if (PyErr_Occurred()) {
                    for (PyObject* cleanup_obj : non_none_values) {
                        Py_DECREF(cleanup_obj);
                    }
                    return NULL;
                }
                buf.push_back((int64_t)v);
            }

            for (PyObject* obj : non_none_values) {
                Py_DECREF(obj);
            }
            non_none_values.clear();

            if (buf.empty()) {
                Py_INCREF(arr_obj);
                return arr_obj;
            }

            try {
                auto fn = reinterpret_cast<void(*)(int64_t*, int32_t)>(addr);
                if (!fn) {
                    PyErr_SetString(PyExc_RuntimeError, "Invalid function pointer");
                    return NULL;
                }
                fn(buf.data(), (int32_t)buf.size());
            } catch (...) {
                PyErr_SetString(PyExc_RuntimeError, "LLVM function call failed");
                return NULL;
            }
            for (size_t i = 0; i < buf.size(); i++) {
                size_t actual_index = lower + i;
                if (actual_index >= arr_len) {
                    PyErr_Format(PyExc_IndexError, "Assignment index %zu out of bounds", actual_index);
                    return NULL;
                }
                PyObject* new_value = PyLong_FromLongLong((long long)buf[i]);
                if (!new_value) return NULL;
                PyObject* index_obj = PyLong_FromSize_t(actual_index);
                if (!index_obj) {
                    Py_DECREF(new_value);
                    return NULL;
                }
                int result = PyObject_SetItem(arr_obj, index_obj, new_value);
                Py_DECREF(index_obj);
                Py_DECREF(new_value);
            }

            for (size_t i = buf.size(); i < N; i++) {
                size_t actual_index = lower + i;

                PyObject* index_obj = PyLong_FromSize_t(actual_index);
                if (!index_obj) {
                    return NULL;
                }
                Py_INCREF(Py_None);
                int result = PyObject_SetItem(arr_obj, index_obj, Py_None);
                Py_DECREF(index_obj);
            }
        }
    }
    else if (dtype == "float32" || dtype == "float64") {
        bool is32 = (dtype == "float32");
        PyObject* addr_obj = get_addr(dtype.c_str());
        if (!addr_obj) {
            for (PyObject* obj : non_none_values) {
                Py_DECREF(obj);
            }
            return NULL;
        }
        long long addr = PyLong_AsLongLong(addr_obj);
        Py_DECREF(addr_obj);
        if (addr == -1 && PyErr_Occurred()) {
            for (PyObject* obj : non_none_values) {
                Py_DECREF(obj);
            }
            return NULL;
        }
        if (is32) {
            std::vector<float> buf;
            buf.reserve(non_none_values.size());

            for (size_t i = 0; i < non_none_values.size(); i++) {
                PyObject* obj = non_none_values[i];
                double v = PyFloat_AsDouble(obj);
                if (PyErr_Occurred()) {
                    for (PyObject* cleanup_obj : non_none_values) {
                        Py_DECREF(cleanup_obj);
                    }
                    return NULL;
                }
                buf.push_back((float)v);
            }

            for (PyObject* obj : non_none_values) {
                Py_DECREF(obj);
            }
            non_none_values.clear();
            if (buf.empty()) {
                Py_INCREF(arr_obj);
                return arr_obj;
            }

            try {
                auto fn = reinterpret_cast<void(*)(float*, int32_t)>(addr);
                if (!fn) {
                    PyErr_SetString(PyExc_RuntimeError, "Invalid function pointer");
                    return NULL;
                }
                fn(buf.data(), (int32_t)buf.size());
            } catch (...) {
                PyErr_SetString(PyExc_RuntimeError, "LLVM function call failed");
                return NULL;
            }

            for (size_t i = 0; i < buf.size(); i++) {
                size_t actual_index = lower + i;
                if (actual_index >= arr_len) {
                    PyErr_Format(PyExc_IndexError, "Assignment index %zu out of bounds", actual_index);
                    return NULL;
                }
                PyObject* new_value = PyFloat_FromDouble((double)buf[i]);
                if (!new_value) return NULL;
                PyObject* index_obj = PyLong_FromSize_t(actual_index);
                if (!index_obj) {
                    Py_DECREF(new_value);
                    return NULL;
                }
                int result = PyObject_SetItem(arr_obj, index_obj, new_value);
                Py_DECREF(index_obj);
                Py_DECREF(new_value);
            }

            for (size_t i = buf.size(); i < N; i++) {
                size_t actual_index = lower + i;

                PyObject* index_obj = PyLong_FromSize_t(actual_index);
                if (!index_obj) {
                    return NULL;
                }
                Py_INCREF(Py_None);
                int result = PyObject_SetItem(arr_obj, index_obj, Py_None);
                Py_DECREF(index_obj);
            }
        }
        else {
            std::vector<double> buf;
            buf.reserve(non_none_values.size());

            for (size_t i = 0; i < non_none_values.size(); i++) {
                PyObject* obj = non_none_values[i];
                double v = PyFloat_AsDouble(obj);
                if (PyErr_Occurred()) {
                    for (PyObject* cleanup_obj : non_none_values) {
                        Py_DECREF(cleanup_obj);
                    }
                    return NULL;
                }
                buf.push_back(v);
            }

            for (PyObject* obj : non_none_values) {
                Py_DECREF(obj);
            }
            non_none_values.clear();

            if (buf.empty()) {
                Py_INCREF(arr_obj);
                return arr_obj;
            }

            try {
                auto fn = reinterpret_cast<void(*)(double*, int32_t)>(addr);
                if (!fn) {
                    PyErr_SetString(PyExc_RuntimeError, "Invalid function pointer");
                    return NULL;
                }
                fn(buf.data(), (int32_t)buf.size());
            } catch (...) {
                PyErr_SetString(PyExc_RuntimeError, "LLVM function call failed");
                return NULL;
            }

            for (size_t i = 0; i < buf.size(); i++) {
                size_t actual_index = lower + i;
                PyObject* new_value = PyFloat_FromDouble(buf[i]);
                if (!new_value) return NULL;

                PyObject* index_obj = PyLong_FromSize_t(actual_index);
                if (!index_obj) {
                    Py_DECREF(new_value);
                    return NULL;
                }

                int result = PyObject_SetItem(arr_obj, index_obj, new_value);
                Py_DECREF(index_obj);
                Py_DECREF(new_value);
            }

            for (size_t i = buf.size(); i < N; i++) {
                size_t actual_index = lower + i;
                PyObject* index_obj = PyLong_FromSize_t(actual_index);
                if (!index_obj) {
                    return NULL;
                }
                Py_INCREF(Py_None);
                int result = PyObject_SetItem(arr_obj, index_obj, Py_None);
                Py_DECREF(index_obj);
            }
        }

    } else {
        for (PyObject* obj : non_none_values) {
            Py_DECREF(obj);
        }
        PyErr_SetString(PyExc_ValueError, "dtype must be one of: int32,int64,float32,float64");
        return NULL;
    }

    if (is_dynamic_array) {
        PyObject* modify_result = PyObject_CallMethod(arr_obj, "_modify", "O", Py_True);
        if (!modify_result) {
            PyErr_Clear();
        } else {
            Py_DECREF(modify_result);
        }
    }

    Py_INCREF(arr_obj);
    return arr_obj;
}

#endif
