from pydatastructs.linear_data_structures.arrays import (
    OneDimensionalArray, DynamicArray, Array)
from pydatastructs.utils.misc_util import _check_type, _comp
from concurrent.futures import ThreadPoolExecutor
from math import log, floor

__all__ = [
    'merge_sort_parallel',
    'brick_sort',
    'brick_sort_parallel',
    'heapsort',
    'matrix_multiply_parallel',
    'counting_sort',
    'bucket_sort',
    'cocktail_shaker_sort',
    'quick_sort',
    'longest_common_subsequence'
]


def _merge(array, sl, el, sr, er, end, comp):
    l, r = [], []
    for i in range(sl, el + 1):
        if i <= end:
            l.append(array[i])
            array[i] = None
    for i in range(sr, er + 1):
        if i <= end:
            r.append(array[i])
            array[i] = None
    i, j, k = 0, 0, sl
    while i < len(l) and j < len(r):
        if _comp(l[i], r[j], comp):
            array[k] = l[i]
            i += 1
        else:
            array[k] = r[j]
            j += 1
        k += 1

    while i < len(l):
        array[k] = l[i]
        i += 1
        k += 1

    while j < len(r):
        array[k] = r[j]
        j += 1
        k += 1


def merge_sort_parallel(array, num_threads, **kwargs):
    """
    Implements parallel merge sort.

    Parameters
    ==========

    array: Array
        The array which is to be sorted.
    num_threads: int
        The maximum number of threads
        to be used for sorting.
    start: int
        The starting index of the portion
        which is to be sorted.
        Optional, by default 0
    end: int
        The ending index of the portion which
        is to be sorted.
        Optional, by default the index
        of the last position filled.
    comp: lambda/function
        The comparator which is to be used
        for sorting. If the function returns
        False then only swapping is performed.
        Optional, by default, less than or
        equal to is used for comparing two
        values.

    Examples
    ========

    >>> from pydatastructs import OneDimensionalArray, merge_sort_parallel
    >>> arr = OneDimensionalArray(int,[3, 2, 1])
    >>> merge_sort_parallel(arr, 3)
    >>> [arr[0], arr[1], arr[2]]
    [1, 2, 3]
    >>> merge_sort_parallel(arr, 3, comp=lambda u, v: u > v)
    >>> [arr[0], arr[1], arr[2]]
    [3, 2, 1]

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Merge_sort
    """
    start = kwargs.get('start', 0)
    end = kwargs.get('end', len(array) - 1)
    comp = kwargs.get("comp", lambda u, v: u <= v)
    for size in range(floor(log(end - start + 1, 2)) + 1):
        pow_2 = 2 ** size
        with ThreadPoolExecutor(max_workers=num_threads) as Executor:
            i = start
            while i <= end:
                Executor.submit(
                    _merge,
                    array,
                    i, i + pow_2 - 1, i + pow_2, i + 2 * pow_2 - 1,
                    end, comp).result()
                i = i + 2 * pow_2

    if _check_type(array, DynamicArray):
        array._modify(force=True)


def brick_sort(array, **kwargs):
    """
    Implements Brick Sort / Odd Even sorting algorithm

    Parameters
    ==========

    array: Array
        The array which is to be sorted.
    start: int
        The starting index of the portion
        which is to be sorted.
        Optional, by default 0
    end: int
        The ending index of the portion which
        is to be sorted.
        Optional, by default the index
        of the last position filled.
    comp: lambda/function
        The comparator which is to be used
        for sorting. If the function returns
        False then only swapping is performed.
        Optional, by default, less than or
        equal to is used for comparing two
        values.

    Examples
    ========
    >>> from pydatastructs import OneDimensionalArray, brick_sort
    >>> arr = OneDimensionalArray(int,[3, 2, 1])
    >>> brick_sort(arr)
    >>> [arr[0], arr[1], arr[2]]
    [1, 2, 3]
    >>> brick_sort(arr, comp=lambda u, v: u > v)
    >>> [arr[0], arr[1], arr[2]]
    [3, 2, 1]

    References
    ==========
    .. [1] https://www.geeksforgeeks.org/odd-even-sort-brick-sort/
    """
    start = kwargs.get('start', 0)
    end = kwargs.get('end', len(array) - 1)
    comp = kwargs.get("comp", lambda u, v: u <= v)

    is_sorted = False
    while is_sorted is False:
        is_sorted = True
        for i in range(start + 1, end, 2):
            if _comp(array[i + 1], array[i], comp):
                array[i], array[i + 1] = array[i + 1], array[i]
                is_sorted = False
        for i in range(start, end, 2):
            if _comp(array[i + 1], array[i], comp):
                array[i], array[i + 1] = array[i + 1], array[i]
                is_sorted = False

    if _check_type(array, DynamicArray):
        array._modify(force=True)


