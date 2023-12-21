from pydatastructs.linear_data_structures.arrays import (
    OneDimensionalArray, DynamicArray, DynamicOneDimensionalArray, Array)
from pydatastructs.linear_data_structures._backend.cpp import _algorithms, _arrays
from pydatastructs.utils.misc_util import (
    _check_type, _comp, Backend,
    raise_if_backend_is_not_python)
from concurrent.futures import ThreadPoolExecutor
from math import log, floor, sqrt

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
    'longest_common_subsequence',
    'is_ordered',
    'upper_bound',
    'lower_bound',
    'longest_increasing_subsequence',
    'next_permutation',
    'prev_permutation',
    'bubble_sort',
    'linear_search',
    'binary_search',
    'jump_search',
    'selection_sort',
    'insertion_sort',
    'intro_sort'
]

def _merge(array, sl, el, sr, er, end, comp):
    l, r = [],  []
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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

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
    raise_if_backend_is_not_python(
            merge_sort_parallel, kwargs.get('backend', Backend.PYTHON))
    start = kwargs.get('start', 0)
    end = kwargs.get('end', len(array) - 1)
    comp = kwargs.get("comp", lambda u, v: u <= v)
    for size in range(floor(log(end - start + 1, 2)) + 1):
        pow_2 = 2**size
        with ThreadPoolExecutor(max_workers=num_threads) as Executor:
            i = start
            while i <= end:
                Executor.submit(
                    _merge,
                    array,
                    i, i + pow_2 - 1,
                    i + pow_2, i + 2*pow_2 - 1,
                    end, comp).result()
                i = i + 2*pow_2

    if _check_type(array, (DynamicArray, _arrays.DynamicOneDimensionalArray)):
        array._modify(True)

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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

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
    raise_if_backend_is_not_python(
        brick_sort, kwargs.get('backend', Backend.PYTHON))
    start = kwargs.get('start', 0)
    end = kwargs.get('end', len(array) - 1)
    comp = kwargs.get("comp", lambda u, v: u <= v)

    is_sorted = False
    while is_sorted is False:
        is_sorted = True
        for i in range(start+1, end, 2):
            if _comp(array[i+1], array[i], comp):
                array[i], array[i+1] = array[i+1], array[i]
                is_sorted = False
        for i in range(start, end, 2):
            if _comp(array[i+1], array[i], comp):
                array[i], array[i+1] = array[i+1], array[i]
                is_sorted = False

    if _check_type(array, (DynamicArray, _arrays.DynamicOneDimensionalArray)):
        array._modify(True)

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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

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
    raise_if_backend_is_not_python(
        brick_sort_parallel, kwargs.get('backend', Backend.PYTHON))
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

    if _check_type(array, (DynamicArray, _arrays.DynamicOneDimensionalArray)):
        array._modify(True)

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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

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
    raise_if_backend_is_not_python(
        heapsort, kwargs.get('backend', Backend.PYTHON))
    from pydatastructs.trees.heaps import BinaryHeap

    start = kwargs.get('start', 0)
    end = kwargs.get('end', len(array) - 1)

    h = BinaryHeap(heap_property="min")
    for i in range(start, end+1):
        if array[i] is not None:
            h.insert(array[i])
        array[i] = None

    i = start
    while not h.is_empty:
        array[i] = h.extract().key
        i += 1

    if _check_type(array, (DynamicArray, _arrays.DynamicOneDimensionalArray)):
        array._modify(True)

