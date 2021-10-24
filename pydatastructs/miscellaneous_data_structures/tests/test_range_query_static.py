from pydatastructs import (
    RangeQueryStatic, minimum, OneDimensionalArray)
from pydatastructs.miscellaneous_data_structures.sparse_table import SparseTable
from pydatastructs.utils.raises_util import raises
import random

def test_RangeQueryStatic_minimum():

    array = OneDimensionalArray(int, [])
    raises(ValueError, lambda: RangeQueryStatic(array, minimum))

    array = OneDimensionalArray(int, [1])
    rq = RangeQueryStatic(array, minimum)
    assert rq.query(0, 1) == 1
    raises(ValueError, lambda: rq.query(0, 0))
    raises(IndexError, lambda: rq.query(0, 2))

    array_sizes = [3, 6, 12, 24, 48, 96]
    random.seed(0)
    for array_size in array_sizes:
        data = random.sample(range(-2*array_size, 2*array_size), array_size)
        array = OneDimensionalArray(int, data)

        expected = []
        inputs = []
        for i in range(array_size):
            for j in range(i + 1, array_size):
                inputs.append((i, j))
                expected.append(min(data[i:j]))

        data_structures = ["array", "sparse_table"]
        for ds in data_structures:
            rmq = RangeQueryStatic(array, minimum, data_structure=ds)
            for input, correct in zip(inputs, expected):
                assert rmq.query(input[0], input[1]) == correct
