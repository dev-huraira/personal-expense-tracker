def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "sara",
            "email": "sara@example.com",
            "password": "SecurePass123!",
        },
    )

    assert response.status_code in (200, 201)
    assert response.json()["email"] == "sara@example.com"


def test_duplicate_email_is_rejected(client):
    payload = {
        "username": "ali",
        "email": "ali@example.com",
        "password": "SecurePass123!",
    }

    first_response = client.post("/auth/register", json=payload)
    second_response = client.post("/auth/register", json=payload)

    assert first_response.status_code in (200, 201)
    assert second_response.status_code == 409


def test_login_user(client):
    client.post(
        "/auth/register",
        json={
            "username": "ali",
            "email": "ali@example.com",
            "password": "SecurePass123!",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "ali@example.com",
            "password": "SecurePass123!",
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_user_profile_requires_authentication(client):
    response = client.get("/users/me")

    assert response.status_code in (401, 403)