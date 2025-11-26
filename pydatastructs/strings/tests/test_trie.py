from pydatastructs import Trie

def test_Trie():

    strings = ["A", "to", "tea", "ted", "ten", "i",
               "in", "inn", "Amfn", "snbr"]
    trie = Trie()
    for string in strings:
        trie.insert(string)

    prefix_strings = ["te", "t", "Am", "snb"]

    for string in strings:
        assert trie.is_inserted(string)

    for string in strings[::-1]:
        assert trie.is_inserted(string)

    for string in prefix_strings:
        assert trie.is_present(string)
        assert not trie.is_inserted(string)

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
                assert not trie.is_inserted(present)
            else:
                assert trie.is_present(present)
                assert trie.is_inserted(present)
        strings.remove(string)

    prefix_strings_1 = ["dict", "dicts", "dicts_lists_tuples"]
    trie_1 = Trie()

    for i in range(len(prefix_strings_1)):
        trie_1.insert(prefix_strings_1[i])
        for j in range(i + 1):
            assert trie_1.is_inserted(prefix_strings_1[j])
            assert trie_1.is_present(prefix_strings_1[j])

    assert trie_1.count_words() == 3

    assert trie_1.longest_common_prefix() == "dict"

    assert trie_1.autocomplete("dict") == ["dict", "dicts", "dicts_lists_tuples"]

    trie_2 = Trie()
    trie_2.insert("apple")
    trie_2.insert("app")
    trie_2.insert("apricot")
    trie_2.insert("banana")
    assert trie_2.count_words() == 4

    trie_2.clear()
    assert trie_2.count_words() == 0

    assert trie_2.is_empty()

    trie_3 = Trie()
    trie_3.insert("hello")
    trie_3.insert("world")
    assert sorted(trie_3.all_words()) == ["hello", "world"]

    trie_4 = Trie()
    trie_4.insert("zebra")
    trie_4.insert("dog")
    trie_4.insert("duck")
    trie_4.insert("dove")
    assert trie_4.shortest_unique_prefix() == {
        "zebra": "z",
        "dog": "dog",
        "duck": "du",
        "dove": "dov"
    }
    assert trie_4.starts_with("do")
    assert not trie_4.starts_with("cat")

    assert trie_4.longest_word() == "zebra"
