#ifndef LINEAR_DATA_STRUCTURES_ARRAYFORTREES_HPP
#define LINEAR_DATA_STRUCTURES_ARRAYFORTREES_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include "DynamicOneDimensionalArray.hpp"
#include "OneDimensionalArray.hpp"

typedef struct {
    PyObject_HEAD
} ArrayForTrees;

static void ArrayForTrees_dealloc(ArrayForTrees *self) {
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* ArrayForTrees__modify(ArrayForTrees *self) {
    if(((double)self->_num/(double)self->_size) < self->_load_factor){
        map<long , long> new_indices;

        // PyObject* arr_new = OneDimensionalArray___new__(self->_dtype, 2*self->_num + 1);
        // This is how arr_new was made in DynamicOneDimensionalArray__modify() for the exact same line :-
        long new_size = 2 * self->_num + 1;
        PyObject** arr_new = reinterpret_cast<PyObject**>(std::malloc(new_size * sizeof(PyObject*)));
        for( i = 0; i < new_size; i++ ) {
            Py_INCREF(Py_None);
            arr_new[i] = Py_None;
        }

        int j=0;
        PyObject** _data = self->_one_dimensional_array->_data;
        for(int i=0; i<=self->_last_pos_filled;i++){
            if(_data[i] != Py_None){ // Check this line. Python code: if self[i] is not None:
                Py_INCREF(Py_None); // This was put in DynamicOneDimensionalArray line 116
                arr_new[j] = _data[i];
                new_indices[_data[i]->key] = j;
                j += 1;
            }
        }
        for(int i=0;i<j;i++){
            if(arr_new[i]->left != Py_None){
                arr_new[i]->left = new_indices[_data[arr_new[i]->left]->key];
            }
            if(arr_new[i]->right != Py_None){
                arr_new[i]->right = new_indices[_data[arr_new[i]->right]->key];
            }
            if(arr_new[i]->parent != Py_None){
                arr_new[i]->parent = new_indices[_data[arr_new[i]->parent]->key];
            }
        }
        self->_last_pos_filled = j - 1;
        self->_one_dimensional_array->_data = arr_new;
        self->_one_dimensional_array->_size = new_size;
        self->_size = new_size;
        return reinterpret_cast<PyObject*>(new_indices);
    }
    Py_INCREF(Py_None);
    return Py_None;
}

static struct PyMethodDef ArrayForTrees_PyMethodDef[] = {
    {"_modify", (PyCFunction) ArrayForTrees__modify, METH_VARARGS, NULL},
    {NULL}
};

static PyTypeObject ArrayForTreesType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "ArrayForTrees",
    /* tp_basicsize */ sizeof(ArrayForTrees),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor) ArrayForTrees_dealloc,
    /* tp_print */ 0,
    /* tp_getattr */ 0,
    /* tp_setattr */ 0,
    /* tp_reserved */ 0,
    /* tp_repr */ 0,
    /* tp_as_number */ 0,
    /* tp_as_sequence */ 0,
    /* tp_as_mapping */ 0,
    /* tp_hash  */ 0,
    /* tp_call */ 0,
    /* tp_str */ 0,
    /* tp_getattro */ 0,
    /* tp_setattro */ 0,
    /* tp_as_buffer */ 0,
    /* tp_flags */ Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    /* tp_doc */ 0,
    /* tp_traverse */ 0,
    /* tp_clear */ 0,
    /* tp_richcompare */ 0,
    /* tp_weaklistoffset */ 0,
    /* tp_iter */ 0,
    /* tp_iternext */ 0,
    /* tp_methods */ ArrayForTrees_PyMethodDef,
    /* tp_members */ 0,
    /* tp_getset */ 0,
    /* tp_base */ &DynamicOneDimensionalArrayType,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ 0,
};

#endif
