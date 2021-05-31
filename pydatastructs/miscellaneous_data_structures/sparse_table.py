
__all__ = ['sparseTable']


class sparseTable(object):
    """
    Represents the sparse table data structure, used to answer range queries efficiently.

    Parameters
    ==========

    arr: OneDimensionalArray
        The given OneDimensionalArray on which the range queries have to be performed.

    combine: lambda/function
        The function whose value is to be computed on the given range. The function must take
        two parameters.

    isIdempotent: Boolean
        Indicates whether the function is idempotent or not. If the function is idempotent,
        range queries can be answered in constant time, whereas for non-idempotent fucntions,
        these queries take O(logn) time. By default, isIdempotent is set to False.

    Examples
    ========

    >>> from pydatastructs import sparseTable, OneDimensionalArray as ODA
    >>> arr1 = ODA(int, [4, 2, 6, 5, 10, 1])
    >>> spTable = sparseTable(arr1, lambda x, y: x + y)
    >>> spTable.query(2, 4)
    21

    >>> gcd = lambda a, b: a if b == 0 else gcd(b, a % b)
    >>> spTable2 = sparseTable(arr1, gcd, isIdempotent = True)
    >>> spTable2.query(0, 2)
    2
    """

    __slots__ = ['table', 'isIdempotent', 'arr', 'combine']

    log_values = [0, 0]

    def __new__(cls, arr, combine, isIdempotent=False):
        n = len(arr)
        obj = object.__new__(cls)
        obj.isIdempotent = isIdempotent
        obj.arr = arr
        obj.combine = combine

        curr_len = len(cls.log_values)
        for i in range(curr_len, n+1):
            cls.log_values.append(cls.log_values[i//2] + 1)

        table = [[0]*(cls.log_values[n]+1) for i in range(n)]
        obj.table = table

        for i in range(n):
            obj.table[i][0] = arr[i]
        for j in range(1, cls.log_values[n]+1):
            i = 0
            while i + (1 << j) <= n:
                obj.table[i][j] = obj.combine(obj.table[i][j-1],
                obj.table[i + (1 << (j-1))][j-1])
                i += 1
        return obj

    @classmethod
    def methods(cls):
        return ['__new__', 'query']

    def query(self, left, right):
        """
        Used to fetch answers to a range query on the given OneDimensionalArray

        Left:
            Left end of the given range

        Right:
            Right end of the given range

        Note: The range is inclusive of both ends.
        """
        largestPowOf2 = self.log_values[right - left + 1]
        lenOfInterval = (1 << largestPowOf2)
        if(self.isIdempotent is True):
            return self.combine(self.table[left][largestPowOf2], self.table[right-(1 << largestPowOf2)+1][largestPowOf2])
        else:
            answer = 0
            for j in range(lenOfInterval, -1, -1):
                if left + (1 << j) - 1 <= right:
                    answer += self.table[left][j]
                    left += (1 << j)
            return answer
