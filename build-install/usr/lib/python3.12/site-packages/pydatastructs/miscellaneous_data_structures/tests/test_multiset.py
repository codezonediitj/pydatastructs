from pydatastructs.miscellaneous_data_structures import Multiset

def test_Multiset():

    ms = Multiset()
    ms.add(5)
    ms.add(5)
    ms.add(3)
    ms.add(7)
    assert len(ms) == 4
    assert 5 in ms
    assert ms.count(5) == 2
    assert ms.count(3) == 1
    assert ms.count(-3) == 0
    assert not 4 in ms
    ms.remove(5)
    assert 5 in ms
    assert ms.lower_bound(5) == 5
    assert ms.upper_bound(5) == 7

    ms = Multiset(5, 3, 7, 2)

    assert len(ms) == 4
    assert 5 in ms
    assert ms.count(7) == 1
    assert not 4 in ms
    assert ms.lower_bound(3) == 3
    assert ms.upper_bound(3) == 5
    assert ms.upper_bound(7) is None

    ms.remove(5)

    assert len(ms) == 3
    assert not 5 in ms

    ms.add(4)

    assert 4 in ms
    assert len(ms) == 4
