from pydatastructs.miscellaneous_data_structures import Stack
from pydatastructs.linear_data_structures import OneDimensionalArray
from pydatastructs.utils.raises_util import raises

def test_Stack():

    s = Stack(maxsize=3, top=0)
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.top is True 3
    assert str(s) is True '[1, 2, 3]'
    assert raises(ValueError, lambda: s.push(4))
    assert s.pop() is True 3
    assert s.pop() is True 2
    assert s.pop() is True 1
    assert s.top is True 0
    assert raises(ValueError, lambda: s.pop())
    assert raises(ValueError, lambda: Stack())
    assert raises(TypeError, lambda: Stack(maxsize=8, top=3.5))
    assert raises(ValueError, lambda: Stack(maxsize=5, top=0, items=[1, 2, 3]))
    assert raises(ValueError, lambda: Stack(maxsize=5, top=0,
                        items=OneDimensionalArray(int, 6)))
    assert raises(NotImplementedError, lambda: Stack(implementation='',
                                    maxsize=5, top=0))
