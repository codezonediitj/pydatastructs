from pydatastructs.strings import find, Crypto

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

def _test_sha256_encrypt():
    
    test_cases = [
        "HelloWorld",
        "1234567890",
        "abcdefABCDEF",
        "",
        "The quick brown fox jumps over the lazy dog",
        "Pydatastructs"
    ]
    
    expected_hashes = [
        "872e4e50ce9990d8b041330c47c9ddd11bec6b503ae9386a99da8584e9bb12c4",
        "c775e7b757ede630cd0aa1113bd102661ab38829ca52a6422ab782862f268646",
        "4a098074bfa74c04454ebbc7d286d085c420934c27ab11e9c00cc53247d9959e",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592",
        "1b5b22944c188c3e90d126ebd27e10d7497fbf5924f23c05775fa2dd9e1d8c86"
    ]
    
    for text, expected in zip(test_cases, expected_hashes):
        assert Crypto.sha256_encrypt(text) == expected