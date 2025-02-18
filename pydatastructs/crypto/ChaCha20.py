from typing import List
import struct
import numpy as np
from copy import deepcopy as dp
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
        if not isinstance(counter, int) or counter < 0:
            raise ValueError("Counter must be a non-negative integer.")
        instance = super().__new__(cls)
        instance.key = key
        instance.nonce = nonce
        instance.counter = counter
        return instance
    
    def __init__(self, key: bytes, nonce: bytes, counter: int = 0):
        """Initializes the ChaCha20 object."""
        # Guard against multiple initializations
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._initialized = True

    def __repr__(self):
        """Returns a string representation of the object for debugging."""
        return f"<ChaCha20(key={self.key[:4].hex()}..., nonce={self.nonce.hex()}, counter={self.counter})>"

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
    def _chacha20_block(self, counter: int) -> bytes:
        """
        Generates a 64-byte keystream block from 16-word (512-bit) state
        The initial state is copied to preserve the original.
        20 rounds (10 double rounds) are performed using quarter-round operations.
        The modified working state is combined with the original state using modular addition (mod 2^32).
        The result is returned as a 64-byte keystream block.
        """
        constants = b"expand 32-byte k"
        state_values = struct.unpack(
            '<16I',
            constants + self.key + struct.pack('<I', counter) + self.nonce
        )
        state = np.array(state_values, dtype=np.uint32).reshape(4, 4)
        working_state = dp(state)
        for _ in range(10):
            self._double_round(working_state)
        final_state = (working_state + state) % (2**32)
        return struct.pack('<16I', *final_state.flatten())
    
    def _apply_keystream(self, data: bytes) -> bytes:
        """
        Applies the ChaCha20 keystream to the input data (plaintext or ciphertext) 
        to perform encryption or decryption.

        This method processes the input data in 64-byte blocks. For each block:
        - A 64-byte keystream is generated using the `_chacha20_block()` function.
        - Each byte of the input block is XORed with the corresponding keystream byte.
        - The XORed result is appended to the output.

        The same function is used for both encryption and decryption because 
        XORing the ciphertext with the same keystream returns the original plaintext.

        Args:
            data (bytes): The input data to be encrypted or decrypted (plaintext or ciphertext).

        Returns:
            bytes: The result of XORing the input data with the ChaCha20 keystream 
                (ciphertext if plaintext was provided, plaintext if ciphertext was provided).
        """
        if len(data) == 0:
            return b""
        result = b""
        chunk_size = 64
        start = 0
        while start < len(data):
            chunk = data[start:start + chunk_size]
            start += chunk_size
            keystream = self._chacha20_block(self.counter)
            self.counter += 1
            xor_block = []
            for idx in range(len(chunk)):
                input_byte = chunk[idx]
                keystream_byte = keystream[idx]
                xor_block.append(input_byte ^ keystream_byte)
            result += bytes(xor_block)
        return result
    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Encrypts the given plaintext using the ChaCha20 stream cipher.

        This method uses the ChaCha20 keystream generated from the 
        key, nonce, and counter to XOR with the plaintext, producing ciphertext.

        Args:
            plaintext (bytes): The plaintext data to be encrypted.

        Returns:
            bytes: The resulting ciphertext.
        """
        return self._apply_keystream(plaintext)
    
    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        Decrypts the given ciphertext using the ChaCha20 stream cipher.

        Since ChaCha20 uses XOR for encryption, decryption is performed 
        using the same keystream and XOR operation.

        Args:
            ciphertext (bytes): The ciphertext data to be decrypted.

        Returns:
            bytes: The resulting plaintext.
        """
        return self.apply_keystream(ciphertext)
    
    def reset(self, counter: int = 0):
        """Resets the ChaCha20 counter to the specified value (default is 0)."""
        if not isinstance(counter, int) or counter < 0:
            raise ValueError("Counter must be a non-negative integer.")
        self.counter = counter