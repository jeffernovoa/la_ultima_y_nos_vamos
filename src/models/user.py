import hashlib
from typing import List
from uuid import uuid4

class User:
    def __init__(self, username: str, password: str, tokens: List[str] = None, user_id: str = None):
        self.user_id = user_id or str(uuid4())
        self.username = username
        self.password_hash = self._hash_password(password)
        self.tokens = tokens or []

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str) -> bool:
        return self.password_hash == self._hash_password(password)

    def add_token(self, token_id: str):
        if token_id not in self.tokens:
            self.tokens.append(token_id)

    def remove_token(self, token_id: str):
        if token_id in self.tokens:
            self.tokens.remove(token_id)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password_hash": self.password_hash,
            "tokens": self.tokens,
        }

    @staticmethod
    def from_dict(data: dict):
        return User(
            username=data["username"],
            password="",  # no se necesita para reconstrucción
            tokens=data.get("tokens", []),
            user_id=data["user_id"]
        )
