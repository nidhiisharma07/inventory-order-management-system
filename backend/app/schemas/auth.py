from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.core.exceptions import ValidationError as AppValidationError
from app.models.user import UserRole

ALLOWED_ROLES = frozenset({UserRole.ADMIN.value, UserRole.STAFF.value})


def parse_user_role(value: Any) -> UserRole:
    """Normalize and validate role from API input."""
    if value is None:
        return UserRole.STAFF

    if isinstance(value, UserRole):
        return value

    if not isinstance(value, str):
        raise AppValidationError("Role must be 'admin' or 'staff'")

    normalized = value.strip().lower()
    if normalized not in ALLOWED_ROLES:
        raise AppValidationError("Role must be 'admin' or 'staff'")

    return UserRole(normalized)


class UserRegister(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)
    role: UserRole = Field(
        default=UserRole.STAFF,
        description="User role: admin or staff",
    )

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        return value.strip()

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()

    @field_validator("role", mode="before")
    @classmethod
    def validate_role(cls, value: Any) -> UserRole:
        return parse_user_role(value)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=72)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: int
    name: str
    email: EmailStr
    role: UserRole
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
