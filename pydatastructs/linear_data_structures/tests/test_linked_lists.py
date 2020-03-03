from pydatastructs.linear_data_structures import DoublyLinkedList, SinglyLinkedList
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
    dll.insert_after(dll[-1], 4)
    dll.insert_after(dll[2], 6)
    dll.insert_before(dll[4], 1)
    dll.insert_before(dll[0], 7)
    dll.insert_at(0, 2)
    dll.insert_at(-1, 9)
    dll.extract(2)
    dll.extract(0)
    dll.extract(-1)
    dll[-2].data = 0
    assert str(dll) == "[7, 5, 1, 6, 1, 0, 9]"
    assert len(dll) == 7
    assert raises(IndexError, lambda: dll.insert_at(8, None))
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

def test_SinglyLinkedList():
    random.seed(1000)
    sll = SinglyLinkedList()
    assert raises(IndexError, lambda: sll[2])
    sll.append_left(5)
    sll.append(1)
    sll.append_left(2)
    sll.append(3)
    sll.insert_after(sll[1], 4)
    sll.insert_after(sll[-1], 6)
    sll.insert_at(0, 2)
    sll.insert_at(-1, 9)
    sll.extract(2)
    sll.extract(0)
    sll.extract(-1)
    sll[-2].data = 0
    assert str(sll) == "[2, 4, 1, 0, 9]"
    assert len(sll) == 5
    assert raises(IndexError, lambda: sll.insert_at(6, None))
    assert raises(IndexError, lambda: sll.extract(20))
    sll_copy = copy.deepcopy(sll)
    for i in range(len(sll)):
        if i%2 == 0:
            sll.pop_left()
        else:
            sll.pop_right()
    assert str(sll) == "[]"
    for _ in range(len(sll_copy)):
        index = random.randint(0, len(sll_copy) - 1)
        sll_copy.extract(index)
    assert str(sll_copy) == "[]"
    assert raises(ValueError, lambda: sll_copy.extract(1))