def counting_sort(array: Array, **kwargs) -> Array:
    """
    Performs counting sort on the given array.

    Parameters
    ==========

    array: Array
        The array which is to be sorted.
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

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
    raise_if_backend_is_not_python(
        counting_sort, kwargs.get('backend', Backend.PYTHON))
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
        count[i], total = total, count[i] +  total

    output = type(array)(array._dtype,
                        [array[i] for i in range(len(array))
                         if array[i] is not None])
    if _check_type(output, DynamicArray):
        output._modify(force=True)

    for i in range(len(array)):
        x = array[i]
        if x is not None:
            output[count[x-min_val]] = x
            count[x-min_val] += 1

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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

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
        raise ValueError("Matrix size mismatch: %s * %s"%(
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
            bucket[j+1] = bucket[j]
            j -= 1
        bucket[j+1] = key
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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

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
    raise_if_backend_is_not_python(
        bucket_sort, kwargs.get('backend', Backend.PYTHON))
    start = kwargs.get('start', 0)
    end = kwargs.get('end', len(array) - 1)

    #Find maximum value in the list and use length of the list to determine which value in the list goes into which bucket
    max_value = None
    for i in range(start, end+1):
        if array[i] is not None:
            max_value = array[i]

    count = 0
    for i in range(start, end+1):
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
                buckets_list[count-1].append(array[i])

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
        array[i] = sorted_list[i-start]
    if _check_type(array, (DynamicArray, _arrays.DynamicOneDimensionalArray)):
        array._modify(True)
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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

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
    raise_if_backend_is_not_python(
        cocktail_shaker_sort, kwargs.get('backend', Backend.PYTHON))
    def swap(i, j):
        array[i], array[j] = array[j], array[i]

    lower = kwargs.get('start', 0)
    upper = kwargs.get('end', len(array) - 1)
    comp = kwargs.get("comp", lambda u, v: u <= v)

    swapping = False
    while (not swapping and upper - lower >= 1):

        swapping = True
        for j in range(lower, upper):
            if _comp(array[j], array[j+1], comp) is False:
                swap(j + 1, j)
                swapping = False

        upper = upper - 1
        for j in range(upper, lower, -1):
            if _comp(array[j-1], array[j], comp) is False:
                swap(j, j - 1)
                swapping = False
        lower = lower + 1

    if _check_type(array, (DynamicArray, _arrays.DynamicOneDimensionalArray)):
        array._modify(True)

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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

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
    backend = kwargs.pop("backend", Backend.PYTHON)
    if backend == Backend.CPP:
        return _algorithms.quick_sort(array, **kwargs)
    from pydatastructs import Stack
    comp = kwargs.get("comp", lambda u, v: u <= v)
    pick_pivot_element = kwargs.get("pick_pivot_element",
                                    lambda low, high, array: array[high])

    def partition(low, high, pick_pivot_element):
        i = (low - 1)
        x = pick_pivot_element(low, high, array)
        for j in range(low , high):
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

    if _check_type(array, (DynamicArray, _arrays.DynamicOneDimensionalArray)):
        array._modify(True)

    return array

def longest_common_subsequence(seq1: OneDimensionalArray, seq2: OneDimensionalArray,
                               **kwargs) -> OneDimensionalArray:
    """
    Finds the longest common subsequence between the
    two given sequences.

    Parameters
    ========

    seq1: OneDimensionalArray
        The first sequence.
    seq2: OneDimensionalArray
        The second sequence.
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

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
    raise_if_backend_is_not_python(
        longest_common_subsequence, kwargs.get('backend', Backend.PYTHON))
    row = len(seq1)
    col = len(seq2)
    check_mat = {0: [(0, []) for _ in range(col + 1)]}

    for i in range(1, row + 1):
        check_mat[i] = [(0, []) for _ in range(col + 1)]
        for j in range(1, col + 1):
            if seq1[i-1] == seq2[j-1]:
                temp = check_mat[i-1][j-1][1][:]
                temp.append(seq1[i-1])
                check_mat[i][j] = (check_mat[i-1][j-1][0] + 1, temp)
            else:
                if check_mat[i-1][j][0] > check_mat[i][j-1][0]:
                    check_mat[i][j] = check_mat[i-1][j]
                else:
                    check_mat[i][j] = check_mat[i][j-1]

    return OneDimensionalArray(seq1._dtype, check_mat[row][col][-1])

