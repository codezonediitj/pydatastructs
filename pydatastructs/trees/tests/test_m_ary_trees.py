from pydatastructs import MAryTree, Trie

def test_MAryTree():
    m = MAryTree(1, 1)
    assert str(m) == '[(1, 1)]'

def test_trie():
    trie = Trie()
    trie.insert("hi")
    trie.insert("search")
    trie.insert("sea")
    trie.insert("see")
    trie.insert("seek")
    print(trie.search("see"))
    print(trie.search("see"))
    print(trie.search("sew"))
    print(trie.search("se"))
    assert trie.search("Bonjour") == False
    assert trie.search("see")
    assert trie.search("sew").sort() == ["search", "sea", "see", "seek"].sort()
    trie.delete("see")
    assert trie.search("see").sort() == ["search", "sea", "seek"].sort()
    assert trie.search("sea")

test_trie()