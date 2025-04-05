#include <Python.h>
#include <iostream>
#include <unordered_map>
#include <vector>
#include <queue>
#include <thread>
#include <functional>
#include <mutex>

// Graph class to represent the graph
class Graph {
public:
    // Add a node to the graph
    void addNode(const std::string& nodeName) {
        adjacencyList[nodeName] = std::vector<std::string>();
    }

    // Add an edge between two nodes
    void addEdge(const std::string& node1, const std::string& node2) {
        adjacencyList[node1].push_back(node2);
        adjacencyList[node2].push_back(node1);  // Assuming undirected graph
    }

    // Get neighbors of a node
    const std::vector<std::string>& getNeighbors(const std::string& node) const {
        return adjacencyList.at(node);
    }

    // Check if node exists
    bool hasNode(const std::string& node) const {
        return adjacencyList.find(node) != adjacencyList.end();
    }

private:
    std::unordered_map<std::string, std::vector<std::string>> adjacencyList;
};

// Python Graph Object Definition
typedef struct {
    PyObject_HEAD
    Graph graph;
} PyGraphObject;

static PyTypeObject PyGraphType;

// Serial BFS Implementation
static PyObject* breadth_first_search(PyObject* self, PyObject* args) {
    PyGraphObject* pyGraph;
    const char* sourceNode;
    PyObject* pyOperation;

    if (!PyArg_ParseTuple(args, "OsO", &pyGraph, &sourceNode, &pyOperation)) {
        return NULL;
    }

    auto operation = [pyOperation](const std::string& currNode, const std::string& nextNode) -> bool {
        PyObject* result = PyObject_CallFunction(pyOperation, "ss", currNode.c_str(), nextNode.c_str());
        if (result == NULL) {
            return false;
        }
        bool status = PyObject_IsTrue(result);
        Py_XDECREF(result);
        return status;
    };

    std::unordered_map<std::string, bool> visited;
    std::queue<std::string> bfsQueue;
    bfsQueue.push(sourceNode);
    visited[sourceNode] = true;

    while (!bfsQueue.empty()) {
        std::string currNode = bfsQueue.front();
        bfsQueue.pop();

        for (const std::string& nextNode : pyGraph->graph.getNeighbors(currNode)) {
            if (!visited[nextNode]) {
                if (!operation(currNode, nextNode)) {
                    Py_RETURN_NONE;
                }
                bfsQueue.push(nextNode);
                visited[nextNode] = true;
            }
        }
    }

    Py_RETURN_NONE;
}

// Parallel BFS Implementation
static PyObject* breadth_first_search_parallel(PyObject* self, PyObject* args) {
    PyGraphObject* pyGraph;
    const char* sourceNode;
    int numThreads;
    PyObject* pyOperation;

    if (!PyArg_ParseTuple(args, "OsIO", &pyGraph, &sourceNode, &numThreads, &pyOperation)) {
        return NULL;
    }

    auto operation = [pyOperation](const std::string& currNode, const std::string& nextNode) -> bool {
        PyObject* result = PyObject_CallFunction(pyOperation, "ss", currNode.c_str(), nextNode.c_str());
        if (result == NULL) {
            return false;
        }
        bool status = PyObject_IsTrue(result);
        Py_XDECREF(result);
        return status;
    };

    std::unordered_map<std::string, bool> visited;
    std::queue<std::string> bfsQueue;
    std::mutex queueMutex;

    bfsQueue.push(sourceNode);
    visited[sourceNode] = true;

    auto bfsWorker = [&](int threadId) {
        while (true) {
            std::string currNode;
            {
                std::lock_guard<std::mutex> lock(queueMutex);
                if (bfsQueue.empty()) return;
                currNode = bfsQueue.front();
                bfsQueue.pop();
            }

            for (const std::string& nextNode : pyGraph->graph.getNeighbors(currNode)) {
                if (!visited[nextNode]) {
                    if (!operation(currNode, nextNode)) {
                        return;
                    }
                    std::lock_guard<std::mutex> lock(queueMutex);
                    bfsQueue.push(nextNode);
                    visited[nextNode] = true;
                }
            }
        }
    };

    std::vector<std::thread> threads;
    for (int i = 0; i < numThreads; ++i) {
        threads.push_back(std::thread(bfsWorker, i));
    }

    for (auto& t : threads) {
        t.join();
    }

    Py_RETURN_NONE;
}

// Module Method Definitions
static PyMethodDef module_methods[] = {
    {"breadth_first_search", breadth_first_search, METH_VARARGS, "Serial Breadth First Search."},
    {"breadth_first_search_parallel", breadth_first_search_parallel, METH_VARARGS, "Parallel Breadth First Search."},
    {NULL, NULL, 0, NULL}
};

// Python Module Definition
static struct PyModuleDef graphmodule = {
    PyModuleDef_HEAD_INIT,
    "_graph_algorithms",
    "Graph Algorithms C++ Backend",
    -1,
    module_methods
};

// Module Initialization
PyMODINIT_FUNC PyInit__graph_algorithms(void) {
    PyObject* m;

    // Initialize Graph Type
    PyGraphType.tp_name = "Graph";
    PyGraphType.tp_basicsize = sizeof(PyGraphObject);
    PyGraphType.tp_flags = Py_TPFLAGS_DEFAULT;
    PyGraphType.tp_doc = "Graph object in C++.";
    
    if (PyType_Ready(&PyGraphType) < 0) {
        return NULL;
    }

    m = PyModule_Create(&graphmodule);
    if (m == NULL) {
        return NULL;
    }

    // Add Graph Type to module
    Py_INCREF(&PyGraphType);
    PyModule_AddObject(m, "Graph", (PyObject*)&PyGraphType);

    return m;
}