def is_ordered(array, **kwargs):
    """
    Checks whether the given array is ordered or not.

    Parameters
    ==========

    array: OneDimensionalArray
        The array which is to be checked for having
        specified ordering among its elements.
    start: int
        The starting index of the portion of the array
        under consideration.
        Optional, by default 0
    end: int
        The ending index of the portion of the array
        under consideration.
        Optional, by default the index
        of the last position filled.
    comp: lambda/function
        The comparator which is to be used
        for specifying the desired ordering.
        Optional, by default, less than or
        equal to is used for comparing two
        values.
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Returns
    =======

    True if the specified ordering is present
    from start to end (inclusive) otherwise False.

    Examples
    ========

    >>> from pydatastructs import OneDimensionalArray, is_ordered
    >>> arr = OneDimensionalArray(int, [1, 2, 3, 4])
    >>> is_ordered(arr)
    True
    >>> arr1 = OneDimensionalArray(int, [1, 2, 3])
    >>> is_ordered(arr1, start=0, end=1, comp=lambda u, v: u > v)
    False
    """
    backend = kwargs.pop("backend", Backend.PYTHON)
    if backend == Backend.CPP:
        return _algorithms.is_ordered(array, **kwargs)
    lower = kwargs.get('start', 0)
    upper = kwargs.get('end', len(array) - 1)
    comp = kwargs.get("comp", lambda u, v: u <= v)

    for i in range(lower + 1, upper + 1):
        if array[i] is None or array[i - 1] is None:
            continue
        if comp(array[i], array[i - 1]):
            return False
    return True

def upper_bound(array, value, **kwargs):
    """
    Finds the index of the first occurence of an element greater than the given
    value according to specified order, in the given OneDimensionalArray using a variation of binary search method.

    Parameters
    ==========

    array: OneDimensionalArray
        The array in which the upper bound has to be found.
    start: int
        The staring index of the portion of the array in which the upper bound
        of a given value has to be looked for.
        Optional, by default 0
    end: int, optional
        The ending index of the portion of the array in which the upper bound
        of a given value has to be looked for.
        Optional, by default the index
        of the last position filled.
    comp: lambda/function
        The comparator which is to be used
        for specifying the desired ordering.
        Optional, by default, less than or
        equal to is used for comparing two
        values.
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Returns
    =======

    index: int
        Index of the upper bound of the given value in the given OneDimensionalArray.

    Examples
    ========

    >>> from pydatastructs import upper_bound, OneDimensionalArray as ODA
    >>> arr1 = ODA(int, [4, 5, 5, 6, 7])
    >>> ub = upper_bound(arr1, 5, start=0, end=4)
    >>> ub
    3
    >>> arr2 = ODA(int, [7, 6, 5, 5, 4])
    >>> ub = upper_bound(arr2, 5, comp=lambda x, y: x > y)
    >>> ub
    4

    Note
    ====

    DynamicOneDimensionalArray objects may not work as expected.
    """
    raise_if_backend_is_not_python(
        upper_bound, kwargs.get('backend', Backend.PYTHON))
    start = kwargs.get('start', 0)
    end = kwargs.get('end', len(array))
    comp = kwargs.get('comp', lambda x, y: x < y)
    index = end
    inclusive_end = end - 1
    if comp(value, array[start]):
        index = start
    while start <= inclusive_end:
        mid = (start + inclusive_end)//2
        if not comp(value, array[mid]):
            start = mid + 1
        else:
            index = mid
            inclusive_end = mid - 1
    return index

