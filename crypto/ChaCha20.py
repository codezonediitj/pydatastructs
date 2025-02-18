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