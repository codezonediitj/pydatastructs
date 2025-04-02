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

def _test_chacha20():
    import binascii
    cnvt = lambda x: binascii.unhexlify(bytes(x, 'ascii'))
    test_cases = [
        ('76b8e0ada0f13d90405d6ae55386bd28bdd219b8a08ded1aa836efcc8b770dc7da41597c5157488d7724e03fb8d84a376a43b8f41518a11cc387b669', '0000000000000000000000000000000000000000000000000000000000000000', '0000000000000000'),
        ('4540f05a9f1fb296d7736e7b208e3c96eb4fe1834688d2604f450952ed432d41bbe2a0b6ea7566d2a5d1e7e20d42af2c53d792b1c43fea817e9ad275', '0000000000000000000000000000000000000000000000000000000000000001', '0000000000000000'),
        ('de9cba7bf3d69ef5e786dc63973f653a0b49e015adbff7134fcb7df137821031e85a050278a7084527214f73efc7fa5b5277062eb7a0433e445f41e3', '0000000000000000000000000000000000000000000000000000000000000000', '0000000000000001'),
        ('ef3fdfd6c61578fbf5cf35bd3dd33b8009631634d21e42ac33960bd138e50d32111e4caf237ee53ca8ad6426194a88545ddc497a0b466e7d6bbdb004', '0000000000000000000000000000000000000000000000000000000000000000', '0100000000000000'),
        ('f798a189f195e66982105ffb640bb7757f579da31602fc93ec01ac56f85ac3c134a4547b733b46413042c9440049176905d3be59ea1c53f15916155c2be8241a38008b9a26bc35941e2444177c8ade6689de95264986d95889fb60e84629c9bd9a5acb1cc118be563eb9b3a4a472f82e09a7e778492b562ef7130e88dfe031c79db9d4f7c7a899151b9a475032b63fc385245fe054e3dd5a97a5f576fe064025d3ce042c566ab2c507b138db853e3d6959660996546cc9c4a6eafdc777c040d70eaf46f76dad3979e5c5360c3317166a1c894c94a371876a94df7628fe4eaaf2ccb27d5aaae0ad7ad0f9d4b6ad3b54098746d4524d38407a6deb', '000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f', '0001020304050607')
    ]

    for i, (ciphertext, key, iv) in enumerate(map(lambda t: tuple(map(cnvt, t)), test_cases)):
        assert Crypto.chacha20_encrypt(b'\0' * len(ciphertext), key, iv) == ciphertext