def lower_bound(array, value, **kwargs):
    """
    Finds the the index of the first occurence of an element which is not
    less than the given value according to specified order,
    in the given OneDimensionalArray using a variation of binary search method.

    Parameters
    ==========

    array: OneDimensionalArray
        The array in which the lower bound has to be found.
    start: int
        The staring index of the portion of the array in which the upper bound
        of a given value has to be looked for.
        Optional, by default 0
    end: int, optional
        The ending index of the portion of the array in which the upper bound
        of a given value has to be looked for.
        Optional, by default the index
        of the last position filled.
    comp: lambda/function
        The comparator which is to be used
        for specifying the desired ordering.
        Optional, by default, less than or
        equal to is used for comparing two
        values.
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Returns
    =======

    index: int
        Index of the lower bound of the given value in the given OneDimensionalArray

    Examples
    ========

    >>> from pydatastructs import lower_bound, OneDimensionalArray as ODA
    >>> arr1 = ODA(int, [4, 5, 5, 6, 7])
    >>> lb = lower_bound(arr1, 5, end=4, comp=lambda x, y : x < y)
    >>> lb
    1
    >>> arr = ODA(int, [7, 6, 5, 5, 4])
    >>> lb = lower_bound(arr, 5, start=0, comp=lambda x, y : x > y)
    >>> lb
    2

    Note
    ====

    DynamicOneDimensionalArray objects may not work as expected.
    """
    raise_if_backend_is_not_python(
        lower_bound, kwargs.get('backend', Backend.PYTHON))
    start = kwargs.get('start', 0)
    end = kwargs.get('end', len(array))
    comp = kwargs.get('comp', lambda x, y: x < y)
    index = end
    inclusive_end = end - 1
    if not comp(array[start], value):
        index = start
    while start <= inclusive_end:
        mid = (start + inclusive_end)//2
        if comp(array[mid], value):
            start = mid + 1
        else:
            index = mid
            inclusive_end = mid - 1
    return index

def longest_increasing_subsequence(array, **kwargs):
    """
    Returns the longest increasing subsequence (as a OneDimensionalArray) that
    can be obtained from a given OneDimensionalArray. A subsequence
    of an array is an ordered subset of the array's elements having the same
    sequential ordering as the original array. Here, an increasing
    sequence stands for a strictly increasing sequence of numbers.

    Parameters
    ==========

    array: OneDimensionalArray
        The given array in the form of a OneDimensionalArray
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Returns
    =======

    output: OneDimensionalArray
        Returns the longest increasing subsequence that can be obtained
        from the given array

    Examples
    ========

    >>> from pydatastructs import lower_bound, OneDimensionalArray as ODA
    >>> from pydatastructs import longest_increasing_subsequence as LIS
    >>> array = ODA(int, [2, 5, 3, 7, 11, 8, 10, 13, 6])
    >>> longest_inc_subsequence = LIS(array)
    >>> str(longest_inc_subsequence)
    '[2, 3, 7, 8, 10, 13]'
    >>> array2 = ODA(int, [3, 4, -1, 5, 8, 2, 2 ,2, 3, 12, 7, 9, 10])
    >>> longest_inc_subsequence = LIS(array2)
    >>> str(longest_inc_subsequence)
    '[-1, 2, 3, 7, 9, 10]'
    """
    raise_if_backend_is_not_python(
        longest_increasing_subsequence,
        kwargs.get('backend', Backend.PYTHON))
    n = len(array)
    dp = OneDimensionalArray(int, n)
    dp.fill(0)
    parent = OneDimensionalArray(int, n)
    parent.fill(-1)
    length = 0
    for i in range(1, n):
        if array[i] <= array[dp[0]]:
            dp[0] = i
        elif array[dp[length]] < array[i]:
            length += 1
            dp[length] = i
            parent[i] = dp[length - 1]
        else:
            curr_array = [array[dp[i]] for i in range(length)]
            ceil = lower_bound(curr_array, array[i])
            dp[ceil] = i
            parent[i] = dp[ceil - 1]
    ans = DynamicOneDimensionalArray(int, 0)
    last_index = dp[length]
    while last_index != -1:
        ans.append(array[last_index])
        last_index = parent[last_index]
    n = ans._last_pos_filled + 1
    ans_ODA = OneDimensionalArray(int, n)
    for i in range(n):
        ans_ODA[n-1-i] = ans[i]
    return ans_ODA

