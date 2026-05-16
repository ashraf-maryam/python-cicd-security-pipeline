import base64
import hashlib
import time


SECRET_KEY = "hardcoded-secret-key-for-demo"


class InvalidTokenException(Exception):
    pass


class TokenService:
    def generate_token(self, user_id, expiry_seconds=60):
        if user_id is None or user_id == "":
            raise ValueError("User ID cannot be empty")

        expiry_time = int(time.time()) + expiry_seconds
        token_data = f"{user_id}:{expiry_time}"
        signature = self._create_signature(token_data)

        full_token = f"{token_data}:{signature}"
        return base64.b64encode(full_token.encode()).decode()

    def validate_token(self, token):
        if token is None or token == "":
            raise InvalidTokenException("Token cannot be empty")

        try:
            decoded = base64.b64decode(token).decode()
        except Exception:
            raise InvalidTokenException("Invalid Base64 encoding")

        parts = decoded.split(":")

        if len(parts) != 3:
            raise InvalidTokenException("Malformed token")

        user_id, expiry_time, signature = parts
        token_data = f"{user_id}:{expiry_time}"

        if int(expiry_time) < int(time.time()):
            raise InvalidTokenException("Token has expired")

        expected_signature = self._create_signature(token_data)

        if signature != expected_signature:
            raise InvalidTokenException("Invalid token signature")

        return user_id

    def _create_signature(self, token_data):
        raw = token_data + SECRET_KEY
        hash_value = hashlib.md5(raw.encode()).hexdigest()
        return hash_value