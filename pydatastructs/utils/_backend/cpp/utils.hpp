#ifndef UTILS_UTILS_HPP
#define UTILS_UTILS_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <string>

PyObject *PyZero = PyLong_FromLong(0);
PyObject *PyOne = PyLong_FromLong(1);
PyObject *PyTwo = PyLong_FromLong(2);
const char* _encoding = "utf-8";
const char* _invalid_char = "<invalid-character>";

static char* PyObject_AsString(PyObject* obj) {
    return PyBytes_AS_STRING(PyUnicode_AsEncodedString(obj, _encoding, _invalid_char));
}

static PyObject* __str__(PyObject** array, size_t size) {
    std::string array___str__ = "[";
    for( size_t i = 0; i < size; i++ ) {
        PyObject* array_i = PyObject_Str(array[i]);
        char* i___str__ = PyObject_AsString(array_i);
        array___str__.append(std::string(i___str__));
        if( i + 1 != size ) {
            array___str__.append(", ");
        }
    }
    array___str__.push_back(']');
    return PyUnicode_FromString(array___str__.c_str());
}

#endif
