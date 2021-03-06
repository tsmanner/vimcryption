"""
Unit tests for `EncryptionEngine`s.
"""
# Standard Library
import base64
import io
import random
import string
import unittest
import numpy as np
# Vimcryption
from encryptionengine import *


class TestEncryptionEngine(unittest.TestCase):
    """ Unit tests for EncryptionEngine
    """
    def test_encrypt_str(self):
        """ Tests encrypting a single string.
        """
        with self.assertRaises(NotImplementedError):
            EncryptionEngine().encrypt("rawr", io.BytesIO())

    def test_encrypt_list(self):
        """ Tests encrypting a list fo strings.
        """
        with self.assertRaises(NotImplementedError):
            EncryptionEngine().encrypt(["r", "a", "w", "r"], io.BytesIO())

    def test_decrypt_list(self):
        """ Tests decrypting a list of strings.
        """
        with self.assertRaises(NotImplementedError):
            EncryptionEngine().decrypt(io.BytesIO(), ["r", "a", "w", "r"])

    def test_decrypt_str(self):
        """ Tests decrypting a single string.
        """
        with self.assertRaises(NotImplementedError):
            EncryptionEngine().decrypt(io.BytesIO(), "rawr")


class TestPassThrough(unittest.TestCase):
    """ Unit tests for PassThrough
    """
    def setUp(self):
        """ Creates a list of randomized strings to use for testing.
        """
        self.test_strings = [
            ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(50, 200)))
            for _ in range(random.randint(10, 50))
        ]

    def test_encrypt_str(self):
        """ Tests encryption passing through a single string.
        """
        file_handle = io.BytesIO()
        test_string = self.test_strings[0]
        PassThrough().encrypt(test_string, file_handle)
        self.assertEqual(test_string, file_handle.getvalue().decode().rstrip("\n"))

    def test_encrypt_list(self):
        """ Tests encryption passing through a list of strings.
        """
        # Encrypt the list of strings into a single document.
        file_handle = io.BytesIO()
        PassThrough().encrypt(self.test_strings, file_handle)
        # Get the encrypted document, split it on newline and compare.
        decrypted_strings = file_handle.getvalue().decode().split("\n")
        if decrypted_strings[-1] == "":
            decrypted_strings.pop(-1)
        self.assertEqual(self.test_strings, decrypted_strings)

    def test_decrypt_str(self):
        """ Tests decryption passing through a single string.
        """
        file_handle = io.BytesIO()
        test_string = self.test_strings[0]
        file_handle.write(test_string.encode("utf8"))
        file_handle.seek(0)
        decrypted_strings = []
        PassThrough().decrypt(file_handle, decrypted_strings)
        self.assertEqual(test_string, decrypted_strings[0])

    def test_decrypt_list(self):
        """ Tests decryption passing through a list of strings.
        """
        # Write all test strings to the file handle, newline separated
        file_handle = io.BytesIO()
        file_handle.write("\n".join(self.test_strings).encode("utf8"))
        file_handle.seek(0)
        decrypted_strings = []
        # Decrypt the file handle into a list and compare
        PassThrough().decrypt(file_handle, decrypted_strings)
        self.assertEqual(self.test_strings, decrypted_strings)


class TestBase64Engine(unittest.TestCase):
    """ Unit tests for Base64Engine
    """
    def setUp(self):
        """ Creates a list of randomized strings to use for testing.
        """
        self.test_strings = [
            ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(50, 200)))
            for _ in range(random.randint(10, 50))
        ]

    def test_encrypt_str(self):
        """ Tests base64 encoding a single string.
        """
        file_handle = io.BytesIO()
        test_string = self.test_strings[0]
        Base64Engine().encrypt(test_string, file_handle)
        encrypted_string = file_handle.getvalue()
        self.assertEqual(base64.b64encode(test_string.encode("utf8")), encrypted_string)

    def test_encrypt_list(self):
        """ Tests base64 encoding a list of strings.
        """
        file_handle = io.BytesIO()
        # Get a list of the encrypted strings
        Base64Engine().encrypt(self.test_strings, file_handle)
        decrypted_strings = base64.b64decode(file_handle.getvalue()).decode().split("\n")
        if decrypted_strings[-1] == "":
            decrypted_strings.pop(-1)
        self.assertEqual(self.test_strings, decrypted_strings)

    def test_decrypt_str(self):
        """ Tests base64 decoding a single string.
        """
        file_handle = io.BytesIO()
        test_string = self.test_strings[0]
        file_handle.write(base64.b64encode(test_string.encode("utf8")))
        file_handle.seek(0)
        decrypted_strings = []
        Base64Engine().decrypt(file_handle, decrypted_strings)
        self.assertEqual(test_string, decrypted_strings[0])

    def test_decrypt_list(self):
        """ Tests base64 decoding a list of strings.
        """
        file_handle = io.BytesIO()
        file_handle.write(base64.b64encode("\n".join(self.test_strings).encode("utf8")))
        file_handle.seek(0)
        # Get a list of the decrypted strings
        decrypted_strings = []
        Base64Engine().decrypt(file_handle, decrypted_strings)
        self.assertEqual(self.test_strings, decrypted_strings)


