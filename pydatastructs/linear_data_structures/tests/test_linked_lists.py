from pydatastructs.linear_data_structures import DoublyLinkedList, SinglyLinkedList, SinglyCircularLinkedList, DoublyCircularLinkedList, SkipList
from pydatastructs.utils.raises_util import raises
import copy, random

def test_DoublyLinkedList():
    random.seed(1000)
    dll = DoublyLinkedList()
    assert raises(IndexError, lambda: dll[2])
    dll.appendleft(5)
    dll.append(1)
    dll.appendleft(2)
    dll.append(3)
    dll.insert_after(dll[-1], 4)
    dll.insert_after(dll[2], 6)
    dll.insert_before(dll[4], 1.1)
    dll.insert_before(dll[0], 7)
    dll.insert_at(0, 2)
    dll.insert_at(-1, 9)
    dll.extract(2)
    assert dll.popleft().key == 2
    assert dll.popright().key == 4
    assert dll.search(3) == dll[-2]
    assert dll.search(-1) is None
    dll[-2].key = 0
    assert str(dll) == ("['(7, None)', '(5, None)', '(1, None)', "
                        "'(6, None)', '(1.1, None)', '(0, None)', "
                        "'(9, None)']")
    assert len(dll) == 7
    assert raises(IndexError, lambda: dll.insert_at(8, None))
    assert raises(IndexError, lambda: dll.extract(20))
    dll_copy = DoublyCircularLinkedList()
    for i in range(dll.size):
        dll_copy.append(dll[i])
    for i in range(len(dll)):
        if i%2 == 0:
            dll.popleft()
        else:
            dll.popright()
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
    sll.appendleft(5)
    sll.append(1)
    sll.appendleft(2)
    sll.append(3)
    sll.insert_after(sll[1], 4)
    sll.insert_after(sll[-1], 6)
    sll.insert_at(0, 2)
    sll.insert_at(-1, 9)
    sll.extract(2)
    assert sll.popleft().key == 2
    assert sll.popright().key == 6
    sll[-2].key = 0
    assert str(sll) == ("['(2, None)', '(4, None)', '(1, None)', "
                        "'(0, None)', '(9, None)']")
    assert len(sll) == 5
    assert raises(IndexError, lambda: sll.insert_at(6, None))
    assert raises(IndexError, lambda: sll.extract(20))
    sll_copy = DoublyCircularLinkedList()
    for i in range(sll.size):
        sll_copy.append(sll[i])
    for i in range(len(sll)):
        if i%2 == 0:
            sll.popleft()
        else:
            sll.popright()
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
    scll.appendleft(5)
    scll.append(1)
    scll.appendleft(2)
    scll.append(3)
    scll.insert_after(scll[1], 4)
    scll.insert_after(scll[-1], 6)
    scll.insert_at(0, 2)
    scll.insert_at(-1, 9)
    scll.extract(2)
    assert scll.popleft().key == 2
    assert scll.popright().key == 6
    assert scll.search(-1) is None
    scll[-2].key = 0
    assert str(scll) == ("['(2, None)', '(4, None)', '(1, None)', "
                         "'(0, None)', '(9, None)']")
    assert len(scll) == 5
    assert raises(IndexError, lambda: scll.insert_at(6, None))
    assert raises(IndexError, lambda: scll.extract(20))
    scll_copy = DoublyCircularLinkedList()
    for i in range(scll.size):
        scll_copy.append(scll[i])
    for i in range(len(scll)):
        if i%2 == 0:
            scll.popleft()
        else:
            scll.popright()
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
    dcll.appendleft(5)
    dcll.append(1)
    dcll.appendleft(2)
    dcll.append(3)
    dcll.insert_after(dcll[-1], 4)
    dcll.insert_after(dcll[2], 6)
    dcll.insert_before(dcll[4], 1)
    dcll.insert_before(dcll[0], 7)
    dcll.insert_at(0, 2)
    dcll.insert_at(-1, 9)
    dcll.extract(2)
    assert dcll.popleft().key == 2
    assert dcll.popright().key == 4
    dcll[-2].key = 0
    assert str(dcll) == ("['(7, None)', '(5, None)', '(1, None)', "
                         "'(6, None)', '(1, None)', '(0, None)', "
                         "'(9, None)']")
    assert len(dcll) == 7
    assert raises(IndexError, lambda: dcll.insert_at(8, None))
    assert raises(IndexError, lambda: dcll.extract(20))
    dcll_copy = DoublyCircularLinkedList()
    for i in range(dcll.size):
        dcll_copy.append(dcll[i])
    for i in range(len(dcll)):
        if i%2 == 0:
            dcll.popleft()
        else:
            dcll.popright()
    assert str(dcll) == "[]"
    for _ in range(len(dcll_copy)):
        index = random.randint(0, len(dcll_copy) - 1)
        dcll_copy.extract(index)
    assert str(dcll_copy) == "[]"
    assert raises(ValueError, lambda: dcll_copy.extract(1))

