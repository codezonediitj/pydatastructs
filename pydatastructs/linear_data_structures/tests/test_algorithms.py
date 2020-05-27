from pydatastructs import (
    merge_sort_parallel, DynamicOneDimensionalArray,
    OneDimensionalArray, brick_sort, brick_sort_parallel,
    heapsort, matrix_multiply_parallel, optimal_grouping)
from pydatastructs.utils.raises_util import raises
import random

def _test_common_sort(sort, *args, **kwargs):
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
    sort(arr, *args, **kwargs, start=2, end=10)
    assert arr._data == expected_arr
    sort(arr, *args, **kwargs)
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
    sort(arr, *args, **kwargs, start=2, end=5)
    assert arr._data == expected_arr

def test_merge_sort_parallel():
    _test_common_sort(merge_sort_parallel, num_threads=5)

def test_brick_sort():
    _test_common_sort(brick_sort)

def test_brick_sort_parallel():
    _test_common_sort(brick_sort_parallel, num_threads=3)

def test_heapsort():
    _test_common_sort(heapsort)

def test_matrix_multiply_parallel():
    ODA = OneDimensionalArray

    expected_result = [[3, 3, 3], [1, 2, 1], [2, 2, 2]]

    I = ODA(ODA, [ODA(int, [1, 1, 0]), ODA(int, [0, 1, 0]), ODA(int, [0, 0, 1])])
    J = ODA(ODA, [ODA(int, [2, 1, 2]), ODA(int, [1, 2, 1]), ODA(int, [2, 2, 2])])
    output = matrix_multiply_parallel(I, J, num_threads=5)
    assert expected_result == output

    I = [[1, 1, 0], [0, 1, 0], [0, 0, 1]]
    J = [[2, 1, 2], [1, 2, 1], [2, 2, 2]]
    output = matrix_multiply_parallel(I, J, num_threads=5)
    assert expected_result == output

    I = [[1, 1, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]]
    J = [[2, 1, 2], [1, 2, 1], [2, 2, 2]]
    assert raises(ValueError, lambda: matrix_multiply_parallel(I, J, num_threads=5))

    I = [[1, 1, 0], [0, 1, 0], [0, 0, 1]]
    J = [[2, 1, 2], [1, 2, 1], [2, 2, 2]]
    output = matrix_multiply_parallel(I, J, num_threads=1)
    assert expected_result == output

def test_optimal_grouping():
    #test case1:
    def cost(matrix, endIndex, middle):

        if endIndex[0] == endIndex[1]:
            return 0
        return matrix[endIndex[0]-1]*matrix[middle]*matrix[endIndex[1]]

    def lookup(position, endIndex, middle):
        if position is 'before':
            return [endIndex[0], middle]
        else:
            return [middle+1, endIndex[1]]
    expected_result = [[float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf')],
                       [float('inf'), 1, 1, 1, 3, 3, 3, float('inf')],
                       [float('inf'), float('inf'), 2, 2, 3, 3, 3, float('inf')],
                       [float('inf'), float('inf'), float('inf'), 3, 3, 3, 3, float('inf')],
                       [float('inf'), float('inf'), float('inf'), float('inf'), 4, 4, 5, float('inf')],
                       [float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 5, 5, float('inf')],
                       [float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), 6, float('inf')],
                       [float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf')]]
    assert expected_result == optimal_grouping([30, 35, 15, 5, 10, 20, 25], False, 2, [1, 6], lookup, cost)

    #test case2:
    expected_result = [[0, float('inf'), float('inf')], [float('inf'), float('inf'), float('inf')], [float('inf'), float('inf'), float('inf')]]
    assert expected_result == optimal_grouping([], False, 2, [0,0], lookup, cost)
