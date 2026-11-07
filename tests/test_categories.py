def test_create_category(client, registered_user):
    response = client.post(
        "/categories",
        headers=registered_user,
        json={
            "name": "Food",
            "type": "expense",
        },
    )

    assert response.status_code in (200, 201)
    assert response.json()["name"] == "Food"


def test_list_categories(client, registered_user):
    client.post(
        "/categories",
        headers=registered_user,
        json={
            "name": "Food",
            "type": "expense",
        },
    )

    response = client.get(
        "/categories",
        headers=registered_user,
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Food"


def test_categories_require_authentication(client):
    response = client.get("/categories")

    assert response.status_code in (401, 403)