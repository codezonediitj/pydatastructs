from pydatastructs.linear_data_structures import (
    OneDimensionalArray, DynamicOneDimensionalArray)
from pydatastructs.utils.raises_util import raises


def test_OneDimensionalArray():
    ODA = OneDimensionalArray
    A = ODA(int, 5, [1, 2, 3, 4, 5], init=6)
    assert A
    assert ODA(int, (1, 2, 3, 4, 5), 5)
    assert ODA(int, 5)
    assert ODA(int, [1, 2, 3])
    raises(IndexError, lambda: A[7])
    raises(IndexError, lambda: A[-1])
    raises(ValueError, lambda: ODA())
    raises(ValueError, lambda: ODA(int, 1, 2, 3))
    raises(TypeError, lambda: ODA(int, 5.0, set([1, 2, 3])))
    raises(TypeError, lambda: ODA(int, 5.0))
    raises(TypeError, lambda: ODA(int, set([1, 2, 3])))
    raises(ValueError, lambda: ODA(int, 3, [1]))

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
    A.fill(4)
    assert A._data == [4, 4, 4]
