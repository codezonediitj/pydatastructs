from pydatastructs.linear_data_structures.arrays import (
    OneDimensionalArray, DynamicArray)
from pydatastructs.utils.misc_util import _check_type
from concurrent.futures import ThreadPoolExecutor
from math import log, floor

__all__ = [
    'merge_sort_parallel'
]

def _merge(array, sl, el, sr, er, end, comp):
    l, r = [],  []
    for i in range(sl, el + 1):
        if (i <= end and
            array[i] is not None):
            l.append(array[i])
            array[i] = None
    for i in range(sr, er + 1):
        if (i <= end and
            array[i] is not None):
            r.append(array[i])
            array[i] = None
    i, j, k = 0, 0, sl
    while i < len(l) and j < len(r):
        if comp(l[i], r[j]):
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