class TestAES128Engine(unittest.TestCase):
    """ Unit tests for AES128
    """
    def setUp(self):
        """ Creates zero hash and matrix members.
        """
        self.zero_hash = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self.zero_matrix = np.matrix(np.zeros((4, 4), dtype=int))

    def test_round_key_gen(self):
        """ Tests generation of the 11 AES round keys based on a fixed base key.
        """
        cipher_key = "\x54\x68\x61\x74\x73\x20\x6D\x79\x20\x4B\x75\x6E\x67\x20\x46\x75"
        expected_keys = [
            "5468617473206d79204b756e67204675",
            "e232fcf191129188b159e4e6d679a293",
            "56082007c71ab18f76435569a03af7fa",
            "d2600de7157abc686339e901c3031efb",
            "a11202c9b468bea1d75157a01452495b",
            "b1293b3305418592d210d232c6429b69",
            "bd3dc287b87c47156a6c9527ac2e0e4e",
            "cc96ed1674eaaa031e863f24b2a8316a",
            "8e51ef21fabb4522e43d7a0656954b6c",
            "bfe2bf904559fab2a16480b4f7f1cbd8",
            "28fddef86da4244accc0a4fe3b316f26"
        ]
        round_keys = AES128Engine.generate_round_keys(cipher_key)
        for round_idx, key in enumerate(round_keys):
            key_string = aesutil.matrix_to_string(key)
            self.assertEqual(key_string, expected_keys[round_idx])

    @staticmethod
    def test_add_round_key():
        """ Tests the `add_round_key` step by XORing a known key with a known state matrix.
        """
        state_matrix = aesutil.bytes_to_matrix("\x54\x77\x6F\x20\x4F\x6E\x65\x20\x4E\x69\x6E\x65\x20\x54\x77\x6F")
        round_key = aesutil.bytes_to_matrix("\x54\x68\x61\x74\x73\x20\x6D\x79\x20\x4B\x75\x6E\x67\x20\x46\x75")
        expected_matrix = aesutil.bytes_to_matrix("\x00\x1F\x0E\x54\x3C\x4E\x08\x59\x6E\x22\x1B\x0B\x47\x74\x31\x1A")

        result_matrix = AES128Engine.add_round_key(state_matrix, round_key)

        np.testing.assert_array_equal(expected_matrix, result_matrix)

    @staticmethod
    def test_nibble_substitution():
        """ Tests SBox nibble substitution.
        """
        state_matrix = aesutil.bytes_to_matrix("\x00\x1F\x0E\x54\x3C\x4E\x08\x59\x6E\x22\x1B\x0B\x47\x74\x31\x1A")
        expected_matrix = aesutil.bytes_to_matrix("\x63\xC0\xAB\x20\xEB\x2F\x30\xCB\x9F\x93\xAF\x2B\xA0\x92\xC7\xA2")

        result_matrix = AES128Engine.nibble_substitution(state_matrix)

        np.testing.assert_array_equal(expected_matrix, result_matrix)

    @staticmethod
    def test_shift_rows():
        """ Tests AES row shifting.
        """
        state_matrix = aesutil.bytes_to_matrix("\x63\xC0\xAB\x20\xEB\x2F\x30\xCB\x9F\x93\xAF\x2B\xA0\x92\xC7\xA2")
        expected_matrix = aesutil.bytes_to_matrix("\x63\x2F\xAF\xA2\xEB\x93\xC7\x20\x9F\x92\xAB\xCB\xA0\xC0\x30\x2B")

        result_matrix = AES128Engine.shift_rows(state_matrix)

        np.testing.assert_array_equal(expected_matrix, result_matrix)

    @staticmethod
    def test_mix_columns():
        """ Tests AES Galois multiplication.
        """
        state_matrix = aesutil.bytes_to_matrix("\x63\x2F\xAF\xA2\xEB\x93\xC7\x20\x9F\x92\xAB\xCB\xA0\xC0\x30\x2B")
        expected_matrix = aesutil.bytes_to_matrix("\xBA\x75\xF4\x7A\x84\xA4\x8D\x32\xE8\x8D\x06\x0E\x1B\x40\x7D\x5D")

        result_matrix = AES128Engine.mix_columns(state_matrix)

        np.testing.assert_array_equal(expected_matrix, result_matrix)

    def test_encrypt_str(self):
        """ Tests end-to-end encryption of a known string with a known key.
        """
        cipher_key = "\x54\x68\x61\x74\x73\x20\x6D\x79\x20\x4B\x75\x6E\x67\x20\x46\x75"
        plaintext_block = "\x54\x77\x6F\x20\x4F\x6E\x65\x20\x4E\x69\x6E\x65\x20\x54\x77\x6F"
        expected_ciphertext = "\x29\xC3\x50\x5F\x57\x14\x20\xF6\x40\x22\x99\xB3\x1A\x02\xD7\x3A"

        aes128 = AES128Engine(prompt=lambda x: cipher_key)
        aes128.round_keys = AES128Engine.generate_round_keys(cipher_key)
        ciphertext = aes128.encrypt_block(plaintext_block)

        self.assertEqual(ciphertext, expected_ciphertext)

    def test_decrypt_str(self):
        """ Tests end-to-end decryption of a known string with a known key.
        """
        cipher_key = "\x54\x68\x61\x74\x73\x20\x6D\x79\x20\x4B\x75\x6E\x67\x20\x46\x75"
        plaintext_block = "\x54\x77\x6F\x20\x4F\x6E\x65\x20\x4E\x69\x6E\x65\x20\x54\x77\x6F"

        aes128 = AES128Engine(prompt=lambda x: cipher_key)
        aes128.round_keys = AES128Engine.generate_round_keys(cipher_key)
        ciphertext = aes128.encrypt_block(plaintext_block)
        plaintext_result = aes128.decrypt_block(ciphertext)

        self.assertEqual(plaintext_block, plaintext_result)
