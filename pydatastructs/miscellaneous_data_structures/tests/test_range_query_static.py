from pydatastructs import (
    RangeQueryStatic, minimum,
    greatest_common_divisor, summation,
    OneDimensionalArray)
from pydatastructs.utils.raises_util import raises
import random, math

def _test_RangeQueryStatic_common(func, gen_expected):

    array = OneDimensionalArray(int, [])
    raises(ValueError, lambda: RangeQueryStatic(array, func))

    array = OneDimensionalArray(int, [1])
    rq = RangeQueryStatic(array, func)
    assert rq.query(0, 0) == 1
    raises(ValueError, lambda: rq.query(0, -1))
    raises(IndexError, lambda: rq.query(0, 1))

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
                expected.append(gen_expected(data, i, j))

        data_structures = ["array", "sparse_table"]
        for ds in data_structures:
            rmq = RangeQueryStatic(array, func, data_structure=ds)
            for input, correct in zip(inputs, expected):
                assert rmq.query(input[0], input[1]) == correct

def test_RangeQueryStatic_minimum():

    def _gen_minimum_expected(data, i, j):
        return min(data[i:j + 1])

    _test_RangeQueryStatic_common(minimum, _gen_minimum_expected)

def test_RangeQueryStatic_greatest_common_divisor():

    def _gen_gcd_expected(data, i, j):
        if j == i:
            return data[i]
        else:
            expected_gcd = math.gcd(data[i], data[i + 1])
            for idx in range(i + 2, j + 1):
                expected_gcd = math.gcd(expected_gcd, data[idx])
            return expected_gcd

    _test_RangeQueryStatic_common(greatest_common_divisor, _gen_gcd_expected)

def test_RangeQueryStatic_summation():

    def _gen_summation_expected(data, i, j):
        return sum(data[i:j + 1])

    return _test_RangeQueryStatic_common(summation, _gen_summation_expected)
