from pydatastructs.utils.misc_util import TrieNode
from collections import deque
import copy

__all__ = [
    'Trie'
]

Stack = Queue = deque

class Trie(object):

    __slots__ = ['root']

    def __new__(cls):
        obj = object.__new__(cls)
        obj.root = TrieNode()
        return obj

    def insert(self, string: str) -> None:
        walk = self.root
        for char in string:
            if walk.get_child(char) is None:
                newNode = TrieNode(char)
                walk.add_child(newNode)
                walk = newNode
            else:
                walk = walk.get_child(char)
        walk.is_terminal = True

    def is_present(self, string: str) -> bool:
        walk = self.root
        for char in string:
            if walk.get_child(char) is None:
                return False
            walk = walk.get_child(char)
        return True

    def delete(self, string: str):
        path = []
        walk = self.root
        size = len(string)
        for i in range(size):
            char = string[i]
            path.append(walk)
            if walk.get_child(char) is None:
                return None
            walk = walk.get_child(char)
        path.append(walk)
        i = len(path) - 1
        path[i].is_terminal = False
        while not path[i]._children and i >= 1:
            path[i-1].remove_child(path[i].char)
            i -= 1
            if path[i].is_terminal:
                return True
        return True

    def strings_with_prefix(self, string: str) -> list:

        def _collect(prefix: str, node: TrieNode, strings: list) -> str:
            TrieNode_stack = Stack()
            TrieNode_stack.append((node, prefix))
            while TrieNode_stack:
                walk, curr_prefix = TrieNode_stack.pop()
                if walk.is_terminal:
                    strings.append(curr_prefix + walk.char)
                for child in walk._children:
                    TrieNode_stack.append((walk.get_child(child), curr_prefix + walk.char))

        strings = []
        prefix = ""
        walk = self.root
        for char in string:
            walk = walk.get_child(char)
            if walk is None:
                return strings
            prefix += char
        if walk.is_terminal:
            strings.append(walk.char)
        for child in walk._children:
            _collect(prefix, walk.get_child(child), strings)
        return strings
