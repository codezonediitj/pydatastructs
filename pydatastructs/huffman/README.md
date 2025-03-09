# Huffman coding algorithm to reduce the size of a file and redundancy

# time complexity: O(nlogn)

# explaination

Huffman coding is a lossless data compression algorithm. The idea is to assign variable-length codes to input characters, lengths of the assigned codes are based on the frequencies of corresponding characters. The most frequent character gets the smallest code and the least frequent character gets the largest code.

- The variable-length codes assigned to input characters are Prefix Codes, means the codes (bit sequences) are assigned in such a way that the code assigned to one character is not the prefix of code assigned to any other character. This is how Huffman Coding makes sure that there is no ambiguity when decoding the generated bitstream.
- Let us understand prefix codes with a counter example. Let there be four characters a, b, c and d, and their corresponding variable length codes be 00, 01, 0 and 1. This coding leads to ambiguity because code assigned to c is the prefix of codes assigned to a and b. If the compressed bit stream is 0001, the de-compressed output may be “cccd” or “ccb” or “acd” or “ab”.

## steps to build a huffman tree

- Create a leaf node for each unique character and build a min heap of all leaf nodes (Min Heap is used as a priority queue. The value of frequency field is used to compare two nodes in min heap. Initially, the least frequent character is at root)

- Extract two nodes with the minimum frequency from the min heap.

- Create a new internal node with a frequency equal to the sum of the two nodes frequencies. Make the first extracted node as its left child and the other extracted node as its right child. Add this node to the min heap.

- Repeat steps#2 and #3 until the heap contains only one node. The remaining node is the root node and the tree is complete.

---

### code snippet :

- we will use a min heap to store the nodes of the tree

```python
class MyHeap():                         # Defining a class for the heap
    def __init__(self):
        self.key = lambda x: x.freq     # Criteria to use for the min heap
        self.index = 0                  # Number of elements in the heap
        self._data = []                 # Initialising it as an empty heap

    def push(self, item):
        heappush(self._data, (self.key(item), self.index, item))
        self.index += 1

    def pop(self):
        self.index -= 1
        return heappop(self._data)[2]

```

---

## Results

we reduced the size of the file from 1.2 MB to 0.6 MB and from Analysis.py we get the error rate also.

- We have also run the file on different test cases in encoded and decoded format.