def _permutation_util(array, start, end, comp, perm_comp):
    size = end - start + 1
    permute = OneDimensionalArray(int, size)
    for i, j in zip(range(start, end + 1), range(size)):
        permute[j] = array[i]
    i = size - 1
    while i > 0 and perm_comp(permute[i - 1], permute[i], comp):
        i -= 1
    if i > 0:
        left, right = i, size - 1
        while left <= right:
            mid = left + (right - left) // 2
            if not perm_comp(permute[i - 1], permute[mid], comp):
                left = mid + 1
            else:
                right = mid - 1
        permute[i - 1], permute[left - 1] = \
            permute[left - 1], permute[i - 1]
    left, right = i, size - 1
    while left < right:
        permute[left], permute[right] = permute[right], permute[left]
        left += 1
        right -= 1
    result =  True if i > 0 else False
    return result, permute

def next_permutation(array, **kwargs):
    """
    If the function can determine the next higher permutation, it
    returns `True` and the permutation in a new array.
    If that is not possible, because it is already at the largest possible
    permutation, it returns the elements according to the first permutation
    and returns `False` and the permutation in a new array.

    Parameters
    ==========

    array: OneDimensionalArray
        The array which is to be used for finding next permutation.
    start: int
        The staring index of the considered portion of the array.
        Optional, by default 0
    end: int, optional
        The ending index of the considered portion of the array.
        Optional, by default the index of the last position filled.
    comp: lambda/function
        The comparator which is to be used for specifying the
        desired lexicographical ordering.
        Optional, by default, less than is
        used for comparing two values.
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.


    Returns
    =======

    output: bool, OneDimensionalArray
        First element is `True` if the function can rearrange
        the given portion of the input array as a lexicographically
        greater permutation, otherwise returns `False`.
        Second element is an array having the next permutation.


    Examples
    ========

    >>> from pydatastructs import next_permutation, OneDimensionalArray as ODA
    >>> array = ODA(int, [1, 2, 3, 4])
    >>> is_greater, next_permute = next_permutation(array)
    >>> is_greater, str(next_permute)
    (True, '[1, 2, 4, 3]')
    >>> array = ODA(int, [3, 2, 1])
    >>> is_greater, next_permute = next_permutation(array)
    >>> is_greater, str(next_permute)
    (False, '[1, 2, 3]')

    References
    ==========

    .. [1] http://www.cplusplus.com/reference/algorithm/next_permutation/
    """
    raise_if_backend_is_not_python(
        next_permutation, kwargs.get('backend', Backend.PYTHON))
    start = kwargs.get('start', 0)
    end = kwargs.get('end', len(array) - 1)
    comp = kwargs.get('comp', lambda x, y: x < y)

    def _next_permutation_comp(x, y, _comp):
        if _comp(x, y):
            return False
        else:
            return True

    return _permutation_util(array, start, end, comp,
                             _next_permutation_comp)

