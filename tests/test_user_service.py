import pytest
from unittest.mock import MagicMock
from src.services.user_service import UserService
import hashlib

@pytest.fixture
def user_service():
    return UserService()

def test_register_and_login(user_service):
    # Mocks para el repositorio
    user_service.user_repo = MagicMock()
    user_service.user_repo.get_by_username.return_value = None

    # Registro exitoso
    result = user_service.register("user1", "password123")
    assert result is True
    user_service.user_repo.save.assert_called_once()
    
    # Registro usuario ya existe
    user_service.user_repo.get_by_username.return_value = {"username": "user1"}
    result = user_service.register("user1", "pass")
    assert result is False

def test_login(user_service):
    # Password correcto
    fake_hash = hashlib.pbkdf2_hmac('sha256', b'password123', b'salt123', 100000).hex()
    user_service.user_repo.get_by_username = MagicMock(return_value={
        "username": "user1",
        "password_hash": fake_hash,
        "salt": b'salt123'
    })

    token = user_service.login("user1", "password123")
    assert token is not None
    assert isinstance(token, str)

    # Password incorrecto
    token = user_service.login("user1", "wrongpass")
    assert token is None

    # Usuario no existe
    user_service.user_repo.get_by_username = MagicMock(return_value=None)
    token = user_service.login("user2", "password123")
    assert token is None