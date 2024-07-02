from pydatastructs.linear_data_structures import (
    OneDimensionalArray, DynamicOneDimensionalArray,
    MultiDimensionalArray, ArrayForTrees)
from pydatastructs.utils.misc_util import Backend
from pydatastructs.utils.raises_util import raises
from pydatastructs.utils import TreeNode
from pydatastructs.utils._backend.cpp import _nodes

def test_OneDimensionalArray():
    ODA = OneDimensionalArray
    A = ODA(int, 5, [1.0, 2, 3, 4, 5], init=6)
    A[1] = 2.0
    assert str(A) == '[1, 2, 3, 4, 5]'
    assert A
    assert ODA(int, [1.0, 2, 3, 4, 5], 5)
    assert ODA(int, 5)
    assert ODA(int, [1.0, 2, 3])
    assert raises(IndexError, lambda: A[7])
    assert raises(IndexError, lambda: A[-1])
    assert raises(ValueError, lambda: ODA())
    assert raises(ValueError, lambda: ODA(int, 1, 2, 3))
    assert raises(TypeError, lambda: ODA(int, 5.0, set([1, 2, 3])))
    assert raises(TypeError, lambda: ODA(int, 5.0))
    assert raises(TypeError, lambda: ODA(int, set([1, 2, 3])))
    assert raises(ValueError, lambda: ODA(int, 3, [1]))

    A = ODA(int, 5, [1, 2, 3, 4, 5], init=6, backend=Backend.CPP)
    A[1] = 2
    assert str(A) == "['1', '2', '3', '4', '5']"
    assert A
    assert ODA(int, [1, 2, 3, 4, 5], 5, backend=Backend.CPP)
    assert ODA(int, 5, backend=Backend.CPP)
    assert ODA(int, [1, 2, 3], backend=Backend.CPP)
    assert raises(TypeError, lambda: ODA(int, [1.0, 2, 3, 4, 5], 5, backend=Backend.CPP))
    assert raises(TypeError, lambda: ODA(int, [1.0, 2, 3], backend=Backend.CPP))
    assert raises(IndexError, lambda: A[7])
    assert raises(IndexError, lambda: A[-1])
    assert raises(ValueError, lambda: ODA(backend=Backend.CPP))
    assert raises(ValueError, lambda: ODA(int, 1, 2, 3, backend=Backend.CPP))
    assert raises(TypeError, lambda: ODA(int, 5.0, set([1, 2, 3]), backend=Backend.CPP))
    assert raises(TypeError, lambda: ODA(int, 5.0, backend=Backend.CPP))
    assert raises(TypeError, lambda: ODA(int, set([1, 2, 3]), backend=Backend.CPP))
    assert raises(ValueError, lambda: ODA(int, 3, [1], backend=Backend.CPP))
    assert raises(ValueError, lambda: ODA(int, 3, [1], backend=Backend.CPP))
    assert raises(TypeError, lambda: A.fill(2.0))


def test_MultiDimensionalArray():
    assert raises(ValueError, lambda: MultiDimensionalArray(int, 2, -1, 3))
    assert MultiDimensionalArray(int, 10).shape == (10,)
    array = MultiDimensionalArray(int, 5, 9, 3, 8)
    assert array.shape == (5, 9, 3, 8)
    array.fill(5)
    array[1, 3, 2, 5] = 2.0
    assert array
    assert array[1, 3, 2, 5] == 2.0
    assert array[1, 3, 0, 5] == 5
    assert array[1, 2, 2, 5] == 5
    assert array[2, 3, 2, 5] == 5
    assert raises(IndexError, lambda: array[5])
    assert raises(IndexError, lambda: array[4, 10])
    assert raises(IndexError, lambda: array[-1])
    assert raises(IndexError, lambda: array[2, 3, 2, 8])
    assert raises(ValueError, lambda: MultiDimensionalArray())
    assert raises(ValueError, lambda: MultiDimensionalArray(int))
    assert raises(TypeError, lambda: MultiDimensionalArray(int, 5, 6, ""))
    array = MultiDimensionalArray(int, 3, 2, 2)
    array.fill(1)
    array[0, 0, 0] = 0
    array[0, 0, 1] = 0
    array[1, 0, 0] = 0
    array[2, 1, 1] = 0
    assert str(array) == '[0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0]'
    array = MultiDimensionalArray(int, 4)
    assert array.shape == (4,)
    array.fill(5)
    array[3] = 3
    assert array[3] == 3

def test_DynamicOneDimensionalArray():
    DODA = DynamicOneDimensionalArray
    A = DODA(int, 0)
    A.append(1)
    A.append(2)
    A.append(3)
    A.append(4)
    assert str(A) == "['1', '2', '3', '4']"
    A.delete(0)
    A.delete(0)
    A.delete(15)
    A.delete(-1)
    A.delete(1)
    A.delete(2)
    assert A._data == [4, None, None]
    assert str(A) == "['4']"
    assert A.size == 3
    A.fill(4)
    assert A._data == [4, 4, 4]
    b = DynamicOneDimensionalArray(int, 0)
    b.append(1)
    b.append(2)
    b.append(3)
    b.append(4)
    b.append(5)
    assert b._data == [1, 2, 3, 4, 5, None, None]
    assert list(reversed(b)) == [5, 4, 3, 2, 1]

    A = DODA(int, 0, backend=Backend.CPP)
    A.append(1)
    A.append(2)
    A.append(3)
    A.append(4)
    assert str(A) == "['1', '2', '3', '4']"
    A.delete(0)
    A.delete(0)
    A.delete(15)
    A.delete(-1)
    A.delete(1)
    A.delete(2)
    assert [A[i] for i in range(A.size)] == [4, None, None]
    assert A.size == 3
    A.fill(4)
    assert [A[0], A[1], A[2]] == [4, 4, 4]
    b = DODA(int, 0, backend=Backend.CPP)
    b.append(1)
    b.append(2)
    b.append(3)
    b.append(4)
    b.append(5)
    assert [b[i] for i in range(b.size)] == [1, 2, 3, 4, 5, None, None]

def test_DynamicOneDimensionalArray2():
    DODA = DynamicOneDimensionalArray
    root = TreeNode(1, 100)
    A = DODA(TreeNode, [root])
    assert str(A[0]) == "(None, 1, 100, None)"

def _test_ArrayForTrees(backend):
    AFT = ArrayForTrees
    root = TreeNode(1, 100,backend=backend)
    if backend==Backend.PYTHON:
        A = AFT(TreeNode, [root], backend=backend)
        B = AFT(TreeNode, 0, backend=backend)
    else:
        A = AFT(_nodes.TreeNode, [root], backend=backend)
        B = AFT(_nodes.TreeNode, 0, backend=backend)
    assert str(A) == "['(None, 1, 100, None)']"
    node = TreeNode(2, 200, backend=backend)
    A.append(node)
    assert str(A) == "['(None, 1, 100, None)', '(None, 2, 200, None)']"
    assert str(B) == "[]"

def test_ArrayForTrees():
    _test_ArrayForTrees(Backend.PYTHON)

def test_cpp_ArrayForTrees():
    _test_ArrayForTrees(Backend.CPP)
