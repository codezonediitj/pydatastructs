from pydatastructs import Trie


def test_Trie():
    strings = ["A", "to", "tea", "ted", "ten", "i", "in", "inn"]
    trie = Trie()
    for string in strings:
        trie.insert(string)

    for string in strings:
        assert trie.is_present(string)

    assert sorted(trie.strings_with_prefix("t")) == ['tea', 'ted', 'ten', 'to']
    assert sorted(trie.strings_with_prefix("te")) == ["tea", "ted", "ten"]
    assert trie.strings_with_prefix("i") == ["i", "in", "inn"]
    assert trie.strings_with_prefix("a") == []

    remove_order = ["to", "tea", "ted", "ten", "inn", "in", "A"]

    assert trie.delete("z") is None

    for string in remove_order:
        trie.delete(string)
        for present in strings:
            if present == string:
                assert not trie.is_present(present)
            else:
                assert trie.is_present(present)
        strings.remove(string)
