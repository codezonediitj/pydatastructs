class Node:
    def __init__(self, t, leaf):
        self.t = t # minimum degree
        self.leaf = leaf
        self.keys = []
        self.children = []

    def traverse(self):
        i = 0
        n = len(self.keys)
        while i < n:
            if self.leaf == False:
                self.children[i].traverse()
            print(self.keys[i])
            i += 1
        if self.leaf == False:
            self.children[i].traverse()

class BTree:
    def __init__(self, t):
        self.t = t # minimum degree
        self.root = None

    def traverse(self):
        if self.root != None:
            self.root.traverse()

    def search(self, k):
        if self.root == None:
            return None
        else:
            return self.root.search(k)

    def insert(self, k):
        if self.root == None:
            self.root = Node(self.t, True)
            self.root.keys.append(k)
        else:
            if len(self.root.keys) == (2 * self.t) - 1:
                new_root = Node(self.t, False)
                new_root.children.append(self.root)
                new_root.split_child(0, self.root)
                i = 0
                if new_root.keys[0] < k:
                    i += 1
                new_root.children[i].insert_non_full(k)
                self.root = new_root
            else:
                self.root.insert_non_full(k)

    def delete(self, k):
        if not self.root:
            print("The tree is empty")
            return

        self.root.delete(k)

        if not self.root.keys:
            self.root = self.root.children[0]


class Node:
    def __init__(self, t, leaf):
        self.t = t
        self.leaf = leaf
        self.keys = []
        self.children = []

    def traverse(self):
        i = 0
        n = len(self.keys)
        while i < n:
            if self.leaf == False:
                self.children[i].traverse()
            print(self.keys[i])
            i += 1
        if self.leaf == False:
            self.children[i].traverse()

    def search(self, k):
        i = 0
        n = len(self.keys)
        while i < n and k > self.keys[i]:
            i += 1
        if self.keys[i] == k:
            return self
        if self.leaf == True:
            return None
        return self.children[i].search(k)

    def insert_non_full(self, k):
        i = len(self.keys) - 1
        if self.leaf == True:
            self.keys.append(0)
            while i >= 0 and self.keys[i] > k:
                self.keys[i+1] = self.keys[i]
                i -= 1
            self.keys[i+1] = k
        else:
            while i >= 0 and self.keys[i] > k:
                i -= 1
            if len(self.children[i+1].keys) == (2 * self.t) - 1:
                self.split_child(i+1, self.children[i+1])
                if self.keys[i+1] < k:
                    i += 1
            self.children[i+1].insert_non_full(k)

    def split_child(self, i, y):
        z = Node(y.t, y.leaf)
        self.children.insert(i+1, z)
        self.keys.insert(i, y.keys[self.t-1])
        z.keys = y.keys[self.t:(2*self.t)-1]
        y.keys = y.keys[0:self.t-1]
        if y.leaf == False:
            z.children = y.children[self.t:(2*self.t)]
            y.children = y.children[0:self.t-1]

    def delete(self, k):
        n = len(self.keys)
        i = 0
        while i < n and k > self.keys[i]:
            i += 1
        if self.leaf:
            if i < n and self.keys[i] == k:
                self.keys.pop(i)
            else:
                print("The key", k, "does not exist in the tree")
                return
        else:
            if i < n and self.keys[i] == k:
                if len(self.children[i].keys) >= self.t:
                    prev = self.get_predecessor(i)
                    self.keys[i] = prev
                    self.children[i].delete(prev)
                elif len(self.children[i+1].keys) >= self.t:
                    succ = self.get_successor(i)
                    self.keys[i] = succ
                    self.children[i+1].delete(succ)
                else:
                    self.merge_children(i)
                    self.children[i].delete(k)
            else:
                if len(self.children[i].keys) == self.t-1:
                    if i > 0 and len(self.children[i-1].keys) >= self.t:
                        self.move_key_to_left_child(i)
                    elif i < n and len(self.children[i+1].keys) >= self:
                        self.move_key_to_right_child(i)
                    else:
                        self.merge_children(i)
                    self.children[i].delete(k)
                else:
                    self.children[i].delete(k)

        if len(self.keys) == 0:
            if self.leaf:
                del self
            else:
                self.children[0].delete(k)

    def get_predecessor(self, i):
        curr = self.children[i]
        while not curr.leaf:
            curr = curr.children[-1]
        return curr.keys[-1]

    def get_successor(self, i):
        curr = self.children[i+1]
        while not curr.leaf:
            curr = curr.children[0]
        return curr.keys[0]

    def merge_children(self, i):
        child1 = self.children[i]
        child2 = self.children[i+1]
        child1.keys.append(self.keys[i])
        child1.keys += child2.keys
        child1.children += child2.children
        self.children.pop(i+1)
        self.keys.pop(i)

    def move_key_to_left_child(self, i):
        child1 = self.children[i-1]
        child2 = self.children[i]
        child2.keys.insert(0, self.keys[i-1])
        self.keys[i-1] = child1.keys.pop(-1)
        if not child1.leaf:
            child2.children.insert(0, child1.children.pop(-1))

    def move_key_to_right_child(self, i):
        child1 = self.children[i]
        child2 = self.children[i+1]
        child1.keys.append(self.keys[i])
        self.keys[i] = child2.keys.pop(0)
        if not child2.leaf:
            child1.children.append(child2.children.pop(0))