def _brick_sort_swap(array, i, j, comp, is_sorted):
    if _comp(array[j], array[i], comp):
        array[i], array[j] = array[j], array[i]
        is_sorted[0] = False


def brick_sort_parallel(array, num_threads, **kwargs):
    """
    Implements Concurrent Brick Sort / Odd Even sorting algorithm

    Parameters
    ==========

    array: Array/list
        The array which is to be sorted.
    num_threads: int
        The maximum number of threads
        to be used for sorting.
    start: int
        The starting index of the portion
        which is to be sorted.
        Optional, by default 0
    end: int
        The ending index of the portion which
        is to be sorted.
        Optional, by default the index
        of the last position filled.
    comp: lambda/function
        The comparator which is to be used
        for sorting. If the function returns
        False then only swapping is performed.
        Optional, by default, less than or
        equal to is used for comparing two
        values.

    Examples
    ========

    >>> from pydatastructs import OneDimensionalArray, brick_sort_parallel
    >>> arr = OneDimensionalArray(int,[3, 2, 1])
    >>> brick_sort_parallel(arr, num_threads=5)
    >>> [arr[0], arr[1], arr[2]]
    [1, 2, 3]
    >>> brick_sort_parallel(arr, num_threads=5, comp=lambda u, v: u > v)
    >>> [arr[0], arr[1], arr[2]]
    [3, 2, 1]

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Odd%E2%80%93even_sort
    """

    start = kwargs.get('start', 0)
    end = kwargs.get('end', len(array) - 1)
    comp = kwargs.get("comp", lambda u, v: u <= v)

    is_sorted = [False]
    with ThreadPoolExecutor(max_workers=num_threads) as Executor:
        while is_sorted[0] is False:
            is_sorted[0] = True
            for i in range(start + 1, end, 2):
                Executor.submit(_brick_sort_swap, array, i, i + 1, comp, is_sorted).result()

            for i in range(start, end, 2):
                Executor.submit(_brick_sort_swap, array, i, i + 1, comp, is_sorted).result()

    if _check_type(array, DynamicArray):
        array._modify(force=True)


def heapsort(array, **kwargs):
    """
    Implements Heapsort algorithm.

    Parameters
    ==========

    array: Array
        The array which is to be sorted.
    start: int
        The starting index of the portion
        which is to be sorted.
        Optional, by default 0
    end: int
        The ending index of the portion which
        is to be sorted.
        Optional, by default the index
        of the last position filled.

    Examples
    ========

    >>> from pydatastructs import OneDimensionalArray, heapsort
    >>> arr = OneDimensionalArray(int,[3, 2, 1])
    >>> heapsort(arr)
    >>> [arr[0], arr[1], arr[2]]
    [1, 2, 3]

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Heapsort

    Note
    ====

    This function does not support custom comparators as is the case with
    other sorting functions in this file.
    """
    from pydatastructs.trees.heaps import BinaryHeap

    start = kwargs.get('start', 0)
    end = kwargs.get('end', len(array) - 1)

    h = BinaryHeap(heap_property="min")
    for i in range(start, end + 1):
        if array[i] is not None:
            h.insert(array[i])
        array[i] = None

    i = start
    while not h.is_empty:
        array[i] = h.extract().key
        i += 1

    if _check_type(array, DynamicArray):
        array._modify(force=True)


