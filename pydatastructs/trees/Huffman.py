class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

class HuffmanCoding:
    q = []
    symbols = {}

    def mergenode(self):
        while (self.q or self.symbols):
            lnode = self.q[0]
            self.q.pop(0)
            if (not self.q):
                if (not self.symbols):
                    return lnode
                self.addtoq()
            rnode = self.q[0]
            self.q.pop(0)
            mnode = Node('\0', lnode.freq + rnode.freq)
            mnode.left = lnode
            mnode.right = rnode
            self.q.append(mnode)
            
    def addtoq(self):
        m = list(self.symbols.values())[0]
        for i in self.symbols.keys():
            if (self.symbols.get(i) == m):
                self.q.append(Node(i, m))
            else:
                break
        for i in self.q:
            self.symbols.pop(i.char)

    def buildHuffmanTree(self, input):
        self.symbols = dict(sorted(input.items(), key=lambda item: item[1]))
        self.addtoq()
        root = self.mergenode()
        return root

    def getcode(self, root, code):
        if (not(root.char == '\0')):
            self.symbols[root.char] = code
            return
        self.getcode(root.left, code + '0')
        self.getcode(root.right, code + '1')

    def generateHuffmanCodes(self, root):
        self.symbols.clear()
        code = ''
        self.getcode(root, code)
        return self.symbols
