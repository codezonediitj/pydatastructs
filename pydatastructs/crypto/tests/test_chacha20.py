import random
import string
from pydatastructs.crypto.ChaCha20 import ChaCha20

VALID_KEY = B"\x00" *32
assert len(VALID_KEY) == 32, "VALID_KEY must be exactly 32 bytes"
VALID_NONCE = B"\x00" * 12
assert len(VALID_NONCE) == 12, "VALID_NONCE must be exactly 12 bytes"

secure_rng = random.SystemRandom()

def test_invalid_key_size():
    """Test invalid key sizes."""
    try:
        ChaCha20(b"short_key", VALID_NONCE)
    except ValueError as e:
        assert "Key must be exactly 32 bytes" in str(e)
    else:
        assert False, "ValueError was not raised for short key"

    try:
        ChaCha20(b"A" * 33, VALID_NONCE)
    except ValueError as e:
        assert "Key must be exactly 32 bytes" in str(e)
    else:
        assert False, "ValueError was not raised for long key"

def test_invalid_nonce_size():
    """Test invalid nonce sizes."""
    try:
        ChaCha20(VALID_KEY, b"short")
    except ValueError as e:
        assert "Nonce must be exactly 12 bytes" in str(e)
    else:
        assert False, "ValueError was not raised for short nonce"

    try:
        ChaCha20(VALID_KEY, b"A" * 13)
    except ValueError as e:
        assert "Nonce must be exactly 12 bytes" in str(e)
    else:
        assert False, "ValueError was not raised for long nonce"

def test_invalid_counter_values():
    """Test invalid counter values for ChaCha20."""
    for invalid_counter in [-1, -100, -999999]:
        try:
            ChaCha20(VALID_KEY, VALID_NONCE, counter=invalid_counter)
        except ValueError as e:
            assert "Counter must be a non-negative integer" in str(e)
        else:
            assert False, f"ValueError not raised for counter={invalid_counter}"

def test_encrypt_decrypt():
    """Test encryption and decryption are symmetric."""
    cipher = ChaCha20(VALID_KEY, VALID_NONCE)
    plaintext = b"Hello, ChaCha20!"
    ciphertext = cipher.encrypt(plaintext)
    decrypted = cipher.decrypt(ciphertext)

    assert decrypted == plaintext, "Decryption failed. Plaintext does not match."

def test_key_reuse_simple():
    """
    Test the vulnerability of key reuse in ChaCha20 encryption.

    This test demonstrates the security flaw of reusing the same key and nonce
    for different plaintexts in stream ciphers. It exploits the property that
    XORing two ciphertexts from the same keystream cancels out the keystream,
    revealing the XOR of the plaintexts.

    Encrypt two different plaintexts with the same key and nonce.
    XOR the resulting ciphertexts to remove the keystream, leaving only the XOR of plaintexts.
    XOR the result with the first plaintext to recover the second plaintext.
    Assert that the recovered plaintext matches the original second plaintext.

    Expected Behavior:
    - If the ChaCha20 implementation is correct, reusing the same key and nonce
      will expose the XOR relationship between plaintexts.
    - The test should successfully recover the second plaintext using XOR operations.

    Assertion:
    - Raises an AssertionError if the recovered plaintext does not match the
      original second plaintext, indicating a failure in the XOR recovery logic.

    Output:
    - Prints the original second plaintext.
    - Prints the recovered plaintext (should be identical to the original).
    - Displays the XOR result (hexadecimal format) for inspection.

    Security Note:
    - This test highlights why it is critical never to reuse the same key and nonce
      in stream ciphers like ChaCha20.
    """


    cipher1 = ChaCha20(VALID_KEY, VALID_NONCE)
    cipher2 = ChaCha20(VALID_KEY, VALID_NONCE)

    plaintext1 = b"Hello, this is message one!"
    plaintext2 = b"Hi there, this is message two!"

    ciphertext1 = cipher1.encrypt(plaintext1)
    ciphertext2 = cipher2.encrypt(plaintext2)

    xor_result = []
    for c1_byte, c2_byte in zip(ciphertext1, ciphertext2):
        xor_result.append(c1_byte ^ c2_byte)
    xor_bytes = bytes(xor_result)
    recovered = []
    for xor_byte, p1_byte in zip(xor_bytes, plaintext1):
        recovered.append(xor_byte ^ p1_byte)
    recovered_plaintext = bytes(recovered)
    assert recovered_plaintext == plaintext2, "Failed to recover second plaintext from XOR pattern"
