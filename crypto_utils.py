import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet, InvalidToken

HEADER = b"SC1"
SALT_SIZE = 16
ITERATIONS = 390000


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))


def encrypt_file(input_path: str, output_path: str, password: str) -> None:
    with open(input_path, "rb") as f:
        data = f.read()
    salt = os.urandom(SALT_SIZE)
    key = derive_key(password, salt)
    token = Fernet(key).encrypt(data)
    with open(output_path, "wb") as f:
        f.write(HEADER + salt + token)


def decrypt_file(input_path: str, output_path: str, password: str) -> None:
    with open(input_path, "rb") as f:
        blob = f.read()
    if not blob.startswith(HEADER):
        raise ValueError("Invalid format")
    salt = blob[len(HEADER) : len(HEADER) + SALT_SIZE]
    token = blob[len(HEADER) + SALT_SIZE :]
    key = derive_key(password, salt)
    fernet = Fernet(key)
    try:
        data = fernet.decrypt(token)
    except InvalidToken:
        raise ValueError("Wrong password or corrupted file")
    with open(output_path, "wb") as f:
        f.write(data)
