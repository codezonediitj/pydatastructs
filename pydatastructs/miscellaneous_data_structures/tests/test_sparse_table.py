from pydatastructs import (
    sparseTable, OneDimensionalArray)
from pydatastructs.utils.raises_util import raises

def test_sparseTable():
    ODA = OneDimensionalArray
    array = ODA(int, [4, 2, 6, 5, 1, 7, 8])

    spTable = sparseTable(array, lambda x, y: min(x, y), isIdempotent=True)

    rangeQueryResult = spTable.query(0, 2)
    expected_result = 2
    assert(rangeQueryResult == expected_result)

    rangeQueryResult = spTable.query(2, 5)
    expected_result = 1
    assert(rangeQueryResult == expected_result)

    def gcd(a, b): return a if b == 0 else gcd(b, a % b)
    spTable2 = sparseTable(array, gcd, isIdempotent=True)

    rangeQueryResult = spTable2.query(0, 2)
    expected_result = 2
    assert(rangeQueryResult == expected_result)

    rangeQueryResult = spTable2.query(5, 6)
    expected_result = 1
    assert(rangeQueryResult == expected_result)

    spTable3 = sparseTable(array, lambda x, y: x + y)

    rangeQueryResult = spTable3.query(2, 5)
    expected_result = 19
    assert(rangeQueryResult == expected_result)

    rangeQueryResult = spTable3.query(1, 4)
    expected_result = 14
    assert(rangeQueryResult == expected_result)
