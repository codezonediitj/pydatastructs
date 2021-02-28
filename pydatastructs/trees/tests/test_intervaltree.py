from pydatastructs.trees.intervaltree import (Node, IntervalTree)

def test_IntervalTree():
    it = IntervalTree(Node([15, 20]))
    it.addNode(Node([10, 30]))
    it.addNode(Node([17, 19]))
    it.addNode(Node([5, 20]))
    it.addNode(Node([12, 15]))
    it.addNode(Node([30, 40]))
    it.constructMax()
    # Explicit check for the printTree() method of IntervalTree Class
    assert it.printTree() == [([15, 20], 40), ([10, 30], 30), ([17, 19], 40), ([5, 20], 20), ([12, 15], 15), ([30, 40], 40)]
    p_node, c_node, ret = it.searchIntervalOverlap([6, 7])
    assert p_node.interval == [10, 30]
    assert c_node.interval == [5, 20]
    assert ret is True
    p_node, c_node, ret = it.searchIntervalOverlap([-1, -2])
    assert p_node is None
    assert c_node is None
    assert ret is False
    assert it.delete_node([9, 11]) is None
    assert it.printTree() == [([15, 20], 40), ([5, 20], 20), ([17, 19], 40), ([12, 15], 15), ([30, 40], 40)]
