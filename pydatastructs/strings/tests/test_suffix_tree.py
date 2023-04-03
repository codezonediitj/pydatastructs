import unittest
from pydatastructs.strings.suffix_tree import SuffixTree


class SuffixTreeTest(unittest.TestCase):
    """Some functional tests.
    """

    def test_empty_string(self):
        st = SuffixTree('')
        self.assertEqual(st.find_substring('not there'), -1)
        self.assertEqual(st.find_substring(''), -1)
        self.assertFalse(st.has_substring('not there'))
        self.assertFalse(st.has_substring(''))

    def test_repeated_string(self):
        st = SuffixTree("aaa")
        self.assertEqual(st.find_substring('a'), 0)
        self.assertEqual(st.find_substring('aa'), 0)
        self.assertEqual(st.find_substring('aaa'), 0)
        self.assertEqual(st.find_substring('b'), -1)
        self.assertTrue(st.has_substring('a'))
        self.assertTrue(st.has_substring('aa'))
        self.assertTrue(st.has_substring('aaa'))

        self.assertFalse(st.has_substring('aaaa'))
        self.assertFalse(st.has_substring('b'))
        # case sensitive by default
        self.assertFalse(st.has_substring('A'))

if __name__ == '__main__':
    unittest.main()
