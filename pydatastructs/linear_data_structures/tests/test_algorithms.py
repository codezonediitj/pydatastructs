from pydatastructs import (
    merge_sort_parallel, DynamicOneDimensionalArray,
    OneDimensionalArray, brick_sort)
import random

def test_merge_sort_parallel():

    random.seed(1000)

    n = random.randint(10, 20)
    arr = DynamicOneDimensionalArray(int, 0)
    for _ in range(n):
        arr.append(random.randint(1, 1000))
    for _ in range(n//3):
        arr.delete(random.randint(0, n//2))
    expected_arr = [686, 779, 102, 134, 362, 448,
                    480, 548, None, None, None,
                    228, 688, 247, 373, 696, None,
                    None, None, None, None, None,
                    None, None, None, None, None,
                    None, None, None, None]
    merge_sort_parallel(arr, 5, start=2, end=10)
    assert arr._data == expected_arr
    merge_sort_parallel(arr, 5)
    expected_arr = [102, 134, 228, 247, 362, 373, 448,
                    480, 548, 686, 688, 696, 779,
                    None, None, None, None, None, None,
                    None, None, None, None, None,
                    None, None, None, None, None, None, None]
    assert arr._data == expected_arr
    assert (arr._last_pos_filled, arr._num, arr._size) == (12, 13, 31)

    n = random.randint(10, 20)
    arr = OneDimensionalArray(int, n)
    for i in range(n):
        arr[i] = random.randint(1, 1000)
    expected_arr = [42, 695, 147, 500, 768,
                    998, 473, 732, 728, 426,
                    709, 910]
    merge_sort_parallel(arr, 5, start=2, end=5)
    assert arr._data == expected_arr

def test_brick_sort():

    random.seed(1000)
    n = 10
    arr = OneDimensionalArray(int, [random.randint(1,1000) for _ in range(n)])
    b = sorted(arr)
    brick_sort(arr)
    assert b == list(arr)

    arr = OneDimensionalArray(int, [random.randint(1,1000) for _ in range(n)])
    brick_sort(arr, comp=lambda u, v: u>v)
    b = list(reversed(sorted(arr)))
    assert b == list(arr)

    arr = DynamicOneDimensionalArray(int, 0)
    for i in range(n):
        arr.append(random.randint(1,1000))

    x = [arr[i] for i in range(arr._last_pos_filled+1)]
    b = sorted(x)
    brick_sort(arr)
    assert b == [arr[i] for i in range(arr._last_pos_filled+1)]
