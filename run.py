from pydatastructs.trees import Redblacktree as RB
rb = RB()
rb.insert(2,1)
rb.insert(3,1)
rb.insert(0,1)
rb.insert(4,1)
print(str(rb))
rb.delete(3)
print(str(rb))
rb.delete(4)
print(str(rb))


