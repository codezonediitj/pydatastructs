from pydatastructs.miscellaneous_data_structures import Queue
from pydatastructs.utils.raises_util import raises

def test_Queue():

    q1 = Queue(implementation='array', items=[0])
    q1.append(1)
    q1.append(2)
    q1.append(3)
    assert str(q1) == '[0, 1, 2, 3]'
    assert len(q1) == 4
    assert q1.popleft() == 0
    assert q1.popleft() == 1
    assert len(q1) == 2
    assert q1.popleft() == 2
    assert q1.popleft() == 3
    assert len(q1) == 0

    q1 = Queue()
    raises(ValueError, lambda: q1.popleft())

    q1 = Queue(implementation='linkedlist')
    q1.append(1)
    assert raises(TypeError, lambda: q1.append('a'))
    assert raises(TypeError, lambda: Queue(implementation='linkedlist', items=[0], dtype=str))
    assert raises(TypeError, lambda: Queue(implementation='linkedlist', items={0, 1}))
    q1 = Queue(implementation='linkedlist', items = [0, 1])
    q1.append(2)
    q1.append(3)
    assert str(q1) == '[0, 1, 2, 3]'
    assert len(q1) == 4
    assert q1.popleft().data == 0
    assert q1.popleft().data == 1
    assert len(q1) == 2
    assert q1.popleft().data == 2
    assert q1.popleft().data == 3
    assert len(q1) == 0
    raises(ValueError, lambda: q1.popleft())
