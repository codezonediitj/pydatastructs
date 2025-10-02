from pydatastructs import (
    RangeQueryDynamic, minimum,
    greatest_common_divisor, summation,
    OneDimensionalArray)
from pydatastructs.utils.raises_util import raises
import random, math
from copy import deepcopy

def _test_RangeQueryDynamic_common(func, gen_expected):

    array = OneDimensionalArray(int, [])
    raises(ValueError, lambda: RangeQueryDynamic(array, func))

    array = OneDimensionalArray(int, [1])
    rq = RangeQueryDynamic(array, func)
    assert rq.query(0, 0) == 1
    raises(ValueError, lambda: rq.query(0, -1))
    raises(IndexError, lambda: rq.query(0, 1))

    array_sizes = [3, 6, 12, 24, 48, 96]
    random.seed(0)
    for array_size in array_sizes:
        inputs = []
        for i in range(array_size):
            for j in range(i + 1, array_size):
                inputs.append((i, j))

        data_structures = ["array", "segment_tree"]
        for ds in data_structures:
            data = random.sample(range(-2*array_size, 2*array_size), array_size)
            array = OneDimensionalArray(int, data)
            rmq = RangeQueryDynamic(array, func, data_structure=ds)
            for input in inputs:
                assert rmq.query(input[0], input[1]) == gen_expected(data, input[0], input[1])

            data_copy = deepcopy(data)
            for _ in range(array_size//2):
                index = random.randint(0, array_size - 1)
                value = random.randint(0, 4 * array_size)
                data_copy[index] = value
                rmq.update(index, value)

            for input in inputs:
                assert rmq.query(input[0], input[1]) == gen_expected(data_copy, input[0], input[1])

def test_RangeQueryDynamic_minimum():

    def _gen_minimum_expected(data, i, j):
        return min(data[i:j + 1])

    _test_RangeQueryDynamic_common(minimum, _gen_minimum_expected)

def test_RangeQueryDynamic_greatest_common_divisor():

    def _gen_gcd_expected(data, i, j):
        if j == i:
            return data[i]
        else:
            expected_gcd = math.gcd(data[i], data[i + 1])
            for idx in range(i + 2, j + 1):
                expected_gcd = math.gcd(expected_gcd, data[idx])
            return expected_gcd

    _test_RangeQueryDynamic_common(greatest_common_divisor, _gen_gcd_expected)

def test_RangeQueryDynamic_summation():

    def _gen_summation_expected(data, i, j):
        return sum(data[i:j + 1])

    return _test_RangeQueryDynamic_common(summation, _gen_summation_expected)
