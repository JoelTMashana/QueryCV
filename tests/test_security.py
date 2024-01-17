from fastapi import APIRouter
from fastapi.testclient import TestClient
from main import app
from schemas import UserLogin
from routes.users import login
from fastapi import HTTPException
import pytest
from security import create_access_token
import logging

client = TestClient(app)

def test_login_successful(test_user, test_db_session):
    
    user_credentials = UserLogin(
        email=test_user.email,
        password="plainpassword"  
    )

    result = login(user_credentials, test_db_session)

    assert "access_token" in result
    assert result["token_type"] == "bearer"



def test_login_not_successful(test_db_session):
    wrong_user_credentials = UserLogin(
        email="wrongemail@example.com", 
        password="wrongpassword" 
    )
    with pytest.raises(HTTPException) as info:
        login(wrong_user_credentials, test_db_session)

    assert info.value.status_code == 401



def test_protected_get_user_experiences_route_access_with_valid_token(test_user, test_db_session):
    
    logging.info("Starting test: test_protected_get_user_experiences_route_access_with_valid_token")
    valid_token = create_access_token({"sub": str(test_user.user_id)})
    headers = {"Authorization": f"Bearer {valid_token}"}
    response = client.get("/api/v1/users/1/experiences", headers=headers) # Sends requests to protected route 
    assert response.status_code == 200
    logging.info("Finished test: test_protected_get_user_experiences_route_access_with_valid_token")

def test_protected_get_user_experiences_route_access_with_invalid_token():
    invalid_token = "invalid"
    headers = {"Authorization": f"Bearer {invalid_token}"}
    response = client.get("/api/v1/users/1/experiences", headers=headers)
    assert response.status_code == 401

def test_protected_get_user_experiences_route_access_without_token():
    response = client.get("/api/v1/users/1/experiences")
    assert response.status_code == 401