def counting_sort(array: Array) -> Array:
    """
    Performs counting sort on the given array.

    Parameters
    ==========

    array: Array
        The array which is to be sorted.

    Returns
    =======

    output: Array
        The sorted array.

    Examples
    ========

    >>> from pydatastructs import DynamicOneDimensionalArray as DODA, counting_sort
    >>> arr = DODA(int, [5, 78, 1, 0])
    >>> out = counting_sort(arr)
    >>> str(out)
    "['0', '1', '5', '78']"
    >>> arr.delete(2)
    >>> out = counting_sort(arr)
    >>> str(out)
    "['0', '5', '78']"

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Counting_sort

    Note
    ====

    Since, counting sort is a non-comparison sorting algorithm,
    custom comparators aren't allowed.
    The ouput array doesn't contain any `None` value.
    """
    max_val, min_val = array[0], array[0]
    none_count = 0
    for i in range(len(array)):
        if array[i] is not None:
            if max_val is None or max_val < array[i]:
                max_val = array[i]
            if min_val is None or array[i] < min_val:
                min_val = array[i]
        else:
            none_count += 1
    if min_val is None or max_val is None:
        return array

    count = [0 for _ in range(max_val - min_val + 1)]
    for i in range(len(array)):
        if array[i] is not None:
            count[array[i] - min_val] += 1

    total = 0
    for i in range(max_val - min_val + 1):
        count[i], total = total, count[i] + total

    output = type(array)(array._dtype,
                         [array[i] for i in range(len(array))
                          if array[i] is not None])
    if _check_type(output, DynamicArray):
        output._modify(force=True)

    for i in range(len(array)):
        x = array[i]
        if x is not None:
            output[count[x - min_val]] = x
            count[x - min_val] += 1

    return output


def _matrix_multiply_helper(m1, m2, row, col):
    s = 0
    for i in range(len(m1)):
        s += m1[row][i] * m2[i][col]
    return s


def matrix_multiply_parallel(matrix_1, matrix_2, num_threads):
    """
    Implements concurrent Matrix multiplication

    Parameters
    ==========

    matrix_1: Any matrix representation
        Left matrix

    matrix_2: Any matrix representation
        Right matrix

    num_threads: int
        The maximum number of threads
        to be used for multiplication.

    Raises
    ======

    ValueError
        When the columns in matrix_1 are not equal to the rows in matrix_2

    Returns
    =======

    C: list
        The result of matrix multiplication.

    Examples
    ========

    >>> from pydatastructs import matrix_multiply_parallel
    >>> I = [[1, 1, 0], [0, 1, 0], [0, 0, 1]]
    >>> J = [[2, 1, 2], [1, 2, 1], [2, 2, 2]]
    >>> matrix_multiply_parallel(I, J, num_threads=5)
    [[3, 3, 3], [1, 2, 1], [2, 2, 2]]

    References
    ==========
    .. [1] https://www3.nd.edu/~zxu2/acms60212-40212/Lec-07-3.pdf
    """
    row_matrix_1, col_matrix_1 = len(matrix_1), len(matrix_1[0])
    row_matrix_2, col_matrix_2 = len(matrix_2), len(matrix_2[0])

    if col_matrix_1 != row_matrix_2:
        raise ValueError("Matrix size mismatch: %s * %s" % (
            (row_matrix_1, col_matrix_1), (row_matrix_2, col_matrix_2)))

    C = [[None for i in range(col_matrix_1)] for j in range(row_matrix_2)]

    with ThreadPoolExecutor(max_workers=num_threads) as Executor:
        for i in range(row_matrix_1):
            for j in range(col_matrix_2):
                C[i][j] = Executor.submit(_matrix_multiply_helper,
                                          matrix_1,
                                          matrix_2,
                                          i, j).result()

    return C


def _bucket_sort_helper(bucket: Array) -> Array:
    for i in range(1, len(bucket)):
        key = bucket[i]
        j = i - 1
        while j >= 0 and bucket[j] > key:
            bucket[j + 1] = bucket[j]
            j -= 1
        bucket[j + 1] = key
    return bucket


