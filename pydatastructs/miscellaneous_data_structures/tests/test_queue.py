from pydatastructs.miscellaneous_data_structures import Queue
from pydatastructs.utils.raises_util import raises

def test_Queue():

    q = Queue(10)
    q.append(1)
    q.append(2)
    q.append(3)
    assert q.popleft()
    assert q.popleft()
    assert print(q.len()) == 1
    assert q.append()
    assert print(q.len()) == 2
