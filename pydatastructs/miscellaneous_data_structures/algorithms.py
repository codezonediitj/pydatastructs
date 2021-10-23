from pydatastructs.miscellaneous_data_structures.sparse_table import SparseTable

__all__ = ['RangeMinimumQuery']


class RangeMinimumQuery:
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

    >>> from pydatastructs import OneDimensionalArray, RangeMinimumQuery
    >>> arr = OneDimensionalArray(int, [4, 6, 1, 5, 7, 3])
    >>> RMQ = RangeMinimumQuery(arr)
    >>> RMQ.query(3,5)
    3
    >>> RMQ.query(0,5)
    1
    >>> RMQ.query(0,3)
    1

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Range_minimum_query
    .. [2] https://cp-algorithms.com/data_structures/sparse-table.html
    """

    def __new__(cls, array, ds='sparse_table'):
        if ds == 'array':
            return RangeMinimumQueryArray(array)
        elif ds == 'sparse_table':
            return RangeMinimumQuerySparseTable(array)
        else:
            raise NotImplementedError(
                "Currently %s data structure for range "
                "minimum query isn't implemented yet."
                % (ds))

    def query(left, right):
        raise NotImplementedError(
            "This is an abstract method.")


class RangeMinimumQuerySparseTable(RangeMinimumQuery):

    __slots__ = ["sparse_table"]

    def __new__(cls, array):
        obj = object.__new__(cls)
        sparse_table = SparseTable(array)
        obj.sparse_table = sparse_table
        return obj

    def query(self, left, right):
        return self.sparse_table.__query__(left, right)


class RangeMinimumQueryArray(RangeMinimumQuery):

    __slots__ = ["array"]

    def __new__(cls, array):
        obj = object.__new__(cls)
        obj.array = array
        return obj

    def query(self, left, right):
        if left >= right:
            raise ValueError("Empty range received.")
        query_ans = self.array[left]
        for i in range(left, right):
            query_ans = min(query_ans, self.array[i])
        return query_ans
