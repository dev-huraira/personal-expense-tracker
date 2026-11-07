def test_missing_endpoint_returns_404(client):
    response = client.get("/this-endpoint-does-not-exist")

    assert response.status_code == 404
    assert response.json()["error"] == "HTTP error"


def test_invalid_transaction_returns_422(
    client,
    registered_user,
):
    response = client.post(
        "/transactions",
        headers=registered_user,
        json={
            "title": "Invalid transaction",
            "amount": "-100",
            "currency": "PKR",
            "type": "expense",
            "transaction_date": "2026-11-01",
            "category_id": 999,
        },
    )

    assert response.status_code == 422
    assert response.json()["error"] == "Validation error"


def test_missing_user_profile_requires_authentication(client):
    response = client.get("/users/me")

    assert response.status_code in (401, 403)