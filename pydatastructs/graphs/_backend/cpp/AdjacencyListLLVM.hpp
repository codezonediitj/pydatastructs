#include <Python.h>
#include <string>
#include <cstring>
#include <stdexcept>
#include <memory>
#include <unordered_map>

extern PyTypeObject AdjacencyListGraphLLVMType;

typedef void* (*GraphInitFunc)();
typedef int (*AddVertexFunc)(void*, const char*, int);
typedef int (*AddEdgeFunc)(void*, const char*, int, const char*, int, double);
typedef int (*IsAdjacentFunc)(void*, const char*, int, const char*, int);
typedef int (*RemoveVertexFunc)(void*, const char*, int);
typedef int (*RemoveEdgeFunc)(void*, const char*, int, const char*, int);
typedef void (*GraphCleanupFunc)(void*);

static GraphInitFunc llvm_graph_init = nullptr;
static AddVertexFunc llvm_add_vertex = nullptr;
static AddEdgeFunc llvm_add_edge = nullptr;
static IsAdjacentFunc llvm_is_adjacent = nullptr;
static RemoveVertexFunc llvm_remove_vertex = nullptr;
static RemoveEdgeFunc llvm_remove_edge = nullptr;
static GraphCleanupFunc llvm_graph_cleanup = nullptr;

static void* llvm_execution_engine = nullptr;
static bool llvm_backend_initialized = false;

typedef struct {
    PyObject_HEAD
    void* llvm_graph_ptr;
    bool is_valid;
} AdjacencyListGraphLLVM;

static int safe_strlen(const char* str) {
    return str ? static_cast<int>(strlen(str)) : 0;
}

static PyObject* initialize_llvm_backend(PyObject* self, PyObject* args) {
    PyObject* func_dict;
    PyObject* ee_obj;

    if (!PyArg_ParseTuple(args, "OO", &func_dict, &ee_obj)) {
        return nullptr;
    }

    if (!PyDict_Check(func_dict)) {
        PyErr_SetString(PyExc_TypeError, "First argument must be a dictionary");
        return nullptr;
    }

    llvm_execution_engine = PyLong_AsVoidPtr(ee_obj);
    if (PyErr_Occurred()) {
        PyErr_SetString(PyExc_ValueError, "Invalid execution engine object");
        return nullptr;
    }

    PyObject* init_ptr = PyDict_GetItemString(func_dict, "graph_init");
    PyObject* add_vertex_ptr = PyDict_GetItemString(func_dict, "add_vertex");
    PyObject* add_edge_ptr = PyDict_GetItemString(func_dict, "add_edge");
    PyObject* is_adjacent_ptr = PyDict_GetItemString(func_dict, "is_adjacent");
    PyObject* remove_vertex_ptr = PyDict_GetItemString(func_dict, "remove_vertex");
    PyObject* remove_edge_ptr = PyDict_GetItemString(func_dict, "remove_edge");
    PyObject* cleanup_ptr = PyDict_GetItemString(func_dict, "graph_cleanup");

    if (!init_ptr || !add_vertex_ptr || !add_edge_ptr || !is_adjacent_ptr ||
        !remove_vertex_ptr || !remove_edge_ptr || !cleanup_ptr) {
        PyErr_SetString(PyExc_ValueError, "Missing required function pointers in dictionary");
        return nullptr;
    }

    llvm_graph_init = (GraphInitFunc)PyLong_AsVoidPtr(init_ptr);
    llvm_add_vertex = (AddVertexFunc)PyLong_AsVoidPtr(add_vertex_ptr);
    llvm_add_edge = (AddEdgeFunc)PyLong_AsVoidPtr(add_edge_ptr);
    llvm_is_adjacent = (IsAdjacentFunc)PyLong_AsVoidPtr(is_adjacent_ptr);
    llvm_remove_vertex = (RemoveVertexFunc)PyLong_AsVoidPtr(remove_vertex_ptr);
    llvm_remove_edge = (RemoveEdgeFunc)PyLong_AsVoidPtr(remove_edge_ptr);
    llvm_graph_cleanup = (GraphCleanupFunc)PyLong_AsVoidPtr(cleanup_ptr);

    if (PyErr_Occurred()) {
        PyErr_SetString(PyExc_ValueError, "Failed to convert function pointers");
        return nullptr;
    }

    if (!llvm_graph_init || !llvm_add_vertex || !llvm_add_edge ||
        !llvm_is_adjacent || !llvm_remove_vertex || !llvm_remove_edge ||
        !llvm_graph_cleanup) {
        PyErr_SetString(PyExc_ValueError, "One or more function pointers are null");
        return nullptr;
    }

    llvm_backend_initialized = true;

    Py_RETURN_NONE;
}

