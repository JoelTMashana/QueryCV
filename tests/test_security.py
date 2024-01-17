from fastapi import APIRouter
from fastapi.testclient import TestClient
from main import app
from schemas import UserLogin
from routes.users import login
from fastapi import HTTPException
import pytest

client = TestClient(app)



def test_login_successful(test_user, test_db_session):
    
    user_credentials = UserLogin(
        email=test_user.email,
        password="plainpassword"  
    )

    result = login(user_credentials, test_db_session)

    assert "access_token" in result
    assert result["token_type"] == "bearer"



def test_login_not_successful(test_user, test_db_session):
    wrong_user_credentials = UserLogin(
        email="wrongemail@example.com", 
        password="wrongpassword" 
    )
    with pytest.raises(HTTPException) as info:
        login(wrong_user_credentials, test_db_session)

    assert info.value.status_code == 401

