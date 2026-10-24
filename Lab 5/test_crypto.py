import unittest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch

import encryption
import password


class TestCryptography(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp_dir.name)

        self.key_file = self.folder / "secret.key"
        self.password_file = self.folder / "password.txt"

        self.key_patch = patch.object(
            encryption, "KEY_FILE", self.key_file
        )

        self.password_patch = patch.object(
            password, "PASSWORD_FILE", self.password_file
        )

        self.key_patch.start()
        self.password_patch.start()

    def tearDown(self):
        self.key_patch.stop()
        self.password_patch.stop()
        self.temp_dir.cleanup()

    def test_file_encryption(self):
        original = self.folder / "secret.txt"
        original.write_text("Secret message")

        encryption.encrypt_file(str(original))

        encrypted = self.folder / "secret.txt.enc"

        self.assertTrue(encrypted.exists())
        self.assertNotEqual(
            original.read_bytes(),
            encrypted.read_bytes()
        )

    def test_file_decryption(self):
        original = self.folder / "secret.txt"
        original.write_text("Secret message")

        encryption.encrypt_file(str(original))
        encryption.decrypt_file(str(original) + ".enc")

        decrypted = self.folder / "secret_decrypted.txt"

        self.assertTrue(decrypted.exists())
        self.assertEqual(
            original.read_bytes(),
            decrypted.read_bytes()
        )

    def test_different_nonce(self):
        original = self.folder / "secret.txt"
        original.write_text("Secret message")

        encryption.encrypt_file(str(original))

        encrypted = self.folder / "secret.txt.enc"
        first_result = encrypted.read_bytes()

        encryption.encrypt_file(str(original))
        second_result = encrypted.read_bytes()

        self.assertNotEqual(first_result, second_result)

    def test_corrupted_file(self):
        original = self.folder / "secret.txt"
        original.write_text("Secret message")

        encryption.encrypt_file(str(original))

        encrypted = self.folder / "secret.txt.enc"
        data = bytearray(encrypted.read_bytes())

        data[-1] ^= 1
        encrypted.write_bytes(data)

        encryption.decrypt_file(str(encrypted))

        decrypted = self.folder / "secret_decrypted.txt"
        self.assertFalse(decrypted.exists())

    def test_password_hashing(self):
        password.hash_password("MyPassword123")

        self.assertTrue(self.password_file.exists())

        stored = self.password_file.read_text()
        self.assertNotIn("MyPassword123", stored)

    def test_password_verification(self):
        password.hash_password("MyPassword123")

        with patch("builtins.print") as mock_print:
            password.verify_password("MyPassword123")

        mock_print.assert_any_call("Password is correct!")

    def test_wrong_password(self):
        password.hash_password("MyPassword123")

        with patch("builtins.print") as mock_print:
            password.verify_password("WrongPassword")

        mock_print.assert_any_call("Incorrect password!")

    def test_wrong_encryption_key(self):
        original = self.folder / "secret.txt"
        original.write_text("Secret message")

        encryption.encrypt_file(str(original))

        encrypted = self.folder / "secret.txt.enc"

        self.key_file.write_bytes(os.urandom(32))

        encryption.decrypt_file(str(encrypted))

        decrypted = self.folder / "secret_decrypted.txt"
        self.assertFalse(decrypted.exists())


if __name__ == "__main__":
    unittest.main()