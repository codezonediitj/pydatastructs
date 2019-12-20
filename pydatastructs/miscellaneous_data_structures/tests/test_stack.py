from pydatastructs.miscellaneous_data_structures import Stack
from pydatastructs.linear_data_structures import OneDimensionalArray
from pydatastructs.utils.raises_util import raises

def test_Stack():

    s = Stack(maxsize=3, top=0)
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.top == 3
    assert str(s) == '[1, 2, 3]'
    assert raises(ValueError, lambda: s.push(4))
    assert s.pop() == 3
    assert s.pop() == 2
    assert s.pop() == 1
    assert s.top == 0
    assert raises(ValueError, lambda: s.pop())
    assert raises(ValueError, lambda: Stack())
    assert raises(TypeError, lambda: Stack(maxsize=8, top=3.5))
    assert raises(ValueError, lambda: Stack(maxsize=5, top=0, items=[1, 2, 3]))
    assert raises(ValueError, lambda: Stack(maxsize=5, top=0,
                        items=OneDimensionalArray(int, 6)))
    assert raises(NotImplementedError, lambda: Stack(implementation='',
                                    maxsize=5, top=0))
