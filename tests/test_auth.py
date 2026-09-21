from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_student_signup_and_login_flow():
    email = "student@example.com"
    student = {"name": "Ava Student", "email": email, "password": "secret123", "role": "student"}

    register_response = client.post("/auth/register", json=student)
    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={"email": email, "password": "secret123", "role": "student"},
    )
    assert login_response.status_code == 200
    payload = login_response.json()
    assert payload["email"] == email
    assert payload["role"] == "student"


def test_admin_login_with_valid_credentials():
    response = client.post(
        "/auth/login",
        json={"email": "admin@mergington.edu", "password": "admin123", "role": "admin"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["role"] == "admin"
    assert payload["email"] == "admin@mergington.edu"


def test_student_cannot_log_in_as_admin_or_admin_as_student():
    student_response = client.post(
        "/auth/login",
        json={"email": "student@example.com", "password": "secret123", "role": "admin"},
    )
    assert student_response.status_code == 403

    admin_response = client.post(
        "/auth/login",
        json={"email": "admin@mergington.edu", "password": "admin123", "role": "student"},
    )
    assert admin_response.status_code == 403


def test_duplicate_registration_is_rejected():
    response = client.post(
        "/auth/register",
        json={"name": "Ava Student", "email": "student@example.com", "password": "secret123", "role": "student"},
    )
    assert response.status_code == 409
