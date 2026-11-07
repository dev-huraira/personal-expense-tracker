from app.routes import currency


def test_currency_rates_endpoint(client, monkeypatch):

    async def fake_fetch_exchange_rates(base, quotes):
        return [
            {
                "date": "2026-11-07",
                "base": base,
                "quote": "USD",
                "rate": 0.0035,
            }
        ]

    monkeypatch.setattr(
        currency,
        "fetch_exchange_rates",
        fake_fetch_exchange_rates,
    )

    response = client.get(
        "/currency/rates?base=PKR&quotes=USD"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["rates"][0]["base"] == "PKR"
    assert data["rates"][0]["quote"] == "USD"