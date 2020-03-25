from pydatastructs.linear_data_structures.arrays import (
    OneDimensionalArray, DynamicArray)
from pydatastructs.utils.misc_util import _check_type, _comp
from concurrent.futures import ThreadPoolExecutor
from math import log, floor

__all__ = [
    'merge_sort_parallel',
    'brick_sort'
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
