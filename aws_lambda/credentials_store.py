import hashlib
import os
from typing import Mapping


class CredentialsStore:
    credentials: Mapping[str, str]
    credentials_file: str
    iterations: int

    def __init__(self, credentials_file: str = ".passwd", iterations: int = 100000):
        self.credentials = {}
        self.credentials_file = credentials_file
        self.iterations = iterations
        self.load()

    def hash_password(self, password: str, custom_salt: bytes = None) -> str:
        """
        Hash the password and return the hashed password.
        """
        salt = custom_salt
        if custom_salt is None:
            salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, self.iterations
        )
        return salt.hex() + "$" + key.hex()

    def validate_password(self, password: str, hashed_password: str) -> bool:
        """
        Validate the password against the hashed password.
        """
        salt, *_ = hashed_password.split("$")
        current_password = self.hash_password(password, custom_salt=bytes.fromhex(salt))
        return current_password == hashed_password

    def add(self, username: str, password: str):
        hashed_password = self.hash_password(password)
        self.credentials[username.lower()] = hashed_password

    def save(self):
        with open(self.credentials_file, "w") as out_file:
            for username, hashed_password in self.credentials.items():
                out_file.write(f"{username}:{hashed_password}\n")

    def load(self):
        try:
            with open(self.credentials_file, "r") as f:
                for line in f:
                    if ":" not in line:
                        continue
                    username, hashed_password = line.strip().split(":")
                    self.credentials[username] = hashed_password
        except FileNotFoundError:
            self.save()
            self.load()

    def validate(self, username: str, password: str) -> bool:
        username = username.lower()
        if username not in self.credentials:
            return False

        return self.validate_password(password, self.credentials[username])
