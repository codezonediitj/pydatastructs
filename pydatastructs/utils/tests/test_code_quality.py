import inspect
import os
import re


def _list_files():
    root_path = os.path.abspath(
        os.path.join(
            os.path.split(__file__)[0],
            os.pardir, os.pardir))
    py_files = []
    for (dirpath, _, filenames) in os.walk(root_path):
        for _file in filenames:
            if re.match(r".*\.py$", _file):
                py_files.append(os.path.join(dirpath, _file))
    return py_files


py_files = _list_files()


def test_trailing_white_spaces():
    for file_path in py_files:
        file = open(file_path, "r")
        line = file.readline()
        while line != "":
            if line.endswith(" \n") or line.endswith("\t\n") or line.endswith(" ") or line.endswith("\t"):
                assert False, "%s contains trailing whitespace at %s" \
                              % (file_path, line)
            line = file.readline()
        file.close()


def test_final_new_lines():
    for file_path in py_files:
        file = open(file_path, "r")
        lines = []
        line = file.readline()
        while line != "":
            lines.append(line)
            line = file.readline()
        if lines:
            if lines[-1][-1] != "\n":
                assert False, "%s doesn't contain new line at the end." % file_path
            if lines[-1] == "\n" and lines[-2][-1] == "\n":
                assert False, "%s contains multiple new lines at the end." % file_path
        file.close()


def test_comparison_True_False_None():
    for file_path in py_files:
        if file_path.find("test_code_quality.py") == -1:
            file = open(file_path, "r")
            line = file.readline()
            while line != "":
                if (line.find("== True") != -1) or (line.find("== False") != -1) or (line.find("== None") != -1) or (line.find("!= True") != -1) or (line.find("!= False") != -1) or (line.find("!= None") != -1):
                    assert False, "%s compares True/False/None using by " \
                                  "value, should be done by reference at %s" \
                                  % (file_path, line)
                line = file.readline()
            file.close()


def test_presence_of_tabs():
    for file_path in py_files:
        file = open(file_path, "r")
        line = file.readline()
        while line != "":
            line = file.readline()
            if line.find('\t') != -1:
                assert False, "Tab present at %s in %s. " \
                              "Configure your editor to use " \
                              "white spaces." % (line, file_path)
        file.close()


def _apis():
    import pydatastructs as pyds
    return [
        pyds.graphs.adjacency_list.AdjacencyList,
        pyds.graphs.adjacency_matrix.AdjacencyMatrix,
        pyds.DoublyLinkedList, pyds.SinglyLinkedList,
        pyds.SinglyCircularLinkedList,
        pyds.DoublyCircularLinkedList,
        pyds.OneDimensionalArray, pyds.MultiDimensionalArray,
        pyds.DynamicOneDimensionalArray,
        pyds.trees.BinaryTree, pyds.BinarySearchTree,
        pyds.AVLTree, pyds.SplayTree, pyds.BinaryTreeTraversal,
        pyds.DHeap, pyds.BinaryHeap, pyds.TernaryHeap, pyds.BinomialHeap,
        pyds.MAryTree, pyds.OneDimensionalSegmentTree,
        pyds.Queue, pyds.miscellaneous_data_structures.queue.ArrayQueue,
        pyds.miscellaneous_data_structures.queue.LinkedListQueue,
        pyds.PriorityQueue,
        pyds.miscellaneous_data_structures.queue.LinkedListPriorityQueue,
        pyds.miscellaneous_data_structures.queue.BinaryHeapPriorityQueue,
        pyds.miscellaneous_data_structures.queue.BinomialHeapPriorityQueue,
        pyds.Stack, pyds.miscellaneous_data_structures.stack.ArrayStack,
        pyds.miscellaneous_data_structures.stack.LinkedListStack,
        pyds.DisjointSetForest, pyds.BinomialTree, pyds.TreeNode, pyds.MAryTreeNode,
        pyds.LinkedListNode, pyds.BinomialTreeNode, pyds.AdjacencyListGraphNode,
        pyds.AdjacencyMatrixGraphNode, pyds.GraphEdge, pyds.Set, pyds.BinaryIndexedTree,
        pyds.CartesianTree, pyds.CartesianTreeNode, pyds.Treap, pyds.RedBlackTreeNode, pyds.RedBlackTree,
        pyds.Trie, pyds.TrieNode]


def test_public_api():
    apis = _apis()
    print("\n\nAPI Report")
    print("==========")
    for name in apis:
        if inspect.isclass(name):
            _class = name
            mro = _class.__mro__
            must_methods = _class.methods()
            print("\n" + str(name))
            print("Methods Implemented")
            print(must_methods)
            print("Parent Classes")
            print(mro[1:])
            for supercls in mro:
                if supercls != _class:
                    for method in must_methods:
                        if hasattr(supercls, method) and getattr(supercls, method) == getattr(_class, method):
                            assert False, ("%s class doesn't "
                                           "have %s method implemented." % (
                                               _class, method
                                           ))
