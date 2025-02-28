from pydatastructs.trees.heaps import BinaryHeap, TernaryHeap, BinomialHeap, DHeap
from pydatastructs.linear_data_structures.arrays import DynamicOneDimensionalArray
from pydatastructs.miscellaneous_data_structures.binomial_trees import BinomialTree
from pydatastructs.utils.misc_util import TreeNode, BinomialTreeNode
from pydatastructs.utils.raises_util import raises
from collections import deque as Queue

def test_BinaryHeap():

    max_heap = BinaryHeap(heap_property="max")

    assert raises(IndexError, lambda: max_heap.extract())

    max_heap.insert(100, 100)
    max_heap.insert(19, 19)
    max_heap.insert(36, 36)
    max_heap.insert(17, 17)
    max_heap.insert(3, 3)
    max_heap.insert(25, 25)
    max_heap.insert(1, 1)
    max_heap.insert(2, 2)
    max_heap.insert(7, 7)
    assert str(max_heap) == \
        ("[(100, 100, [1, 2]), (19, 19, [3, 4]), "
        "(36, 36, [5, 6]), (17, 17, [7, 8]), "
        "(3, 3, []), (25, 25, []), (1, 1, []), "
        "(2, 2, []), (7, 7, [])]")

    assert max_heap.extract().key == 100

    expected_sorted_elements = [36, 25, 19, 17, 7, 3, 2, 1]
    l = max_heap.heap[0].left
    l = max_heap.heap[0].right
    sorted_elements = []
    for _ in range(8):
        sorted_elements.append(max_heap.extract().key)
    assert expected_sorted_elements == sorted_elements

    elements = [
                TreeNode(7, 7), TreeNode(25, 25), TreeNode(100, 100),
                TreeNode(1, 1), TreeNode(2, 2), TreeNode(3, 3),
                TreeNode(17, 17), TreeNode(19, 19), TreeNode(36, 36)
            ]
    min_heap = BinaryHeap(elements=elements, heap_property="min")
    assert min_heap.extract().key == 1

    expected_sorted_elements = [2, 3, 7, 17, 19, 25, 36, 100]
    sorted_elements = [min_heap.extract().key for _ in range(8)]
    assert expected_sorted_elements == sorted_elements

    non_TreeNode_elements = [
                (7, 7), TreeNode(25, 25), TreeNode(100, 100),
                TreeNode(1, 1), (2, 2), TreeNode(3, 3),
                TreeNode(17, 17), TreeNode(19, 19), TreeNode(36, 36)
            ]
    assert raises(TypeError, lambda:
                BinaryHeap(elements = non_TreeNode_elements, heap_property='min'))

    non_TreeNode_elements = DynamicOneDimensionalArray(int, 0)
    non_TreeNode_elements.append(1)
    non_TreeNode_elements.append(2)
    assert raises(TypeError, lambda:
                BinaryHeap(elements = non_TreeNode_elements, heap_property='min'))

    non_heapable = "[1, 2, 3]"
    assert raises(ValueError, lambda:
                BinaryHeap(elements = non_heapable, heap_property='min'))

def test_TernaryHeap():
    max_heap = TernaryHeap(heap_property="max")
    assert raises(IndexError, lambda: max_heap.extract())
    max_heap.insert(100, 100)
    max_heap.insert(19, 19)
    max_heap.insert(36, 36)
    max_heap.insert(17, 17)
    max_heap.insert(3, 3)
    max_heap.insert(25, 25)
    max_heap.insert(1, 1)
    max_heap.insert(2, 2)
    max_heap.insert(7, 7)
    assert str(max_heap) == \
           ('[(100, 100, [1, 2, 3]), (25, 25, [4, 5, 6]), '
            '(36, 36, [7, 8]), (17, 17, []), '
            '(3, 3, []), (19, 19, []), (1, 1, []), '
            '(2, 2, []), (7, 7, [])]')

    assert max_heap.extract().key == 100

    expected_sorted_elements = [36, 25, 19, 17, 7, 3, 2, 1]
    sorted_elements = []
    for _ in range(8):
        sorted_elements.append(max_heap.extract().key)
    assert expected_sorted_elements == sorted_elements

    elements = [
        TreeNode(7, 7), TreeNode(25, 25), TreeNode(100, 100),
        TreeNode(1, 1), TreeNode(2, 2), TreeNode(3, 3),
        TreeNode(17, 17), TreeNode(19, 19), TreeNode(36, 36)
    ]
    min_heap = TernaryHeap(elements=elements, heap_property="min")
    expected_extracted_element = min_heap.heap[0].key
    assert min_heap.extract().key == expected_extracted_element

    expected_sorted_elements = [2, 3, 7, 17, 19, 25, 36, 100]
    sorted_elements = [min_heap.extract().key for _ in range(8)]
    assert expected_sorted_elements == sorted_elements

