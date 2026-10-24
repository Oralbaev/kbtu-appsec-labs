import os
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag


KEY_FILE = Path("secret.key")


def load_key():
    if KEY_FILE.exists():
        key = KEY_FILE.read_bytes()

        if len(key) != 32:
            raise ValueError("Invalid AES key length")

        return key

    key = AESGCM.generate_key(bit_length=256)
    KEY_FILE.write_bytes(key)
    return key


def encrypt_file(filename):
    path = Path(filename)

    if not path.is_file():
        print("File not found!")
        return

    key = load_key()
    aes = AESGCM(key)

    nonce = os.urandom(12)
    data = path.read_bytes()

    encrypted = aes.encrypt(nonce, data, None)

    output = path.with_name(path.name + ".enc")
    output.write_bytes(nonce + encrypted)

    print(f"Encrypted file saved: {output}")


def decrypt_file(filename):
    path = Path(filename)

    if not path.is_file():
        print("File not found!")
        return

    if not KEY_FILE.exists():
        print("Secret key not found!")
        return

    key = load_key()
    aes = AESGCM(key)

    encrypted_data = path.read_bytes()

    if len(encrypted_data) < 28:
        print("Invalid encrypted file!")
        return

    nonce = encrypted_data[:12]
    ciphertext = encrypted_data[12:]

    try:
        decrypted = aes.decrypt(nonce, ciphertext, None)
    except InvalidTag:
        print("Decryption failed! Wrong key or corrupted file.")
        return

    if path.suffix != ".enc":
        print("Expected a .enc file!")
        return

    original = path.with_suffix("")
    output = original.with_name(original.stem + "_decrypted" + original.suffix)

    if output.exists():
        print(f"Output file already exists: {output}")
        return

    output.write_bytes(decrypted)
    print(f"Decrypted file saved: {output}")