import random
from segmentTree import SegmentTree


def genRange(listSize) :

    left = random.randint(0, listSize - 1)
    right = random.randint(left, listSize - 1)

    return left, right


def genQueryType() :

    return random.randint(1, 3)


for _ in range(10) :

    listSmall = [random.randint(-50, 50) for i in range(10)]
    # listLarge = [random.randint(-10 ** 6, 10 ** 6) for i in range(10 ** 4)]

    treeSmall = SegmentTree(listSmall)
    # treeLarge = SegmentTree(listLarge)

    print("Initial List :", listSmall)
    print()

    for queries in range(100) :

        query = genQueryType()

        if query == 1 :

            l, r = genRange(len(listSmall))
            print("Range Query", [l, r], " = ", treeSmall.rangeQuery(l, r))

            # l, r = genRange(len(listLarge))
            # print(treeLarge.rangeQuery(l, r))

        elif query == 2 :

            val = random.randint(-50, 50)

            posSmall = random.randint(0, len(listSmall) - 1)
            # posLarge = random.randint(0, len(listLarge) - 1)

            treeSmall.pointUpdate(posSmall, val)
            # treeLarge.pointUpdate(posLarge, val)

            print("Point Update", [posSmall, val])

        else :

            val = random.randint(-50, 50)

            l, r = genRange(len(listSmall))
            treeSmall.rangeUpdate(l, r, val)

            # l, r = genRange(len(listLarge))
            # treeLarge.rangeUpdate(l, r, val)

            print("Range Update", [l, r, val])

        treeSmall.printTree()
        print()
