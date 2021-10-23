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

    def __new__(cls, array):
        obj = object.__new__(cls)
        N = len(array)
        LOGN = int(math.log2(N)) + 1
        obj.table = MultiDimensionalArray(int, N, LOGN)
        for i in range(N):
            obj.table[i][0] = array[i]
        for j in range(1, LOGN + 1):
            for i in range(N - (1 << j) + 1):
                obj.table[i][j] = min(
                    obj.table[i][j-1],
                    obj.table[i+(1 << (j-1))][j-1])

        obj.logs = OneDimensionalArray(int, N+1)
        obj.logs[0] = obj.logs[1] = 0
        for i in range(2, N+1):
            obj.logs[i] = obj.logs[int(i/2)] + 1
        return obj

    @classmethod
    def methods(cls):
        return ['__query__']

    def __query__(self, left, right):
        j = self.logs[right-left+1]
        return min(
            self.table[left][j],
            self.table[right-(1 << j)+1][j])
