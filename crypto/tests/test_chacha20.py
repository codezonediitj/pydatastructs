import random
import string
from crypto.ChaCha20 import ChaCha20

VALID_KEY = b"\x00" *32
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