def bucket_sort(array: Array, **kwargs) -> Array:
    """
    Performs bucket sort on the given array.

    Parameters
    ==========

    array: Array
        The array which is to be sorted.
    start: int
        The starting index of the portion
        which is to be sorted.
        Optional, by default 0
    end: int
        The ending index of the portion which
        is to be sorted.
        Optional, by default the index
        of the last position filled.

    Returns
    =======

    output: Array
        The sorted array.

    Examples
    ========

    >>> from pydatastructs import DynamicOneDimensionalArray as DODA, bucket_sort
    >>> arr = DODA(int, [5, 78, 1, 0])
    >>> out = bucket_sort(arr)
    >>> str(out)
    "['0', '1', '5', '78']"
    >>> arr.delete(2)
    >>> out = bucket_sort(arr)
    >>> str(out)
    "['0', '1', '78']"

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Bucket_sort

    Note
    ====

    This function does not support custom comparators as is the case with
    other sorting functions in this file.
    """
    start = kwargs.get('start', 0)
    end = kwargs.get('end', len(array) - 1)

    # Find maximum value in the list and use length of the list to determine which value in the list goes into which
    # - bucket
    max_value = None
    for i in range(start, end + 1):
        if array[i] is not None:
            max_value = array[i]

    count = 0
    for i in range(start, end + 1):
        if array[i] is not None:
            count += 1
            if array[i] > max_value:
                max_value = array[i]

    number_of_null_values = end - start + 1 - count
    size = max_value // count

    # Create n empty buckets where n is equal to the length of the input list
    buckets_list = [[] for _ in range(count)]

    # Put list elements into different buckets based on the size
    for i in range(start, end + 1):
        if array[i] is not None:
            j = array[i] // size
            if j is not count:
                buckets_list[j].append(array[i])
            else:
                buckets_list[count - 1].append(array[i])

    # Sort elements within the buckets using Insertion Sort
    for z in range(count):
        _bucket_sort_helper(buckets_list[z])

    # Concatenate buckets with sorted elements into a single array
    sorted_list = []
    for x in range(count):
        sorted_list.extend(buckets_list[x])
    for i in range(end, end - number_of_null_values, -1):
        array[i] = None
    for i in range(start, end - number_of_null_values + 1):
        array[i] = sorted_list[i - start]
    if _check_type(array, DynamicArray):
        array._modify(force=True)
    return array


def cocktail_shaker_sort(array: Array, **kwargs) -> Array:
    """
    Performs cocktail sort on the given array.

    Parameters
    ==========

    array: Array
        The array which is to be sorted.
    start: int
        The starting index of the portion
        which is to be sorted.
        Optional, by default 0
    end: int
        The ending index of the portion which
        is to be sorted.
        Optional, by default the index
        of the last position filled.
    comp: lambda/function
        The comparator which is to be used
        for sorting. If the function returns
        False then only swapping is performed.
        Optional, by default, less than or
        equal to is used for comparing two
        values.

    Returns
    =======

    output: Array
        The sorted array.

    Examples
    ========

    >>> from pydatastructs import OneDimensionalArray as ODA, cocktail_shaker_sort
    >>> arr = ODA(int, [5, 78, 1, 0])
    >>> out = cocktail_shaker_sort(arr)
    >>> str(out)
    '[0, 1, 5, 78]'
    >>> arr = ODA(int, [21, 37, 5])
    >>> out = cocktail_shaker_sort(arr)
    >>> str(out)
    '[5, 21, 37]'

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Cocktail_shaker_sort
    """

    def swap(i, j):
        array[i], array[j] = array[j], array[i]

    lower = kwargs.get('start', 0)
    upper = kwargs.get('end', len(array) - 1)
    comp = kwargs.get("comp", lambda u, v: u <= v)

    swapping = False
    while (not swapping and upper - lower >= 1):

        swapping = True
        for j in range(lower, upper):
            if _comp(array[j], array[j + 1], comp) is False:
                swap(j + 1, j)
                swapping = False

        upper = upper - 1
        for j in range(upper, lower, -1):
            if _comp(array[j - 1], array[j], comp) is False:
                swap(j, j - 1)
                swapping = False
        lower = lower + 1

    if _check_type(array, DynamicArray):
        array._modify(force=True)

    return array


