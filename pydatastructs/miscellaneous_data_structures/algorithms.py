from pydatastructs.miscellaneous_data_structures.sparse_table import SparseTable

__all__ = ['RangeQueryStatic']


class RangeQueryStatic:
    """
    Answers incoming queries of the form (L, R), which ask to find
    the minimum element in array A between positions L (inclusive) and
    R (exclusive).

    Parameters
    ==========

    array: OneDimensionalArray
        The array for which we need to answer queries.
    ds: str
        The data structure we want to use for RangeMinimumQuery.

        'array' -> Simple array implementation

        'sparse_table' -> Sparse Table implementation as given in [2]

    Examples
    ========

    >>> from pydatastructs import OneDimensionalArray, RangeQueryStatic
    >>> from pydatastructs import minimum
    >>> arr = OneDimensionalArray(int, [4, 6, 1, 5, 7, 3])
    >>> RMQ = RangeQueryStatic(arr, minimum)
    >>> RMQ.query(3, 5)
    3
    >>> RMQ.query(0, 5)
    1
    >>> RMQ.query(0, 3)
    1

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Range_minimum_query
    .. [2] https://cp-algorithms.com/data_structures/sparse-table.html
    """

    def __new__(cls, array, func, data_structure='sparse_table'):
        if data_structure == 'array':
            return RangeQueryStaticArray(array, func)
        elif data_structure == 'sparse_table':
            return RangeQueryStaticSparseTable(array, func)
        else:
            raise NotImplementedError(
                "Currently %s data structure for range "
                "query without updates isn't implemented yet."
                % (data_structure))

    def query(start, end):
        raise NotImplementedError(
            "This is an abstract method.")


class RangeQueryStaticSparseTable(RangeQueryStatic):

    __slots__ = ["sparse_table"]

    def __new__(cls, array, func):
        obj = object.__new__(cls)
        sparse_table = SparseTable(array, func)
        obj.sparse_table = sparse_table
        return obj

    def query(self, start, end):
        if start >= end:
            raise ValueError("Input (%d, %d) range is empty."%(start, end))
        return self.sparse_table.query(start, end)


class RangeQueryStaticArray(RangeQueryStatic):

    __slots__ = ["array", "func"]

    def __new__(cls, array, func):
        obj = object.__new__(cls)
        obj.array = array
        obj.func = func
        return obj

    def query(self, start, end):
        if start >= end:
            raise ValueError("Input (%d, %d) range is empty."%(start, end))

        rsize = end - start

        if rsize == 1:
            return self.func((self.array[start],))

        query_ans = self.func((self.array[start], self.array[start + 1]))
        for i in range(start + 2, end):
            query_ans = self.func(query_ans, self.array[i])
        return query_ans
