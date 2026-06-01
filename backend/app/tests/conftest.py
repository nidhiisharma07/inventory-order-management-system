import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.security import create_access_token, hash_password
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models import Customer, Order, OrderItem, Product, User  # noqa: F401
from app.models.user import UserRole

SQLALCHEMY_TEST_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def _create_user(db_session, *, email: str, role: UserRole) -> User:
    user = User(
        name="Test User",
        email=email,
        hashed_password=hash_password("password123"),
        role=role,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def _auth_header_for(user: User) -> dict[str, str]:
    token = create_access_token(user_id=user.id, role=user.role.value)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(autouse=True)
def setup_database() -> None:
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def admin_user(db_session):
    return _create_user(db_session, email="admin@test.com", role=UserRole.ADMIN)


@pytest.fixture
def staff_user(db_session):
    return _create_user(db_session, email="staff@test.com", role=UserRole.STAFF)


@pytest.fixture
def admin_headers(admin_user):
    return _auth_header_for(admin_user)


@pytest.fixture
def staff_headers(staff_user):
    return _auth_header_for(staff_user)


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
