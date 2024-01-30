from fastapi import Depends, APIRouter
from fastapi.testclient import TestClient
from main import app
from schemas import UserLogin
from routes.users import login
from fastapi import HTTPException
import pytest
from security import create_access_token, get_current_user
from fastapi import Response
from unittest.mock import MagicMock, ANY


client = TestClient(app)


def test_login_successful(test_user, test_db_session):
    user_credentials = UserLogin(
        email=test_user.email,
        password="plainpassword"
    )
    mock_response = Response()
    mock_response.set_cookie = MagicMock()

    result = login(user_credentials, mock_response, test_db_session)

    mock_response.set_cookie.assert_called_once_with(key="access_token", value=ANY, httponly=True, samesite='Strict')

    assert result["message"] == "User logged in successfully."


def test_login_not_successful(test_db_session):
    wrong_user_credentials = UserLogin(
        email="wrongemail@example.com", 
        password="wrongpassword"
    )

    mock_response = Response()
    mock_response.set_cookie = MagicMock()

    with pytest.raises(HTTPException) as info:
        login(wrong_user_credentials, mock_response, test_db_session)

    assert info.value.status_code == 401