static bool check_llvm_backend() {
    return llvm_backend_initialized && llvm_graph_init && llvm_add_vertex &&
           llvm_add_edge && llvm_is_adjacent && llvm_remove_vertex &&
           llvm_remove_edge && llvm_graph_cleanup;
}

static void AdjacencyListGraphLLVM_dealloc(AdjacencyListGraphLLVM* self) {
    if (self->is_valid && self->llvm_graph_ptr && llvm_graph_cleanup) {
        llvm_graph_cleanup(self->llvm_graph_ptr);
        self->llvm_graph_ptr = nullptr;
        self->is_valid = false;
    }
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* AdjacencyListGraphLLVM_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    AdjacencyListGraphLLVM* self = (AdjacencyListGraphLLVM*)type->tp_alloc(type, 0);
    if (!self) {
        return nullptr;
    }

    self->llvm_graph_ptr = nullptr;
    self->is_valid = false;

    return (PyObject*)self;
}

static int AdjacencyListGraphLLVM_init(AdjacencyListGraphLLVM* self, PyObject* args, PyObject* kwds) {
    if (!check_llvm_backend()) {
        PyErr_SetString(PyExc_RuntimeError,
            "LLVM backend not initialized. Call initialize_llvm_backend() first.");
        return -1;
    }

    self->llvm_graph_ptr = llvm_graph_init();
    if (!self->llvm_graph_ptr) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to initialize LLVM graph");
        return -1;
    }

    self->is_valid = true;
    return 0;
}

static PyObject* AdjacencyListGraphLLVM_add_vertex(AdjacencyListGraphLLVM* self, PyObject* args) {
    const char* name;

    if (!PyArg_ParseTuple(args, "s", &name)) {
        return nullptr;
    }

    if (!self->is_valid || !self->llvm_graph_ptr) {
        PyErr_SetString(PyExc_RuntimeError, "Invalid graph object");
        return nullptr;
    }

    if (!check_llvm_backend()) {
        PyErr_SetString(PyExc_RuntimeError, "LLVM backend not properly initialized");
        return nullptr;
    }

    int name_len = safe_strlen(name);
    int result = llvm_add_vertex(self->llvm_graph_ptr, name, name_len);

    if (result != 0) {
        if (result == -1) {
            PyErr_SetString(PyExc_ValueError, "Vertex with this name already exists");
        } else {
            PyErr_Format(PyExc_RuntimeError, "Failed to add vertex (error code: %d)", result);
        }
        return nullptr;
    }

    Py_RETURN_NONE;
}

static PyObject* AdjacencyListGraphLLVM_add_edge(AdjacencyListGraphLLVM* self, PyObject* args) {
    const char* source;
    const char* target;
    double weight = 1.0;

    if (!PyArg_ParseTuple(args, "ss|d", &source, &target, &weight)) {
        return nullptr;
    }

    if (!self->is_valid || !self->llvm_graph_ptr) {
        PyErr_SetString(PyExc_RuntimeError, "Invalid graph object");
        return nullptr;
    }

    if (!check_llvm_backend()) {
        PyErr_SetString(PyExc_RuntimeError, "LLVM backend not properly initialized");
        return nullptr;
    }

    int src_len = safe_strlen(source);
    int tgt_len = safe_strlen(target);
    int result = llvm_add_edge(self->llvm_graph_ptr, source, src_len, target, tgt_len, weight);

    if (result != 0) {
        if (result == -1) {
            PyErr_SetString(PyExc_ValueError, "Source vertex not found");
        } else if (result == -2) {
            PyErr_SetString(PyExc_ValueError, "Target vertex not found");
        } else {
            PyErr_Format(PyExc_RuntimeError, "Failed to add edge (error code: %d)", result);
        }
        return nullptr;
    }

    Py_RETURN_NONE;
}

static PyObject* AdjacencyListGraphLLVM_is_adjacent(AdjacencyListGraphLLVM* self, PyObject* args) {
    const char* node1;
    const char* node2;

    if (!PyArg_ParseTuple(args, "ss", &node1, &node2)) {
        return nullptr;
    }

    if (!self->is_valid || !self->llvm_graph_ptr) {
        PyErr_SetString(PyExc_RuntimeError, "Invalid graph object");
        return nullptr;
    }

    if (!check_llvm_backend()) {
        PyErr_SetString(PyExc_RuntimeError, "LLVM backend not properly initialized");
        return nullptr;
    }

    int node1_len = safe_strlen(node1);
    int node2_len = safe_strlen(node2);
    int result = llvm_is_adjacent(self->llvm_graph_ptr, node1, node1_len, node2, node2_len);

    if (result == 1) {
        Py_RETURN_TRUE;
    } else {
        Py_RETURN_FALSE;
    }
}

