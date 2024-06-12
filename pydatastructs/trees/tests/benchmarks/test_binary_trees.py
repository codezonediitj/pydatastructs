import timeit, functools, os, pytest
from pydatastructs.trees.binary_trees import (BinarySearchTree, RedBlackTree)
from pydatastructs.utils.misc_util import Backend

@pytest.mark.xfail
def test_BinarySearchTree(**kwargs):
    cpp = Backend.CPP
    repeat = 1
    number = 1

    size = int(os.environ.get("PYDATASTRUCTS_BENCHMARK_SIZE", "1000"))
    size = kwargs.get("size", size)

    BST = BinarySearchTree
    b1 = BST(backend=Backend.PYTHON)
    b2 = BST(backend=Backend.CPP)

    def f(backend, tree):
        for node in range(-1000,1000):
            tree.insert(node, node)
    def g(backend, tree):
        for node in range(-1000, 1000):
            tree.search(node)
    def h(backend, tree):
        for node in range(-1000, 1000):
            tree.delete(node)

    kwds_dict_PY = {"backend": Backend.PYTHON, "tree":b1}
    kwds_dict_CPP = {"backend": Backend.CPP, "tree":b2}

    timer_python = timeit.Timer(functools.partial(f, **kwds_dict_PY))
    python_insert = min(timer_python.repeat(repeat, number))

    timer_cpp = timeit.Timer(functools.partial(f, **kwds_dict_CPP))
    cpp_insert = min(timer_cpp.repeat(repeat, number))
    assert cpp_insert < python_insert

    timer_python = timeit.Timer(functools.partial(g, **kwds_dict_PY))
    python_search = min(timer_python.repeat(repeat, number))

    timer_cpp = timeit.Timer(functools.partial(g, **kwds_dict_CPP))
    cpp_search = min(timer_cpp.repeat(repeat, number))
    assert cpp_search < python_search

    timer_python = timeit.Timer(functools.partial(h, **kwds_dict_PY))
    python_delete = min(timer_python.repeat(repeat, number))

    timer_cpp = timeit.Timer(functools.partial(h, **kwds_dict_CPP))
    cpp_delete = min(timer_cpp.repeat(repeat, number))
    assert cpp_delete < python_delete

@pytest.mark.xfail
def test_RedBlackTree(**kwargs):
    cpp = Backend.CPP
    repeat = 1
    number = 1

    size = int(os.environ.get("PYDATASTRUCTS_BENCHMARK_SIZE", "1000"))
    size = kwargs.get("size", size)

    RBT = RedBlackTree
    b1 = RBT(backend=Backend.PYTHON)
    b2 = RBT(backend=Backend.CPP)

    def f(backend, tree):
        for node in range(-1000,1000):
            tree.insert(node, node)

    def g(backend, tree):
        for node in range(-1000, 1000):
            tree.search(node)
    def h(backend, tree):
        for node in range(-1000, 1000):
            tree.delete(node)

    kwds_dict_PY = {"backend": Backend.PYTHON, "tree":b1}
    kwds_dict_CPP = {"backend": Backend.CPP, "tree":b2}

    timer_python = timeit.Timer(functools.partial(f, **kwds_dict_PY))
    python_insert = min(timer_python.repeat(repeat, number))

    timer_cpp = timeit.Timer(functools.partial(f, **kwds_dict_CPP))
    cpp_insert = min(timer_cpp.repeat(repeat, number))
    assert cpp_insert < python_insert

    timer_python = timeit.Timer(functools.partial(g, **kwds_dict_PY))
    python_search = min(timer_python.repeat(repeat, number))

    timer_cpp = timeit.Timer(functools.partial(g, **kwds_dict_CPP))
    cpp_search = min(timer_cpp.repeat(repeat, number))
    assert cpp_search < python_search

    timer_python = timeit.Timer(functools.partial(h, **kwds_dict_PY))
    python_delete = min(timer_python.repeat(repeat, number))

    timer_cpp = timeit.Timer(functools.partial(h, **kwds_dict_CPP))
    cpp_delete = min(timer_cpp.repeat(repeat, number))
    assert cpp_delete < python_delete
