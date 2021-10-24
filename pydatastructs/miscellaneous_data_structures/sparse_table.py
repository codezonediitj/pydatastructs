from pydatastructs.linear_data_structures.arrays import (
    MultiDimensionalArray, OneDimensionalArray)
from pydatastructs.utils.misc_util import NoneType
import math

__all__ = ['SparseTable']


class SparseTable(object):
    """
    Represents a sparse table

    References
    ==========

    .. [1] https://cp-algorithms.com/data_structures/sparse-table.html
    """

    __slots__ = ['table', 'func']

    def __new__(cls, array, func):

        if len(array) == 0:
            raise ValueError("Input %s array is empty."%(array))

        obj = object.__new__(cls)
        size = len(array)
        log_size = int(math.log2(size)) + 1
        obj.table = [OneDimensionalArray(int, log_size) for _ in range(size)]
        obj.func = func

        for i in range(size):
            obj.table[i][0] = func((array[i],))

        for j in range(1, log_size + 1):
            for i in range(size - (1 << j) + 1):
                obj.table[i][j] = func((obj.table[i][j - 1],
                                        obj.table[i + (1 << (j - 1))][j - 1]))

        return obj

    @classmethod
    def methods(cls):
        return ['query']

    def query(self, start, end):
        end -= 1
        j = int(math.log2(end - start + 1)) + 1
        answer = None
        while j >= 0:
            if start + (1 << j) - 1 <= end:
                answer = self.func((answer, self.table[start][j]))
                start += 1 << j
            j -= 1
        return answer

    def __str__(self):
        return str([str(array) for array in self.table])
