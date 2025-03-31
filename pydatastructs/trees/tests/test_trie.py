import pytest
from pydatastructs.trees.trie import Trie

def test_trie_insert_and_search():
    trie = Trie()
    trie.insert("apple")
    assert trie.search("apple") is True  # Word should be present
    assert trie.search("app") is False  # Partial word should not be found
    assert trie.starts_with("app") is True  # Prefix should be detected

def test_trie_multiple_inserts():
    trie = Trie()
    trie.insert("apple")
    trie.insert("app")
    assert trie.search("app") is True  # Now "app" should be present
    assert trie.search("apple") is True

def test_trie_delete():
    trie = Trie()
    trie.insert("apple")
    trie.insert("app")
    assert trie.delete("apple") is True  # "apple" should be removed
    assert trie.search("apple") is False  # "apple" should not be found
    assert trie.search("app") is True  # "app" should still exist

def test_trie_delete_non_existent():
    trie = Trie()
    assert trie.delete("banana") is False  # Deleting a non-existent word should return False

def test_trie_empty_string():
    trie = Trie()
    assert trie.search("") is False  # Searching for an empty string should return False
    assert trie.starts_with("") is True  # Empty prefix should return True

if __name__ == "__main__":
    pytest.main()