static PyObject* AdjacencyListGraphLLVM_remove_vertex(AdjacencyListGraphLLVM* self, PyObject* args) {
    const char* name;

    if (!PyArg_ParseTuple(args, "s", &name)) {
        return nullptr;
    }

    if (!self->is_valid || !self->llvm_graph_ptr) {
        PyErr_SetString(PyExc_RuntimeError, "Invalid graph object");
        return nullptr;
    }

    if (!check_llvm_backend()) {
        PyErr_SetString(PyExc_RuntimeError, "LLVM backend not properly initialized");
        return nullptr;
    }

    int name_len = safe_strlen(name);
    int result = llvm_remove_vertex(self->llvm_graph_ptr, name, name_len);

    if (result != 0) {
        if (result == -1) {
            PyErr_SetString(PyExc_ValueError, "Vertex not found");
        } else {
            PyErr_Format(PyExc_RuntimeError, "Failed to remove vertex (error code: %d)", result);
        }
        return nullptr;
    }

    Py_RETURN_NONE;
}

static PyObject* AdjacencyListGraphLLVM_remove_edge(AdjacencyListGraphLLVM* self, PyObject* args) {
    const char* source;
    const char* target;

    if (!PyArg_ParseTuple(args, "ss", &source, &target)) {
        return nullptr;
    }

    if (!self->is_valid || !self->llvm_graph_ptr) {
        PyErr_SetString(PyExc_RuntimeError, "Invalid graph object");
        return nullptr;
    }

    if (!check_llvm_backend()) {
        PyErr_SetString(PyExc_RuntimeError, "LLVM backend not properly initialized");
        return nullptr;
    }

    int src_len = safe_strlen(source);
    int tgt_len = safe_strlen(target);
    int result = llvm_remove_edge(self->llvm_graph_ptr, source, src_len, target, tgt_len);

    if (result != 0) {
        if (result == -1) {
            PyErr_SetString(PyExc_ValueError, "Source vertex not found");
        } else if (result == -2) {
            PyErr_SetString(PyExc_ValueError, "Target vertex not found");
        } else {
            PyErr_Format(PyExc_RuntimeError, "Failed to remove edge (error code: %d)", result);
        }
        return nullptr;
    }

    Py_RETURN_NONE;
}

static PyMethodDef AdjacencyListGraphLLVM_methods[] = {
    {"add_vertex", (PyCFunction)AdjacencyListGraphLLVM_add_vertex, METH_VARARGS,
     "Add a vertex to the graph"},
    {"add_edge", (PyCFunction)AdjacencyListGraphLLVM_add_edge, METH_VARARGS,
     "Add an edge to the graph"},
    {"is_adjacent", (PyCFunction)AdjacencyListGraphLLVM_is_adjacent, METH_VARARGS,
     "Check if two vertices are adjacent"},
    {"remove_vertex", (PyCFunction)AdjacencyListGraphLLVM_remove_vertex, METH_VARARGS,
     "Remove a vertex from the graph"},
    {"remove_edge", (PyCFunction)AdjacencyListGraphLLVM_remove_edge, METH_VARARGS,
     "Remove an edge from the graph"},
    {nullptr}
};

PyTypeObject AdjacencyListGraphLLVMType = {
    PyVarObject_HEAD_INIT(nullptr, 0)
    "llvm_graph.AdjacencyListGraphLLVM",     // tp_name
    sizeof(AdjacencyListGraphLLVM),          // tp_basicsize
    0,                                       // tp_itemsize
    (destructor)AdjacencyListGraphLLVM_dealloc, // tp_dealloc
    0,                                       // tp_vectorcall_offset
    0,                                       // tp_getattr
    0,                                       // tp_setattr
    0,                                       // tp_as_async
    0,                                       // tp_repr
    0,                                       // tp_as_number
    0,                                       // tp_as_sequence
    0,                                       // tp_as_mapping
    0,                                       // tp_hash
    0,                                       // tp_call
    0,                                       // tp_str
    0,                                       // tp_getattro
    0,                                       // tp_setattro
    0,                                       // tp_as_buffer
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, // tp_flags
    "LLVM-backed adjacency list graph",      // tp_doc
    0,                                       // tp_traverse
    0,                                       // tp_clear
    0,                                       // tp_richcompare
    0,                                       // tp_weaklistoffset
    0,                                       // tp_iter
    0,                                       // tp_iternext
    AdjacencyListGraphLLVM_methods,          // tp_methods
    0,                                       // tp_members
    0,                                       // tp_getset
    0,                                       // tp_base
    0,                                       // tp_dict
    0,                                       // tp_descr_get
    0,                                       // tp_descr_set
    0,                                       // tp_dictoffset
    (initproc)AdjacencyListGraphLLVM_init,   // tp_init
    0,                                       // tp_alloc
    AdjacencyListGraphLLVM_new,              // tp_new
};
