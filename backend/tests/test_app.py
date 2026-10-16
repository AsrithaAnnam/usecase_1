
from backend.app import app


def test_health_check():
    client = app.test_client()

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "healthy",
        "service": "claims-backend"
    }


def test_create_claim_missing_fields():
    client = app.test_client()

    response = client.post(
        "/api/claims",
        json={"customer_name": "Ravi"}
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == (
        "Customer name and amount are required"
    )


def test_update_claim_invalid_status():
    client = app.test_client()

    response = client.put(
        "/api/claims/1",
        json={"status": "Unknown"}
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid status"


def test_register_missing_fields():
    client = app.test_client()

    response = client.post(
        "/api/register",
        json={"name": "Ravi", "email": "ravi@example.com"}
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "All fields are required"


def test_login_missing_fields():
    client = app.test_client()

    response = client.post(
        "/api/login",
        json={"email": "ravi@example.com"}
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == (
        "Email and password are required"
    )
