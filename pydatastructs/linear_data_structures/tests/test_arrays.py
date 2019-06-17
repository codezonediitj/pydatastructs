from pydatastructs.linear_data_structures import OneDimensionalArray
from pydatastructs.utils.raises_util import raises

def test_OneDimensionalArray():
    ODA = OneDimensionalArray
    assert ODA(5, [1, 2, 3, 4, 5], init=6)
    assert ODA((1, 2, 3, 4, 5), 5)
    assert ODA(5)
    assert ODA([1, 2, 3])
    raises(ValueError, lambda: ODA())
    raises(ValueError, lambda: ODA(1, 2, 3))
    raises(TypeError, lambda: ODA(5.0, set([1, 2, 3])))
    raises(TypeError, lambda: ODA(5.0))
    raises(TypeError, lambda: ODA(set([1, 2, 3])))
    raises(ValueError, lambda: ODA(3, [1]))