def test_SkipList():
    random.seed(0)
    sl = SkipList()
    sl.insert(2)
    sl.insert(10)
    sl.insert(92)
    sl.insert(1)
    sl.insert(4)
    sl.insert(27)
    sl.extract(10)
    assert str(sl) == ("(1, None) None None None None \n"
                       "(1, None) None None None None \n"
                       "(1, None) (2, None) (4, None) (27, None) (92, None) \n")
    assert raises(KeyError, lambda: sl.extract(15))
    assert sl.search(1) is True
    assert sl.search(47) is False

    sl = SkipList()

    for a in range(0, 20, 2):
        sl.insert(a)
    assert sl.search(16) is True
    for a in range(4, 20, 4):
        sl.extract(a)
    assert sl.search(10) is True
    for a in range(4, 20, 4):
        sl.insert(a)
    for a in range(0, 20, 2):
        sl.extract(a)
    assert sl.search(3) is False

    li = SkipList()
    li.insert(1)
    li.insert(2)
    assert li.levels == 1
    assert li.size == 2

def test_DoublyLinkedList_XOR():
    """
    Test XOR-based doubly linked list implementation.
    Tests should produce the same results as standard mode.
    """
    random.seed(1000)

    # Test basic operations
    dll_xor = DoublyLinkedList(mode='xor')
    assert raises(IndexError, lambda: dll_xor[2])

    # Test append and appendleft
    dll_xor.appendleft(5)
    dll_xor.append(1)
    dll_xor.appendleft(2)
    dll_xor.append(3)

    # Test insert_after
    dll_xor.insert_after(dll_xor[-1], 4)
    dll_xor.insert_after(dll_xor[2], 6)

    # Test insert_before
    dll_xor.insert_before(dll_xor[4], 1.1)
    dll_xor.insert_before(dll_xor[0], 7)

    # Test insert_at
    dll_xor.insert_at(0, 2)
    dll_xor.insert_at(-1, 9)

    # Test extract
    dll_xor.extract(2)

    # Test popleft and popright
    assert dll_xor.popleft().key == 2
    assert dll_xor.popright().key == 4

    # Test search
    assert dll_xor.search(3) == dll_xor[-2]
    assert dll_xor.search(-1) is None

    # Test key modification
    dll_xor[-2].key = 0

    # Verify final state
    assert str(dll_xor) == ("['(7, None)', '(5, None)', '(1, None)', "
                            "'(6, None)', '(1.1, None)', '(0, None)', "
                            "'(9, None)']")
    assert len(dll_xor) == 7

    # Test error cases
    assert raises(IndexError, lambda: dll_xor.insert_at(8, None))
    assert raises(IndexError, lambda: dll_xor.extract(20))

    # Test complete extraction
    for i in range(len(dll_xor)):
        if i % 2 == 0:
            dll_xor.popleft()
        else:
            dll_xor.popright()
    assert str(dll_xor) == "[]"
    assert raises(ValueError, lambda: dll_xor.extract(1))

def test_DoublyLinkedList_XOR_vs_Standard():
    """
    Compare XOR mode behavior with standard mode to ensure consistency.
    """
    # Create both types
    dll_std = DoublyLinkedList(mode='standard')
    dll_xor = DoublyLinkedList(mode='xor')

    # Perform identical operations
    operations = [
        ('append', 10),
        ('append', 20),
        ('append', 30),
        ('appendleft', 5),
        ('appendleft', 1),
    ]

    for op, val in operations:
        getattr(dll_std, op)(val)
        getattr(dll_xor, op)(val)

    # Verify both produce same string representation
    assert str(dll_std) == str(dll_xor)
    assert len(dll_std) == len(dll_xor)

    # Test element access
    for i in range(len(dll_std)):
        assert dll_std[i].key == dll_xor[i].key

    # Test extraction
    extracted_std = dll_std.extract(2)
    extracted_xor = dll_xor.extract(2)
    assert extracted_std.key == extracted_xor.key
    assert str(dll_std) == str(dll_xor)

def test_DoublyLinkedList_XOR_EdgeCases():
    """
    Test edge cases for XOR mode.
    """
    # Test single element
    dll = DoublyLinkedList(mode='xor')
    dll.append(42)
    assert dll[0].key == 42
    assert dll.head.key == 42
    assert dll.tail.key == 42
    assert len(dll) == 1

    # Test extract single element
    node = dll.extract(0)
    assert node.key == 42
    assert len(dll) == 0
    assert dll.head is None
    assert dll.tail is None

    # Test two elements
    dll.append(1)
    dll.append(2)
    assert dll[0].key == 1
    assert dll[1].key == 2

    # Test insert at beginning
    dll.insert_at(0, 0)
    assert dll[0].key == 0
    assert dll[1].key == 1
    assert dll[2].key == 2

    # Test insert at end
    dll.insert_at(3, 3)
    assert dll[3].key == 3

    # Test insert in middle
    dll.insert_at(2, 1.5)
    assert dll[2].key == 1.5

    # Verify integrity
    assert len(dll) == 5
    keys = [dll[i].key for i in range(len(dll))]
    assert keys == [0, 1, 1.5, 2, 3]

def test_DoublyLinkedList_InvalidMode():
    """
    Test that invalid mode raises ValueError.
    """
    assert raises(ValueError, lambda: DoublyLinkedList(mode='invalid'))
