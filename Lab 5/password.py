import os
import hashlib
import hmac
from pathlib import Path


PASSWORD_FILE = Path("password.txt")
ITERATIONS = 600_000


def hash_password(password):
    salt = os.urandom(16)

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS
    )

    PASSWORD_FILE.write_text(
        salt.hex() + ":" + hashed.hex(),
        encoding="utf-8"
    )

    print("Password hashed successfully!")
    print(f"Salt: {salt.hex()}")
    print(f"Hash: {hashed.hex()}")


def verify_password(password):
    if not PASSWORD_FILE.exists():
        print("No password hash found!")
        return

    try:
        stored = PASSWORD_FILE.read_text(
            encoding="utf-8"
        ).strip()

        salt_hex, hash_hex = stored.split(":")
        salt = bytes.fromhex(salt_hex)
        stored_hash = bytes.fromhex(hash_hex)

        if len(salt) != 16 or len(stored_hash) != 32:
            raise ValueError("Invalid password record")

    except (ValueError, OSError):
        print("Invalid password file!")
        return

    new_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS
    )

    if hmac.compare_digest(new_hash, stored_hash):
        print("Password is correct!")
    else:
        print("Incorrect password!")