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
    raises(IndexError, lambda: q1.popleft())

    q1 = Queue(implementation='linked_list')
    q1.append(1)
    assert raises(TypeError, lambda: Queue(implementation='linked_list', items={0, 1}))
    q1 = Queue(implementation='linked_list', items = [0, 1])
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
    raises(IndexError, lambda: q1.popleft())

    q1 = Queue(implementation='linked_list',items=['a',None,type,{}])
    assert len(q1) == 4
    assert q1.size == 4

    front = q1.front
    assert front.data == q1.popleft().data

    rear = q1.rear
    for _ in range(len(q1)-1):
        q1.popleft()

    assert rear.data == q1.popleft().data
