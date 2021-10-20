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

    __slots__ = ['table']

    def __new__(cls, array, N=500000):
        obj = object.__new__(cls)
        MAXLOG = int(math.log2(2*N))
        obj.table = MultiDimensionalArray(int, 2*N+10, MAXLOG)
        obj.logs = OneDimensionalArray(int, 2*N+10)
        obj.logs[0] = obj.logs[1] = 0
        for i in range(2, N):
            obj.logs[i] = obj.logs[int(i/2)] + 1
        for i in range(len(array)):
            obj.table[i][0] = array[i]
        for j in range(1, obj.MAXLOG):
            for i in range(len(array) - (1 << j) + 1):
                obj.table[i][j] = min(
                    obj.table[i][j-1],
                    obj.table[i+(1 << (j-1))][j-1])
        return obj

    @classmethod
    def methods(cls):
        return ['__rangequery__']

    def __rangequery__(self, left, right):
        j = self.logs[right-left+1]
        return min(
            self.table[left][j],
            self.table[right-(1 << j)+1][j])
