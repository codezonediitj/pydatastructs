import os, re, sys, pydatastructs, inspect
from typing import Type

def _list_files(checker):
    root_path = os.path.abspath(
                os.path.join(
                os.path.split(__file__)[0],
                os.pardir, os.pardir))
    code_files = []
    for (dirpath, _, filenames) in os.walk(root_path):
        for _file in filenames:
            if checker(_file):
                code_files.append(os.path.join(dirpath, _file))
    return code_files

checker = lambda _file: (re.match(r".*\.py$", _file) or
                         re.match(r".*\.cpp$", _file) or
                         re.match(r".*\.hpp$", _file))
code_files = _list_files(checker)

def test_trailing_white_spaces():
    messages = [("The following places in your code "
                 "end with white spaces.")]
    msg = "{}:{}"
    for file_path in code_files:
        file = open(file_path, "r")
        line = file.readline()
        line_number = 1
        while line != "":
            if line.endswith(" \n") or line.endswith("\t\n") \
                or line.endswith(" ") or line.endswith("\t"):
                messages.append(msg.format(file_path, line_number))
            line = file.readline()
            line_number += 1
        file.close()

    if len(messages) > 1:
        assert False, '\n'.join(messages)

def test_final_new_lines():
    messages = [("The following files in your code "
                 "do not end with a single new line.")]
    msg1 = "No new line in {}:{}"
    msg2 = "More than one new line in {}:{}"
    for file_path in code_files:
        file = open(file_path, "r")
        lines = []
        line = file.readline()
        while line != "":
            lines.append(line)
            line = file.readline()
        if lines:
            if lines[-1][-1] != "\n":
                messages.append(msg1.format(file_path, len(lines)))
            if lines[-1] == "\n" and lines[-2][-1] == "\n":
                messages.append(msg2.format(file_path, len(lines)))
        file.close()

    if len(messages) > 1:
        assert False, '\n'.join(messages)

def test_comparison_True_False_None():
    messages = [("The following places in your code "
                 "use `!=` or `==` for comparing True/False/None."
                 "Please use `is` instead.")]
    msg = "{}:{}"
    checker = lambda _file: re.match(r".*\.py$", _file)
    py_files = _list_files(checker)
    for file_path in py_files:
        if file_path.find("test_code_quality.py") == -1:
            file = open(file_path, "r")
            line = file.readline()
            line_number = 1
            while line != "":
                if ((line.find("== True") != -1) or
                    (line.find("== False") != -1) or
                    (line.find("== None") != -1) or
                    (line.find("!= True") != -1) or
                    (line.find("!= False") != -1) or
                    (line.find("!= None") != -1)):
                    messages.append(msg.format(file_path, line_number))
                line = file.readline()
                line_number += 1
            file.close()

    if len(messages) > 1:
        assert False, '\n'.join(messages)

def test_reinterpret_cast():

    def is_variable(str):
        for ch in str:
            if not (ch == '_' or ch.isalnum()):
                return False
        return True

    checker = lambda _file: (re.match(r".*\.cpp$", _file) or
                             re.match(r".*\.hpp$", _file))
    cpp_files = _list_files(checker)
    messages = [("The following lines should use reinterpret_cast"
                 " to cast pointers from one type to another")]
    msg = "Casting to {} at {}:{}"
    for file_path in cpp_files:
        file = open(file_path, "r")
        line = file.readline()
        line_number = 1
        while line != "":
            found_open = False
            between_open_close = ""
            for char in line:
                if char == '(':
                    found_open = True
                elif char == ')':
                    if (between_open_close and
                        between_open_close[-1] == '*' and
                        is_variable(between_open_close[:-1])):
                        messages.append(msg.format(between_open_close[:-1],
                                                   file_path, line_number))
                    between_open_close = ""
                    found_open = False
                elif char != ' ' and found_open:
                    between_open_close += char
            line = file.readline()
            line_number += 1
        file.close()

    if len(messages) > 1:
        assert False, '\n'.join(messages)

def test_presence_of_tabs():
    messages = [("The following places in your code "
                 "use tabs instead of spaces.")]
    msg = "{}:{}"
    for file_path in code_files:
        file = open(file_path, "r")
        line_number = 1
        line = file.readline()
        while line != "":
            if (line.find('\t') != -1):
                messages.append(msg.format(file_path, line_number))
            line = file.readline()
            line_number += 1
        file.close()

    if len(messages) > 1:
        assert False, '\n'.join(messages)

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
    pyds.Trie, pyds.TrieNode, pyds.SkipList, pyds.RangeQueryStatic, pyds.RangeQueryDynamic, pyds.SparseTable,
    pyds.miscellaneous_data_structures.segment_tree.OneDimensionalArraySegmentTree,
    pyds.bubble_sort, pyds.linear_search, pyds.binary_search, pyds.jump_search,
    pyds.selection_sort, pyds.insertion_sort, pyds.quick_sort, pyds.intro_sort]

def test_public_api():
    pyds = pydatastructs
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
                        if hasattr(supercls, method) and \
                            getattr(supercls, method) == \
                            getattr(_class, method):
                            assert False, ("%s class doesn't "
                                "have %s method implemented."%(
                                    _class, method
                                ))

def test_backend_argument_message():

    import pydatastructs as pyds
    backend_implemented = [
        pyds.OneDimensionalArray,
        pyds.DynamicOneDimensionalArray,
        pyds.quick_sort
    ]

    def call_and_raise(api, pos_args_count=0):
        try:
            if pos_args_count == 0:
                api(backend=None)
            elif pos_args_count == 1:
                api(None, backend=None)
            elif pos_args_count == 2:
                api(None, None, backend=None)
        except ValueError as value_error:
            assert str(api) in value_error.args[0]
        except TypeError as type_error:
            max_pos_args_count = 2
            if pos_args_count <= max_pos_args_count:
                call_and_raise(api, pos_args_count + 1)
            else:
                raise type_error

    apis = _apis()
    for api in apis:
        if api not in backend_implemented:
            call_and_raise(api, 0)
