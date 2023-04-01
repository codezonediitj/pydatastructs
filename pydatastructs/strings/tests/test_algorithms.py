from pydatastructs.strings import find

import random, string

def test_kmp():
    _test_common_string_matching('kmp')

def test_rka():
    _test_common_string_matching('rabin_karp')

def test_bm():
    _test_common_string_matching('boyer_moore')

def test_zf():
    _test_common_string_matching('z_function')

def _test_common_string_matching(algorithm):
    true_text_pattern_dictionary = {
        "Knuth-Morris-Pratt": "-Morris-",
        "abcabcabcabdabcabdabcabca": "abcabdabcabca",
        "aefcdfaecdaefaefcdaefeaefcdcdeae": "aefcdaefeaefcd",
        "aaaaaaaa": "aaa",
        "fullstringmatch": "fullstringmatch",
        "z-function": "z-fun"
    }
    for test_case_key in true_text_pattern_dictionary:
        text = test_case_key
        query = true_text_pattern_dictionary[test_case_key]
        positions = find(text, query, algorithm)
        for i in range(positions._last_pos_filled):
            p = positions[i]
            assert text[p:p + len(query)] == query

    false_text_pattern_dictionary = {
        "Knuth-Morris-Pratt": "-Pratt-",
        "abcabcabcabdabcabdabcabca": "qwertyuiopzxcvbnm",
        "aefcdfaecdaefaefcdaefeaefcdcdeae": "cdaefaefe",
        "fullstringmatch": "fullstrinmatch",
        "z-function": "function-",
        "abc": "",
        "": "abc"
    }

    for test_case_key in false_text_pattern_dictionary:
        text = test_case_key
        query = false_text_pattern_dictionary[test_case_key]
        positions = find(text, query, algorithm)
        assert positions.size == 0

    random.seed(1000)

    def gen_random_string(length):
        ascii = string.ascii_uppercase
        digits = string.digits
        return ''.join(random.choices(ascii + digits, k=length))

    for _ in range(100):
        query = gen_random_string(random.randint(3, 10))
        num_times = random.randint(1, 10)
        freq = 0
        text = ""
        while freq < num_times:
            rand_str = gen_random_string(random.randint(5, 10))
            if rand_str != query:
                freq += 1
                text += query + rand_str + query
        positions = find(text, query, algorithm)
        assert positions._num == num_times * 2
        for i in range(positions._last_pos_filled):
            p = positions[i]
            assert text[p:p + len(query)] == query

        text = gen_random_string(len(query))
        if text != query:
            positions = find(text, query, algorithm)
            assert positions.size == 0
