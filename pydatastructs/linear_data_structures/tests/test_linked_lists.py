from pydatastructs.linear_data_structures import DoublyLinkedList
from pydatastructs.utils.raises_util import raises
import copy, random

def test_DoublyLinkedList():
    random.seed(1000)
    dll = DoublyLinkedList()
    assert raises(IndexError, lambda: dll[2])
    dll.append_left(5)
    dll.append(1)
    dll.append_left(2)
    dll.append(3)
    dll.insert_after(dll[1], 4)
    dll.insert_after(dll[-1], 6)
    dll.insert_before(dll[0], 1)
    dll.insert_at(0, 2)
    dll.insert_at(-1, 9)
    dll.extract(2)
    dll.extract(0)
    dll.extract(-1)
    dll[-2].data = 0
    assert str(dll) == "[1, 5, 4, 1, 0, 9]"
    assert len(dll) == 6
    assert raises(IndexError, lambda: dll.insert_at(7, None))
    assert raises(IndexError, lambda: dll.extract(20))
    dll_copy = copy.deepcopy(dll)
    for i in range(len(dll)):
        if i%2 == 0:
            dll.pop_left()
        else:
            dll.pop_right()
    assert str(dll) == "[]"
    for _ in range(len(dll_copy)):
        index = random.randint(0, len(dll_copy) - 1)
        dll_copy.extract(index)
    assert str(dll_copy) == "[]"
    assert raises(ValueError, lambda: dll_copy.extract(1))
