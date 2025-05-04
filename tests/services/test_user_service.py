import pytest
from unittest.mock import Mock, patch
from services import user_service
from models.user_model import UserModel
from schemas.user_schema import UserCreateSchema

@pytest.fixture
def mock_db():
    return Mock()

def test_get_user_by_email_calls_repository(mock_db):
    with patch("services.user_service.user_repository.get_user_by_email", return_value="user") as mock_get:
        result = user_service.get_user_by_email("email@test.com", mock_db)
        mock_get.assert_called_once_with(mock_db, "email@test.com")
        assert result == "user"

def test_create_user_hashes_password_and_calls_repository(mock_db):
    user_data = UserCreateSchema(
        first_name="John",
        last_name="Doe",
        date_of_birth="2000-01-01",
        email="john@example.com",
        hashed_password="plaintext"
    )

    with patch("services.user_service.user_repository.create_user") as mock_create, \
         patch("services.user_service.hash.bcrypt.hash", return_value="hashed_pass"):
        result = user_service.create_user(user_data, mock_db)
        mock_create.assert_called_once()
        assert isinstance(result, UserModel)
        assert result.hashed_password == "hashed_pass"

def test_authenticate_user_success(mock_db):
    mock_user = Mock()
    mock_user.verify_password.return_value = True
    with patch("services.user_service.get_user_by_email", return_value=mock_user):
        result = user_service.authenticate_user("user@example.com", "correctpass", mock_db)
        assert result == mock_user

def test_authenticate_user_user_not_found(mock_db):
    with patch("services.user_service.get_user_by_email", return_value=None):
        result = user_service.authenticate_user("user@example.com", "pass", mock_db)
        assert result is False

def test_authenticate_user_wrong_password(mock_db):
    mock_user = Mock()
    mock_user.verify_password.return_value = False
    with patch("services.user_service.get_user_by_email", return_value=mock_user):
        result = user_service.authenticate_user("user@example.com", "wrongpass", mock_db)
        assert result is False

def test_create_token_returns_jwt():
    user = Mock(id="user-id")
    with patch("services.user_service.user_schema.UserSchema.from_orm"), \
         patch("services.user_service.create_access_token", return_value="jwt-token") as mock_create:
        result = user_service.create_token(user)
        mock_create.assert_called_once_with(identity="user-id")
        assert result == {"access_token": "jwt-token", "token_type": "bearer"}