def prev_permutation(array, **kwargs):
    """
    If the function can determine the next lower permutation, it
    returns `True` and the permutation in a new array.
    If that is not possible, because it is already at the lowest possible
    permutation, it returns the elements according to the last permutation
    and returns `False` and the permutation in a new array.

    Parameters
    ==========

    array: OneDimensionalArray
        The array which is to be used for finding next permutation.
    start: int
        The staring index of the considered portion of the array.
        Optional, by default 0
    end: int, optional
        The ending index of the considered portion of the array.
        Optional, by default the index of the last position filled.
    comp: lambda/function
        The comparator which is to be used for specifying the
        desired lexicographical ordering.
        Optional, by default, less than is
        used for comparing two values.
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.


    Returns
    =======

    output: bool, OneDimensionalArray
        First element is `True` if the function can rearrange
        the given portion of the input array as a lexicographically
        smaller permutation, otherwise returns `False`.
        Second element is an array having the previous permutation.


    Examples
    ========

    >>> from pydatastructs import prev_permutation, OneDimensionalArray as ODA
    >>> array = ODA(int, [1, 2, 4, 3])
    >>> is_lower, prev_permute = prev_permutation(array)
    >>> is_lower, str(prev_permute)
    (True, '[1, 2, 3, 4]')
    >>> array = ODA(int, [1, 2, 3, 4])
    >>> is_lower, prev_permute = prev_permutation(array)
    >>> is_lower, str(prev_permute)
    (False, '[4, 3, 2, 1]')

    References
    ==========

    .. [1] http://www.cplusplus.com/reference/algorithm/prev_permutation/
    """
    raise_if_backend_is_not_python(
        prev_permutation, kwargs.get('backend', Backend.PYTHON))
    start = kwargs.get('start', 0)
    end = kwargs.get('end', len(array) - 1)
    comp = kwargs.get('comp', lambda x, y: x < y)

    def _prev_permutation_comp(x, y, _comp):
        if _comp(x, y):
            return True
        else:
            return False

    return _permutation_util(array, start, end, comp,
                             _prev_permutation_comp)

def bubble_sort(array, **kwargs):
    """
    Implements bubble sort algorithm.

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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Returns
    =======

    output: Array
        The sorted array.

    Examples
    ========

    >>> from pydatastructs import OneDimensionalArray, bubble_sort
    >>> arr = OneDimensionalArray(int,[3, 2, 1])
    >>> out = bubble_sort(arr)
    >>> str(out)
    '[1, 2, 3]'
    >>> out = bubble_sort(arr, comp=lambda u, v: u > v)
    >>> str(out)
    '[3, 2, 1]'

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Bubble_sort
    """
    backend = kwargs.pop("backend", Backend.PYTHON)
    if backend == Backend.CPP:
        return _algorithms.bubble_sort(array, **kwargs)
    start = kwargs.get('start', 0)
    end = kwargs.get('end', len(array) - 1)
    comp = kwargs.get("comp", lambda u, v: u <= v)
    arr_len = len(array)
    for i in range(arr_len - 1):
        for j in range(start , end):
            if not _comp(array[j], array[j + 1], comp):
                array[j], array[j + 1] = array[j + 1], array[j]

    if _check_type(array, (DynamicArray, _arrays.DynamicOneDimensionalArray)):
        array._modify(True)

    return array

def selection_sort(array, **kwargs):
    """
    Implements selection sort algorithm.

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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Returns
    =======

    output: Array
        The sorted array.

    Examples
    ========

    >>> from pydatastructs import OneDimensionalArray, selection_sort
    >>> arr = OneDimensionalArray(int,[3, 2, 1])
    >>> out = selection_sort(arr)
    >>> str(out)
    '[1, 2, 3]'
    >>> out = selection_sort(arr, comp=lambda u, v: u > v)
    >>> str(out)
    '[3, 2, 1]'

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Selection_sort
    """
    backend = kwargs.pop("backend", Backend.PYTHON)
    if backend == Backend.CPP:
        return _algorithms.bubble_sort(array, **kwargs)
    start = kwargs.get('start', 0)
    end = kwargs.get('end', len(array) - 1)
    comp = kwargs.get('comp', lambda u, v: u <= v)

    for i in range(start, end + 1):
        jMin = i
        for j in range(i + 1, end + 1):
            if not _comp(array[jMin], array[j], comp):
                jMin = j
        if jMin != i:
            array[i], array[jMin] = array[jMin], array[i]

    if _check_type(array, (DynamicArray, _arrays.DynamicOneDimensionalArray)):
        array._modify(True)

    return array

