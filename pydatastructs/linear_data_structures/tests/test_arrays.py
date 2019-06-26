from pydatastructs.linear_data_structures import OneDimensionalArray
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
