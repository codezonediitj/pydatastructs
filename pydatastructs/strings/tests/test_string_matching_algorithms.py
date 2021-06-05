from pydatastructs.strings.string_matching_algorithms import find_string

def test_kms():
    _test_common_string_matching('kmp')


def _test_common_string_matching(algorithm):
    true_text_pattern_dictionary = {
        "Knuth-Morris-Pratt": "-Morris-",
        "abcabcabcabdabcabdabcabca": "abcabdabcabca",
        "aefcdfaecdaefaefcdaefeaefcdcdeae": "aefcdaefeaefcd",
        "aaaaaaaa": "aaa",
        "fullstringmatch": "fullstringmatch"
    }
    for test_case_key in true_text_pattern_dictionary:
        assert find_string(test_case_key, true_text_pattern_dictionary[test_case_key], algorithm) is True

    false_text_pattern_dictionary = {
        "Knuth-Morris-Pratt": "-Pratt-",
        "abcabcabcabdabcabdabcabca": "qwertyuiopzxcvbnm",
        "aefcdfaecdaefaefcdaefeaefcdcdeae": "cdaefaefe",
        "fullstringmatch": "fullstrinmatch"
    }

    for test_case_key in false_text_pattern_dictionary:
        assert find_string(test_case_key, false_text_pattern_dictionary[test_case_key], algorithm) is False
