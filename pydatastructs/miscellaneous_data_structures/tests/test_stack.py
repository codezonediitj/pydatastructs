from pydatastructs.miscellaneous_data_structures import Stack, ArrayStack, LinkedListStack
from pydatastructs.linear_data_structures import OneDimensionalArray
from pydatastructs.utils.raises_util import raises

def test_Stack():
    s = Stack(implementation='array')
    s = Stack()
    s = Stack(implementation='linked_list')

def test_ArrayStack():
    s = ArrayStack()
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.peek == 3
    assert str(s) == '[1, 2, 3]'
    assert s.pop() == 3
    assert s.pop() == 2
    assert s.pop() == 1
    assert s.is_empty is True
    assert raises(IndexError, lambda : s.pop())
    _s = Stack(items=[1, 2, 3])
    assert str(_s) == '[1, 2, 3]'
    assert len(_s) == 3
    assert raises(NotImplementedError, lambda: Stack(implementation=''))

def test_LinkedListStack():
    s = Stack(implementation='linked_list')
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.peek.data == 3
    assert str(s) == '[1, 2, 3]'
    assert s.pop().data == 3
    assert s.pop().data == 2
    assert s.pop().data == 1
    assert s.is_empty is True
    assert raises(IndexError, lambda : s.pop())
    assert str(s) == '[]'
    _s = Stack(implementation='linked_list',items=[1, 2, 3])
    assert str(_s) == '[1, 2, 3]'
    assert len(_s) == 3

    s = Stack(implementation='linked_list',items=['a',None,type,{}])
    assert len(s) == 4
    assert s.size == 4

    peek = s.peek
    assert peek.data == s.pop().data
    assert raises(TypeError, lambda: Stack(implementation='linked_list', items={0, 1}))
