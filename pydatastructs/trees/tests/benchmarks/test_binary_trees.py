import random, timeit, functools, os, pytest
from pydatastructs.trees.binary_trees import (BinarySearchTree)
from pydatastructs.utils.misc_util import Backend
import random

@pytest.mark.xfail
def test_BST_insert(**kwargs):
    cpp = Backend.CPP
    repeat = 2
    number = 2

    size = int(os.environ.get("PYDATASTRUCTS_BENCHMARK_SIZE", "1000"))
    size = kwargs.get("size", size)

    def f(backend):
        BST = BinarySearchTree
        b = BST(backend=backend)
        for node in range(-1000,1000):
            b.insert(node, node)
        for node in range(-1000, 1000):
            b.search(node)
        for node in range(2000):
            b.delete(node)

    backend_dict = {"backend": Backend.PYTHON}
    timer_python = timeit.Timer(functools.partial(f, **backend_dict))
    python_backend = min(timer_python.repeat(repeat, number))

    backend_dict = {"backend": Backend.CPP}
    timer_cpp = timeit.Timer(functools.partial(f, **backend_dict))
    cpp_backend = min(timer_cpp.repeat(repeat, number))
    print("Python time: ", python_backend)
    print("C++ time: ", cpp_backend)
    assert cpp_backend < python_backend
