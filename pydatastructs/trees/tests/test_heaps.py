from pydatastructs.trees.heaps import BinaryHeap as BH

def test_minheap():
    testminHeap = BH(_type='min')
    
    assert testminHeap.extract() == "Nothing to extract!"
    
    testminHeap.insert(111)
    testminHeap.insert(1111)
    testminHeap.insert(11)
    testminHeap.insert(1)
    testminHeap.insert(-1)
    testminHeap.insert(-11)
    
    assert testminHeap.extract() == -11
    assert testminHeap.extract() == -1
    
    testminHeap.extract()
    
    assert testminHeap.extract() == 11
    
    testminHeap.insert(1)
    testminHeap.insert(2)
    testminHeap.insert(3)
    testminHeap.insert(4)
    
    assert testminHeap.extract() == 1
    
    
    
def test_maxheap():
    testmaxHeap = BH(_type='max')
    
    assert testmaxHeap.extract() == "Nothing to extract!"

    
    testmaxHeap.insert(111)
    testmaxHeap.insert(1111)
    testmaxHeap.insert(11)
    testmaxHeap.insert(1)
    testmaxHeap.insert(-1)
    testmaxHeap.insert(-11)
    testmaxHeap.insert(11111)
    
    assert testmaxHeap.extract() == 11111
    assert testmaxHeap.extract() == 1111
    assert testmaxHeap.extract() == 111
    
    testmaxHeap.extract()
    
    assert testmaxHeap.extract() == 1
    
    testmaxHeap.insert(1)
    testmaxHeap.insert(2)
    testmaxHeap.insert(3)
    testmaxHeap.insert(4)
    
    assert testmaxHeap.extract() == 4
    
test_minheap()
test_maxheap()
     