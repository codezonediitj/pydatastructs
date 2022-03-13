from pydatastructs.linear_data_structures.arrays import OneDimensionalArray
from pydatastructs.utils.misc_util import (
    Backend, raise_if_backend_is_not_python)
import math

__all__ = ['SparseTable']


class SparseTable(object):
    """
    Represents the sparse table data structure.

    Parameters
    ==========

    array: OneDimensionalArray
        The array to be used for filling the sparse table.
    func: callable
        The function to be used for filling the sparse table.
        It should accept only one tuple as an argument. The
        size of the tuple will be either 1 or 2 and any one
        of the elements can be `None`. You can treat `None` in
        whatever way you want. For example, in case of minimum
        values, `None` can be treated as infinity. We provide
        the following which can be used as an argument value for this
        parameter,

        `minimum` - For range minimum queries.

        `greatest_common_divisor` - For queries finding greatest
                                    common divisor of a range.

        `summation` - For range sum queries.
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Examples
    ========

    >>> from pydatastructs import SparseTable, minimum
    >>> from pydatastructs import OneDimensionalArray
    >>> arr = OneDimensionalArray(int, [1, 2, 3, 4, 5])
    >>> s_t = SparseTable(arr, minimum)
    >>> str(s_t)
    "['[1, 1, 1]', '[2, 2, 2]', '[3, 3, None]', '[4, 4, None]', '[5, None, None]']"

    References
    ==========

    .. [1] https://cp-algorithms.com/data_structures/sparse-table.html
    """

    __slots__ = ['_table', 'func']

    def __new__(cls, array, func, **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))

        # TODO: If possible remove the following check.
        if len(array) == 0:
            raise ValueError("Input %s array is empty."%(array))

        obj = object.__new__(cls)
        size = len(array)
        log_size = int(math.log2(size)) + 1
        obj._table = [OneDimensionalArray(int, log_size) for _ in range(size)]
        obj.func = func

        for i in range(size):
            obj._table[i][0] = func((array[i],))

        for j in range(1, log_size + 1):
            for i in range(size - (1 << j) + 1):
                obj._table[i][j] = func((obj._table[i][j - 1],
                                         obj._table[i + (1 << (j - 1))][j - 1]))

        return obj

    @classmethod
    def methods(cls):
        return ['query', '__str__']

    def query(self, start, end):
        """
        Method to perform a query on sparse table in [start, end)
        range.

        Parameters
        ==========

        start: int
            The starting index of the range.
        end: int
            The ending index of the range.
        """
        j = int(math.log2(end - start + 1)) + 1
        answer = None
        while j >= 0:
            if start + (1 << j) - 1 <= end:
                answer = self.func((answer, self._table[start][j]))
                start += 1 << j
            j -= 1
        return answer

    def __str__(self):
        return str([str(array) for array in self._table])
