def test_dashboard_stats(client, admin_headers):
    client.post(
        "/api/v1/products",
        headers=admin_headers,
        json={
            "name": "Dash Product",
            "sku": "dash-01",
            "price": "100.00",
            "stock_quantity": 50,
        },
    )
    customer = client.post(
        "/api/v1/customers",
        json={
            "full_name": "Dash Customer",
            "email": "dash@example.com",
            "phone": "555",
        },
    ).json()

    client.post(
        "/api/v1/orders",
        json={
            "customer_id": customer["id"],
            "items": [{"product_id": 1, "quantity": 2}],
        },
    )

    response = client.get("/api/v1/dashboard/stats")
    assert response.status_code == 200
    body = response.json()
    assert body["total_orders"] >= 1
    assert float(body["total_revenue"]) >= 200.0
    assert len(body["recent_orders"]) >= 1
