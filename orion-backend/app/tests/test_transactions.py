from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.modules.auth import service as auth_service
from app.modules.auth.schemas import UserCreate

def get_auth_headers(test_client: TestClient, db: Session) -> dict[str, str]:
    """
    Helper function to create a user, log in, and return auth headers.
    """
    user_data = UserCreate(email="test_transactions@example.com", password="password123", role="user")
    auth_service.create_user(db=db, user=user_data)

    login_response = test_client.post(
        "/api/v1/auth/login",
        data={"username": user_data.email, "password": user_data.password},
    )
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_and_read_transaction(test_client: TestClient, db_session: Session):
    """
    Test creating a transaction and then reading it back.
    """
    headers = get_auth_headers(test_client, db_session)

    # Create a transaction
    transaction_data = {
        "date": "2025-01-01T00:00:00",
        "description": "Coffee",
        "amount": -4.50,
        "category": "Food",
        "account": "Checking",
        "status": "completed"
    }
    create_response = test_client.post(
        "/api/v1/transactions/",
        json=transaction_data,
        headers=headers,
    )
    assert create_response.status_code == 200
    created_transaction = create_response.json()
    assert created_transaction["description"] == "Coffee"
    assert created_transaction["amount"] == -4.50

    # Read transactions and verify the new one is there
    read_response = test_client.get("/api/v1/transactions/", headers=headers)
    assert read_response.status_code == 200
    transactions = read_response.json()
    assert len(transactions) == 1
    assert transactions[0]["description"] == "Coffee"

def test_unauthenticated_access(test_client: TestClient):
    """
    Test that unauthenticated users cannot access transaction endpoints.
    """
    # Test GET without auth
    read_response = test_client.get("/api/v1/transactions/")
    assert read_response.status_code == 401
    assert read_response.json()["detail"] == "Not authenticated"

    # Test POST without auth
    transaction_data = {
        "date": "2025-01-01T00:00:00",
        "description": "Lunch",
        "amount": -12.00,
        "category": "Food",
        "account": "Credit Card",
        "status": "completed"
    }
    create_response = test_client.post("/api/v1/transactions/", json=transaction_data)
    assert create_response.status_code == 401
    assert create_response.json()["detail"] == "Not authenticated"