from pydatastructs.miscellaneous_data_structures import Queue
from pydatastructs.utils.raises_util import raises

def test_Queue():

    q = Queue()
    q.push(1)
    q.push(2)
    q.push(3)
    assert q.popleft() == 1
    assert q.popleft() == 2
    assert q.len() == 2
    assert q.popleft() == 3
    assert q.len() == 0
    assert q.is_empty is True
    assert raises(ValueError, lambda : q.popleft())