def quick_sort(array: Array, **kwargs) -> Array:
    """
    Performs quick sort on the given array.

    Parameters
    ==========

    array: Array
        The array which is to be sorted.
    start: int
        The starting index of the portion
        which is to be sorted.
        Optional, by default 0
    end: int
        The ending index of the portion which
        is to be sorted.
        Optional, by default the index
        of the last position filled.
    comp: lambda/function
        The comparator which is to be used
        for sorting. If the function returns
        False then only swapping is performed.
        Optional, by default, less than or
        equal to is used for comparing two
        values.
    pick_pivot_element: lambda/function
        The function implementing the pivot picking
        logic for quick sort. Should accept, `low`,
        `high`, and `array` in this order, where `low`
        represents the left end of the current partition,
        `high` represents the right end, and `array` is
        the original input array to `quick_sort` function.
        Optional, by default, picks the element at `high`
        index of the current partition as pivot.

    Returns
    =======

    output: Array
        The sorted array.

    Examples
    ========

    >>> from pydatastructs import OneDimensionalArray as ODA, quick_sort
    >>> arr = ODA(int, [5, 78, 1, 0])
    >>> out = quick_sort(arr)
    >>> str(out)
    '[0, 1, 5, 78]'
    >>> arr = ODA(int, [21, 37, 5])
    >>> out = quick_sort(arr)
    >>> str(out)
    '[5, 21, 37]'

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Quicksort
    """
    from pydatastructs import Stack
    comp = kwargs.get("comp", lambda u, v: u <= v)
    pick_pivot_element = kwargs.get("pick_pivot_element",
                                    lambda low, high, array: array[high])

    def partition(low, high, pick_pivot_element):
        i = (low - 1)
        x = pick_pivot_element(low, high, array)
        for j in range(low, high):
            if _comp(array[j], x, comp) is True:
                i = i + 1
                array[i], array[j] = array[j], array[i]
        array[i + 1], array[high] = array[high], array[i + 1]
        return (i + 1)

    lower = kwargs.get('start', 0)
    upper = kwargs.get('end', len(array) - 1)
    stack = Stack()

    stack.push(lower)
    stack.push(upper)

    while stack.is_empty is False:
        high = stack.pop()
        low = stack.pop()
        p = partition(low, high, pick_pivot_element)
        if p - 1 > low:
            stack.push(low)
            stack.push(p - 1)
        if p + 1 < high:
            stack.push(p + 1)
            stack.push(high)

    if _check_type(array, DynamicArray):
        array._modify(force=True)

    return array


def longest_common_subsequence(seq1: OneDimensionalArray, seq2: OneDimensionalArray) -> OneDimensionalArray:
    """
    Finds the longest common subsequence between the
    two given sequences.

    Parameters
    ========

    seq1: OneDimensionalArray
        The first sequence.
    seq2: OneDimensionalArray
        The second sequence.

    Returns
    =======

    output: OneDimensionalArray
        The longest common subsequence.

    Examples
    ========

    >>> from pydatastructs import longest_common_subsequence as LCS, OneDimensionalArray as ODA
    >>> arr1 = ODA(str, ['A', 'B', 'C', 'D', 'E'])
    >>> arr2 = ODA(str, ['A', 'B', 'C', 'G' ,'D', 'E', 'F'])
    >>> lcs = LCS(arr1, arr2)
    >>> str(lcs)
    "['A', 'B', 'C', 'D', 'E']"
    >>> arr1 = ODA(str, ['A', 'P', 'P'])
    >>> arr2 = ODA(str, ['A', 'p', 'P', 'S', 'P'])
    >>> lcs = LCS(arr1, arr2)
    >>> str(lcs)
    "['A', 'P', 'P']"

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Longest_common_subsequence_problem

    Note
    ====

    The data types of elements across both the sequences
    should be same and should be comparable.
    """
    row = len(seq1)
    col = len(seq2)
    check_mat = {0: [(0, []) for _ in range(col + 1)]}

    for i in range(1, row + 1):
        check_mat[i] = [(0, []) for _ in range(col + 1)]
        for j in range(1, col + 1):
            if seq1[i - 1] == seq2[j - 1]:
                temp = check_mat[i - 1][j - 1][1][:]
                temp.append(seq1[i - 1])
                check_mat[i][j] = (check_mat[i - 1][j - 1][0] + 1, temp)
            else:
                if check_mat[i - 1][j][0] > check_mat[i][j - 1][0]:
                    check_mat[i][j] = check_mat[i - 1][j]
                else:
                    check_mat[i][j] = check_mat[i][j - 1]

    return OneDimensionalArray(seq1._dtype, check_mat[row][col][-1])
