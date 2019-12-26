from pydatastructs import OneDimensionalSegmentTree
from pydatastructs.utils.raises_util import raises

def test_OneDimensionalSegmentTree():
    ODST = OneDimensionalSegmentTree
    segt = ODST([(0, 5), (1, 6), (9, 13), (1, 2), (3, 8), (9, 20)])
    assert segt.cache is False
    segt2 = ODST([(1, 4)])
    assert str(segt2) == ("[(None, [False, 0, 1, False], None, None), "
    "(None, [True, 1, 1, True], ['(None, [True, 1, 4, True], None, None)'], "
    "None), (None, [False, 1, 4, False], None, None), (None, [True, 4, 4, True], "
    "None, None), (0, [False, 0, 1, True], None, 1), (2, [False, 1, 4, True], "
    "['(None, [True, 1, 4, True], None, None)'], 3), (4, [False, 0, 4, True], "
    "None, 5), (None, [False, 4, 5, False], None, None), (-3, [False, 0, 5, "
    "False], None, -2)]")
    assert len(segt.query(1.5)) == 3
    assert segt.cache is True
    assert len(segt.query(-1)) == 0
    assert len(segt.query(2.8)) == 2
    assert raises(ValueError, lambda: ODST([(1, 2, 3)]))
