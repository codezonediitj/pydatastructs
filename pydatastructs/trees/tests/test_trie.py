from pydatastructs.trees.trie_structure import Trie

def test_trie():
    trie = Trie()
    trie.insert("hi")
    trie.insert("search")
    trie.insert("sea")
    trie.insert("see")
    trie.insert("seek")
    assert trie.search("Bonjour") == False
    assert trie.search("see")
    assert trie.search("sew") == False
    trie.delete("see")
    assert trie.search("see") == False
    assert trie.search("sea")
