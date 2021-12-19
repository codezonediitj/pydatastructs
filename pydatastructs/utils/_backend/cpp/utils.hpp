#ifndef UTILS_UTILS_HPP
#define UTILS_UTILS_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <string>

PyObject *PyZero = PyLong_FromLong(0);
PyObject *PyOne = PyLong_FromLong(1);
PyObject *PyTwo = PyLong_FromLong(2);

static PyObject* __str__(PyObject** array, size_t size) {
    std::string array___str__ = "[";
    for( size_t i = 0; i < size; i++ ) {
        char* i___str__ = PyBytes_AS_STRING(PyObject_Str(array[i]));
        array___str__.append(std::string(i___str__));
        if( i + 1 != size ) {
            array___str__.append(", ");
        }
    }
    array___str__.push_back(']');
    return PyBytes_FromString(array___str__.c_str());
}

#endif
