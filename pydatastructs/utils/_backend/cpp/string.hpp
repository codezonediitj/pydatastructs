#ifndef STRINGS_UTILS_HPP
#define STRINGS_UTILS_HPP

#include <Python.h>
#include <vector>
#include <string>

// Convert Python string to C++ string
std::string pyobj_to_string(PyObject* obj);

// Convert C++ string to Python string
PyObject* string_to_pyobj(const std::string& str);

// Convert C++ vector to Python list
PyObject* vector_to_pylist(const std::vector<int>& vec);

#endif