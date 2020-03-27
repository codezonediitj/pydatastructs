from pydatastructs.linear_data_structures import (
    OneDimensionalArray, DynamicOneDimensionalArray)
from pydatastructs.utils.raises_util import raises


def test_OneDimensionalArray():
    ODA = OneDimensionalArray
    A = ODA(int, 5, [1.0, 2, 3, 4, 5], init=6)
    A[1] = 2.0
    assert str(A) == '[1, 2, 3, 4, 5]'
    assert A
    assert ODA(int, [1.0, 2, 3, 4, 5], 5)
    assert ODA(int, 5)
    assert ODA(int, [1.0, 2, 3])
    assert raises(IndexError, lambda: A[7])
    assert raises(IndexError, lambda: A[-1])
    assert raises(ValueError, lambda: ODA())
    assert raises(ValueError, lambda: ODA(int, 1, 2, 3))
    assert raises(TypeError, lambda: ODA(int, 5.0, set([1, 2, 3])))
    assert raises(TypeError, lambda: ODA(int, 5.0))
    assert raises(TypeError, lambda: ODA(int, set([1, 2, 3])))
    assert raises(ValueError, lambda: ODA(int, 3, [1]))

def test_DynamicOneDimensionalArray():
    DODA = DynamicOneDimensionalArray
    A = DODA(int, 0)
    A.append(1)
    A.append(2)
    A.append(3)
    A.append(4)
    assert str(A) == "['1', '2', '3', '4']"
    A.delete(0)
    A.delete(0)
    A.delete(15)
    A.delete(-1)
    A.delete(1)
    A.delete(2)
    assert A._data == [4, None, None]
    assert str(A) == "['4']"
    assert A.size == 3
    A.fill(4)
    assert A._data == [4, 4, 4]
    b = DynamicOneDimensionalArray(int, 0)
    b.append(1)
    b.append(2)
    b.append(3)
    b.append(4)
    b.append(5)
    assert b._data == [1, 2, 3, 4, 5, None, None]
    assert list(reversed(b)) == [5, 4, 3, 2, 1]
