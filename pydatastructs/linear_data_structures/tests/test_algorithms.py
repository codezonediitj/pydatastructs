from pydatastructs import (
    merge_sort_parallel, DynamicOneDimensionalArray,
    OneDimensionalArray)
import random

def test_merge_sort_parallel():

    random.seed(1000)

    n = random.randint(10, 20)
    arr = DynamicOneDimensionalArray(int, 0)
    for _ in range(n):
        arr.append(random.randint(1, 1000))
    for _ in range(n//3):
        arr.delete(random.randint(0, n//2))
    expected_arr = [686, 779, 102, 134, 362,
                    448, 480, 548, 228, 688,
                    247, 373, 696, None, None,
                    None, None, None, None,
                    None, None, None, None,
                    None, None, None, None]
    merge_sort_parallel(arr, 5, start=2, end=10)
    assert arr._data == expected_arr

    n = random.randint(10, 20)
    arr = OneDimensionalArray(int, n)
    for i in range(n):
        arr[i] = random.randint(1, 1000)
    expected_arr = [42, 695, 147, 500, 768,
                    998, 473, 732, 728, 426,
                    709, 910]
    merge_sort_parallel(arr, 5, start=2, end=5)
    assert arr._data == expected_arr
