def _create_product(client, sku: str, price: str, stock: int, headers: dict) -> dict:
    response = client.post(
        "/api/v1/products",
        headers=headers,
        json={
            "name": f"Product {sku}",
            "sku": sku,
            "price": price,
            "stock_quantity": stock,
        },
    )
    assert response.status_code == 201
    return response.json()


def _create_customer(client, email: str, full_name: str = "Jane Doe") -> dict:
    response = client.post(
        "/api/v1/customers",
        json={"full_name": full_name, "email": email, "phone": "555-0100"},
    )
    assert response.status_code == 201
    return response.json()


def _create_order(client, customer_id: int, product_id: int, quantity: int = 1) -> dict:
    response = client.post(
        "/api/v1/orders",
        json={
            "customer_id": customer_id,
            "items": [{"product_id": product_id, "quantity": quantity}],
        },
    )
    assert response.status_code == 201
    return response.json()


def test_pagination_metadata(client, admin_headers):
    product = _create_product(client, "pg-1", "10.00", 100, admin_headers)
    customer = _create_customer(client, "paginate@example.com")

    for _ in range(3):
        _create_order(client, customer["id"], product["id"])

    response = client.get("/api/v1/orders?page=1&limit=2")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 3
    assert body["page"] == 1
    assert body["limit"] == 2
    assert len(body["data"]) == 2


def test_search_by_customer_email(client, admin_headers):
    product = _create_product(client, "pg-2", "5.00", 50, admin_headers)
    customer = _create_customer(client, "findme@acme.com", "Acme Buyer")
    _create_order(client, customer["id"], product["id"])

    response = client.get("/api/v1/orders", params={"search": "findme@acme"})
    body = response.json()
    assert body["total"] >= 1
    assert body["data"][0]["customer_name"] == "Acme Buyer"


def test_search_by_order_id(client, admin_headers):
    product = _create_product(client, "pg-3", "8.00", 50, admin_headers)
    customer = _create_customer(client, "orderid@example.com")
    order = _create_order(client, customer["id"], product["id"])

    response = client.get("/api/v1/orders", params={"search": str(order["id"])})
    body = response.json()
    assert body["total"] == 1
    assert body["data"][0]["id"] == order["id"]


def test_sort_highest_total(client, admin_headers):
    product = _create_product(client, "pg-4", "10.00", 100, admin_headers)
    customer = _create_customer(client, "sort@example.com")
    _create_order(client, customer["id"], product["id"], quantity=1)
    _create_order(client, customer["id"], product["id"], quantity=5)

    response = client.get("/api/v1/orders", params={"sort": "highest_total", "limit": 10})
    totals = [row["total_amount"] for row in response.json()["data"]]
    assert totals == sorted(totals, reverse=True)


def test_invalid_pagination_returns_422(client):
    response = client.get("/api/v1/orders", params={"page": 0})
    assert response.status_code == 422

    response = client.get("/api/v1/orders", params={"limit": 200})
    assert response.status_code == 422


def test_invalid_sort_returns_422(client):
    response = client.get("/api/v1/orders", params={"sort": "invalid"})
    assert response.status_code == 422
