from pydatastructs.trees.heaps import BinaryHeap
from pydatastructs.utils.misc_util import TreeNode
from pydatastructs.utils.raises_util import raises

def test_BinaryHeap():

    max_heap = BinaryHeap(heap_property="max")

    assert max_heap.extract() is None

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
    ("[(1, 100, 100, 2), (3, 19, 19, 4), "
    "(5, 36, 36, 6), (7, 17, 17, 8), "
    "(None, 3, 3, None), (None, 25, 25, None), "
    "(None, 1, 1, None), (None, 2, 2, None), (None, 7, 7, None)]")

    expected_extracted_element = max_heap.heap[0].key
    assert max_heap.extract().key == expected_extracted_element

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
    min_heap = BinaryHeap(elements = elements, heap_property="min")
    expected_extracted_element = min_heap.heap[0].key
    assert min_heap.extract().key == expected_extracted_element

    expected_sorted_elements = [2, 3, 7, 17, 19, 25, 36, 100]
    sorted_elements = [min_heap.extract().key for _ in range(8)]
    assert expected_sorted_elements == sorted_elements
