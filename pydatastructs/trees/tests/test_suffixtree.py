from pydatastructs import SuffixTree

def test_suffixtree():
    s = SuffixTree("HelloworldHe")
    assert s.find("Hel") == 0
    assert s.find_all("He") == {0, 10}
    assert s.find("Win") == -1
