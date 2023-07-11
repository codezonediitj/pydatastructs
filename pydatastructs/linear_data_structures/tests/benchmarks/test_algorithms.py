import random, timeit, functools, os, pytest
from pydatastructs import (OneDimensionalArray, Backend,
    DynamicOneDimensionalArray, quick_sort, bubble_sort)

def _test_common_sort(sort, **kwargs):
    cpp = Backend.CPP
    repeat = 2
    number = 2

    size = int(os.environ.get("PYDATASTRUCTS_BENCHMARK_SIZE", "1000"))
    size = kwargs.get("size", size)

    def _common(array_type, dtype, *args, **kwargs):
        array = array_type(dtype, *args, **kwargs)

        timer_python = timeit.Timer(functools.partial(sort, array))
        python_backend = min(timer_python.repeat(repeat, number))

        backend_dict = {"backend": cpp}
        timer_cpp = timeit.Timer(functools.partial(sort, array, **backend_dict))
        cpp_backend = min(timer_cpp.repeat(repeat, number))

        assert cpp_backend < python_backend

    # Case 1: int
    data = [random.randint(0, 2 * size) for _ in range(size)]
    _common(OneDimensionalArray, int, data, backend=cpp)

    # Case 3: float
    data = [random.random() * 2 * size for _ in range(size)]
    _common(OneDimensionalArray, float, data, backend=cpp)


@pytest.mark.xfail
def test_quick_sort():
    _test_common_sort(quick_sort, size=4000)


@pytest.mark.xfail
def test_bubble_sort():
    _test_common_sort(bubble_sort, size=2000)
