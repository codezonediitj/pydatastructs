from pydatastructs import (
    RangeQueryStatic, minimum, OneDimensionalArray)
from pydatastructs.miscellaneous_data_structures.sparse_table import SparseTable
from pydatastructs.utils.raises_util import raises

def test_RangeQueryStatic_minimum():

    array = OneDimensionalArray(int, [])
    raises(ValueError, lambda: RangeQueryStatic(array, minimum))

    array = OneDimensionalArray(int, [1])
    rq = RangeQueryStatic(array, minimum)
    assert rq.query(0, 1) == 1
    raises(ValueError, lambda: rq.query(0, 0))
    raises(IndexError, lambda: rq.query(0, 2))
