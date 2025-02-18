import random
import string
from crypto.ChaCha20 import ChaCha20

VALID_KEY = b"\x00" *32
assert len(VALID_KEY) == 32, "VALID_KEY must be exactly 32 bytes"
VALID_NONCE = B"\x00" * 12
assert len(VALID_NONCE) == 12, "VALID_NONCE must be exactly 12 bytes"

secure_rng = random.SystemRandom()