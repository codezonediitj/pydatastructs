from pydatastructs.linear_data_structures import DoublyLinkedList, SinglyLinkedList, SinglyCircularLinkedList, DoublyCircularLinkedList
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

def test_SinglyCircularLinkedList():
    random.seed(1000)
    scll = SinglyCircularLinkedList()
    assert raises(IndexError, lambda: scll[2])
    scll.append_left(5)
    scll.append(1)
    scll.append_left(2)
    scll.append(3)
    scll.insert_after(scll[1], 4)
    scll.insert_after(scll[-1], 6)
    scll.insert_at(0, 2)
    scll.insert_at(-1, 9)
    scll.extract(2)
    scll.extract(0)
    scll.extract(-1)
    scll[-2].data = 0
    assert str(scll) == "[2, 4, 1, 0, 9]"
    assert len(scll) == 5
    assert raises(IndexError, lambda: scll.insert_at(6, None))
    assert raises(IndexError, lambda: scll.extract(20))
    scll_copy = copy.deepcopy(scll)
    for i in range(len(scll)):
        if i%2 == 0:
            scll.pop_left()
        else:
            scll.pop_right()
    assert str(scll) == "[]"
    for _ in range(len(scll_copy)):
        index = random.randint(0, len(scll_copy) - 1)
        scll_copy.extract(index)
    assert str(scll_copy) == "[]"
    assert raises(ValueError, lambda: scll_copy.extract(1))

def test_DoublyCircularLinkedList():
    random.seed(1000)
    dcll = DoublyCircularLinkedList()
    assert raises(IndexError, lambda: dcll[2])
    dcll.append_left(5)
    dcll.append(1)
    dcll.append_left(2)
    dcll.append(3)
    dcll.insert_after(dcll[-1], 4)
    dcll.insert_after(dcll[2], 6)
    dcll.insert_before(dcll[4], 1)
    dcll.insert_before(dcll[0], 7)
    dcll.insert_at(0, 2)
    dcll.insert_at(-1, 9)
    dcll.extract(2)
    dcll.extract(0)
    dcll.extract(-1)
    dcll[-2].data = 0
    assert str(dcll) == "[7, 5, 1, 6, 1, 0, 9]"
    assert len(dcll) == 7
    assert raises(IndexError, lambda: dcll.insert_at(8, None))
    assert raises(IndexError, lambda: dcll.extract(20))
    dcll_copy = copy.deepcopy(dcll)
    for i in range(len(dcll)):
        if i%2 == 0:
            dcll.pop_left()
        else:
            dcll.pop_right()
    assert str(dcll) == "[]"
    for _ in range(len(dcll_copy)):
        index = random.randint(0, len(dcll_copy) - 1)
        dcll_copy.extract(index)
    assert str(dcll_copy) == "[]"
    assert raises(ValueError, lambda: dcll_copy.extract(1))
