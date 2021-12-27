import random, timeit, functools, os
from pydatastructs import OneDimensionalArray, Backend

def test_OneDimensionalArray():
    ODA = OneDimensionalArray
    cpp = Backend.CPP

    def _test___new__(size):
        # Case 1: dtype, size
        arr = ODA(int, size)
        timer_python = timeit.Timer(functools.partial(ODA, int, size))
        python_backend = min(timer_python.repeat(10, 10))
        timer_cpp = timeit.Timer(functools.partial(ODA, int, size, backend=cpp))
        cpp_backend = min(timer_cpp.repeat(10, 10))
        assert cpp_backend < python_backend

        # # Case 2: dtype, list
        # data = [random.randint(0, 2 * size) for _ in range(size)]
        # arr = ODA(int, data)

        # # Case 3: dtype, size, init
        # arr = ODA(float, size, init=random.randint(0, 2 * size))

    size = int(os.environ.get("PYDATASTRUCTS_BENCHMARK_SIZE", "1000"))
    _test___new__(size)
