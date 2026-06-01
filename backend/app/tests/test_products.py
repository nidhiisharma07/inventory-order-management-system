def test_create_and_get_product(client, admin_headers):
    payload = {
        "name": "Wireless Mouse",
        "sku": "wm-001",
        "price": "29.99",
        "stock_quantity": 50,
    }
    create_response = client.post("/api/v1/products", json=payload, headers=admin_headers)
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["sku"] == "WM-001"
    assert created["stock_quantity"] == 50

    get_response = client.get(f"/api/v1/products/{created['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Wireless Mouse"


def test_list_products(client, admin_headers):
    client.post(
        "/api/v1/products",
        headers=admin_headers,
        json={
            "name": "Keyboard",
            "sku": "kb-001",
            "price": "79.99",
            "stock_quantity": 20,
        },
    )
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] >= 1
    assert len(body["items"]) >= 1


def test_update_product(client, admin_headers):
    created = client.post(
        "/api/v1/products",
        headers=admin_headers,
        json={
            "name": "Monitor",
            "sku": "mon-001",
            "price": "199.99",
            "stock_quantity": 10,
        },
    ).json()

    response = client.put(
        f"/api/v1/products/{created['id']}",
        json={"stock_quantity": 5, "price": "189.99"},
    )
    assert response.status_code == 200
    assert response.json()["stock_quantity"] == 5


def test_delete_product(client, admin_headers):
    created = client.post(
        "/api/v1/products",
        headers=admin_headers,
        json={
            "name": "Webcam",
            "sku": "wc-001",
            "price": "49.99",
            "stock_quantity": 15,
        },
    ).json()

    delete_response = client.delete(f"/api/v1/products/{created['id']}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/products/{created['id']}")
    assert get_response.status_code == 404


def test_duplicate_sku_returns_conflict(client, admin_headers):
    payload = {
        "name": "Headphones",
        "sku": "hp-001",
        "price": "99.99",
        "stock_quantity": 30,
    }
    client.post("/api/v1/products", json=payload, headers=admin_headers)
    response = client.post("/api/v1/products", json=payload, headers=admin_headers)
    assert response.status_code == 409


def test_negative_stock_rejected(client, admin_headers):
    response = client.post(
        "/api/v1/products",
        headers=admin_headers,
        json={
            "name": "Invalid Product",
            "sku": "inv-001",
            "price": "10.00",
            "stock_quantity": -1,
        },
    )
    assert response.status_code == 422


def test_product_not_found(client):
    response = client.get("/api/v1/products/9999")
    assert response.status_code == 404
