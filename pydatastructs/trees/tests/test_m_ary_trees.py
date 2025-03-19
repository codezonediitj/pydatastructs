from pydatastructs import MAryTree
from pydatastructs.trees.m_ary_trees import ParentPointerTree

def test_MAryTree():
    m = MAryTree(1, 1)
    assert str(m) == '[(1, 1)]'

def test_ParentPointerTree(): 
    pass