def insertion_sort(array, **kwargs):
    """
    Implements insertion sort algorithm.

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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Returns
    =======

    output: Array
        The sorted array.

    Examples
    ========

    >>> from pydatastructs import OneDimensionalArray, insertion_sort
    >>> arr = OneDimensionalArray(int,[3, 2, 1])
    >>> out = insertion_sort(arr)
    >>> str(out)
    '[1, 2, 3]'
    >>> out = insertion_sort(arr, comp=lambda u, v: u > v)
    >>> str(out)
    '[3, 2, 1]'

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Insertion_sort
    """
    backend = kwargs.pop("backend", Backend.PYTHON)
    if backend == Backend.CPP:
        return _algorithms.insertion_sort(array, **kwargs)
    start = kwargs.get('start', 0)
    end = kwargs.get('end', len(array) - 1)
    comp = kwargs.get('comp', lambda u, v: u <= v)

    for i in range(start + 1, end + 1):
        temp = array[i]
        j = i
        while j > start and not _comp(array[j - 1], temp, comp):
            array[j] = array[j - 1]
            j -= 1
        array[j] = temp

    if _check_type(array, (DynamicArray, _arrays.DynamicOneDimensionalArray)):
        array._modify(True)

    return array

def linear_search(array, value, **kwargs):
    """
    Implements linear search algorithm.

    Parameters
    ==========

    array: OneDimensionalArray
        The array which is to be searched.
    value:
        The value which is to be searched
        inside the array.
    start: int
        The starting index of the portion
        which is to be searched.
        Optional, by default 0
    end: int
        The ending index of the portion which
        is to be searched.
        Optional, by default the index
        of the last position filled.
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Returns
    =======

    output: int
        The index of value if found.
        If not found, returns None.

    Examples
    ========

    >>> from pydatastructs import OneDimensionalArray, linear_search
    >>> arr = OneDimensionalArray(int,[3, 2, 1])
    >>> linear_search(arr, 2)
    1

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Linear_search
    """
    backend = kwargs.pop("backend", Backend.PYTHON)
    if backend == Backend.CPP:
        return _algorithms.linear_search(array, value, **kwargs)
    start = kwargs.get('start', 0)
    end = kwargs.get('end', len(array) - 1)

    for i in range(start, end + 1):
        if array[i] == value:
            return i

    return None

def binary_search(array, value, **kwargs):
    """
    Implements binary search algorithm.

    Parameters
    ==========

    array: OneDimensionalArray
        The array which is to be searched.
    value:
        The value which is to be searched
        inside the array.
    start: int
        The starting index of the portion
        which is to be searched.
        Optional, by default 0
    end: int
        The ending index of the portion which
        is to be searched.
        Optional, by default the index
        of the last position filled.
    comp: lambda/function
        The comparator which is to be used
        for performing comparisons.
        Optional, by default, less than or
        equal to is used for comparing two
        values.
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Returns
    =======

    output: int
        The index of elem if found.
        If not found, returns None.

    Examples
    ========

    >>> from pydatastructs import OneDimensionalArray, binary_search
    >>> arr = OneDimensionalArray(int,[1, 2, 3, 5, 10, 12])
    >>> binary_search(arr, 5)
    3

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Binary_search_algorithm

    Note
    ====

    This algorithm assumes that the portion of the array
    to be searched is already sorted.
    """
    backend = kwargs.pop("backend", Backend.PYTHON)
    if backend == Backend.CPP:
        return _algorithms.binary_search(array, value, **kwargs)
    start = kwargs.get('start', 0)
    end = kwargs.get('end', len(array) - 1)
    comp = kwargs.get("comp", lambda u, v: u <= v)

    left = start
    right = end
    while left <= right:
        middle = left//2 + right//2 + left % 2 * right % 2
        if array[middle] == value:
                return middle
        if comp(array[middle], value):
            left = middle + 1
        else:
            right = middle - 1

    return None

