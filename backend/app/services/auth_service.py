from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.exceptions import UnauthorizedError
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenResponse, UserLogin, UserRegister, UserResponse, parse_user_role

settings = get_settings()


class AuthService:
    def __init__(self, db: Session) -> None:
        self.repository = UserRepository(db)
        self.db = db

    def register(self, data: UserRegister) -> UserResponse:
        assigned_role = parse_user_role(data.role)
        hashed = hash_password(data.password)

        user = self.repository.create(
            name=data.name,
            email=str(data.email),
            hashed_password=hashed,
            role=assigned_role,
        )
        self.db.commit()
        self.db.refresh(user)
        return UserResponse.model_validate(user)

    def login(self, data: UserLogin) -> TokenResponse:
        user = self.repository.get_by_email(str(data.email))
        if user is None or not verify_password(data.password, user.hashed_password):
            raise UnauthorizedError("Invalid email or password")

        token = create_access_token(user_id=user.id, role=user.role.value)
        return TokenResponse(
            access_token=token,
            expires_in=settings.jwt_expire_minutes * 60,
        )

    def get_current_user(self, user_id: int) -> UserResponse:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise UnauthorizedError("User not found")
        return UserResponse.model_validate(user)
