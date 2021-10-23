from pydatastructs.miscellaneous_data_structures.sparse_table import SparseTable


__all__ = ['RangeMinimumQuery']

class RangeMinimumQuery:
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
