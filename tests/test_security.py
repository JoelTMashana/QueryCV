from fastapi import APIRouter
from fastapi.testclient import TestClient
from main import app
from schemas import UserLogin
from routes.users import login

client = TestClient(app)



def test_login_successful(test_user, test_db_session):
    user_credentials = UserLogin(
        email=test_user.email,
        password="plainpassword"  
    )

    result = login(user_credentials, test_db_session)

    assert "access_token" in result
    assert result["token_type"] == "bearer"
