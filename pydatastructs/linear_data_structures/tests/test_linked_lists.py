from pydatastructs.linear_data_structures import DoublyLinkedList, SinglyLinkedList, SinglyCircularLinkedList, DoublyCircularLinkedList, SkipList
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
    assert dll.pop_left().data == 2
    assert dll.pop_right().data == 4
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
    assert sll.pop_left().data == 2
    assert sll.pop_right().data == 6
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
    assert scll.pop_left().data == 2
    assert scll.pop_right().data == 6
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
    assert dcll.pop_left().data == 2
    assert dcll.pop_right().data == 4
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

def test_SkipList():

    def test_insert():
        skip_list = SkipList()
        skip_list.insert("Key1", 3)
        skip_list.insert("Key2", 12)
        skip_list.insert("Key3", 41)
        skip_list.insert("Key4", -19)

        node = skip_list.head
        all_values = {}
        while node.level != 0:
            node = node.forward[0]
            all_values[node.key] = node.value

        assert len(skip_list) == 4
        assert len(all_values) == 4
        assert all_values["Key1"] == 3
        assert all_values["Key2"] == 12
        assert all_values["Key3"] == 41
        assert all_values["Key4"] == -19


    def test_insert_overrides_existing_value():
        skip_list = SkipList()
        skip_list.insert("Key1", 10)
        skip_list.insert("Key1", 12)

        skip_list.insert("Key5", 7)
        skip_list.insert("Key7", 10)
        skip_list.insert("Key10", 5)

        skip_list.insert("Key7", 7)
        skip_list.insert("Key5", 5)
        skip_list.insert("Key10", 10)

        node = skip_list.head
        all_values = dict()
        while node.level != 0:
            node = node.forward[0]
            all_values[node.key] = node.value

        assert len(all_values) == 4
        assert all_values["Key1"] == 12
        assert all_values["Key7"] == 7
        assert all_values["Key5"] == 5
        assert all_values["Key10"] == 10


    def test_searching_empty_list_returns_none():
        skip_list = SkipList()
        assert skip_list.find("Some key") is None


    def test_search():
        skip_list = SkipList()

        skip_list.insert("Key2", 20)
        assert skip_list.find("Key2") == 20

        skip_list.insert("Some Key", 10)
        skip_list.insert("Key2", 8)
        skip_list.insert("V", 13)

        assert skip_list.find("Y") is None
        assert skip_list.find("Key2") == 8
        assert skip_list.find("Some Key") == 10
        assert skip_list.find("V") == 13


    def test_deleting_item_from_empty_list_do_nothing():
        skip_list = SkipList()
        skip_list.delete("Some key")

        assert len(skip_list.head.forward) == 0


    def test_deleted_items_are_not_founded_by_find_method():
        skip_list = SkipList()

        skip_list.insert("Key1", 12)
        skip_list.insert("V", 13)
        skip_list.insert("X", 14)
        skip_list.insert("Key2", 15)

        skip_list.delete("V")
        skip_list.delete("Key2")

        assert skip_list.find("V") is None
        assert skip_list.find("Key2") is None


    def test_delete_removes_only_given_key():
        skip_list = SkipList()

        skip_list.insert("Key1", 12)
        skip_list.insert("V", 13)
        skip_list.insert("X", 14)
        skip_list.insert("Key2", 15)

        skip_list.delete("V")
        assert len(skip_list) == 3
        assert skip_list.find("V") is None
        assert skip_list.find("X") == 14
        assert skip_list.find("Key1") == 12
        assert skip_list.find("Key2") == 15

        skip_list.delete("X")
        assert len(skip_list) == 2
        assert skip_list.find("V") is None
        assert skip_list.find("X") is None
        assert skip_list.find("Key1") == 12
        assert skip_list.find("Key2") == 15

        skip_list.delete("Key1")
        assert skip_list.find("V") is None
        assert skip_list.find("X") is None
        assert skip_list.find("Key1") is None
        assert skip_list.find("Key2") == 15

        skip_list.delete("Key2")
        assert skip_list.find("V") is None
        assert skip_list.find("X") is None
        assert skip_list.find("Key1") is None
        assert skip_list.find("Key2") is None


    def test_delete_doesnt_leave_dead_nodes():
        skip_list = SkipList()

        skip_list.insert("Key1", 12)
        skip_list.insert("V", 13)
        skip_list.insert("X", 142)
        skip_list.insert("Key2", 15)

        skip_list.delete("X")

        def traverse_keys(node):
            yield node.key
            for forward_node in node.forward:
                yield from traverse_keys(forward_node)

        x = len(set(traverse_keys(skip_list.head)))
        assert x == 4

    def test_iter_always_yields_sorted_values():
        def is_sorted(lst):
            for item, next_item in zip(lst, lst[1:]):
                if next_item < item:
                    return False
            return True

        skip_list = SkipList()
        for i in range(10):
            skip_list.insert(i, i)
        assert is_sorted(list(skip_list))
        skip_list.delete(5)
        skip_list.delete(8)
        skip_list.delete(2)
        assert is_sorted(list(skip_list))
        skip_list.insert(-12, -12)
        skip_list.insert(77, 77)
        assert is_sorted(list(skip_list))

    for i in range(100):
        test_insert()
        test_insert_overrides_existing_value()

        test_searching_empty_list_returns_none()
        test_search()

        test_deleting_item_from_empty_list_do_nothing()
        test_deleted_items_are_not_founded_by_find_method()
        test_delete_removes_only_given_key()
        test_delete_doesnt_leave_dead_nodes()

        test_iter_always_yields_sorted_values()
