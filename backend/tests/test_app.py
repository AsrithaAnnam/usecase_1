
import psycopg2
from werkzeug.security import generate_password_hash

from unittest.mock import MagicMock, patch

from backend.app import app


def client():
    app.config["TESTING"] = True
    return app.test_client()


def mock_database(rows=None, row=None):
    conn = MagicMock()
    cursor = MagicMock()
    conn.__enter__.return_value = conn
    conn.cursor.return_value.__enter__.return_value = cursor
    cursor.fetchall.return_value = rows if rows is not None else []
    cursor.fetchone.return_value = row
    return conn


def test_health_check():
    response = client().get("/api/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_get_claims_success():
    conn = mock_database(rows=[{"id": 1, "customer_name": "Ravi"}])
    with patch("backend.app.get_db", return_value=conn):
        response = client().get("/api/claims")
    assert response.status_code == 200
    assert response.get_json()[0]["customer_name"] == "Ravi"

def test_get_claims_database_error():
    with patch(
        "backend.app.get_db",
        side_effect=__import__("psycopg2").OperationalError("DB error")
    ):
        response = client().get("/api/claims")
    assert response.status_code == 500

def test_create_claim_missing_fields():
    response = client().post("/api/claims", json={"customer_name": "Ravi"})
    assert response.status_code == 400


def test_create_claim_invalid_json():
    response = client().post(
        "/api/claims", data="invalid", content_type="application/json"
    )
    assert response.status_code == 400


def test_create_claim_success():
    conn = mock_database(
        row={"id": 1, "customer_name": "Ravi", "amount": 100}
    )
    with patch("backend.app.get_db", return_value=conn):
        response = client().post(
            "/api/claims",
            json={"customer_name": "Ravi", "amount": 100}
        )
    assert response.status_code == 201


def test_update_claim_invalid_status():
    response = client().put("/api/claims/1", json={"status": "Unknown"})
    assert response.status_code == 400


def test_update_claim_not_found():
    conn = mock_database(row=None)
    with patch("backend.app.get_db", return_value=conn):
        response = client().put(
            "/api/claims/999", json={"status": "Approved"}
        )
    assert response.status_code == 404


def test_register_missing_fields():
    response = client().post(
        "/api/register",
        json={"name": "Ravi", "email": "ravi@example.com"}
    )
    assert response.status_code == 400


def test_register_invalid_json():
    response = client().post(
        "/api/register", data="invalid", content_type="application/json"
    )
    assert response.status_code == 400


def test_login_missing_fields():
    response = client().post(
        "/api/login", json={"email": "ravi@example.com"}
    )
    assert response.status_code == 400


def test_login_invalid_json():
    response = client().post(
        "/api/login", data="invalid", content_type="application/json"
    )
    assert response.status_code == 400

def test_create_claim_database_error():
    with patch(
        "backend.app.get_db",
        side_effect=psycopg2.OperationalError("DB error")
    ):
        response = client().post(
            "/api/claims",
            json={"customer_name": "Ravi", "amount": 100}
        )
    assert response.status_code == 500


def test_create_claim_missing_customer_name():
    response = client().post(
        "/api/claims",
        json={"amount": 100}
    )
    assert response.status_code == 400


def test_update_claim_invalid_json():
    response = client().put(
        "/api/claims/1",
        data="invalid",
        content_type="application/json"
    )
    assert response.status_code == 400


def test_update_claim_success():
    conn = mock_database(
        row={"id": 1, "status": "Approved", "customer_name": "Ravi"}
    )
    with patch("backend.app.get_db", return_value=conn):
        response = client().put(
            "/api/claims/1",
            json={"status": "Approved"}
        )
    assert response.status_code == 200
    assert response.get_json()["status"] == "Approved"


def test_update_claim_database_error():
    with patch(
        "backend.app.get_db",
        side_effect=psycopg2.OperationalError("DB error")
    ):
        response = client().put(
            "/api/claims/1",
            json={"status": "Approved"}
        )
    assert response.status_code == 500


def test_register_success():
    conn = mock_database(
        row={"id": 1, "name": "Ravi", "email": "ravi@example.com"}
    )
    with patch("backend.app.get_db", return_value=conn):
        response = client().post(
            "/api/register",
            json={
                "name": "Ravi",
                "email": "ravi@example.com",
                "password": "TestPassword123!"
            }
        )
    assert response.status_code == 201
    assert response.get_json()["email"] == "ravi@example.com"


def test_register_duplicate_email():
    conn = mock_database()
    conn.cursor.return_value.__enter__.return_value.execute.side_effect = (
        psycopg2.errors.UniqueViolation("duplicate email")
    )
    with patch("backend.app.get_db", return_value=conn):
        response = client().post(
            "/api/register",
            json={
                "name": "Ravi",
                "email": "ravi@example.com",
                "password": "TestPassword123!"
            }
        )
    assert response.status_code == 409


def test_register_database_error():
    with patch(
        "backend.app.get_db",
        side_effect=psycopg2.OperationalError("DB error")
    ):
        response = client().post(
            "/api/register",
            json={
                "name": "Ravi",
                "email": "ravi@example.com",
                "password": "TestPassword123!"
            }
        )
    assert response.status_code == 500


def test_login_user_not_found():
    conn = mock_database(row=None)
    with patch("backend.app.get_db", return_value=conn):
        response = client().post(
            "/api/login",
            json={
                "email": "unknown@example.com",
                "password": "TestPassword123!"
            }
        )
    assert response.status_code == 401


def test_login_wrong_password():
    conn = mock_database(
        row={
            "id": 1,
            "name": "Ravi",
            "email": "ravi@example.com",
            "password_hash": generate_password_hash("CorrectPassword123!")
        }
    )
    with patch("backend.app.get_db", return_value=conn):
        response = client().post(
            "/api/login",
            json={
                "email": "ravi@example.com",
                "password": "WrongPassword123!"
            }
        )
    assert response.status_code == 401


def test_login_success():
    conn = mock_database(
        row={
            "id": 1,
            "name": "Ravi",
            "email": "ravi@example.com",
            "password_hash": generate_password_hash("TestPassword123!")
        }
    )
    with patch("backend.app.get_db", return_value=conn):
        response = client().post(
            "/api/login",
            json={
                "email": "ravi@example.com",
                "password": "TestPassword123!"
            }
        )
    assert response.status_code == 200
    assert response.get_json()["message"] == "Login successful"
    assert response.get_json()["user"]["name"] == "Ravi"


def test_login_database_error():
    with patch(
        "backend.app.get_db",
        side_effect=psycopg2.OperationalError("DB error")
    ):
        response = client().post(
            "/api/login",
            json={
                "email": "ravi@example.com",
                "password": "TestPassword123!"
            }
        )
    assert response.status_code == 500

