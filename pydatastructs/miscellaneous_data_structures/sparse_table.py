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

    __slots__ = ['table', 'logs', 'func']

    def __new__(cls, array, func):
        obj = object.__new__(cls)
        size = len(array)
        log_size = int(math.log2(size)) + 1
        obj.table = [OneDimensionalArray(int, log_size) for _ in range(size)]
        obj.logs = OneDimensionalArray(int, size + 1)
        obj.func = func

        for i in range(size):
            obj.table[i][0] = func((array[i],))

        for j in range(1, log_size + 1):
            for i in range(size - (1 << j) + 1):
                obj.table[i][j] = func((obj.table[i][j - 1],
                                        obj.table[i + (1 << (j - 1))][j - 1]))

        obj.logs[0] = obj.logs[1] = 0
        for i in range(2, size + 1):
            obj.logs[i] = obj.logs[i//2] + 1
        return obj

    @classmethod
    def methods(cls):
        return ['query']

    def query(self, start, end):
        rsize = end - start
        log_rsize = self.logs[rsize + 1]
        return self.func((self.table[end][log_rsize],
                          self.table[end - (1 << log_rsize) + 1][log_rsize]))

    def __str__(self):
        return str([str(array) for array in self.table])
