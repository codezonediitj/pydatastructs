from pydatastructs import MAryTree

def test_MAryTree():
    m = MAryTree(1, 1)
    assert str(m) == '[(1, 1)]'
