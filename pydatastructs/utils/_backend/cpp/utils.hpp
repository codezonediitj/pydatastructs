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

static PyObject* __str__(PyObject** array, size_t size, long last_pos_filled=-1) {
    std::string array___str__ = "[";
    size_t end = last_pos_filled == -1 ? size : (size_t) (last_pos_filled + 1);
    for( size_t i = 0; i < end; i++ ) {
        if( array[i] == Py_None ) {
            array___str__.append("''");
        } else {
            PyObject* array_i = PyObject_Str(array[i]);
            char* i___str__ = PyObject_AsString(array_i);
            array___str__.append("'" + std::string(i___str__) + "'");
        }
        if( i + 1 != end ) {
            array___str__.append(", ");
        }
    }
    array___str__.push_back(']');
    return PyUnicode_FromString(array___str__.c_str());
}

static int set_exception_if_dtype_mismatch(PyObject* value, PyObject* dtype) {
    if( !PyObject_IsInstance(value, dtype) ) {
        PyErr_WriteUnraisable(
            PyErr_Format(PyExc_TypeError,
            "Unable to store %s object in %s type array.",
            PyObject_AsString(PyObject_Repr(PyObject_Type(value))),
            PyObject_AsString(PyObject_Repr(dtype))));
        return 1;
    }
    return 0;
}

static int raise_exception_if_dtype_mismatch(PyObject* value, PyObject* dtype) {
    if( !PyObject_IsInstance(value, dtype) ) {
        PyErr_Format(PyExc_TypeError,
        "Unable to store %s object in %s type array.",
        PyObject_AsString(PyObject_Repr(PyObject_Type(value))),
        PyObject_AsString(PyObject_Repr(dtype)));
        return 1;
    }
    return 0;
}

#endif
