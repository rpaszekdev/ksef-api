"""Symmetric Fernet crypto for encrypting KSeF tokens/certs at rest."""

from functools import lru_cache

from cryptography.fernet import Fernet

from app.core.config import get_settings


@lru_cache(maxsize=1)
def _cipher() -> Fernet:
    settings = get_settings()
    if not settings.fernet_key:
        raise RuntimeError(
            "FERNET_KEY not set. Generate with: python -c "
            "'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'"
        )
    return Fernet(settings.fernet_key.encode())


def encrypt(plaintext: str) -> str:
    return _cipher().encrypt(plaintext.encode()).decode()


def decrypt(ciphertext: str) -> str:
    return _cipher().decrypt(ciphertext.encode()).decode()
