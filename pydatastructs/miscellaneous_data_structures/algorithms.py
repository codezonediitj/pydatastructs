from pydatastructs.miscellaneous_data_structures.sparse_table import SparseTable
from pydatastructs.utils.misc_util import _check_range_query_inputs

__all__ = ['RangeQueryStatic']


class RangeQueryStatic:
    """
    Produces results for range queries of different kinds
    by using specified data structure.

    Parameters
    ==========

    array: OneDimensionalArray
        The array for which we need to answer queries.
        All the elements should be of type `int`.
    func: callable
        The function to be used for generating results
        of a query. It should accept only one tuple as an
        argument. The size of the tuple will be either 1 or 2
        and any one of the elements can be `None`. You can treat
        `None` in whatever way you want according to the query
        you are performing. For example, in case of range minimum
        queries, `None` can be treated as infinity. We provide
        the following which can be used as an argument value for this
        parameter,

        `minimum` - For range minimum queries.

        `greatest_common_divisor` - For queries finding greatest
                                    common divisor of a range.

        `summation` - For range sum queries.
    data_structure: str
        The data structure to be used for performing
        range queries.
        Currently the following data structures are supported,

        'array' -> Array data structure.
                   Each query takes O(end - start) time asymptotically.

        'sparse_table' -> Sparse table data structure.
                          Each query takes O(log(end - start)) time
                          asymptotically.

        By default, 'sparse_table'.

    Examples
    ========

    >>> from pydatastructs import OneDimensionalArray, RangeQueryStatic
    >>> from pydatastructs import minimum
    >>> arr = OneDimensionalArray(int, [4, 6, 1, 5, 7, 3])
    >>> RMQ = RangeQueryStatic(arr, minimum)
    >>> RMQ.query(3, 4)
    5
    >>> RMQ.query(0, 4)
    1
    >>> RMQ.query(0, 2)
    1

    Note
    ====

    The array once passed as an input should not be modified
    once the `RangeQueryStatic` constructor is called. If you
    have updated the array, then you need to create a new
    `RangeQueryStatic` object with this updated array.
    """

    def __new__(cls, array, func, data_structure='sparse_table'):
        if len(array) == 0:
            raise ValueError("Input %s array is empty."%(array))

        if data_structure == 'array':
            return RangeQueryStaticArray(array, func)
        elif data_structure == 'sparse_table':
            return RangeQueryStaticSparseTable(array, func)
        else:
            raise NotImplementedError(
                "Currently %s data structure for range "
                "query without updates isn't implemented yet."
                % (data_structure))

    @classmethod
    def methods(cls):
        return ['query']

    def query(start, end):
        """
        Method to perform a query in [start, end) range.

        Parameters
        ==========

        start: int
            The starting index of the range.
        end: int
            The ending index of the range.
        """
        raise NotImplementedError(
            "This is an abstract method.")


class RangeQueryStaticSparseTable(RangeQueryStatic):

    __slots__ = ["sparse_table", "bounds"]

    def __new__(cls, array, func):
        obj = object.__new__(cls)
        sparse_table = SparseTable(array, func)
        obj.bounds = (0, len(array))
        obj.sparse_table = sparse_table
        return obj

    @classmethod
    def methods(cls):
        return ['query']

    def query(self, start, end):
        _check_range_query_inputs((start, end + 1), self.bounds)
        return self.sparse_table.query(start, end)


class RangeQueryStaticArray(RangeQueryStatic):

    __slots__ = ["array", "func"]

    def __new__(cls, array, func):
        obj = object.__new__(cls)
        obj.array = array
        obj.func = func
        return obj

    @classmethod
    def methods(cls):
        return ['query']

    def query(self, start, end):
        _check_range_query_inputs((start, end + 1), (0, len(self.array)))

        rsize = end - start + 1

        if rsize == 1:
            return self.func((self.array[start],))

        query_ans = self.func((self.array[start], self.array[start + 1]))
        for i in range(start + 2, end + 1):
            query_ans = self.func((query_ans, self.array[i]))
        return query_ans
