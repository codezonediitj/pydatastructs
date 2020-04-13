from pydatastructs.linear_data_structures import (
    OneDimensionalArray, DynamicOneDimensionalArray, MultiDimensionalArray)
from pydatastructs.utils.raises_util import raises


def test_OneDimensionalArray():
    ODA = OneDimensionalArray
    A = ODA(int, 5, [1.0, 2, 3, 4, 5], init=6)
    A[1] = 2.0
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
    MDA = MultiDimensionalArray
    A = MDA(int, 5, 9, 3, 8)
    A[1] = 2.0
    assert A
    assert raises(IndexError, lambda: A[5])
    assert raises(IndexError, lambda: A[4][10])
    assert raises(IndexError, lambda: A[-1])
    assert raises(ValueError, lambda: MDA())
    assert raises(ValueError, lambda: MDA(int))
    assert raises(TypeError, lambda: MDA(int, 0))
    assert raises(TypeError, lambda: MDA(int, 5, 6, ""))

def test_DynamicOneDimensionalArray():
    DODA = DynamicOneDimensionalArray
    A = DODA(int, 0)
    A.append(1)
    A.append(2)
    A.append(3)
    A.append(4)
    A.delete(0)
    A.delete(0)
    A.delete(15)
    A.delete(-1)
    A.delete(1)
    A.delete(2)
    assert A._data == [4, None, None]
    assert A.size == 3
    A.fill(4)
    assert A._data == [4, 4, 4]
