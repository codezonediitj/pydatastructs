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

    def __init__(self, array, N):
        self.table = MultiDimensionalArray(int, 2*N+10, self.MAXLOG)
        self.logs = OneDimensionalArray(int, 2*N+10)
        self.logs[0] = self.logs[1] = 0
        for i in range(2, N):
            self.logs[i] = self.logs[int(i/2)] + 1

    @classmethod
    def methods(cls):
        return ['__createtable__', '__rangequery__']

    def _comp(x, y):
        if(x < y):
            return x
        else:
            return y

    def __createtable__(self, arr, comp=_comp):
        for i in range(len(arr)):
            self.table[i][0] = arr[i]
        for j in range(1, self.MAXLOG):
            for i in range(len(arr) - (1 << j) + 1):
                self.table[i][j] = comp(
                    self.table[i][j-1],
                    self.table[i+(1 << (j-1))][j-1])

    def __rangequery__(self, L, R, comp=_comp):
        j = self.logs[R-L+1]
        return comp(
            self.table[L][j],
            self.table[R-(1 << j)+1][j])
