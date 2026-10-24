# Lab 5 — Cryptography Application

## Overview

This project demonstrates two real-world applications of cryptography using Python.

The application implements:

1. File encryption and decryption using AES-256-GCM.
2. Password hashing and verification using PBKDF2-HMAC-SHA256.

Additionally, VeraCrypt was used to demonstrate encryption with open-source software.

## Technologies

- Python 3
- cryptography library
- hashlib
- hmac
- unittest
- VeraCrypt

## Features

### 1. File Encryption

The application uses AES-256-GCM to encrypt and decrypt files.

- 256-bit encryption key
- 96-bit random nonce
- Authenticated encryption
- Detection of modified ciphertext

### 2. Password Hashing

The application uses PBKDF2-HMAC-SHA256 to securely derive and verify password hashes.

- Random 128-bit salt
- 600,000 iterations
- Constant-time hash comparison

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

## Running Tests

```bash
python -m unittest test_crypto.py -v
```

## VeraCrypt Demonstration

VeraCrypt is an open-source disk encryption application.

Demonstration procedure:

1. Create an encrypted file container.
2. Select AES encryption.
3. Set a password.
4. Mount the encrypted volume.
5. Create and store a test file.
6. Dismount the volume.
7. Verify that an incorrect password prevents mounting.
8. Mount with the correct password and verify file integrity.

## Security Notes

This is an educational demonstration, not a production-ready security system.

The AES key is stored locally without additional protection, and files are processed entirely in memory. Password verification parameters are fixed in the code. Real applications require stronger key management and more robust data handling.

## Conclusion

The project demonstrates the difference between reversible encryption and one-way password hashing, as well as the practical application of cryptography in VeraCrypt.
