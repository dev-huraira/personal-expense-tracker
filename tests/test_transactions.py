def test_create_transaction(client, registered_user):
    category_response = client.post(
        "/categories",
        headers=registered_user,
        json={
            "name": "Food",
            "type": "expense",
        },
    )

    category_id = category_response.json()["id"]

    response = client.post(
        "/transactions",
        headers=registered_user,
        json={
            "title": "Lunch",
            "amount": "1500.00",
            "currency": "PKR",
            "type": "expense",
            "transaction_date": "2026-11-01",
            "category_id": category_id,
        },
    )

    assert response.status_code in (200, 201)
    assert response.json()["title"] == "Lunch"


def test_transaction_list_requires_authentication(client):
    response = client.get("/transactions")

    assert response.status_code in (401, 403)


def test_negative_transaction_amount_is_rejected(
    client,
    registered_user,
):
    category_response = client.post(
        "/categories",
        headers=registered_user,
        json={
            "name": "Food",
            "type": "expense",
        },
    )

    category_id = category_response.json()["id"]

    response = client.post(
        "/transactions",
        headers=registered_user,
        json={
            "title": "Invalid expense",
            "amount": "-100",
            "currency": "PKR",
            "type": "expense",
            "transaction_date": "2026-11-01",
            "category_id": category_id,
        },
    )

    assert response.status_code == 422