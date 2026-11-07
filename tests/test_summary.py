def test_empty_month_returns_empty_summaries(
    client,
    registered_user,
):
    response = client.get(
        "/summary?year=2025&month=1",
        headers=registered_user,
    )

    assert response.status_code == 200
    assert response.json()["summaries"] == []


def test_summary_rejects_invalid_month(
    client,
    registered_user,
):
    response = client.get(
        "/summary?year=2026&month=13",
        headers=registered_user,
    )

    assert response.status_code == 422