from pydatastructs.miscellaneous_data_structures import Queue
from pydatastructs.miscellaneous_data_structures.queue import (
    ArrayQueue, LinkedListQueue, PriorityQueue,
    LinkedListPriorityQueue)
from pydatastructs.utils.raises_util import raises
from pydatastructs.utils.misc_util import _check_type

def test_Queue():
    q = Queue(implementation='array')
    q1 = Queue()
    assert _check_type(q, ArrayQueue) is True
    assert _check_type(q1, ArrayQueue) is True
    q2 = Queue(implementation='linked_list')
    assert _check_type(q2, LinkedListQueue) is True
    assert raises(NotImplementedError, lambda: Queue(implementation=''))

def test_ArrayQueue():
    q1 = Queue()
    raises(IndexError, lambda: q1.popleft())
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

def test_LinkedListQueue():
    q1 = Queue(implementation='linked_list')
    q1.append(1)
    assert raises(TypeError, lambda: Queue(implementation='linked_list', items={0, 1}))
    q1 = Queue(implementation='linked_list', items = [0, 1])
    q1.append(2)
    q1.append(3)
    assert str(q1) == "['0', '1', '2', '3']"
    assert len(q1) == 4
    assert q1.popleft().key == 0
    assert q1.popleft().key == 1
    assert len(q1) == 2
    assert q1.popleft().key == 2
    assert q1.popleft().key == 3
    assert len(q1) == 0
    raises(IndexError, lambda: q1.popleft())

    q1 = Queue(implementation='linked_list',items=['a',None,type,{}])
    assert len(q1) == 4
    assert q1.size == 4

    front = q1.front
    assert front.key == q1.popleft().key

    rear = q1.rear
    for _ in range(len(q1)-1):
        q1.popleft()

    assert rear.key == q1.popleft().key

def test_PriorityQueue():
    pq1 = PriorityQueue(implementation='linked_list')
    assert _check_type(pq1, LinkedListPriorityQueue) is True
    assert raises(NotImplementedError, lambda: Queue(implementation=''))

def test_ImplementationPriorityQueue():
    impls = ['linked_list', 'binomial_heap', 'binary_heap']
    for impl in impls:
        pq1 = PriorityQueue(implementation=impl)
        pq1.push(1, 4)
        pq1.push(2, 3)
        pq1.push(3, 2)
        assert pq1.peek.data == 3
        assert pq1.pop() == 3
        assert pq1.peek.data == 2
        assert pq1.pop() == 2
        assert pq1.peek.data == 1
        assert pq1.pop() == 1
        assert pq1.is_empty is True
        assert raises(IndexError, lambda: pq1.peek)