def jump_search(array, value, **kwargs):
    """
    Implements jump search algorithm.

    Parameters
    ==========

    array: OneDimensionalArray
        The array which is to be searched.
    value:
        The value which is to be searched
        inside the array.
    start: int
        The starting index of the portion
        which is to be searched.
        Optional, by default 0
    end: int
        The ending index of the portion which
        is to be searched.
        Optional, by default the index
        of the last position filled.
    comp: lambda/function
        The comparator which is to be used
        for performing comparisons.
        Optional, by default, less than or
        equal to is used for comparing two
        values.
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Returns
    =======

    output: int
        The index of elem if found.
        If not found, returns None.

    Examples
    ========

    >>> from pydatastructs import OneDimensionalArray, jump_search
    >>> arr = OneDimensionalArray(int,[1, 2, 3, 5, 10, 12])
    >>> linear_search(arr, 5)
    3

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Jump_search

    Note
    ====

    This algorithm assumes that the portion of the array
    to be searched is already sorted.
    """
    backend = kwargs.pop("backend", Backend.PYTHON)
    if backend == Backend.CPP:
        return _algorithms.jump_search(array, value, **kwargs)
    start = kwargs.get('start', 0)
    end = kwargs.get('end', len(array) - 1)
    comp = kwargs.get("comp", lambda u, v: u < v)

    step = int(sqrt(end - start + 1))
    current_position = step
    prev = start
    while comp(array[min(current_position, end)], value):
        prev = current_position
        current_position += step
        if prev > end:
            return None
    while prev <= min(current_position, end):
        if array[prev] == value:
            return prev
        prev += 1

    return None

def intro_sort(array, **kwargs) -> Array:
    """
    Performs intro sort on the given array.

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
    maxdepth: Enables the user to define the maximum
        recursion depth, takes value 2*log(length(A))
        by default (ref: Wikipedia[1]).
    ins_threshold: Threshold under which insertion
        sort has to be performed, default value is
        16 (ref: Wikipedia[1]).
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Returns
    =======

    output: Array
        The sorted array.

    Examples
    ========

    >>> from pydatastructs import OneDimensionalArray as ODA, intro_sort
    >>> arr = ODA(int, [5, 78, 1, 0])
    >>> out = intro_sort(arr)
    >>> str(out)
    '[0, 1, 5, 78]'
    >>> arr = ODA(int, [21, 37, 5])
    >>> out = intro_sort(arr)
    >>> str(out)
    '[5, 21, 37]'

    Note
    ====

    This function does not support custom comparators as
    is the case with other sorting functions in this file.
    This is because of heapsort's limitation.

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Introsort
    """
    raise_if_backend_is_not_python(
        intro_sort, kwargs.get('backend', Backend.PYTHON))

    # Always sorts in increasing order, this is because of
    # heapsort's limitation
    comp = lambda u, v: u <= v
    lower = kwargs.get('start', 0)
    upper = kwargs.get('end', len(array) - 1)
    n = upper - lower + 1
    if n <= 0:
        maxdepth = 0
    else:
        maxdepth = kwargs.get("maxdepth", int(2 * (log(n)/log(2))))

    ins_threshold = kwargs.get("ins_threshold", 16)

    def partition(array, lower, upper):
        pivot = array[lower]
        left = lower + 1
        right = upper
        done = False
        while not done:
            while left <= right and _comp(array[left], pivot, comp):
                left += 1
            while _comp(pivot, array[right], comp) and right >= left:
                right -= 1
            if right < left:
                done = True
            else:
                array[left], array[right] = array[right], array[left]
                left+=1
                right-=1

        array[lower], array[right] = array[right], array[lower]
        return right

    if n < ins_threshold:
        return insertion_sort(array, start=lower, end=upper)
    elif maxdepth == 0:
        heapsort(array, start=lower, end=upper)
        return array
    else:
        p = partition(array, lower, upper)

        intro_sort(array, start=lower, end=p-1, maxdepth=maxdepth-1, ins_threshold=ins_threshold)
        intro_sort(array, start=p+1, end=upper,  maxdepth=maxdepth-1, ins_threshold=ins_threshold)

        return array
