#ifndef LINEAR_DATA_STRUCTURES_ARRAYFORTREES_HPP
#define LINEAR_DATA_STRUCTURES_ARRAYFORTREES_HPP

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
// #include <iostream>
#include "DynamicOneDimensionalArray.hpp"
#include "OneDimensionalArray.hpp"
#include "../../../../utils/_backend/cpp/TreeNode.hpp"
#include "../../../../utils/_backend/cpp/utils.hpp"

typedef struct {
    PyObject_HEAD
    DynamicOneDimensionalArray* dynamic_one_dimensional_array;
} ArrayForTrees;

static void ArrayForTrees_dealloc(ArrayForTrees *self) {
    DynamicOneDimensionalArray_dealloc(self->dynamic_one_dimensional_array);
    Py_TYPE(self)->tp_free(reinterpret_cast<PyObject*>(self));
}

static PyObject* ArrayForTrees___new__(PyTypeObject* type, PyObject *args, PyObject *kwds) {
    ArrayForTrees *self;
    self = reinterpret_cast<ArrayForTrees*>(type->tp_alloc(type, 0));

    if (PyType_Ready(&DynamicOneDimensionalArrayType) < 0) { // This has to be present to finalize a type object. This should be called on all type objects to finish their initialization.
        return NULL;
    }
    PyObject* doda = DynamicOneDimensionalArray___new__(&DynamicOneDimensionalArrayType, args, kwds);
    self->dynamic_one_dimensional_array = reinterpret_cast<DynamicOneDimensionalArray*>(doda);

    return reinterpret_cast<PyObject*>(self);
}

// static PyObject* ArrayForTrees__modify(ArrayForTrees *self) {
//     if(((double)self->_dynamic_one_dimensional_array->_num/(double)self->_dynamic_one_dimensional_array->_size) < self->_dynamic_one_dimensional_array->_load_factor){
//         PyObject* new_indices = PyDict_New();

//         // PyObject* arr_new = OneDimensionalArray___new__(&TreeNodeType, reinterpret_cast<PyObject*>(2*self->_num + 1));
//         // This is how arr_new was made in DynamicOneDimensionalArray__modify() for the previous line :-
//         long new_size = 2 * self->_dynamic_one_dimensional_array->_num + 1;
//         PyObject** arr_new = reinterpret_cast<PyObject**>(std::malloc(new_size * sizeof(PyObject*)));
//         for( int i = 0; i < new_size; i++ ) {
//             Py_INCREF(Py_None);
//             arr_new[i] = Py_None;
//         }

//         int j=0;
//         PyObject** _data = self->_dynamic_one_dimensional_array->_one_dimensional_array->_data; // Check this line
//         for(int i=0; i<=self->_dynamic_one_dimensional_array->_last_pos_filled;i++){
//             if(_data[i] != Py_None){ // Check this line. Python code: if self[i] is not None:
//                 Py_INCREF(Py_None); // This was put in DynamicOneDimensionalArray line 116
//                 arr_new[j] = _data[i];
//                 PyObject_SetItem(new_indices, reinterpret_cast<PyObject*>(reinterpret_cast<TreeNode*>(_data[i])->key), reinterpret_cast<PyObject*>(j));
//                 j += 1;
//             }
//         }
//         for(int i=0;i<j;i++){
//             if(reinterpret_cast<TreeNode*>(arr_new[i])->left != Py_None){
//                 reinterpret_cast<TreeNode*>(arr_new[i])->left = PyObject_GetItem(
//                     new_indices,
//                     PyLong_FromLong(
//                         reinterpret_cast<TreeNode*>(_data[PyLong_AsLong(reinterpret_cast<TreeNode*>(arr_new[i])->left)])->key
//                     )
//                 );
//             }
//             if(reinterpret_cast<TreeNode*>(arr_new[i])->right != Py_None){
//                 reinterpret_cast<TreeNode*>(arr_new[i])->right = PyObject_GetItem(
//                     new_indices,
//                     PyLong_FromLong(
//                         reinterpret_cast<TreeNode*>(_data[PyLong_AsLong(reinterpret_cast<TreeNode*>(arr_new[i])->right)])->key
//                     )
//                 );
//             }
//             if(reinterpret_cast<TreeNode*>(arr_new[i])->parent != Py_None){
//                 reinterpret_cast<TreeNode*>(arr_new[i])->parent = PyObject_GetItem(
//                     new_indices,
//                     PyLong_FromLong(
//                         reinterpret_cast<TreeNode*>(_data[PyLong_AsLong(reinterpret_cast<TreeNode*>(arr_new[i])->parent)])->key
//                     )
//                 );
//             }
//         }
//         self->_dynamic_one_dimensional_array->_last_pos_filled = j - 1;
//         self->_dynamic_one_dimensional_array->_one_dimensional_array->_data = arr_new;
//         self->_dynamic_one_dimensional_array->_size = new_size;
//         self->_dynamic_one_dimensional_array->_size = new_size;
//         return new_indices;
//     }
//     Py_INCREF(Py_None);
//     return Py_None;
// }

static struct PyMethodDef ArrayForTrees_PyMethodDef[] = {
    // {"_modify", (PyCFunction) ArrayForTrees__modify, METH_NOARGS, NULL},
    {NULL}
};

// Check T_OBJECT in the following
static struct PyMemberDef ArrayForTrees_PyMemberDef[] = {
    {"dynamic_one_dimensional_array", T_OBJECT,
     offsetof(ArrayForTrees, dynamic_one_dimensional_array),
     0, "doda for ArrayForTrees"},
    {NULL},
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
    /* tp_members */ ArrayForTrees_PyMemberDef,
    /* tp_getset */ 0,
    /* tp_base */ &DynamicOneDimensionalArrayType,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ ArrayForTrees___new__,
};

#endif
