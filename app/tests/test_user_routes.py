# tests/test_auth_routes.py
import pytest
from app.models.user import User
from sqlalchemy.exc import IntegrityError

# AttributeError: 'Flask' object has no attribute 'login_manager'
# Solution: the flask_login_fixture initializes the app with the LoginManager
def test_authenticate_authenticated_user(client, db_session, flask_login_fixture):
    """
    Test the authenticate endpoint when a user is logged in.
    """
    user = User(name="testuser")
    user.set_password("password123")
    db_session.add(user)
    db_session.commit()

    response_login = client.post("/api/v2/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })

    assert response_login.status_code == 200

    response = client.get("/api/v2/auth/")

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["data"]["name"] == "testuser"
    assert json_data["error"] is None

def test_authenticate_unauthenticated_user(client, db_session, flask_login_fixture):
    """
    Test the authenticate endpoint when no user is logged in.
    """
    response = client.get("/api/v2/auth/")

    assert response.status_code == 401
    json_data = response.get_json()
    assert json_data["data"] == None
    assert json_data["error"] == "Unauthorized"

def test_login_success(client, db_session, flask_login_fixture):
    """
    Test successful login with valid credentials.
    """
    user = User(name="loginuser")
    user.set_password("securepassword")
    db_session.add(user)
    db_session.commit()

    response = client.post("/api/v2/auth/login", json={
        "username": "loginuser",
        "password": "securepassword"
    })

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["data"]["name"] == "loginuser"
    assert json_data["error"] is None

def test_login_missing_fields(client, db_session, flask_login_fixture):
    """
    Test login with missing username or password.
    """
    response = client.post("/api/v2/auth/login", json={
        "username": "userwithoutpassword"
    })

    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["data"] == None
    assert json_data["error"] == "Missing username or password."

    response = client.post("/api/v2/auth/login", json={
        "password": "passwordwithoutusername"
    })

    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["data"] == None
    assert json_data["error"] == "Missing username or password."

def test_login_invalid_credentials(client, db_session, flask_login_fixture):
    """
    Test login with invalid username or password.
    """
    user = User(name="invaliduser")
    user.set_password("validpassword")
    db_session.add(user)
    db_session.commit()

    response = client.post("/api/v2/auth/login", json={
        "username": "wronguser",
        "password": "validpassword"
    })

    assert response.status_code == 401
    json_data = response.get_json()
    assert json_data["data"] == None
    assert json_data["error"] == "Invalid username or password."

    response = client.post("/api/v2/auth/login", json={
        "username": "invaliduser",
        "password": "wrongpassword"
    })

    assert response.status_code == 401
    json_data = response.get_json()
    assert json_data["data"] == None
    assert json_data["error"] == "Invalid username or password."

def test_logout_success(client, db_session, flask_login_fixture):
    """
    Test successful logout when a user is logged in.
    """
    user = User(name="logoutuser")
    user.set_password("logoutpassword")
    db_session.add(user)
    db_session.commit()

    response_login = client.post("/api/v2/auth/login", json={
        "username": "logoutuser",
        "password": "logoutpassword"
    })

    assert response_login.status_code == 200

    response = client.post("/api/v2/auth/logout")

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["data"]["message"] == "User logged out"
    assert json_data["error"] is None

    # Verify the user is logged out
    response = client.get("/api/v2/auth/")
    assert response.status_code == 401

def test_logout_without_login(client, db_session, flask_login_fixture):
    """
    Test logout when no user is logged in.
    """
    response = client.post("/api/v2/auth/logout")

    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["data"] == None
    assert json_data["error"] == "User not logged in."

def test_signup_success(client, db_session, flask_login_fixture):
    """
    Test successful user signup with valid credentials.
    """
    response = client.post("/api/v2/auth/signup", json={
        "username": "newuser",
        "password": "newpassword"
    })

    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["error"] is None
    assert json_data["data"]["name"] == "newuser"
    # Ensure password is not exposed when creating a user, indirectly testing the to_dict method under User as well
    assert "password" not in json_data["data"]
    assert "password_hash" not in json_data["data"]

    response = client.get("/api/v2/auth/")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["data"]["name"] == "newuser"

def test_signup_missing_fields(client, db_session, flask_login_fixture):
    """
    Test signup with missing username or password.
    """
    response = client.post("/api/v2/auth/signup", json={
        "username": "userwithoutpassword"
    })

    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["data"] == None
    assert json_data["error"] == "Missing username or password."

    response = client.post("/api/v2/auth/signup", json={
        "password": "passwordwithoutusername"
    })

    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["data"] == None
    assert json_data["error"] == "Missing username or password."

def test_signup_username_already_exists(client, db_session, flask_login_fixture):
    """
    Test signup with a username that already exists.
    """
    user = User(name="existinguser")
    user.set_password("password")
    db_session.add(user)
    db_session.commit()

    response = client.post("/api/v2/auth/signup", json={
        "username": "existinguser",
        "password": "newpassword"
    })

    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["data"] == None
    assert json_data["error"] == "Username already exists."
