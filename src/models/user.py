import hashlib

class User:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = self._hash_password(password)
        self.tokens = []

    def _hash_password(self, password):
        return hashlib.pbkdf2_hmac('sha256', password.encode(), b'salt', 100000).hex()

    def verify_password(self, password):
        return self.password_hash == self._hash_password(password)
