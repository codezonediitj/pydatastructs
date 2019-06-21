from pydatastructs import OneDimensionalSegmentTree
from pydatastructs.utils.raises_util import raises

def test_OneDimensionalSegmentTree():
    ODST = OneDimensionalSegmentTree
    segt = ODST([(0, 5), (1, 6), (9, 13), (1, 2), (3, 8), (9, 20)])
    assert segt.cache == False
    segt.build()
    assert segt.cache == True
    assert str(segt) == \
    ("[(None, [False, -1, 0, False], None, None), (None, [True, 0, 0, True], "
    "['(None, [True, 0, 5, True], None, None)'], None), (None, [False, 0, 1, "
    "False], None, None), (None, [True, 1, 1, True], ['(None, [True, 1, 6, "
    "True], None, None)', '(None, [True, 1, 2, True], None, None)'], None), "
    "(None, [False, 1, 1, False], None, None), (None, [True, 1, 1, True], "
    "None, None), (None, [False, 1, 2, False], None, None), (None, "
    "[True, 2, 2, True], None, None), (None, [False, 2, 3, False], None, "
    "None), (None, [True, 3, 3, True], ['(None, [True, 3, 8, True], None, "
    "None)'], None), (None, [False, 3, 5, False], None, None), (None, "
    "[True, 5, 5, True], None, None), (None, [False, 5, 6, False], None, "
    "None), (None, [True, 6, 6, True], None, None), (None, [False, 6, 8, "
    "False], None, None), (None, [True, 8, 8, True], None, None), "
    "(None, [False, 8, 9, False], None, None), (None, [True, 9, 9, True], "
    "['(None, [True, 9, 13, True], None, None)', '(None, [True, 9, 20, True], "
    "None, None)'], None), (None, [False, 9, 9, False], None, None), "
    "(None, [True, 9, 9, True], None, None), (None, [False, 9, 13, False], "
    "None, None), (None, [True, 13, 13, True], None, None), (None, [False, "
    "13, 20, False], None, None), (None, [True, 20, 20, True], None, None), "
    "(0, [False, -1, 0, True], None, 1), (2, [False, 0, 1, True], None, 3), "
    "(4, [False, 1, 1, True], None, 5), (6, [False, 1, 2, True], None, 7), "
    "(8, [False, 2, 3, True], None, 9), (10, [False, 3, 5, True], None, 11), "
    "(12, [False, 5, 6, True], None, 13), (14, [False, 6, 8, True], None, 15), "
    "(16, [False, 8, 9, True], None, 17), (18, [False, 9, 9, True], None, 19), "
    "(20, [False, 9, 13, True], None, 21), (22, [False, 13, 20, True], None, "
    "23), (24, [False, -1, 1, True], None, 25), (26, [False, 1, 2, True], "
    "None, 27), (28, [False, 2, 5, True], None, 29), (30, [False, 5, 8, True], "
    "None, 31), (32, [False, 8, 9, True], None, 33), (34, [False, 9, 20, True], "
    "None, 35), (36, [False, -1, 2, True], None, 37), (38, [False, 2, 8, True], "
    "None, 39), (40, [False, 8, 20, True], None, 41), (None, [False, 20, 21, "
    "False], None, None), (42, [False, -1, 8, True], None, 43), (44, [False, "
    "8, 21, False], None, 45), (-3, [False, -1, 21, False], None, -2)]")
    segt2 = ODST([(1, 4)])
    assert str(segt2) ==  ("[(None, [False, 0, 1, False], None, None), "
    "(None, [True, 1, 1, True], ['(None, [True, 1, 4, True], None, None)'], "
    "None), (None, [False, 1, 4, False], None, None), (None, [True, 4, 4, True], "
    "None, None), (0, [False, 0, 1, True], None, 1), (2, [False, 1, 4, True], "
    "None, 3), (4, [False, 0, 4, True], None, 5), (None, [False, 4, 5, False], "
    "None, None), (-3, [False, 0, 5, False], None, -2)]")
    raises(ValueError, lambda: ODST([(1, 2, 3)]))
