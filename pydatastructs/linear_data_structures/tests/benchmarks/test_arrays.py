import random, timeit, functools, os, pytest
from pydatastructs import (OneDimensionalArray, Backend,
    DynamicOneDimensionalArray)

def _test_OneDimensionalArray_DynamicOneDimensionalArray(array_type):
    cpp = Backend.CPP
    repeat = 2
    number = 1000

    def _test___new__(size):

        def _common(dtype, *args, **kwargs):
            timer_python = timeit.Timer(functools.partial(array_type, dtype, *args, **kwargs))
            python_backend = min(timer_python.repeat(repeat, number))

            kwargs["backend"] = cpp
            timer_cpp = timeit.Timer(functools.partial(array_type, dtype, *args, **kwargs))
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
        array_python = array_type(float, size)
        array_cpp = array_type(float, size, backend=cpp)
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
        array_python = array_type(float, size)
        array_cpp = array_type(float, size, backend=cpp)
        value = random.random()

        timer_python = timeit.Timer(functools.partial(array_python.fill, value))
        python_backend = min(timer_python.repeat(repeat, number))

        timer_cpp = timeit.Timer(functools.partial(array_cpp.fill, value))
        cpp_backend = min(timer_cpp.repeat(repeat, number))

        assert cpp_backend < python_backend

    def _test_len(size):
        array_python = array_type(float, size)
        array_cpp = array_type(float, size, backend=cpp)

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

@pytest.mark.xfail
def test_OneDimensionalArray():
    _test_OneDimensionalArray_DynamicOneDimensionalArray(OneDimensionalArray)

@pytest.mark.xfail
def test_DynamicOneDimensionalArray():
    _test_OneDimensionalArray_DynamicOneDimensionalArray(DynamicOneDimensionalArray)

    repeat = 2
    number = 1000

    def _test_append(size):
        data = [random.randint(-size, size) for _ in range(size)]
        doda_cpp = DynamicOneDimensionalArray(int, 0, backend=Backend.CPP)
        doda_python = DynamicOneDimensionalArray(int, 0)
        python_list = []

        cpp_backend, python_backend, list_time = (0, 0, 0)
        for datum in data:
            timer_cpp = timeit.Timer(functools.partial(doda_cpp.append, datum))
            cpp_backend += min(timer_cpp.repeat(repeat, number))

            timer_python = timeit.Timer(functools.partial(doda_python.append, datum))
            python_backend += min(timer_python.repeat(repeat, number))

            timer_list = timeit.Timer(functools.partial(python_list.append, datum))
            list_time += min(timer_list.repeat(repeat, number))

        assert cpp_backend < python_backend
        assert cpp_backend/list_time < 1.5

    def _test_delete(size):
        data = [random.random() * 2 * size for _ in range(size)]
        doda_cpp = DynamicOneDimensionalArray(float, data, backend=Backend.CPP)
        doda_python = DynamicOneDimensionalArray(float, data)
        python_list = [datum for datum in data]
        list_indices = [i for i in range(size)]
        random.seed(0)
        random.shuffle(list_indices)

        def _list_remove(obj, index):
            del obj[index]

        list_time = 0
        for i in range(size):
            idx = list_indices[i]

            timer_list = timeit.Timer(functools.partial(_list_remove, python_list, idx))
            list_time += min(timer_list.repeat(1, 1))

            for j in range(i + 1, size):
                if list_indices[j] > idx:
                    list_indices[j] -= 1

        cpp_backend, python_backend = (0, 0)
        while doda_cpp._num > 0:
            indices = [i for i in range(doda_cpp._last_pos_filled + 1)]
            random.shuffle(indices)
            for idx in indices:
                timer_cpp = timeit.Timer(functools.partial(doda_cpp.delete, idx))
                cpp_backend += min(timer_cpp.repeat(1, 1))

                timer_python = timeit.Timer(functools.partial(doda_python.delete, idx))
                python_backend += min(timer_python.repeat(1, 1))

                if doda_cpp._num == 0:
                    break

        assert cpp_backend < python_backend
        assert cpp_backend < list_time

    size = int(os.environ.get("PYDATASTRUCTS_BENCHMARK_SIZE", "1000"))
    _test_append(size)
    _test_delete(size * 4)
