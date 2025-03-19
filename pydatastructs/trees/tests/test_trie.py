import pytest
from pydatastructs.trees.trie import Trie

def test_trie_insert_search():
    trie = Trie()
    trie.insert("apple")
    assert trie.search("apple")
    assert not trie.search("app")
    trie.insert("app")
    assert trie.search("app")

def test_trie_starts_with():
    trie = Trie()
    trie.insert("apple")
    assert trie.starts_with("app")
    assert trie.starts_with("a")
    assert not trie.starts_with("b")
    assert not trie.starts_with("applxyz")

def test_trie_empty():
    trie = Trie()
    assert not trie.search("apple")
    assert not trie.starts_with("app")

def test_trie_multiple_words():
    trie = Trie()
    trie.insert("apple")
    trie.insert("application")
    trie.insert("banana")
    assert trie.search("apple")
    assert trie.search("application")
    assert trie.search("banana")
    assert not trie.search("app")
    assert trie.starts_with("app")
    assert trie.starts_with("ban")
    assert not trie.starts_with("aplx")

def test_trie_case_sensitive():
    trie = Trie()
    trie.insert("Apple")
    assert trie.search("Apple")
    assert not trie.search("apple")

def test_count_words():
    trie = Trie()
    assert trie.count_words() == 0
    trie.insert("apple")
    assert trie.count_words() == 1
    trie.insert("app")
    assert trie.count_words() == 2
    trie.insert("apple")
    assert trie.count_words() == 2

def test_longest_common_prefix():
    trie = Trie()
    assert trie.longest_common_prefix() == ""
    trie.insert("apple")
    assert trie.longest_common_prefix() == "apple"
    trie.insert("application")
    assert trie.longest_common_prefix() == "appl"
    trie.insert("banana")
    assert trie.longest_common_prefix() == ""

def test_autocomplete():
    trie = Trie()
    trie.insert("apple")
    trie.insert("application")
    trie.insert("app")
    assert trie.autocomplete("app") == ["app", "apple", "application"]
    assert trie.autocomplete("appl") == ["apple", "application"]
    assert trie.autocomplete("b") == []

def test_bulk_insert():
    trie = Trie()
    trie.bulk_insert(["apple", "banana", "orange"])
    assert trie.search("apple")
    assert trie.search("banana")
    assert trie.search("orange")
    assert trie.count_words() == 3

def test_clear():
    trie = Trie()
    trie.insert("apple")
    trie.clear()
    assert trie.is_empty()
    assert trie.count_words() == 0
    assert not trie.search("apple")

def test_is_empty():
    trie = Trie()
    assert trie.is_empty()
    trie.insert("apple")
    assert not trie.is_empty()
    trie.clear()
    assert trie.is_empty()

def test_find_all_words():
    trie = Trie()
    trie.bulk_insert(["apple", "banana", "orange"])
    assert sorted(trie.find_all_words()) == sorted(["apple", "banana", "orange"])
    trie.clear()
    assert trie.find_all_words() == []


def test_longest_word():
    trie = Trie()
    assert trie.longest_word() is None
    trie.bulk_insert(["apple", "banana", "application"])
    assert trie.longest_word() == "application"
    trie.insert("a")
    assert trie.longest_word() == "application"

