from fastapi.testclient import TestClient

def test_register_user_success(test_client: TestClient):
    """
    Test successful user registration.
    """
    response = test_client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "role": "user"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "hashed_password" not in data
    assert data["role"] == "user"

def test_register_user_duplicate_email(test_client: TestClient):
    """
    Test registration with a duplicate email.
    """
    # First, create a user
    test_client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "role": "user"
        },
    )
    # Then, try to create another user with the same email
    response = test_client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "password456",
            "role": "user"
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_for_access_token_success(test_client: TestClient):
    """
    Test successful login and token generation.
    """
    # First, create a user
    test_client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "role": "user"
        },
    )
    # Then, log in with the user's credentials
    response = test_client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_for_access_token_incorrect_password(test_client: TestClient):
    """
    Test login with an incorrect password.
    """
    # First, create a user
    test_client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "role": "user"
        },
    )
    # Then, try to log in with the wrong password
    response = test_client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_login_for_access_token_nonexistent_user(test_client: TestClient):
    """
    Test login with a non-existent username.
    """
    response = test_client.post(
        "/api/v1/auth/login",
        data={"username": "nonexistent@example.com", "password": "password123"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"