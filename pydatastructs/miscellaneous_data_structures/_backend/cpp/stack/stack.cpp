#include <Python.h>
#include <vector>
#include <stdexcept>
#include "SinglyLinkedList.hpp"
#include "DynamicOneDimensionalArray.hpp"

// Forward declarations for types in the module
extern PyTypeObject ArrayStackType;
extern PyTypeObject LinkedListStackType;

static struct PyModuleDef stackmodule = {
    PyModuleDef_HEAD_INIT,
    "_stack",
    "Stack Data Structure Module",
    -1,
    NULL
};

// Stack base class (Abstract class)
class Stack {
public:
    virtual void push(PyObject* x) = 0;
    virtual PyObject* pop() = 0;
    virtual bool is_empty() = 0;
    virtual PyObject* peek() = 0;
    virtual Py_ssize_t __len__() = 0;
    virtual const char* __str__() = 0;
};

// ArrayStack Implementation (Derived class)
class ArrayStack : public Stack {
public:
    std::vector<PyObject*> items; // Dynamic array to store items

    ArrayStack() {}

    ArrayStack(std::vector<PyObject*> initial_items) {
        items = initial_items;
    }

    void push(PyObject* x) override {
        items.push_back(x);
    }

    PyObject* pop() override {
        if (is_empty()) {
            throw std::out_of_range("Stack is empty");
        }
        PyObject* top_element = items.back();
        items.pop_back();
        return top_element;
    }

    bool is_empty() override {
        return items.empty();
    }

    PyObject* peek() override {
        if (is_empty()) {
            throw std::out_of_range("Stack is empty");
        }
        return items.back();
    }

    Py_ssize_t __len__() override {
        return items.size();
    }

    const char* __str__() override {
        std::string result = "[";
        for (size_t i = 0; i < items.size(); ++i) {
            result += PyUnicode_AsUTF8(PyObject_Str(items[i]));
            if (i != items.size() - 1) {
                result += ", ";
            }
        }
        result += "]";
        return result.c_str();
    }
};

// LinkedListStack Implementation (Derived class)
class LinkedListStack : public Stack {
public:
    SinglyLinkedList stack; // Linked list to store the stack elements

    LinkedListStack() {}

    LinkedListStack(std::vector<PyObject*> initial_items) {
        for (auto& item : initial_items) {
            push(item);
        }
    }

    void push(PyObject* x) override {
        stack.appendleft(x);
    }

    PyObject* pop() override {
        if (is_empty()) {
            throw std::out_of_range("Stack is empty");
        }
        return stack.popleft();
    }

    bool is_empty() override {
        return stack.size() == 0;
    }

    PyObject* peek() override {
        return stack.head;
    }

    Py_ssize_t __len__() override {
        return stack.size();
    }

    const char* __str__() override {
        std::string result = "[";
        auto node = stack.head;
        while (node != nullptr) {
            result += PyUnicode_AsUTF8(PyObject_Str(node->data));
            if (node->next != nullptr) {
                result += ", ";
            }
            node = node->next;
        }
        result += "]";
        return result.c_str();
    }
};

// Python Module Initialization
PyMODINIT_FUNC PyInit__stack(void) {
    PyObject *stack_module = PyModule_Create(&stackmodule);
    if (PyType_Ready(&ArrayStackType) < 0)
        return NULL;
    Py_INCREF(&ArrayStackType);
    PyModule_AddObject(stack_module, "ArrayStack", (PyObject*)&ArrayStackType);

    if (PyType_Ready(&LinkedListStackType) < 0)
        return NULL;
    Py_INCREF(&LinkedListStackType);
    PyModule_AddObject(stack_module, "LinkedListStack", (PyObject*)&LinkedListStackType);

    return stack_module;
}
