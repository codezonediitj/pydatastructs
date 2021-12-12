#ifndef UTILS_UTILS_HPP
#define UTILS_UTILS_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>

PyObject *PyZero = PyLong_FromLong(0);
PyObject *PyOne = PyLong_FromLong(1);
PyObject *PyTwo = PyLong_FromLong(2);

#endif
