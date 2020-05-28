from pydatastructs.linear_data_structures.arrays import (
    OneDimensionalArray, DynamicArray)
from pydatastructs.utils.misc_util import _check_type, _comp
from concurrent.futures import ThreadPoolExecutor
from math import log, floor
from typing import List

__all__ = [
    'merge_sort_parallel',
    'brick_sort',
    'brick_sort_parallel',
    'heapsort',
    'matrix_multiply_parallel',
    'optimal_grouping'
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
        for i in range(start+1, end, 2):
            if _comp(array[i+1], array[i], comp):
                array[i], array[i+1] = array[i+1], array[i]
                is_sorted = False
        for i in range(start, end, 2):
            if _comp(array[i+1], array[i], comp):
                array[i], array[i+1] = array[i+1], array[i]
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
    for i in range(start, end+1):
        if array[i] is not None:
            h.insert(array[i])
        array[i] = None

    i = start
    while not h.is_empty:
        array[i] = h.extract().key
        i += 1

    if _check_type(array, DynamicArray):
        array._modify(force=True)

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

def _compare_opt_group(maximize, value, compareWith=None):
    """
    compares a value with another. if compareWith is None then value is compared with Infinity or -Infinity
    parameters
        [maximize] if True then the function returns true if value is greater than compareWith and vice versa
    """
    if compareWith is None:
        if maximize:
            compareWith = float('-inf')
        else:
            compareWith = float('inf')
    if maximize:
        return value > compareWith
    return value < compareWith

def _initialize_arrays_opt_group(maximize, rows, columns):
    """
    returns a 2-d array of rows*columns size filled with either Infinity or -Infinity
    parameters:
        [maximize]
            if 'True' fills with -Infinity and vice versa
        [rows]
            expects a number
        [columns]
            expects a number
    """
    value = float('inf')
    if maximize:
        value = float('-inf')
    return [[value for a in range(0, columns+1)] for a in range(0, rows+1)]

def _optimal_grouping_rec(object_arr, cost_storage, solution_matrix, maximize_prob, min_compare_len, lookup_index, get_lookup_fn, cost_fn):
    """
    Helper function for optimal_grouping function
    """

    # gets the present value at the present index
    present_value = cost_storage[lookup_index[0]][lookup_index[1]]
    # return the present value if it is not infinity
    if _compare_opt_group(maximize_prob, present_value):
        return present_value

    # get the start and end indices where end index depends on the min_compare_len
    start_index = lookup_index[0]
    end_index = lookup_index[1]+1-(min_compare_len-1)

    if start_index is end_index or start_index > end_index:
        cost = cost_fn(object_arr, lookup_index, start_index)
        if _compare_opt_group(maximize_prob, cost, present_value):
            cost_storage[lookup_index[0]][lookup_index[1]] = cost
            solution_matrix[lookup_index[0]][lookup_index[1]] = start_index
            present_value = cost

    for i in range(start_index, end_index):

        # get indices for left recursion tree
        left_rec_indices = get_lookup_fn('before', lookup_index, i)

        cost = _optimal_grouping_rec(object_arr, cost_storage, solution_matrix, maximize_prob,
                                     min_compare_len, left_rec_indices, get_lookup_fn, cost_fn)

        # get indices for right recursion tree
        right_rec_indices = get_lookup_fn('after', lookup_index, i)

        cost = cost+_optimal_grouping_rec(object_arr, cost_storage, solution_matrix, maximize_prob,
                                          min_compare_len, right_rec_indices, get_lookup_fn, cost_fn)

        # get cost for present partition
        cost = cost+cost_fn(object_arr, lookup_index, i)

        # update the values if this is the best solution until now
        if _compare_opt_group(maximize_prob, cost, present_value):
            cost_storage[lookup_index[0]][lookup_index[1]] = cost
            solution_matrix[lookup_index[0]][lookup_index[1]] = i
            present_value = cost

    return present_value

def optimal_grouping(process_objects, maximize_prob, min_compare_len, lookup_index, get_lookup_fn, cost_fn):
    """
    Description
    ===========
    Optimal Grouping groups given set of objects using the given cost function

    Parameters
    ==========
     process_objects
        accepts array of objects on which the algorithm is supposed to run
     maximize_prob
        pass True if the algorithm should find maximum value of the cost function otherwise pass False
     min_compare_len
        a positive number decides to which level of gap the algorithm can maintain while iterating from start to end,
        for example-> if minimun length is 2 then it can only iterate if endIndex=startIndex+2
     lookup_index
        format-->[start_index,endIndex] algorithm runs from start to end
     get_lookup_fn
      should return next range of indices
      sample -> get_lookup_fn(position, rangeIndices, currentIndex)
       position is either 'before' or 'after'
       rangeIndices is the present range of index like [start_index,endIndex]
     cost_fn
      should return the cost
      sample -> cost_fn(process_objects,rangeIndices,currentIndex)


    Usage examples
    ==============

      1.OPTIMAL BINARY SEARCH TREE

        from binarytree import Node
        n = 5
        p = [None, Node(0.15), Node(0.10), Node(0.05), Node(0.10), Node(0.20)]
        q = [Node(0.05), Node(0.10), Node(0.05), Node(0.05), Node(0.05), Node(0.10)]


        def lookup(position, endIndex, middle):
            if position is 'before':
             return [endIndex[0], middle-1]
            else:
             return [middle+1, endIndex[1]]


        def cost(obj, endIndex, middle):

            if(endIndex[1]<endIndex[0]):
                return obj['q'][endIndex[1]].value

            sum = 0
            for i in range(endIndex[0], endIndex[1]+1):
                sum += obj['p'][i].value
            for i in range(endIndex[0]-1, endIndex[1]+1):
                sum += obj['q'][i].value
            return sum


        print(optimal_grouping({'p': p, 'q': q},  False, 1, [1, n], lookup, cost))



      2.MATRIX CHAIN MULTIPLICATION

        def cost(matrix, endIndex, middle):

            if endIndex[0] == endIndex[1]:
            return 0
        return matrix[endIndex[0]-1]*matrix[middle]*matrix[endIndex[1]]


        def lookup(position, endIndex, middle):
        if position is 'before':
            return [endIndex[0], middle]
        else:
            return [middle+1, endIndex[1]]


        print(optimal_grouping([30, 35, 15, 5, 10, 20, 25], False, 2, [1, 6], lookup, cost))

    """

    if min_compare_len < 1:
        raise ValueError(
            'min_compare_len should be a positive integer')

    if lookup_index.__len__() < 2 or lookup_index[0] > lookup_index[1]:
        raise ValueError(
            'lookup index should at least have 2 integer items, first specifying the start and second specifying the last indices')
    #  end of edge cases

    length = lookup_index[1]-lookup_index[0]+1

    # for storing the computed values (helper array)
    cost_storage = _initialize_arrays_opt_group(
        maximize_prob, length+1, length+1)
    #  for storing the solutions
    solution_matrix = _initialize_arrays_opt_group(
        maximize_prob, length+1, length+1)

    _optimal_grouping_rec(process_objects, cost_storage, solution_matrix, maximize_prob,
                          min_compare_len, lookup_index, get_lookup_fn, cost_fn)
    return solution_matrix
