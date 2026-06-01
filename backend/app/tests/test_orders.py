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


def _create_customer(client, email: str) -> dict:
    response = client.post(
        "/api/v1/customers",
        json={
            "full_name": "Jane Doe",
            "email": email,
            "phone": "555-0100",
        },
    )
    assert response.status_code == 201
    return response.json()


def test_create_order_reduces_stock_and_calculates_total(client, admin_headers):
    product_a = _create_product(client, "ord-p1a", "10.00", 20, admin_headers)
    product_b = _create_product(client, "ord-p1b", "5.00", 10, admin_headers)
    customer = _create_customer(client, "jane@example.com")

    response = client.post(
        "/api/v1/orders",
        json={
            "customer_id": customer["id"],
            "items": [
                {"product_id": product_a["id"], "quantity": 3},
                {"product_id": product_b["id"], "quantity": 2},
            ],
        },
    )
    assert response.status_code == 201
    order = response.json()
    assert order["total_amount"] == "40.00"
    assert order["status"] == "active"
    assert len(order["items"]) == 2

    product_a_after = client.get(f"/api/v1/products/{product_a['id']}").json()
    product_b_after = client.get(f"/api/v1/products/{product_b['id']}").json()
    assert product_a_after["stock_quantity"] == 17
    assert product_b_after["stock_quantity"] == 8


def test_duplicate_products_in_order_rejected(client, admin_headers, db_session):
    product = _create_product(client, "ord-dup", "10.00", 20, admin_headers)
    customer = _create_customer(client, "dup@example.com")

    response = client.post(
        "/api/v1/orders",
        json={
            "customer_id": customer["id"],
            "items": [
                {"product_id": product["id"], "quantity": 2},
                {"product_id": product["id"], "quantity": 1},
            ],
        },
    )
    assert response.status_code == 422

    from sqlalchemy import func, select

    from app.models.order import Order

    count = db_session.scalar(select(func.count()).select_from(Order))
    assert count == 0
    assert client.get(f"/api/v1/products/{product['id']}").json()["stock_quantity"] == 20


def test_insufficient_stock_rolls_back_transaction(client, admin_headers, db_session):
    product = _create_product(client, "ord-p2", "5.00", 2, admin_headers)
    customer = _create_customer(client, "stock@example.com")

    response = client.post(
        "/api/v1/orders",
        json={
            "customer_id": customer["id"],
            "items": [{"product_id": product["id"], "quantity": 5}],
        },
    )
    assert response.status_code == 400
    assert "Insufficient stock" in response.json()["detail"]

    from sqlalchemy import func, select

    from app.models.order import Order

    count = db_session.scalar(select(func.count()).select_from(Order))
    assert count == 0
    assert client.get(f"/api/v1/products/{product['id']}").json()["stock_quantity"] == 2


def test_cancel_order_restores_stock(client, admin_headers):
    product = _create_product(client, "ord-p3", "20.00", 10, admin_headers)
    customer = _create_customer(client, "cancel@example.com")

    order = client.post(
        "/api/v1/orders",
        json={
            "customer_id": customer["id"],
            "items": [{"product_id": product["id"], "quantity": 4}],
        },
    ).json()

    cancel_response = client.delete(f"/api/v1/orders/{order['id']}", headers=admin_headers)
    assert cancel_response.status_code == 200
    assert cancel_response.json()["status"] == "cancelled"

    product_response = client.get(f"/api/v1/products/{product['id']}")
    assert product_response.json()["stock_quantity"] == 10


def test_cancel_already_cancelled_order(client, admin_headers):
    product = _create_product(client, "ord-p4", "15.00", 5, admin_headers)
    customer = _create_customer(client, "twice@example.com")
    order = client.post(
        "/api/v1/orders",
        json={
            "customer_id": customer["id"],
            "items": [{"product_id": product["id"], "quantity": 1}],
        },
    ).json()

    client.delete(f"/api/v1/orders/{order['id']}", headers=admin_headers)
    response = client.delete(f"/api/v1/orders/{order['id']}", headers=admin_headers)
    assert response.status_code == 400


def test_order_requires_existing_customer(client, admin_headers):
    product = _create_product(client, "ord-p5", "8.00", 5, admin_headers)
    response = client.post(
        "/api/v1/orders",
        json={
            "customer_id": 9999,
            "items": [{"product_id": product["id"], "quantity": 1}],
        },
    )
    assert response.status_code == 404


def test_order_requires_existing_product(client):
    customer = _create_customer(client, "noprod@example.com")
    response = client.post(
        "/api/v1/orders",
        json={
            "customer_id": customer["id"],
            "items": [{"product_id": 9999, "quantity": 1}],
        },
    )
    assert response.status_code == 404


def test_list_and_get_order(client, admin_headers):
    product = _create_product(client, "ord-p6", "12.50", 8, admin_headers)
    customer = _create_customer(client, "list@example.com")
    created = client.post(
        "/api/v1/orders",
        json={
            "customer_id": customer["id"],
            "items": [{"product_id": product["id"], "quantity": 2}],
        },
    ).json()

    list_response = client.get("/api/v1/orders")
    assert list_response.status_code == 200
    body = list_response.json()
    assert body["total"] >= 1
    assert "data" in body
    assert body["page"] == 1

    get_response = client.get(f"/api/v1/orders/{created['id']}")
    assert get_response.status_code == 200
    body = get_response.json()
    assert body["customer_email"] == "list@example.com"
    assert body["items"][0]["quantity"] == 2
    assert body["total_amount"] == "25.00"
