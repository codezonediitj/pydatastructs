from pydatastructs.miscellaneous_data_structures.sparse_table import SparseTable


class RangeMinimumQuery:
    def __new__(cls, array, ds='sparse_table'):
        if ds == 'array':
            return RangeMinimumQueryArray(cls)
        elif ds == 'sparse_table':
            return RangeMinimumQuerySparseTable(cls)
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

    def query(self, i, j):
        return self.sparse_table.__rangequery__(i, j)


class RangeMinimumQueryArray(RangeMinimumQuery):
    pass
