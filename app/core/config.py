"""Application settings loaded from environment via pydantic-settings."""

from functools import lru_cache
from typing import Literal

from pydantic import Field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # App
    env: Literal["dev", "test", "prod"] = "dev"
    debug: bool = False
    app_name: str = "ksef-api"
    base_url: str = "http://localhost:8000"

    # Security
    fernet_key: str = Field(
        default="",
        description="Base64 Fernet key for encrypting KSeF tokens/certs at rest.",
    )
    jwt_secret: str = Field(default="", description="HMAC secret for login JWTs.")
    jwt_alg: str = "HS256"
    jwt_ttl_min: int = 60

    # Database
    database_url: PostgresDsn = Field(
        default="postgresql+asyncpg://ksef:ksef@localhost:5432/ksef"  # type: ignore[arg-type]
    )

    # Redis
    redis_url: RedisDsn = Field(default="redis://localhost:6379/0")  # type: ignore[arg-type]

    # KSeF
    ksef_env: Literal["test", "demo", "prod"] = "test"

    # Stripe (filled in week 3)
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_price_solo: str = ""
    stripe_price_biuro: str = ""
    stripe_price_biuro_pro: str = ""

    # Observability
    sentry_dsn: str = ""

    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:8000"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
