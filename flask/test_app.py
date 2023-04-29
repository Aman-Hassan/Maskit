from werkzeug.security import check_password_hash
from flask import session
from app import app


def test_register(client):
    # Test register with valid data
    response = client.post("/register", data={"name": "new_user", "password": "new_password", "confirmation": "new_password"})
    assert response.status_code == 302
    assert session["user_id"] == 2

    # Test register with invalid data
    response = client.post("/register", data={"name": "", "password": "", "confirmation": ""})
    assert response.status_code == 400
    assert b"must provide username" in response.data
    assert b"must password" in response.data
    assert b"must confirm password" in response.data

    response = client.post("/register", data={"name": "test_user", "password": "test_password", "confirmation": "test_password"})
    assert response.status_code == 400
    assert b"Username is taken" in response.data

    response = client.post("/register", data={"name": "new_user", "password": "new_password", "confirmation": "wrong_password"})
    assert response.status_code == 400
    assert b"password is not same as Confirm Password" in response.data


def test_login(client):
    # Test login with valid data
    response = client.post("/login", data={"name": "test_user", "password": "test_password"})
    assert response.status_code == 302
    assert session["user_id"] == 1

    # Test login with invalid data
    response = client.post("/login", data={"name": "", "password": ""})
    assert response.status_code == 400
    assert b"must provide username" in response.data
    assert b"must provide password" in response.data

    response = client.post("/login", data={"name": "test_user", "password": "wrong_password"})
    assert response.status_code == 403
    assert b"invalid username and/or password" in response.data
