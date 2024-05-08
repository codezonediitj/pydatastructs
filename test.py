from BST import BST

def int_comp(curr, new):
    if curr > new:
        return 1
    elif curr < new:
        return -1
    else:
        return 0

b = BST(1, 666);
print(b)

print(b.data)
print(b.key)

# Keywords can now be used. But all must be keywords or none
b.insert(data=777, key=2)
# b = b.insert(2, 777, int_comp)
b.insert(3, 888)
b.insert(4, 555, int_comp)
print(b.listify())
b.insert(3, 333)
print(b.listify())
print(b.search(3))
print(b.search(8))
# print(b.left)
# print(b.right)

# print(str(b))

# b.left = BST(777)
# b.right = BST(888)

# print(b.listify())
