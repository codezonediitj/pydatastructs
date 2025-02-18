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