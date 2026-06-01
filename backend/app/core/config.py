from functools import lru_cache
from typing import Literal

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    environment: Literal["development", "staging", "production"] = "development"
    app_name: str = "Inventory & Order Management API"
    app_version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"

    database_url: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/inventory_db"
    )

    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    jwt_secret_key: str = "change-this-secret-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]

    @model_validator(mode="after")
    def validate_production_settings(self) -> "Settings":
        if self.is_production:
            if self.jwt_secret_key == "change-this-secret-in-production":
                raise ValueError(
                    "JWT_SECRET_KEY must be set to a strong secret in production"
                )
            if not self.cors_origin_list:
                raise ValueError("CORS_ORIGINS must include your frontend URL in production")
        return self

    def validate_runtime(self) -> None:
        """Hook for explicit startup validation."""
        _ = self.is_production


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.validate_runtime()
    return settings