def test_DHeap():
    assert raises(ValueError, lambda: DHeap(heap_property="none", d=4))
    max_heap = DHeap(heap_property="max", d=5)
    assert raises(IndexError, lambda: max_heap.extract())
    max_heap.insert(100, 100)
    max_heap.insert(19, 19)
    max_heap.insert(36, 36)
    max_heap.insert(17, 17)
    max_heap.insert(3, 3)
    max_heap.insert(25, 25)
    max_heap.insert(1, 1)
    max_heap = DHeap(max_heap.heap, heap_property="max", d=4)
    max_heap.insert(2, 2)
    max_heap.insert(7, 7)
    assert str(max_heap) == \
           ('[(100, 100, [1, 2, 3, 4]), (25, 25, [5, 6, 7, 8]), '
           '(36, 36, []), (17, 17, []), (3, 3, []), (19, 19, []), '
           '(1, 1, []), (2, 2, []), (7, 7, [])]')

    assert max_heap.extract().key == 100

    expected_sorted_elements = [36, 25, 19, 17, 7, 3, 2, 1]
    sorted_elements = []
    for _ in range(8):
        sorted_elements.append(max_heap.extract().key)
    assert expected_sorted_elements == sorted_elements

    elements = [
        TreeNode(7, 7), TreeNode(25, 25), TreeNode(100, 100),
        TreeNode(1, 1), TreeNode(2, 2), TreeNode(3, 3),
        TreeNode(17, 17), TreeNode(19, 19), TreeNode(36, 36)
    ]
    min_heap = DHeap(elements=DynamicOneDimensionalArray(TreeNode, 9, elements), heap_property="min")
    assert min_heap.extract().key == 1

    expected_sorted_elements = [2, 3, 7, 17, 19, 25, 36, 100]
    sorted_elements = [min_heap.extract().key for _ in range(8)]
    assert expected_sorted_elements == sorted_elements

def test_BinomialHeap():

    # Corner cases
    assert raises(TypeError, lambda:
                  BinomialHeap(
                    root_list=[BinomialTreeNode(1, 1), None])
                  ) is True
    tree1 = BinomialTree(BinomialTreeNode(1, 1), 0)
    tree2 = BinomialTree(BinomialTreeNode(2, 2), 0)
    bh = BinomialHeap(root_list=[tree1, tree2])
    assert raises(TypeError, lambda:
                  bh.merge_tree(BinomialTreeNode(2, 2), None))
    assert raises(TypeError, lambda:
                  bh.merge(None))

    # Testing BinomialHeap.merge
    nodes = [BinomialTreeNode(1, 1), # 0
            BinomialTreeNode(3, 3), # 1
            BinomialTreeNode(9, 9), # 2
            BinomialTreeNode(11, 11), # 3
            BinomialTreeNode(6, 6), # 4
            BinomialTreeNode(14, 14), # 5
            BinomialTreeNode(2, 2), # 6
            BinomialTreeNode(7, 7), # 7
            BinomialTreeNode(4, 4), # 8
            BinomialTreeNode(8, 8), # 9
            BinomialTreeNode(12, 12), # 10
            BinomialTreeNode(10, 10), # 11
            BinomialTreeNode(5, 5), # 12
            BinomialTreeNode(21, 21)] # 13

    nodes[2].add_children(nodes[3])
    nodes[4].add_children(nodes[5])
    nodes[6].add_children(nodes[9], nodes[8], nodes[7])
    nodes[7].add_children(nodes[11], nodes[10])
    nodes[8].add_children(nodes[12])
    nodes[10].add_children(nodes[13])

    tree11 = BinomialTree(nodes[0], 0)
    tree12 = BinomialTree(nodes[2], 1)
    tree13 = BinomialTree(nodes[6], 3)
    tree21 = BinomialTree(nodes[1], 0)

    heap1 = BinomialHeap(root_list=[tree11, tree12, tree13])
    heap2 = BinomialHeap(root_list=[tree21])

    def bfs(heap):
        bfs_trav = []
        for i in range(len(heap.root_list)):
            layer = []
            bfs_q = Queue()
            bfs_q.append(heap.root_list[i].root)
            while len(bfs_q) != 0:
                curr_node = bfs_q.popleft()
                if curr_node is not None:
                    layer.append(curr_node.key)
                    for _i in range(curr_node.children._last_pos_filled + 1):
                        bfs_q.append(curr_node.children[_i])
            if layer != []:
                bfs_trav.append(layer)
        return bfs_trav

    heap1.merge(heap2)
    expected_bfs_trav = [[1, 3, 9, 11], [2, 8, 4, 7, 5, 10, 12, 21]]
    assert bfs(heap1) == expected_bfs_trav

    # Testing Binomial.find_minimum
    assert heap1.find_minimum().key == 1

    # Testing Binomial.delete_minimum
    heap1.delete_minimum()
    assert bfs(heap1) == [[3], [9, 11], [2, 8, 4, 7, 5, 10, 12, 21]]
    assert raises(ValueError, lambda: heap1.decrease_key(nodes[3], 15))
    heap1.decrease_key(nodes[3], 0)
    assert bfs(heap1) == [[3], [0, 9], [2, 8, 4, 7, 5, 10, 12, 21]]
    heap1.delete(nodes[12])
    assert bfs(heap1) == [[3, 8], [0, 9, 2, 7, 4, 10, 12, 21]]

    # Testing BinomialHeap.insert
    heap = BinomialHeap()
    assert raises(IndexError, lambda: heap.find_minimum())
    heap.insert(1, 1)
    heap.insert(3, 3)
    heap.insert(6, 6)
    heap.insert(9, 9)
    heap.insert(14, 14)
    heap.insert(11, 11)
    heap.insert(2, 2)
    heap.insert(7, 7)
    assert bfs(heap) == [[1, 3, 6, 2, 9, 7, 11, 14]]
