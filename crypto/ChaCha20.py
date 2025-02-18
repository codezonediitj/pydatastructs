from typing import List
import struct

__all__ = ['ChaCha20']
class ChaCha20:
    """
    Implementation of the ChaCha20 stream cipher.
    
    Attributes
    ----------
    key : bytes
        32-byte (256-bit) encryption key.
    nonce : bytes
        12-byte (96-bit) nonce.
    counter : int
        32-bit counter, typically starts at 0.
    """
    def __new__(cls, key: bytes, nonce: bytes, counter: int = 0):
        if not isinstance(key, bytes) or len(key) != 32:
            raise ValueError("Key must be exactly 32 bytes (256 bits).")
        if not isinstance(nonce, bytes) or len(nonce) != 12:
            raise ValueError("Nonce must be exactly 12 bytes (96 bits).")
        instance = super().__new__(cls)
        instance.key = key
        instance.nonce = nonce
        instance.counter = counter
        return instance
    def _quarter_round(self, state: List[int], a: int, b: int, c: int, d: int):
        state[a] = (state[a] + state[b]) % (2**32)
        state[d] ^= state[a]
        state[d] = ((state[d] << 16) | (state[d] >> 16)) % (2**32)
        state[c] = (state[c] + state[d]) % (2**32)
        state[b] ^= state[c]
        state[b] = ((state[b] << 12) | (state[b] >> 20)) % (2**32)
        state[a] = (state[a] + state[b]) % (2**32)
        state[d] ^= state[a]
        state[d] = ((state[d] << 8) | (state[d] >> 24)) % (2**32)
        state[c] = (state[c] + state[d]) % (2**32)
        state[b] ^= state[c]
        state[b] = ((state[b] << 7) | (state[b] >> 25)) % (2**32)
    def _double_round(self, state: List[int]):
        self._quarter_round(state, 0, 4, 8, 12)
        self._quarter_round(state, 1, 5, 9, 13)
        self._quarter_round(state, 2, 6, 10, 14)
        self._quarter_round(state, 3, 7, 11, 15)
        self._quarter_round(state, 0, 5, 10, 15)
        self._quarter_round(state, 1, 6, 11, 12)
        self._quarter_round(state, 2, 7, 8, 13)
        self._quarter_round(state, 3, 4, 9, 14)