from pydatastructs.miscellaneous_data_structures import Stack
from pydatastructs.linear_data_structures import OneDimensionalArray
from pydatastructs.utils.raises_util import raises

def test_Stack():

    s = Stack(implementation='array')
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.peek == 3
    assert str(s) == '[1, 2, 3]'
    assert s.pop() == 3
    assert s.pop() == 2
    assert s.pop() == 1
    assert s.is_empty is True
    assert raises(ValueError, lambda : s.pop())
    _s = Stack(implementation='array',items=[1, 2, 3])
    assert str(_s) == '[1, 2, 3]'
    assert raises(NotImplementedError, lambda: Stack(implementation=''))

    s1 = Stack(implementation='linkedlist')
    s1.push(1)
    assert raises(TypeError, lambda: s1.push('a'))
    assert raises(TypeError, lambda: Stack(implementation='linkedlist', items=[0], dtype=str))
    assert raises(TypeError, lambda: Stack(implementation='linkedlist', items={0, 1}))
    s1 = Stack(implementation='linkedlist', items = [0, 1])
    s1.push(2)
    s1.push(3)
    assert str(s1) == '[3, 2, 1, 0]'
    assert len(s1) == 4
    assert s1.pop().data == 3
    assert s1.pop().data == 2
    assert len(s1) == 2
    assert s1.pop().data == 1
    assert s1.pop().data == 0
    assert len(s1) == 0
    raises(ValueError, lambda: s1.pop())
