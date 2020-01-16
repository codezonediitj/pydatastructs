from pydatastructs.miscellaneous_data_structures import Queue
from pydatastructs.utils.raises_util import raises

def test_Queue():

    q = Queue(10)
    q.append(1)
    q.append(2)
    q.append(3)
    assert q.popleft() == 1
    assert q.popleft() == 2
    assert q.len() == 2
    assert q.popleft() == 3
    assert q.len() == 0
    assert q.is_empty is True
    assert raises(ValueError, lambda : q.popleft())
