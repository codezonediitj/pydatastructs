import random, timeit, functools, os
from pydatastructs import OneDimensionalArray, Backend

def test_OneDimensionalArray():
    ODA = OneDimensionalArray
    cpp = Backend.CPP
    repeat = 2
    number = 1000

    def _test___new__(size):

        def _common(dtype, *args, **kwargs):
            timer_python = timeit.Timer(functools.partial(ODA, dtype, *args, **kwargs))
            python_backend = min(timer_python.repeat(repeat, number))

            kwargs["backend"] = cpp
            timer_cpp = timeit.Timer(functools.partial(ODA, dtype, *args, **kwargs))
            cpp_backend = min(timer_cpp.repeat(repeat, number))

            assert cpp_backend < python_backend

        # Case 1: dtype, size
        _common(int, size)

        # Case 2: dtype, list
        data = [random.randint(0, 2 * size) for _ in range(size)]
        _common(int, data)

        # Case 3: dtype, size, init
        _common(float, size, init=random.random() * 2 * size)

    def _test___getitem_____setitem__(size, func):
        array_python = ODA(float, size)
        array_cpp = ODA(float, size, backend=cpp)
        python_backend = 0
        cpp_backend = 0
        for idx in range(size):
            timer_python = timeit.Timer(functools.partial(func, array_python, idx))
            timer_cpp = timeit.Timer(functools.partial(func, array_cpp, idx))
            python_backend += min(timer_python.repeat(repeat, number))
            cpp_backend += min(timer_cpp.repeat(repeat, number))

        assert cpp_backend < python_backend

    def _test___getitem__(size):
        def func(array, i):
            return array[i]
        _test___getitem_____setitem__(size, func)

    def _test___setitem__(size):
        def func(array, i):
            array[i] = random.random() * 2 * size
        _test___getitem_____setitem__(size, func)

    def _test_fill(size):
        array_python = ODA(float, size)
        array_cpp = ODA(float, size, backend=cpp)
        value = random.random()

        timer_python = timeit.Timer(functools.partial(array_python.fill, value))
        python_backend = min(timer_python.repeat(repeat, number))

        timer_cpp = timeit.Timer(functools.partial(array_cpp.fill, value))
        cpp_backend = min(timer_cpp.repeat(repeat, number))

        assert cpp_backend < python_backend

    def _test_len(size):
        array_python = ODA(float, size)
        array_cpp = ODA(float, size, backend=cpp)

        timer_python = timeit.Timer(functools.partial(len, array_python))
        python_backend = min(timer_python.repeat(repeat, number * 10))

        timer_cpp = timeit.Timer(functools.partial(len, array_cpp))
        cpp_backend = min(timer_cpp.repeat(repeat, number * 10))

        assert cpp_backend < python_backend


    size = int(os.environ.get("PYDATASTRUCTS_BENCHMARK_SIZE", "1000"))
    _test___new__(size)
    _test___getitem__(size)
    _test___setitem__(size)
    _test_fill(size)
    _test_len(size)
