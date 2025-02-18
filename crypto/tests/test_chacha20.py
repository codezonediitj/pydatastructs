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
