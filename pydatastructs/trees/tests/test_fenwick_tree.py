from pydatastructs.trees import FenwickTree
from pydatastructs.utils.raises_util import raises
from copy import deepcopy
def test_FenwickTree():
    FT = FenwickTree
    t = FT([1,2,3,4,5,6,7,8,9,10])
    assert t.get_sum(0,2) == 6
    assert t.get_sum(0,4) == 15
    assert t.get_sum(0,9) == 55
    t.update(0,100)
    assert t.get_sum(0,2) == 105
    assert t.get_sum(0,4) == 114
    assert t.get_sum(0,9) == 154
