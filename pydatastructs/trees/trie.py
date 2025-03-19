class TrieNode:
    """Represents a node in the Trie data structure."""
    def __init__(self):
        """Initializes a TrieNode with empty children and is_end_of_word set to False."""
        self.children = {}
        self.is_end_of_word = False
        self.word = None

class Trie:
    """Represents the Trie (prefix tree) data structure."""
    def __init__(self):
        """Initializes an empty Trie with a root TrieNode."""
        self.root = TrieNode()
        self.word_count = 0

    def insert(self, word):
        """Inserts a word into the Trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        if not node.is_end_of_word:
          node.is_end_of_word = True
          node.word = word
          self.word_count += 1

    def search(self, word):
        """Searches for a word in the Trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix):
        """Checks if any word in the Trie starts with the given prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    def count_words(self):
        """Returns the total number of words stored in the Trie."""
        return self.word_count

    def longest_common_prefix(self):
        """Finds the longest common prefix among all words in the Trie."""
        node = self.root
        prefix = ""
        while len(node.children) == 1 and not node.is_end_of_word:
            char = next(iter(node.children))
            prefix += char
            node = node.children[char]
        return prefix

    def autocomplete(self, prefix):
        """Provides a list of words that match a given prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        def collect_words(current_node, current_prefix):
            words = []
            if current_node.is_end_of_word:
                words.append(current_prefix)
            for char, child_node in current_node.children.items():
                words.extend(collect_words(child_node, current_prefix + char))
            return words

        return collect_words(node, prefix)

    def bulk_insert(self, words):
        """Inserts multiple words into the Trie in a single operation."""
        for word in words:
            self.insert(word)

    def clear(self):
        """Removes all words from the Trie, resetting it."""
        self.root = TrieNode()
        self.word_count = 0

    def is_empty(self):
        """Returns True if the Trie is empty, otherwise False."""
        return self.word_count == 0

    def find_all_words(self):
        """Retrieves all words currently stored in the Trie."""
        def collect_words(current_node):
            words = []
            if current_node.is_end_of_word:
                words.append(current_node.word)
            for child_node in current_node.children.values():
                words.extend(collect_words(child_node))
            return words

        return collect_words(self.root)

    def shortest_unique_prefix(self, word):
        """Determines the shortest unique prefix for a given word."""
        node = self.root
        prefix = ""
        for char in word:
            prefix += char
            if len(node.children[char].children) <= 1 and node.children[char].is_end_of_word is False :
                return prefix
            node = node.children[char]
        return word

    def longest_word(self):
        """Finds and returns the longest word in the Trie."""
        all_words = self.find_all_words()
        if not all_words:
            return None
        return max(all_words, key=len)
