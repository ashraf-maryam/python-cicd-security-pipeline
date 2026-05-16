import base64
import time
import pytest
from token_service import TokenService, InvalidTokenException


def test_generate_token_success():
    service = TokenService()
    token = service.generate_token("maryam123")
    assert token is not None
    assert isinstance(token, str)


def test_generate_token_invalid_user_id():
    service = TokenService()

    with pytest.raises(ValueError):
        service.generate_token("")


def test_validate_token_success():
    service = TokenService()
    token = service.generate_token("maryam123")
    user_id = service.validate_token(token)

    assert user_id == "maryam123"


def test_validate_null_token():
    service = TokenService()

    with pytest.raises(InvalidTokenException):
        service.validate_token(None)


def test_validate_empty_token():
    service = TokenService()

    with pytest.raises(InvalidTokenException):
        service.validate_token("")


def test_validate_malformed_token():
    service = TokenService()
    bad_token = base64.b64encode("bad:token".encode()).decode()

    with pytest.raises(InvalidTokenException):
        service.validate_token(bad_token)


def test_validate_invalid_base64():
    service = TokenService()

    with pytest.raises(InvalidTokenException):
        service.validate_token("not-valid-base64!!!")


def test_validate_expired_token():
    service = TokenService()
    token = service.generate_token("maryam123", expiry_seconds=-1)

    with pytest.raises(InvalidTokenException):
        service.validate_token(token)


def test_validate_tampered_token():
    service = TokenService()
    token = service.generate_token("maryam123")

    decoded = base64.b64decode(token).decode()
    tampered = decoded.replace("maryam123", "attacker")
    tampered_token = base64.b64encode(tampered.encode()).decode()

    with pytest.raises(InvalidTokenException):
        service.validate_token(tampered_token)