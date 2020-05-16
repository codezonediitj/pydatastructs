from pydatastructs.linear_data_structures import (
    OneDimensionalArray, DynamicOneDimensionalArray, MultiDimensionalArray)
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


def test_MultiDimensionalArray():
    assert raises(ValueError, lambda: MultiDimensionalArray(int, 2, -1, 3))
    assert MultiDimensionalArray(int, 10).shape == (10,)
    array = MultiDimensionalArray(int, 5, 9, 3, 8)
    assert array.shape == (5, 9, 3, 8)
    array.fill(5)
    array[1, 3, 2, 5] = 2.0
    assert array
    assert array[1, 3, 2, 5] == 2.0
    assert array[1, 3, 0, 5] == 5
    assert array[1, 2, 2, 5] == 5
    assert array[2, 3, 2, 5] == 5
    assert raises(IndexError, lambda: array[5])
    assert raises(IndexError, lambda: array[4, 10])
    assert raises(IndexError, lambda: array[-1])
    assert raises(IndexError, lambda: array[2, 3, 2, 8])
    assert raises(ValueError, lambda: MultiDimensionalArray())
    assert raises(ValueError, lambda: MultiDimensionalArray(int))
    assert raises(TypeError, lambda: MultiDimensionalArray(int, 5, 6, ""))
    array = MultiDimensionalArray(int, 3, 2, 2)
    array.fill(1)
    array[0, 0, 0] = 0
    array[0, 0, 1] = 0
    array[1, 0, 0] = 0
    array[2, 1, 1] = 0
    assert str(array) == '[0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0]'
    array = MultiDimensionalArray(int, 4)
    assert array.shape == (4,)
    array.fill(5)
    array[3] = 3
    assert array[3] == 3

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
