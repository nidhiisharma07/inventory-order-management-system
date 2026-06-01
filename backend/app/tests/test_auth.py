def test_register_without_role_defaults_to_staff(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Staff User",
            "email": "staff@inventory.com",
            "password": "securepass123",
        },
    )
    assert response.status_code == 201
    assert response.json()["role"] == "staff"


def test_register_with_explicit_admin_role(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Admin User",
            "email": "admin@inventory.com",
            "password": "securepass123",
            "role": "admin",
        },
    )
    assert response.status_code == 201
    assert response.json()["role"] == "admin"


def test_register_with_explicit_staff_role(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "name": "Admin User",
            "email": "admin@inventory.com",
            "password": "securepass123",
            "role": "admin",
        },
    )
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Staff User",
            "email": "staff@inventory.com",
            "password": "securepass123",
            "role": "staff",
        },
    )
    assert response.status_code == 201
    assert response.json()["role"] == "staff"


def test_register_invalid_role_returns_422(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Bad Role User",
            "email": "badrole@inventory.com",
            "password": "securepass123",
            "role": "superuser",
        },
    )
    assert response.status_code == 422


def test_register_admin_role_persisted_in_database(client, db_session):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "DB Admin",
            "email": "dbadmin@inventory.com",
            "password": "securepass123",
            "role": "admin",
        },
    )
    assert response.status_code == 201
    assert response.json()["role"] == "admin"

    from app.models.user import User, UserRole

    user = db_session.query(User).filter_by(email="dbadmin@inventory.com").one()
    assert user.role == UserRole.ADMIN
    assert user.role.value == "admin"


def test_login_token_includes_role_claim(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "name": "Admin User",
            "email": "admin@inventory.com",
            "password": "securepass123",
            "role": "admin",
        },
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@inventory.com", "password": "securepass123"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["expires_in"] > 0

    from jose import jwt
    from app.core.config import get_settings

    settings = get_settings()
    payload = jwt.decode(
        body["access_token"],
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )
    assert payload["role"] == "admin"


def test_me_requires_authentication(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_me_returns_current_user(client, admin_headers):
    response = client.get("/api/v1/auth/me", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "admin@test.com"


def test_staff_cannot_create_product(client, staff_headers):
    response = client.post(
        "/api/v1/products",
        headers=staff_headers,
        json={
            "name": "Blocked Product",
            "sku": "blk-001",
            "price": "10.00",
            "stock_quantity": 1,
        },
    )
    assert response.status_code == 403


def test_staff_cannot_delete_customer(client, staff_headers, admin_headers):
    customer = client.post(
        "/api/v1/customers",
        json={
            "full_name": "Delete Test",
            "email": "delete@test.com",
            "phone": "555",
        },
    ).json()

    response = client.delete(
        f"/api/v1/customers/{customer['id']}",
        headers=staff_headers,
    )
    assert response.status_code == 403
