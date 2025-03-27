#include "utils.hpp"

std::string pyobj_to_string(PyObject* obj) {
    if (!PyUnicode_Check(obj)) {
        PyErr_SetString(PyExc_TypeError, "Expected a string object.");
        return "";
    }
    return PyUnicode_AsUTF8(obj);
}

PyObject* string_to_pyobj(const std::string& str) {
    return PyUnicode_FromString(str.c_str());
}

PyObject* vector_to_pylist(const std::vector<int>& vec) {
    PyObject* list = PyList_New(vec.size());
    for (size_t i = 0; i < vec.size(); i++) {
        PyList_SetItem(list, i, PyLong_FromLong(vec[i]));
    }
    return list;
}