from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError
from app.models.user import User, UserRole
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, User)

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.db.execute(stmt).scalar_one_or_none()

    def count_users(self) -> int:
        return self.db.scalar(select(func.count()).select_from(User)) or 0

    def create(
        self,
        *,
        name: str,
        email: str,
        hashed_password: str,
        role: UserRole,
    ) -> User:
        if role not in (UserRole.ADMIN, UserRole.STAFF):
            raise ValueError(f"Invalid role for persistence: {role!r}")

        user = User(
            name=name,
            email=email,
            hashed_password=hashed_password,
            role=role,
        )
        self.db.add(user)
        try:
            self.db.flush()
            self.db.refresh(user)
        except IntegrityError as exc:
            self.db.rollback()
            raise ConflictError(f"User with email '{email}' already exists") from exc
        return user
